"""Pexels API ile sahne basina stok gorsel indirir."""
import requests
from pathlib import Path
import config


def gorsel_indir(sorgu: str, hedef_yol: Path) -> Path:
    headers = {"Authorization": config.PEXELS_API_KEY}
    params = {"query": sorgu, "per_page": 1, "orientation": "landscape"}
    r = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=30)
    r.raise_for_status()
    sonuclar = r.json().get("photos", [])
    if not sonuclar:
        raise ValueError(f"'{sorgu}' icin gorsel bulunamadi")

    gorsel_url = sonuclar[0]["src"]["large2x"]
    veri = requests.get(gorsel_url, timeout=60).content
    hedef_yol.write_bytes(veri)
    return hedef_yol


if __name__ == "__main__":
    gorsel_indir("black hole space", Path("test.jpg"))
