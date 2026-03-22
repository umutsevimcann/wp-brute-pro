"""Result reporting — log, MD report, JSON"""
import os
from datetime import datetime
from lang import t


class Reporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.log_file = os.path.join(output_dir, "log.txt")

    def log(self, msg, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] {msg}"
        print(line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def info(self, msg):
        self.log(msg, "INFO")

    def success(self, msg):
        self.log(msg, "SUCCESS")

    def warning(self, msg):
        self.log(msg, "WARN")

    def error(self, msg):
        self.log(msg, "ERROR")

    def banner(self, msg):
        sep = "=" * 55
        self.log(sep)
        self.log(msg)
        self.log(sep)

    def found(self, username, password):
        self.log("")
        self.log("!" * 55, "FOUND")
        self.log(f"{t('password_found')}: {username}:{password}", "FOUND")
        self.log("!" * 55, "FOUND")
        self.log("")

    def write_report(self, scan_info, tracker_state, throttle_stats):
        report_file = os.path.join(self.output_dir, "report.md")
        found = tracker_state.get("found", [])

        lines = [
            f"# {t('report_title')}",
            f"",
            f"**{t('stat_target')}:** {tracker_state.get('target', '?')}",
            f"**{t('report_date')}:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"",
            f"## {t('phase1')}",
            f"",
        ]

        if scan_info:
            lines.append(f"| | |")
            lines.append(f"|---|---|")
            lines.append(f"| WordPress | {scan_info.get('wp_version', '?')} |")
            lines.append(f"| Login URL | {scan_info.get('login_url', '?')} |")
            xmlrpc = f"{t('scan_active')} ({scan_info.get('xmlrpc_methods', 0)})" if scan_info.get('xmlrpc_active') else t('scan_disabled')
            lines.append(f"| XML-RPC | {xmlrpc} |")
            lines.append(f"| WAF | {scan_info.get('waf_name') or t('scan_no')} |")
            lines.append(f"| CAPTCHA | {t('scan_yes') if scan_info.get('has_captcha') else t('scan_no')} |")
            lines.append(f"")

        lines.append(f"## {t('phase5')}")
        lines.append(f"")
        lines.append(f"| | |")
        lines.append(f"|---|---|")
        lines.append(f"| {t('total_tried')} | {tracker_state.get('total_tried', 0)} |")
        lines.append(f"| {t('total_generated')} | {tracker_state.get('total_generated', 0)} |")
        lines.append(f"| {t('found_count')} | {len(found)} |")
        lines.append(f"| {t('http_requests')} | {throttle_stats.get('total_requests', 0)} |")
        lines.append(f"| {t('blocks')} | {throttle_stats.get('total_blocks', 0)} |")
        lines.append(f"")

        if found:
            lines.append(f"## {t('found_header')}")
            lines.append(f"")
            lines.append(f"| {t('report_user')} | {t('report_password')} | {t('report_time')} |")
            lines.append(f"|------|----------|------|")
            for f_entry in found:
                lines.append(f"| {f_entry['username']} | {f_entry['password']} | {f_entry['time']} |")
        else:
            lines.append(f"**{t('no_password')}**")

        with open(report_file, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))
