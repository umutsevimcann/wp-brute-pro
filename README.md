# WP-BRUTE-PRO v3.0

> **[Türkçe](#türkçe)** | **[English](#english)**

---

<a name="english"></a>
## English

WordPress password testing tool for authorized penetration testing. Features colored TUI, arrow-key selection, smart wordlist generation, proxy rotation, and ban evasion.

### Installation

```bash
pip install requests
```

### Quick Start

```bash
# Interactive mode (recommended) — asks questions, you pick options
python wp_brute.py

# CLI mode
python wp_brute.py -u https://target.com -U admin

# Turkish interface
python wp_brute.py --lang tr
```

### Features

| Feature | Description |
|---------|-------------|
| **3 Attack Methods** | XML-RPC multicall (fast), wp-login.php POST, REST API Basic Auth |
| **Auto Discovery** | Detects WP version, login URL (hidden too), XML-RPC, WAF, CAPTCHA, users |
| **Smart Wordlist** | 5-layer generation: company, username, site crawl, mutations, common |
| **Proxy Rotation** | Auto-switch proxy on ban, supports HTTP/SOCKS5 |
| **Ban Evasion** | Adaptive throttling, auto delay increase, batch size reduction |
| **Resume** | Saves progress, continue after ban/restart with `--resume` |
| **Arrow Key UI** | Select options with arrow keys, colored output, progress bars |
| **Multi-language** | English (default) and Turkish |
| **False Positive Protection** | Every candidate verified with direct API call |

### Usage

```bash
# Full options
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

# From config file
python wp_brute.py --config config.json
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-u, --url` | — | Target WordPress URL |
| `-U, --users` | auto | Usernames (comma separated) |
| `--method` | auto | Attack method: auto/xmlrpc/wplogin/restapi |
| `--batch-size` | 50 | Passwords per XML-RPC request |
| `--delay` | 3.0 | Seconds between requests |
| `--company` | — | Company name for wordlist generation |
| `--keywords` | — | Extra keywords for wordlist |
| `--crawl` | off | Crawl site for words (like CeWL) |
| `--wordlist` | — | Extra wordlist file path |
| `--proxy` | — | Single proxy: `http://ip:port` |
| `--proxy-list` | — | Proxy list file (one per line) |
| `--resume` | off | Continue from where it left off |
| `--lang` | en | Language: en/tr |
| `--config` | — | JSON config file |
| `-v` | off | Verbose output |

### Language

```bash
# English (default)
python wp_brute.py -u https://target.com -U admin

# Turkish
python wp_brute.py -u https://target.com -U admin --lang tr

# Interactive mode auto-asks language at start
python wp_brute.py
```

### Output

```
results/
├── report.md    — Human-readable report
├── found.txt    — Found credentials (user:pass)
├── state.json   — State file (for resume)
├── tried.txt    — Tried passwords
└── log.txt      — Detailed log
```

---

<a name="türkçe"></a>
## Türkçe

WordPress şifre test aracı — yetkili penetrasyon testleri için. Renkli TUI, ok tuşu seçim, akıllı wordlist üretimi, proxy rotasyonu ve ban koruması.

### Kurulum

```bash
pip install requests
```

### Hızlı Başlangıç

```bash
# İnteraktif mod (önerilen) — sorular sorar, okla seç
python wp_brute.py

# CLI mod
python wp_brute.py -u https://hedef.com -U admin --lang tr

# Türkçe arayüz
python wp_brute.py --lang tr
```

### Özellikler

| Özellik | Açıklama |
|---------|----------|
| **3 Saldırı Yöntemi** | XML-RPC multicall (hızlı), wp-login.php POST, REST API Basic Auth |
| **Otomatik Keşif** | WP sürümü, login URL (gizli dahil), XML-RPC, WAF, CAPTCHA, kullanıcılar |
| **Akıllı Wordlist** | 5 katman: firma, kullanıcı, site crawl, mutasyonlar, yaygın şifreler |
| **Proxy Rotasyonu** | Ban'da otomatik proxy değiştirme, HTTP/SOCKS5 desteği |
| **Ban Koruması** | Adaptif hız kontrolü, otomatik delay artırma, batch küçültme |
| **Resume** | İlerleme kaydeder, ban/kapatma sonrası `--resume` ile devam |
| **Ok Tuşu UI** | Seçenekleri okla seç, renkli çıktı, progress bar |
| **Çoklu Dil** | İngilizce (varsayılan) ve Türkçe |
| **False Positive Koruması** | Her aday direkt API çağrısıyla doğrulanır |

### Kullanım

```bash
# Tam seçenekler
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

### Parametreler

| Parametre | Varsayılan | Açıklama |
|-----------|------------|----------|
| `-u, --url` | — | Hedef WordPress URL |
| `-U, --users` | otomatik | Kullanıcı adları (virgülle) |
| `--method` | auto | Saldırı yöntemi: auto/xmlrpc/wplogin/restapi |
| `--batch-size` | 50 | İstek başına şifre sayısı |
| `--delay` | 3.0 | İstekler arası bekleme (saniye) |
| `--company` | — | Wordlist için firma adı |
| `--keywords` | — | Wordlist için ek kelimeler |
| `--crawl` | kapalı | Siteden kelime çek (CeWL benzeri) |
| `--wordlist` | — | Ek wordlist dosyası |
| `--proxy` | — | Tek proxy: `http://ip:port` |
| `--proxy-list` | — | Proxy listesi dosyası |
| `--resume` | kapalı | Kaldığı yerden devam |
| `--lang` | en | Dil: en/tr |
| `--config` | — | JSON config dosyası |
| `-v` | kapalı | Detaylı çıktı |

### Mimari

```
wp-brute-pro/
├── wp_brute.py          # Ana CLI
├── ui.py                # Renkli TUI (progress, seçim, banner)
├── lang.py              # Çoklu dil desteği (EN/TR)
├── core/
│   ├── scanner.py       # Hedef keşif
│   ├── xmlrpc.py        # XML-RPC multicall saldırı
│   ├── wplogin.py       # wp-login.php POST saldırı
│   ├── restapi.py       # REST API Basic Auth saldırı
│   └── validator.py     # False positive koruması
├── wordlist/
│   ├── generator.py     # 5 katmanlı şifre üretici
│   ├── mutator.py       # Leet, case, suffix mutasyonları
│   └── common.txt       # Yaygın şifreler
├── evasion/
│   ├── useragent.py     # User-Agent rotasyonu
│   ├── throttle.py      # Akıllı hız kontrolü
│   └── proxy.py         # Proxy rotasyonu
├── state/
│   └── tracker.py       # Resume desteği
└── output/
    └── reporter.py      # Rapor üretici
```

### Yasal Uyarı / Legal Disclaimer

Bu araç yalnızca **yetkili penetrasyon testleri** için tasarlanmıştır.
This tool is designed for **authorized penetration testing** only.
Unauthorized use is illegal and strictly prohibited.
