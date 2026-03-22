<p align="center">
  <img src="https://img.shields.io/badge/version-3.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/language-EN%20%7C%20TR-orange" alt="Language">
</p>

<h1 align="center">WP-BRUTE-PRO</h1>
<p align="center">WordPress Password Testing Tool for Authorized Penetration Testing</p>
<p align="center">
  <a href="#english">English</a> · <a href="#türkçe">Türkçe</a>
</p>

---

<a name="english"></a>

## English

### What is WP-BRUTE-PRO?

WP-BRUTE-PRO is a professional WordPress password testing tool designed for authorized penetration testers and security researchers. It automates the process of testing WordPress login credentials using multiple attack vectors while intelligently evading detection mechanisms.

### Why Another Tool?

| Feature | WPScan | Hydra | WP-BRUTE-PRO |
|---------|--------|-------|--------------|
| XML-RPC Multicall | ✗ | ✗ | **✔** (50 pwd/req) |
| Smart Wordlist Generation | ✗ | ✗ | **✔** (5-layer) |
| Proxy Support | ✔ (manual) | ✔ (manual) | **✔** (auto rotation) |
| Throttle/Delay | ✔ (manual) | ✗ | **✔** (adaptive) |
| Resume | ✗ | ✗ | **✔** |
| Interactive UI | ✗ | ✗ | **✔** |
| CVE/Vulnerability Scan | **✔** (API) | ✗ | ✗ |
| Plugin/Theme Detection | **✔** (aggressive) | ✗ | Basic |

> **Note:** WPScan is a vulnerability scanner, WP-BRUTE-PRO is a password tester. They complement each other — use WPScan for CVE detection and WP-BRUTE-PRO for password testing.

WPScan and Hydra test passwords one-by-one via wp-login.php. WP-BRUTE-PRO uses XML-RPC `system.multicall` to test **50 passwords in a single HTTP request**, making it significantly faster while appearing as a single request in server logs.

### Features

**Attack Methods**
- **XML-RPC Multicall** — Tests 50+ passwords per request. Fastest method, ideal for sites without WAF
- **wp-login.php POST** — Traditional login form brute force. Works when XML-RPC is disabled
- **REST API Basic Auth** — Tests via WordPress REST API. Works when Application Passwords are enabled

**Smart Wordlist Generation**
- 5-layer priority system: company name → usernames → site keywords → common passwords → mutations
- Built-in site crawler (CeWL-like) extracts keywords from target pages
- Leet speak mutations: `a→@/4, e→3, i→1/!, o→0, s→$/5, t→7`
- Case variations: lower, UPPER, Capitalize, sWAPcASE
- Year/suffix append: 2020-2026, !, @, #, 123, 1234
- Turkish character normalization: `ğ→g, ü→u, ş→s, ı→i, ö→o, ç→c`
- Username + company combination generator

**Evasion & Detection**
- Adaptive throttling: automatically slows down when blocks are detected
- Proxy rotation: switches to next proxy on ban (HTTP, SOCKS5 supported)
- User-Agent rotation: 20 real browser fingerprints, rotated per request
- Batch size reduction: automatically decreases on server errors
- Ban detection: identifies 403, 429, 503 responses and connection timeouts

**Reconnaissance**
- WordPress version detection (meta tag, RSS feed, generator tag)
- Hidden login URL discovery (15+ common paths: /giris, /login, /panel, /admin...)
- XML-RPC status check via direct POST (not GET — avoids false negatives)
- WAF detection (Cloudflare, Sucuri, Wordfence)
- CAPTCHA detection (reCAPTCHA, Turnstile, hCaptcha)
- User enumeration (REST API, `?rest_route=` bypass, `?author=N` enumeration)
- Plugin & version fingerprinting from HTML source

**Quality of Life**
- Interactive TUI with arrow-key selection menus
- Colored terminal output with progress bars
- Resume support: saves progress, continues after interruption
- Multi-language: English (default) and Turkish
- JSON config file support
- False positive protection: every candidate verified with direct API call
- Detailed logging and markdown report generation

### Installation

```bash
git clone https://github.com/umutsevimcann/wp-brute-pro.git
cd wp-brute-pro
pip install requests
```

No other dependencies required.

### Quick Start

```bash
# Interactive mode — guided setup with arrow-key menus
python wp_brute.py

# CLI mode — direct execution
python wp_brute.py -u https://target.com -U admin

# With company info for smarter wordlist
python wp_brute.py -u https://target.com -U admin --company "Acme Corp" --crawl

# Turkish interface
python wp_brute.py --lang tr
```

### Usage Examples

**Basic scan with auto-detection:**
```bash
python wp_brute.py -u https://target.com -U admin -v
```
Automatically discovers WordPress version, login URL, XML-RPC status, and selects the best attack method.

**Full options:**
```bash
python wp_brute.py \
  -u https://target.com \
  -U admin,editor \
  --company "Acme Corp" \
  --keywords "marketing,sales,digital" \
  --crawl \
  --method xmlrpc \
  --batch-size 50 \
  --delay 3 \
  --proxy-list proxies.txt \
  --resume \
  --lang en \
  -v
```

**With proxy rotation:**
```bash
python wp_brute.py \
  -u https://target.com \
  -U admin \
  --proxy-list proxies.txt \
  --method xmlrpc \
  --batch-size 30 \
  --delay 3 \
  --resume -v
```

**From config file:**
```bash
python wp_brute.py --config config.json
```

```json
{
  "url": "https://target.com",
  "users": "admin,editor",
  "company": "Acme Corp",
  "keywords": "marketing,sales",
  "crawl": true,
  "method": "auto",
  "batch_size": 50,
  "delay": 3,
  "proxy_file": "proxies.txt",
  "output": "results",
  "resume": true,
  "verbose": true,
  "lang": "en"
}
```

### Parameters

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--url` | `-u` | — | Target WordPress URL |
| `--users` | `-U` | auto | Usernames, comma separated. Empty = auto-discover |
| `--method` | | `auto` | Attack method: `auto`, `xmlrpc`, `wplogin`, `restapi` |
| `--batch-size` | | `50` | Passwords per XML-RPC request (10-200) |
| `--delay` | | `3.0` | Seconds between requests (0.5-10) |
| `--company` | | — | Company name for targeted wordlist generation |
| `--keywords` | | — | Extra keywords for wordlist, comma separated |
| `--crawl` | | off | Crawl target site for keywords |
| `--wordlist` | | — | Path to additional wordlist file |
| `--proxy` | | — | Single proxy: `http://ip:port` or `socks5://ip:port` |
| `--proxy-list` | | — | Proxy list file, one per line |
| `--output` | | `results` | Output directory for reports and logs |
| `--config` | | — | JSON configuration file |
| `--resume` | | off | Continue from previous progress |
| `--lang` | | `en` | Language: `en` or `tr` |
| `--no-scan` | | off | Skip reconnaissance phase |
| `--verbose` | `-v` | off | Show detailed output |
| `--interactive` | `-i` | — | Force interactive mode |

### Attack Flow

```
Phase 1: RECONNAISSANCE
├── Detect WordPress version
├── Find login URL (including hidden paths)
├── Check XML-RPC status (direct POST test)
├── Detect WAF (Cloudflare, Sucuri, Wordfence)
├── Check for CAPTCHA
├── Enumerate users (REST API, author enum)
└── Fingerprint plugins & versions

Phase 2: STRATEGY
├── XML-RPC active → multicall (fastest)
├── XML-RPC disabled → wp-login.php POST
├── Both disabled → REST API Basic Auth
└── CAPTCHA on login → switch to XML-RPC

Phase 3: WORDLIST GENERATION
├── Layer 1: Company + username combinations (~500)
├── Layer 2: Site crawl keywords + extra keywords (~200)
├── Layer 3: Common weak passwords (~200)
├── Layer 4: Mutations of all above (~15,000+)
└── Layer 5: External wordlist file (optional)

Phase 4: ATTACK
├── Send batches in priority order
├── Parse responses for success indicators
├── On candidate → verify with direct API call
├── On block → increase delay, reduce batch
├── On ban → rotate proxy or pause
└── Save progress after each batch

Phase 5: REPORT
├── results/report.md  — Human-readable report
├── results/found.txt  — Found credentials
├── results/state.json — State for resume
├── results/tried.txt  — Tried passwords
└── results/log.txt    — Detailed log
```

### Ban Evasion Logic

| Event | Response |
|-------|----------|
| HTTP 429 (Rate Limit) | Double delay, wait 60s |
| HTTP 403 (Forbidden) | Double delay, wait 60s |
| HTTP 503 (Server Error) | Triple delay, halve batch size, wait 120s |
| Connection Timeout | Triple delay, wait 60s |
| 3 consecutive failures | Switch proxy (if available) or warn user |
| 5 successful batches | Decrease delay by 0.3s (speed up) |
| 10 successful batches | Increase batch size (restore) |

### Proxy Support

```bash
# Single proxy
python wp_brute.py -u https://target.com -U admin --proxy http://127.0.0.1:8080

# SOCKS5 proxy (Tor)
python wp_brute.py -u https://target.com -U admin --proxy socks5://127.0.0.1:9050

# Proxy list with auto-rotation
python wp_brute.py -u https://target.com -U admin --proxy-list proxies.txt
```

**proxies.txt:**
```
http://proxy1.example.com:8080
http://proxy2.example.com:3128
socks5://proxy3.example.com:1080
http://user:pass@proxy4.example.com:8080
```

### Architecture

```
wp-brute-pro/
├── wp_brute.py              # Main CLI entry point
├── ui.py                    # Terminal UI (colors, menus, progress)
├── lang.py                  # Multi-language support (EN/TR)
├── core/
│   ├── scanner.py           # Target reconnaissance
│   ├── xmlrpc.py            # XML-RPC multicall attack
│   ├── wplogin.py           # wp-login.php POST attack
│   ├── restapi.py           # REST API Basic Auth attack
│   └── validator.py         # False positive verification
├── wordlist/
│   ├── generator.py         # 5-layer password generator
│   ├── mutator.py           # Leet, case, suffix mutations
│   └── common.txt           # Common weak passwords
├── evasion/
│   ├── useragent.py         # User-Agent rotation
│   ├── throttle.py          # Adaptive speed control
│   └── proxy.py             # Proxy rotation
├── state/
│   └── tracker.py           # Progress tracking & resume
└── output/
    └── reporter.py          # Report generation
```

---

<a name="türkçe"></a>

## Türkçe

### WP-BRUTE-PRO Nedir?

WP-BRUTE-PRO, yetkili penetrasyon testleri ve güvenlik araştırmaları için tasarlanmış profesyonel bir WordPress şifre test aracıdır. Birden fazla saldırı vektörü kullanarak WordPress giriş bilgilerini test eder ve tespit mekanizmalarından akıllıca kaçınır.

### Neden Bu Araç?

| Özellik | WPScan | Hydra | WP-BRUTE-PRO |
|---------|--------|-------|--------------|
| XML-RPC Multicall | ✗ | ✗ | **✔** (50 şifre/istek) |
| Akıllı Wordlist Üretimi | ✗ | ✗ | **✔** (5 katman) |
| Proxy Desteği | ✔ (manuel) | ✔ (manuel) | **✔** (otomatik rotasyon) |
| Hız Kontrolü | ✔ (manuel) | ✗ | **✔** (adaptif) |
| Devam (Resume) | ✗ | ✗ | **✔** |
| Etkileşimli UI | ✗ | ✗ | **✔** |
| CVE/Zafiyet Tarama | **✔** (API ile) | ✗ | ✗ |
| Eklenti/Tema Tespiti | **✔** (agresif) | ✗ | Temel |

> **Not:** WPScan bir zafiyet tarayıcısı, WP-BRUTE-PRO bir şifre test aracıdır. Birbirini tamamlarlar — CVE tespiti için WPScan, şifre testi için WP-BRUTE-PRO kullanın.

WPScan ve Hydra şifreleri wp-login.php üzerinden teker teker dener. WP-BRUTE-PRO, XML-RPC `system.multicall` ile **tek HTTP isteğinde 50 şifre** test eder. Sunucu loglarında tek istek olarak görünürken çok daha hızlı çalışır.

### Özellikler

**Saldırı Yöntemleri**
- **XML-RPC Multicall** — İstek başına 50+ şifre. En hızlı yöntem, WAF olmayan siteler için ideal
- **wp-login.php POST** — Geleneksel giriş formu. XML-RPC kapalıysa kullanılır
- **REST API Basic Auth** — WordPress REST API üzerinden test. Application Passwords aktifse çalışır

**Akıllı Wordlist Üretimi**
- 5 katmanlı öncelik sistemi: firma adı → kullanıcı adları → site kelimeleri → yaygın şifreler → mutasyonlar
- Dahili site tarayıcı (CeWL benzeri) hedef sayfalardan anahtar kelime çıkarır
- Leet speak mutasyonları: `a→@/4, e→3, i→1/!, o→0, s→$/5, t→7`
- Harf varyasyonları: küçük, BÜYÜK, Baş Harf, tErS
- Yıl/sonek ekleme: 2020-2026, !, @, #, 123, 1234
- Türkçe karakter normalizasyonu: `ğ→g, ü→u, ş→s, ı→i, ö→o, ç→c`
- Kullanıcı adı + firma adı kombinasyon üretici

**Kaçınma ve Tespit**
- Uyarlanabilir hız: engel algılandığında otomatik yavaşlama
- Proxy rotasyonu: ban durumunda sonraki proxy'ye geçiş (HTTP, SOCKS5)
- User-Agent rotasyonu: 20 gerçek tarayıcı parmak izi, her istekte değişir
- Batch küçültme: sunucu hatalarında otomatik azaltma
- Ban algılama: 403, 429, 503 yanıtları ve bağlantı zaman aşımlarını tanır

**Keşif**
- WordPress sürüm tespiti (meta tag, RSS feed, generator tag)
- Gizli giriş URL keşfi (15+ yaygın yol: /giris, /login, /panel, /admin...)
- XML-RPC durum kontrolü direkt POST ile (GET değil — yanlış negatif önler)
- WAF tespiti (Cloudflare, Sucuri, Wordfence)
- CAPTCHA tespiti (reCAPTCHA, Turnstile, hCaptcha)
- Kullanıcı keşfi (REST API, `?rest_route=` bypass, `?author=N` numaralandırma)
- Eklenti ve sürüm parmak izi HTML kaynağından

**Kullanım Kolaylığı**
- Ok tuşlarıyla etkileşimli seçim menüleri
- Renkli terminal çıktısı ve ilerleme çubukları
- Devam desteği: ilerlemeyi kaydeder, kesintiden sonra devam eder
- Çoklu dil: İngilizce (varsayılan) ve Türkçe
- JSON yapılandırma dosyası desteği
- False positive koruması: her aday direkt API çağrısıyla doğrulanır
- Detaylı loglama ve markdown rapor üretimi

### Kurulum

```bash
git clone https://github.com/umutsevimcann/wp-brute-pro.git
cd wp-brute-pro
pip install requests
```

Başka bağımlılık gerekmiyor.

### Hızlı Başlangıç

```bash
# Etkileşimli mod — ok tuşlu menülerle adım adım kurulum
python wp_brute.py

# CLI mod — direkt çalıştırma
python wp_brute.py -u https://hedef.com -U admin --lang tr

# Firma bilgisiyle akıllı wordlist
python wp_brute.py -u https://hedef.com -U admin --company "Ornek Teknoloji" --crawl --lang tr
```

### Kullanım Örnekleri

**Otomatik algılamalı temel tarama:**
```bash
python wp_brute.py -u https://hedef.com -U admin --lang tr -v
```

**Tam seçenekler:**
```bash
python wp_brute.py \
  -u https://hedef.com \
  -U admin,editor \
  --company "Ornek Teknoloji" \
  --keywords "yazilim,tasarim,destek" \
  --crawl \
  --method xmlrpc \
  --batch-size 50 \
  --delay 3 \
  --proxy-list proxies.txt \
  --resume \
  --lang tr \
  -v
```

**Proxy rotasyonu ile:**
```bash
python wp_brute.py \
  -u https://hedef.com \
  -U admin \
  --proxy-list proxies.txt \
  --batch-size 30 \
  --delay 3 \
  --resume --lang tr -v
```

### Parametreler

| Parametre | Kısa | Varsayılan | Açıklama |
|-----------|------|------------|----------|
| `--url` | `-u` | — | Hedef WordPress URL |
| `--users` | `-U` | otomatik | Kullanıcı adları, virgülle. Boş = otomatik keşif |
| `--method` | | `auto` | Saldırı yöntemi: `auto`, `xmlrpc`, `wplogin`, `restapi` |
| `--batch-size` | | `50` | XML-RPC istek başına şifre sayısı (10-200) |
| `--delay` | | `3.0` | İstekler arası bekleme süresi (0.5-10 saniye) |
| `--company` | | — | Hedefli wordlist üretimi için firma adı |
| `--keywords` | | — | Wordlist için ek anahtar kelimeler, virgülle |
| `--crawl` | | kapalı | Hedef siteden anahtar kelime çek |
| `--wordlist` | | — | Ek wordlist dosyası yolu |
| `--proxy` | | — | Tek proxy: `http://ip:port` veya `socks5://ip:port` |
| `--proxy-list` | | — | Proxy listesi dosyası, satır satır |
| `--output` | | `results` | Rapor ve loglar için çıktı dizini |
| `--config` | | — | JSON yapılandırma dosyası |
| `--resume` | | kapalı | Önceki ilerlemeden devam et |
| `--lang` | | `en` | Dil: `en` veya `tr` |
| `--no-scan` | | kapalı | Keşif aşamasını atla |
| `--verbose` | `-v` | kapalı | Detaylı çıktı göster |
| `--interactive` | `-i` | — | Etkileşimli modu zorla |

### Saldırı Akışı

```
Faz 1: KEŞİF
├── WordPress sürümünü tespit et
├── Giriş URL'sini bul (gizli yollar dahil)
├── XML-RPC durumunu kontrol et (direkt POST testi)
├── WAF tespit et (Cloudflare, Sucuri, Wordfence)
├── CAPTCHA kontrolü
├── Kullanıcıları keşfet (REST API, author enum)
└── Eklenti ve sürüm parmak izi

Faz 2: STRATEJİ
├── XML-RPC aktifse → multicall (en hızlı)
├── XML-RPC kapalıysa → wp-login.php POST
├── İkisi de kapalıysa → REST API Basic Auth
└── Login'de CAPTCHA varsa → XML-RPC'ye geç

Faz 3: WORDLIST ÜRETİMİ
├── Katman 1: Firma + kullanıcı adı kombinasyonları (~500)
├── Katman 2: Site crawl kelimeleri + ek kelimeler (~200)
├── Katman 3: Yaygın zayıf şifreler (~200)
├── Katman 4: Tüm üsttekilerin mutasyonları (~15.000+)
└── Katman 5: Harici wordlist dosyası (opsiyonel)

Faz 4: SALDIRI
├── Öncelik sırasıyla batch'ler gönder
├── Yanıtları başarı göstergesi için parse et
├── Aday bulunursa → direkt API çağrısıyla doğrula
├── Engel alınırsa → delay artır, batch küçült
├── Ban algılanırsa → proxy değiştir veya bekle
└── Her batch sonrası ilerlemeyi kaydet

Faz 5: RAPOR
├── results/report.md  — Okunabilir rapor
├── results/found.txt  — Bulunan şifreler
├── results/state.json — Devam etmek için durum
├── results/tried.txt  — Denenen şifreler
└── results/log.txt    — Detaylı log
```

### Mimari

```
wp-brute-pro/
├── wp_brute.py              # Ana CLI giriş noktası
├── ui.py                    # Terminal UI (renkler, menüler, ilerleme)
├── lang.py                  # Çoklu dil desteği (EN/TR)
├── core/
│   ├── scanner.py           # Hedef keşif
│   ├── xmlrpc.py            # XML-RPC multicall saldırı
│   ├── wplogin.py           # wp-login.php POST saldırı
│   ├── restapi.py           # REST API Basic Auth saldırı
│   └── validator.py         # False positive doğrulama
├── wordlist/
│   ├── generator.py         # 5 katmanlı şifre üretici
│   ├── mutator.py           # Leet, harf, sonek mutasyonları
│   └── common.txt           # Yaygın zayıf şifreler
├── evasion/
│   ├── useragent.py         # User-Agent rotasyonu
│   ├── throttle.py          # Uyarlanabilir hız kontrolü
│   └── proxy.py             # Proxy rotasyonu
├── state/
│   └── tracker.py           # İlerleme takibi ve devam
└── output/
    └── reporter.py          # Rapor üretici
```

---

## Legal Disclaimer / Yasal Uyarı

This tool is designed for **authorized penetration testing only**. Unauthorized access to computer systems is illegal. The user assumes all responsibility for compliance with applicable laws.

Bu araç yalnızca **yetkili penetrasyon testleri** için tasarlanmıştır. Bilgisayar sistemlerine yetkisiz erişim yasadışıdır. Kullanıcı, geçerli yasalara uygunluk konusunda tüm sorumluluğu üstlenir.

---

<p align="center">
  Made with Python | <a href="https://github.com/umutsevimcann/wp-brute-pro">GitHub</a>
</p>
