"""Sahne gorsel+ses ikililerini Ken Burns efektiyle video klibe cevirir ve birlestirir.
Sistemde ffmpeg ve ffprobe kurulu olmali (https://ffmpeg.org/download.html)."""
import subprocess
import json
from pathlib import Path


def ses_suresi(ses_yolu: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(ses_yolu),
    ]
    cikti = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(json.loads(cikti.stdout)["format"]["duration"])


def sahne_klip_olustur(gorsel_yolu: Path, ses_yolu: Path, hedef_yol: Path):
    sure = ses_suresi(ses_yolu) + 0.3
    # Ken Burns: yavas zoom-in efekti
    zoompan = (
        f"scale=1600:900,zoompan=z='min(zoom+0.0008,1.15)':d={int(sure * 25)}:"
        f"s=1280x720:fps=25"
    )
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(gorsel_yolu), "-i", str(ses_yolu),
        "-filter:v", zoompan, "-c:v", "libx264", "-t", str(sure),
        "-c:a", "aac", "-shortest", "-pix_fmt", "yuv420p", str(hedef_yol),
    ]
    subprocess.run(cmd, check=True)


def klipleri_birlestir(klip_yollari: list, hedef_yol: Path):
    liste_dosyasi = hedef_yol.parent / "klip_listesi.txt"
    liste_dosyasi.write_text(
        "\n".join(f"file '{k.resolve()}'" for k in klip_yollari)
    )
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(liste_dosyasi),
        "-c", "copy", str(hedef_yol),
    ]
    subprocess.run(cmd, check=True)
