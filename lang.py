"""Multi-language support — EN (default) / TR"""

LANG = "en"  # default

STRINGS = {
    "en": {
        # Banner
        "banner_title": "WordPress Password Tester",
        "banner_auth": "Authorized Use Only",

        # Headers
        "config": "CONFIGURATION",
        "phase1": "PHASE 1: RECONNAISSANCE",
        "phase2": "PHASE 2: STRATEGY",
        "phase3": "PHASE 3: WORDLIST",
        "phase4": "PHASE 4: ATTACK",
        "phase5": "PHASE 5: REPORT",
        "found_header": "CREDENTIALS FOUND",

        # Interactive
        "target_url": "Target URL",
        "usernames": "Usernames (comma separated, empty=auto discover)",
        "company_name": "Company name (for wordlist, empty=skip)",
        "extra_keywords": "Extra keywords (comma separated, empty=skip)",
        "crawl_site": "Crawl site for words?",
        "extra_wordlist": "Extra wordlist file (empty=skip)",
        "proxy_file": "Proxy list file (empty=skip)",
        "output_dir": "Output directory",
        "start_confirm": "Start attack?",
        "cancelled": "Cancelled.",
        "url_required": "URL is required!",

        # Method select
        "method_title": "Attack method",
        "method_auto": "auto    — Automatically select best method (recommended)",
        "method_xmlrpc": "xmlrpc  — XML-RPC multicall (fast, bulk testing, ideal without WAF)",
        "method_wplogin": "wplogin — wp-login.php POST (slow but reliable, works everywhere)",
        "method_restapi": "restapi — REST API Basic Auth (slow, requires Application Passwords)",

        # Batch select
        "batch_title": "Batch size (passwords per request)",
        "batch_10": "10  — Very slow but safe, low ban risk on WAF sites",
        "batch_25": "25  — Balanced, medium speed, suitable for most sites",
        "batch_50": "50  — Fast, recommended for sites without WAF (default)",
        "batch_100": "100 — Very fast but risky, noticeable in server logs",
        "batch_200": "200 — Aggressive, high ban risk, use only with proxies",

        # Delay select
        "delay_title": "Delay between requests",
        "delay_05": "0.5s — Very fast, very high ban risk, proxy only",
        "delay_1": "1s   — Fast, usable on sites without WAF",
        "delay_2": "2s   — Balanced, suitable for most sites",
        "delay_3": "3s   — Safe, recommended for WAF sites (default)",
        "delay_5": "5s   — Very safe, slow but almost zero ban risk",
        "delay_10": "10s  — Ultra safe, takes long but completely undetectable",

        # Risk
        "risk_high": "High risk profile — high chance of getting banned!",
        "risk_high_tip": "Tip: add proxy list or increase delay",
        "risk_medium": "Medium risk profile — proceed carefully",
        "risk_low": "Low risk profile — safe settings",
        "risk_label": "Risk",

        # Stats table
        "stat_target": "Target",
        "stat_user": "Username",
        "stat_company": "Company",
        "stat_method": "Method",
        "stat_batch": "Batch",
        "stat_delay": "Delay",
        "stat_proxy": "Proxy",
        "stat_pwd_per_req": "pwd/req",
        "stat_none": "none",
        "stat_auto": "auto discover",

        # Scanner
        "scanning": "Scanning target...",
        "scan_wp": "WordPress",
        "scan_login": "Login URL",
        "scan_xmlrpc": "XML-RPC",
        "scan_captcha": "CAPTCHA",
        "scan_waf": "WAF",
        "scan_users": "Users",
        "scan_plugins": "Plugins",
        "scan_active": "ACTIVE",
        "scan_methods": "methods",
        "scan_disabled": "DISABLED",
        "scan_yes": "YES",
        "scan_no": "NO",
        "scan_not_found": "not found",
        "scan_new_user": "New user discovered",

        # Wordlist
        "generating": "Generating passwords...",
        "generated": "passwords generated",
        "users_label": "Users",

        # Attack
        "all_tried": "All passwords already tried",
        "passwords": "passwords",
        "batches": "batches",
        "candidate": "Candidate",
        "verifying": "verifying...",
        "false_positive": "False positive",
        "not_found": "not found",
        "attempts": "attempts",
        "banned_proxy": "Switching proxy",
        "remaining": "remaining",
        "all_proxies_banned": "All proxies banned!",
        "ip_banned": "IP BANNED! Change VPN and use --resume to continue",
        "connection_lost": "Connection lost",
        "waiting": "waiting",
        "ban_detected": "Ban detected",

        # Report
        "total_tried": "Total tried",
        "total_generated": "Total generated",
        "found_count": "Found",
        "http_requests": "HTTP requests",
        "blocks": "Blocks",
        "ban_count": "Ban count",
        "no_password": "No password found — but unblocked attack is itself a vulnerability",
        "report_at": "Report",
        "log_at": "Log",

        # Found
        "password_found": "PASSWORD FOUND!",
        "no_user": "No username found! Use -U to specify.",

        # Risk labels
        "risk_low_label": "low",
        "risk_medium_label": "medium",
        "risk_high_label": "high",

        # Language selection
        "lang_select": "Language / Dil",
        "lang_en": "English",
        "lang_tr": "Türkçe",

        # Strategy
        "strategy_xmlrpc": "XML-RPC multicall — fastest method",
        "strategy_wplogin": "wp-login.php POST",
        "strategy_restapi": "REST API Basic Auth",
        "strategy_captcha_switch": "CAPTCHA detected! Switching to XML-RPC",

        # Report table headers
        "report_user": "User",
        "report_password": "Password",
        "report_time": "Time",
        "report_title": "WordPress Brute Force Report",
        "report_date": "Date",

        # Misc
        "scan_start": "Scanning target...",
    },

    "tr": {
        # Banner
        "banner_title": "WordPress Şifre Test Aracı",
        "banner_auth": "Yalnızca Yetkili Kullanım",

        # Headers
        "config": "YAPILANDIRMA",
        "phase1": "FAZ 1: KEŞİF",
        "phase2": "FAZ 2: STRATEJİ",
        "phase3": "FAZ 3: WORDLIST",
        "phase4": "FAZ 4: SALDIRI",
        "phase5": "FAZ 5: RAPOR",
        "found_header": "BULUNAN ŞİFRELER",

        # Interactive
        "target_url": "Hedef URL",
        "usernames": "Kullanıcı adları (virgülle, boş=otomatik keşfet)",
        "company_name": "Firma adı (wordlist için, boş=atla)",
        "extra_keywords": "Ek anahtar kelimeler (virgülle, boş=atla)",
        "crawl_site": "Siteden kelime çek?",
        "extra_wordlist": "Ek wordlist dosyası (boş=atla)",
        "proxy_file": "Proxy listesi dosyası (boş=atla)",
        "output_dir": "Çıktı dizini",
        "start_confirm": "Başlatılsın mı?",
        "cancelled": "İptal edildi.",
        "url_required": "URL gerekli!",

        # Method select
        "method_title": "Saldırı yöntemi",
        "method_auto": "auto    — Otomatik en iyi yöntemi seç (önerilen)",
        "method_xmlrpc": "xmlrpc  — XML-RPC multicall (hızlı, toplu deneme, WAF yoksa ideal)",
        "method_wplogin": "wplogin — wp-login.php POST (yavaş ama güvenilir, her sitede çalışır)",
        "method_restapi": "restapi — REST API Basic Auth (yavaş, Application Passwords gerekli)",

        # Batch select
        "batch_title": "Batch boyutu (tek istekte kaç şifre)",
        "batch_10": "10  — Çok yavaş ama güvenli, WAF olan sitelerde ban riski düşük",
        "batch_25": "25  — Dengeli, orta hızda, çoğu site için uygun",
        "batch_50": "50  — Hızlı, WAF olmayan sitelerde önerilen (varsayılan)",
        "batch_100": "100 — Çok hızlı ama riskli, sunucu log'larında dikkat çeker",
        "batch_200": "200 — Agresif, ban riski yüksek, sadece proxy ile kullan",

        # Delay select
        "delay_title": "İstekler arası bekleme",
        "delay_05": "0.5s — Çok hızlı, ban riski çok yüksek, sadece proxy ile",
        "delay_1": "1s   — Hızlı, WAF olmayan sitelerde kullanılabilir",
        "delay_2": "2s   — Dengeli, çoğu site için uygun",
        "delay_3": "3s   — Güvenli, WAF olan sitelerde önerilen (varsayılan)",
        "delay_5": "5s   — Çok güvenli, yavaş ama ban riski neredeyse sıfır",
        "delay_10": "10s  — Ultra güvenli, uzun sürer ama kesinlikle tespit edilmez",

        # Risk
        "risk_high": "Yüksek risk profili — ban yeme ihtimali yüksek!",
        "risk_high_tip": "Öneri: proxy listesi ekle veya delay'i artır",
        "risk_medium": "Orta risk profili — dikkatli devam edin",
        "risk_low": "Düşük risk profili — güvenli ayarlar",
        "risk_label": "Risk",

        # Stats table
        "stat_target": "Hedef",
        "stat_user": "Kullanıcı",
        "stat_company": "Firma",
        "stat_method": "Yöntem",
        "stat_batch": "Batch",
        "stat_delay": "Delay",
        "stat_proxy": "Proxy",
        "stat_pwd_per_req": "şifre/istek",
        "stat_none": "yok",
        "stat_auto": "otomatik keşif",

        # Scanner
        "scanning": "Hedef taranıyor...",
        "scan_wp": "WordPress",
        "scan_login": "Login URL",
        "scan_xmlrpc": "XML-RPC",
        "scan_captcha": "CAPTCHA",
        "scan_waf": "WAF",
        "scan_users": "Kullanıcılar",
        "scan_plugins": "Eklentiler",
        "scan_active": "AKTİF",
        "scan_methods": "method",
        "scan_disabled": "KAPALI",
        "scan_yes": "VAR",
        "scan_no": "YOK",
        "scan_not_found": "bulunamadı",
        "scan_new_user": "Yeni kullanıcı keşfedildi",

        # Wordlist
        "generating": "Şifreler üretiliyor...",
        "generated": "şifre üretildi",
        "users_label": "Kullanıcılar",

        # Attack
        "all_tried": "Tüm şifreler zaten denenmiş",
        "passwords": "şifre",
        "batches": "paket",
        "candidate": "Aday",
        "verifying": "doğrulanıyor...",
        "false_positive": "False positive",
        "not_found": "bulunamadı",
        "attempts": "deneme",
        "banned_proxy": "Proxy değiştiriliyor",
        "remaining": "kaldı",
        "all_proxies_banned": "Tüm proxy'ler banlandı!",
        "ip_banned": "IP BANLANDI! VPN değiştirip --resume ile devam edin",
        "connection_lost": "Bağlantı kesildi",
        "waiting": "bekleniyor",
        "ban_detected": "Ban algılandı",

        # Report
        "total_tried": "Toplam denenen",
        "total_generated": "Toplam üretilen",
        "found_count": "Bulunan",
        "http_requests": "HTTP istek",
        "blocks": "Engellenme",
        "ban_count": "Ban sayısı",
        "no_password": "Şifre bulunamadı — saldırının engellenmemesi başlı başına bir açık",
        "report_at": "Rapor",
        "log_at": "Log",

        # Found
        "password_found": "ŞİFRE BULUNDU!",
        "no_user": "Kullanıcı adı bulunamadı! -U ile belirtin.",

        # Risk labels
        "risk_low_label": "düşük",
        "risk_medium_label": "orta",
        "risk_high_label": "yüksek",

        # Language selection
        "lang_select": "Language / Dil",
        "lang_en": "English",
        "lang_tr": "Türkçe",

        # Strategy
        "strategy_xmlrpc": "XML-RPC multicall — en hızlı yöntem",
        "strategy_wplogin": "wp-login.php POST",
        "strategy_restapi": "REST API Basic Auth",
        "strategy_captcha_switch": "CAPTCHA tespit edildi! XML-RPC'ye geçiliyor",

        # Report table headers
        "report_user": "Kullanıcı",
        "report_password": "Şifre",
        "report_time": "Zaman",
        "report_title": "WordPress Brute Force Raporu",
        "report_date": "Tarih",

        # Misc
        "scan_start": "Hedef taranıyor...",
    },
}


def set_lang(code):
    global LANG
    if code in STRINGS:
        LANG = code


def t(key):
    """Translation function"""
    return STRINGS.get(LANG, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
