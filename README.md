# Kanal Otomasyonu

Faceless YouTube kanalı için uçtan uca AI içerik hattı. **Yükleme dışında her adım
otomatik**; yükleme bilinçli olarak ayrı bir script (`yukle.py`) ve sadece sen
çalıştırdığında video YouTube'a gider.

## Akış

```
main.py  → niş seçimi → senaryo → sahne başına görsel+ses → montaj → SEO metni
           (hepsi otomatik, onay_bekleyen/<video_id>/ klasörüne kaydedilir)

sen      → videoyu izlersin, metadata.json'u kontrol edersin

yukle.py → sadece sen çalıştırınca YouTube'a "private" olarak yükler
           (sen YouTube Studio'dan public yaparsın)
```

## Kurulum

1. **Python 3.10+** ve **ffmpeg** kurulu olmalı (`ffmpeg -version` ile kontrol et).
2. Bağımlılıkları kur:
   ```
   pip install -r requirements.txt
   ```
3. `.env.example` dosyasını `.env` olarak kopyala ve kendi API anahtarlarını gir:
   - **Anthropic**: console.anthropic.com — senaryo/SEO metni için
   - **Pexels**: pexels.com/api — ücretsiz stok görsel için
   - **ElevenLabs**: elevenlabs.io — Türkçe seslendirme için
   - **Telegram bot** (opsiyonel): BotFather ile bot oluştur, token ve kendi chat_id'ni gir
4. YouTube yüklemesi için Google Cloud Console'dan bir proje aç, YouTube Data API v3'ü
   etkinleştir, OAuth istemci kimliği (Desktop app) oluştur ve `client_secrets.json`
   olarak proje köküne indir. İlk `yukle.py` çalıştırmanda tarayıcı açılıp senden
   giriş isteyecek, sonrasında token dosyaya kaydedilir.

## Kullanım

```
python main.py              # yeni bir video otomatik üretir
python yukle.py <video_id>  # onay_bekleyen/ altındaki bir videoyu yükler
```

`video_id`, `onay_bekleyen/` altında oluşan klasörün adıdır (örn. `20260916_1430_a1b2c3`).

## Zamanlama (opsiyonel)

`main.py`'yi otomatik tetiklemek için cron kullanabilirsin (Mac/Linux):
```
crontab -e
# Her gün saat 09:00'da bir video hazırla:
0 9 * * * cd /proje/yolu && /usr/bin/python3 main.py >> log.txt 2>&1
```
`yukle.py`'yi **asla** cron'a ekleme — o senin bilinçli tetiklediğin adım olarak kalmalı.

## GitHub Actions ile bulutta çalıştırma (önerilen)

Bu sayede bilgisayarın kapalıyken bile sistem kendi kendine video üretir.

### 1. Repo oluştur
Bu klasörü yeni bir GitHub reposuna push'la (private repo öneririm, API anahtarların
kod içinde olmasa da içerikler görünür olur).

### 2. Secrets ekle
Repo → **Settings → Secrets and variables → Actions → New repository secret** yolundan
şunları tek tek ekle:

| Secret adı | Değer |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API anahtarın |
| `PEXELS_API_KEY` | Pexels API anahtarın |
| `ELEVENLABS_API_KEY` | ElevenLabs API anahtarın |
| `ELEVENLABS_VOICE_ID` | Kullanacağın ses ID'si |
| `TELEGRAM_BOT_TOKEN` | Bildirim botu token'ı |
| `TELEGRAM_CHAT_ID` | Senin chat ID'n |
| `YOUTUBE_CLIENT_SECRETS_B64` | `client_secrets.json`'ın base64 hali |
| `YOUTUBE_TOKEN_B64` | `youtube_token.json`'ın base64 hali (aşağıya bak) |

### 3. YouTube token'ını bir kere yerelde üret
GitHub Actions'ta tarayıcı açılamadığı için bu tek adımı kendi bilgisayarında yapman
gerekiyor:
```
pip install -r requirements.txt
python youtube_token_uret.py
```
Tarayıcı açılıp Google hesabınla giriş yapmanı isteyecek. İşlem bitince oluşan
`youtube_token.json` ve `client_secrets.json` dosyalarını base64'e çevirip yukarıdaki
iki secret'a yapıştır (detay için `youtube_token_uret.py` içindeki yorumlara bak).
Bu token uzun ömürlü (refresh token içerir), tekrar tekrar yapmana gerek yok.

### 4. İki workflow nasıl çalışır
- **`video_uret`**: Her gün otomatik tetiklenir (saat `.github/workflows/video_uret.yml`
  içinde `cron` satırından ayarlanır), tüm AI adımlarını çalıştırır, videoyu Telegram'a
  yollar ve GitHub Actions "Artifacts" bölümüne yükler.
- **`video_yukle`**: **Otomatik tetiklenmez.** Telegram'dan videoyu izleyip
  onayladıktan sonra Actions sekmesinden elle "Run workflow" ile, `kaynak_run_id`
  (video_uret'in çalıştırma numarası) ve `video_id` (Telegram mesajında yazar)
  girerek sen tetiklersin. Bu, insan onayının sisteme gömülü kalmasını sağlar.

## Önemli notlar

- Bu kod bir **iskelet/başlangıç noktası**. Gerçek API anahtarlarıyla ilk çalıştırmada
  muhtemelen küçük hatalar çıkacaktır (JSON parse hataları, API limitleri, ffmpeg
  filtre ince ayarları) — bunlar normal, birlikte debug edebiliriz.
- `NIS_LISTESI` (config.py) ve prompt'lar (`modules/*.py` içindeki metinler) senin
  kanalının tonuna göre özelleştirilmeli — şu an genel amaçlı yazıldı.
- Videolar önce **private** yüklenir; sen kontrol edip public yapmadan kimse göremez.
- Telif hakkı: Pexels görselleri ücretsiz ticari kullanım için uygundur, yine de
  video yayınlamadan önce lisans şartlarını kontrol et.
