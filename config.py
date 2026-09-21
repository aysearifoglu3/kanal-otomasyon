import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ONAY_BEKLEYEN_DIR = BASE_DIR / "onay_bekleyen"
ONAY_BEKLEYEN_DIR.mkdir(exist_ok=True)

# LLM (nis, senaryo, SEO metni icin)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-6")

# Gorsel kaynagi (Pexels ucretsiz stok gorsel API - pexels.com/api)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Seslendirme (ElevenLabs)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")

# YouTube yukleme (Google Cloud Console'dan OAuth client_secrets.json indirilmeli)
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
YOUTUBE_TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "youtube_token.json")

# Telegram bildirimi (opsiyonel - video hazir olunca sana mesaj atar)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Kanal nis listesi - kendi ilgi alanina gore duzenle
NIS_LISTESI = [
    "tarih ve gizemli olaylar",
    "bilim ve uzay",
    "kisisel gelisim ve motivasyon",
    "para ve finans egitimi",
]

SAHNE_SAYISI = int(os.getenv("SAHNE_SAYISI", "6"))
