"""Terminal UI — colored output, interactive selection, animated progress"""
import sys
import time
import shutil
import subprocess

# Windows color support
if sys.platform == "win32":
    subprocess.run(["cmd", "/c", "echo."], capture_output=True)  # ANSI aktif


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    BG_GREEN = "\033[42m"
    CLEAR_LINE = "\033[2K"
    CURSOR_UP = "\033[A"
    CURSOR_HIDE = "\033[?25l"
    CURSOR_SHOW = "\033[?25h"


C = Colors


def term_width():
    return shutil.get_terminal_size().columns


def banner():
    print(f"""{C.RED}
  ██╗    ██╗██████╗ {C.WHITE}      ██████╗ ██████╗ ██╗   ██╗████████╗███████╗
  {C.RED}██║    ██║██╔══██╗{C.WHITE}      ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
  {C.RED}██║ █╗ ██║██████╔╝{C.YELLOW}█████╗{C.WHITE}██████╔╝██████╔╝██║   ██║   ██║   █████╗
  {C.RED}██║███╗██║██╔═══╝ {C.YELLOW}╚════╝{C.WHITE}██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝
  {C.RED}╚███╔███╔╝██║     {C.WHITE}      ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
  {C.RED} ╚══╝╚══╝ ╚═╝     {C.WHITE}      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
  {C.GRAY}─────────────────────────────────────────────────────────────
  {C.CYAN}{C.BOLD}WordPress Password Tester {C.YELLOW}v3.0{C.GRAY}  │  {C.RED}Authorized Use Only{C.RESET}
""")


def header(text):
    w = min(term_width(), 60)
    line = "─" * (w - 2)
    print(f"\n{C.CYAN}┌{line}┐{C.RESET}")
    print(f"{C.CYAN}│{C.BOLD}{C.WHITE} {text:<{w-3}}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{line}┘{C.RESET}")


def info(msg):
    print(f"  {C.BLUE}●{C.RESET} {msg}")


def success(msg):
    print(f"  {C.GREEN}✔{C.RESET} {msg}")


def warning(msg):
    print(f"  {C.YELLOW}⚠{C.RESET} {msg}")


def error(msg):
    print(f"  {C.RED}✖{C.RESET} {msg}")


def found_password(username, password):
    w = min(term_width(), 60)
    line = "═" * (w - 2)
    print(f"\n{C.BG_GREEN}{C.WHITE}{C.BOLD}")
    print(f"  ╔{line}╗")
    print(f"  ║{'SIFRE BULUNDU!':^{w-2}}║")
    print(f"  ║{f'{username}:{password}':^{w-2}}║")
    print(f"  ╚{line}╝")
    print(f"{C.RESET}\n")


def batch_result(batch_num, total_batches, tried, total, status="miss"):
    pct = tried / total if total > 0 else 0
    filled = int(30 * pct)
    bar = f"{C.GREEN}{'█' * filled}{C.GRAY}{'░' * (30 - filled)}{C.RESET}"

    symbols = {
        "miss": f"{C.RED}✗{C.RESET}",
        "candidate": f"{C.YELLOW}?{C.RESET}",
        "found": f"{C.GREEN}✔{C.RESET}",
        "blocked": f"{C.MAGENTA}⊘{C.RESET}",
    }
    sym = symbols.get(status, f"{C.GRAY}·{C.RESET}")

    line = (f"\r  {sym} {bar} "
            f"{C.WHITE}{tried:>6}{C.GRAY}/{total}{C.RESET} "
            f"{C.GRAY}B{batch_num}/{total_batches}{C.RESET} "
            f"{C.CYAN}{pct:.0%}{C.RESET}  ")
    sys.stdout.write(line)
    sys.stdout.flush()


def batch_newline():
    print()


def scan_result(key, value, status="info"):
    symbols = {
        "good": f"{C.GREEN}✔{C.RESET}",
        "bad": f"{C.RED}✖{C.RESET}",
        "warn": f"{C.YELLOW}⚠{C.RESET}",
        "info": f"{C.BLUE}●{C.RESET}",
    }
    sym = symbols.get(status, symbols["info"])
    print(f"  {sym} {C.WHITE}{key:<16}{C.RESET} {value}")


def select_menu(title, options, default=0):
    """Arrow key selection menu (Windows)"""
    try:
        if sys.platform == "win32":
            import msvcrt
            return _select_win(title, options, default)
        else:
            return _select_fallback(title, options, default)
    except Exception:
        return _select_fallback(title, options, default)


def _select_win(title, options, default):
    import msvcrt
    selected = default
    total_lines = len(options) + 1  # title + options
    first_draw = True

    while True:
        # First draw: print fresh. Subsequent: overwrite in place.
        if not first_draw:
            # Move cursor up to title line
            for _ in range(total_lines):
                sys.stdout.write(f"\033[A\033[2K\r")

        sys.stdout.write(f"\033[?25l")  # hide cursor
        sys.stdout.write(f"  {C.BOLD}{C.WHITE}{title}{C.RESET}\n")
        for i, opt in enumerate(options):
            if i == selected:
                sys.stdout.write(f"  {C.CYAN}> {C.BOLD}{C.WHITE}{opt}{C.RESET}\n")
            else:
                sys.stdout.write(f"  {C.GRAY}  {opt}{C.RESET}\n")
        sys.stdout.flush()
        first_draw = False

        key = msvcrt.getch()
        if key == b'\xe0':
            arrow = msvcrt.getch()
            if arrow == b'H':  # up
                selected = (selected - 1) % len(options)
            elif arrow == b'P':  # down
                selected = (selected + 1) % len(options)
        elif key == b'\r':  # enter
            # Clear menu and show result
            for _ in range(total_lines):
                sys.stdout.write(f"\033[A\033[2K\r")
            sys.stdout.write(f"\033[?25h")  # show cursor
            sys.stdout.write(f"  {C.GREEN}✔{C.RESET} {title}: {C.BOLD}{options[selected]}{C.RESET}\n")
            sys.stdout.flush()
            return selected


def _select_fallback(title, options, default):
    print(f"\n  {C.BOLD}{C.WHITE}{title}{C.RESET}")
    for i, opt in enumerate(options):
        marker = f"{C.CYAN}>{C.RESET}" if i == default else " "
        print(f"  {marker} {i+1}. {opt}")
    try:
        choice = input(f"\n  Select [{default+1}]: ").strip()
        if not choice:
            return default
        return max(0, min(int(choice) - 1, len(options) - 1))
    except (ValueError, EOFError):
        return default


def ask_input(prompt, default=""):
    if default:
        result = input(f"  {C.YELLOW}?{C.RESET} {prompt} {C.GRAY}[{default}]{C.RESET}: ").strip()
    else:
        result = input(f"  {C.YELLOW}?{C.RESET} {prompt}: ").strip()
    return result if result else default


def ask_confirm(prompt, default=True):
    hint = "E/h" if default else "e/H"
    result = input(f"  {C.YELLOW}?{C.RESET} {prompt} [{hint}]: ").strip().lower()
    if not result:
        return default
    return result in ["e", "evet", "y", "yes"]


def stats_table(data):
    if not data:
        return
    max_key = max(len(str(k)) for k, v in data)
    print()
    for key, value in data:
        print(f"  {C.GRAY}{str(key):<{max_key+2}}{C.RESET} {C.WHITE}{value}{C.RESET}")
    print()


def spinner(msg, duration=2):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {C.CYAN}{chars[i % len(chars)]}{C.RESET} {msg}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{C.CLEAR_LINE}")
