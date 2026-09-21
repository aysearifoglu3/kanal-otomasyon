"""ElevenLabs ile sahne metnini seslendirir."""
import requests
from pathlib import Path
import config


def seslendir(metin: str, hedef_yol: Path) -> Path:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": config.ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": metin,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    hedef_yol.write_bytes(r.content)
    return hedef_yol


if __name__ == "__main__":
    seslendir("Merhaba, bu bir test.", Path("test.mp3"))
