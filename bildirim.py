"""Telegram uzerinden bildirim ve video onizleme gonderir.
GitHub Actions'ta calisirken sonucu gormek icin en pratik yol budur -
Actions sekmesine girmene gerek kalmadan videoyu telefonundan izleyebilirsin."""
from pathlib import Path
import requests
import config


def mesaj_gonder(mesaj: str):
    if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID):
        print("[bildirim] Telegram ayarli degil, mesaj atlanadi.")
        return
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": config.TELEGRAM_CHAT_ID, "text": mesaj}, timeout=15)


def video_gonder(video_yolu: Path, aciklama: str = ""):
    if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID):
        return
    # Telegram Bot API'de dosya boyutu limiti ~50MB. Asarsa sadece mesaj atilir,
    # video GitHub Actions'in 'Artifacts' bolumunden indirilebilir.
    if video_yolu.stat().st_size > 49 * 1024 * 1024:
        mesaj_gonder(f"{aciklama}\n\n(Video 50MB sinirini astigi icin Actions "
                     f"artifact'inden indirmen gerekiyor.)")
        return
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(video_yolu, "rb") as f:
        requests.post(
            url,
            data={"chat_id": config.TELEGRAM_CHAT_ID, "caption": aciklama},
            files={"video": f},
            timeout=120,
        )
