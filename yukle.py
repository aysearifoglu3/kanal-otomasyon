"""YouTube'a yukleme. Bu script SADECE sen manuel calistirdiginda video yukler.
main.py bunu asla otomatik cagirmaz - son onay her zaman insanda kalir.

Kullanim: python yukle.py <video_id>
(video_id, onay_bekleyen/ altindaki klasor adidir)
"""
import sys
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def yetkilendir():
    creds = None
    token_yolu = Path(config.YOUTUBE_TOKEN_FILE)
    if token_yolu.exists():
        creds = Credentials.from_authorized_user_file(str(token_yolu), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.YOUTUBE_CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        token_yolu.write_text(creds.to_json())
    return creds


def yukle(video_id: str):
    dizin = config.ONAY_BEKLEYEN_DIR / video_id
    video_yolu = dizin / "final_video.mp4"
    metadata = json.loads((dizin / "metadata.json").read_text())

    creds = yetkilendir()
    youtube = build("youtube", "v3", credentials=creds)

    istek_govdesi = {
        "snippet": {
            "title": metadata["baslik"],
            "description": metadata["aciklama"],
            "tags": metadata["etiketler"],
            "categoryId": "27",  # Egitim - ihtiyaca gore degistir
        },
        # Onay icin once 'private' yukleniyor - sen izleyip YouTube Studio'dan
        # 'public' yapana kadar kimse goremez.
        "status": {"privacyStatus": "private"},
    }

    medya = MediaFileUpload(str(video_yolu), chunksize=-1, resumable=True)
    istek = youtube.videos().insert(
        part="snippet,status", body=istek_govdesi, media_body=medya
    )
    yanit = istek.execute()
    print(f"Yuklendi (private): https://studio.youtube.com/video/{yanit['id']}/edit")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanim: python yukle.py <video_id>")
        sys.exit(1)
    yukle(sys.argv[1])
