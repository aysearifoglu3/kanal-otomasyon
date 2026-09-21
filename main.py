"""Orkestrator: nis seciminden montaja kadar tum otomatik adimlari calistirir.
YouTube'a YUKLEME BURADA YOK - o adim bilincli olarak yukle.py'de, senin
manuel onayinla calisir.

Kullanim: python main.py
"""
import json
import uuid
from datetime import datetime

import config
import bildirim
from modules import nis_secimi, senaryo, gorsel_video, seslendirme, montaj, seo_metin


def calistir():
    video_id = f"{datetime.now().strftime('%Y%m%d_%H%M')}_{uuid.uuid4().hex[:6]}"
    calisma_dizini = config.ONAY_BEKLEYEN_DIR / video_id
    calisma_dizini.mkdir(parents=True)

    print("1/6 Nis ve konu seciliyor...")
    konu = nis_secimi.konu_sec()

    print("2/6 Senaryo yaziliyor...")
    senaryo_veri = senaryo.senaryo_yaz(konu)
    sahneler = senaryo_veri["sahneler"]

    klip_yollari = []
    for i, sahne in enumerate(sahneler):
        print(f"3-4/6 Sahne {i + 1}/{len(sahneler)}: gorsel + seslendirme...")
        gorsel_yolu = calisma_dizini / f"sahne_{i:02d}.jpg"
        ses_yolu = calisma_dizini / f"sahne_{i:02d}.mp3"
        klip_yolu = calisma_dizini / f"sahne_{i:02d}.mp4"

        gorsel_video.gorsel_indir(sahne["gorsel_sorgu"], gorsel_yolu)
        seslendirme.seslendir(sahne["metin"], ses_yolu)
        montaj.sahne_klip_olustur(gorsel_yolu, ses_yolu, klip_yolu)
        klip_yollari.append(klip_yolu)

    print("5/6 Sahneler birlestiriliyor...")
    final_video_yolu = calisma_dizini / "final_video.mp4"
    montaj.klipleri_birlestir(klip_yollari, final_video_yolu)

    print("6/6 Baslik, aciklama, etiket uretiliyor...")
    tum_metin = " ".join(s["metin"] for s in sahneler)
    seo = seo_metin.seo_uret(senaryo_veri.get("baslik_taslak", konu["konu"]), tum_metin)

    metadata = {"nis": konu["nis"], "konu": konu["konu"], **seo}
    (calisma_dizini / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2)
    )

    print(f"\nTamamlandi: {calisma_dizini}")
    bildirim.video_gonder(
        final_video_yolu,
        aciklama=(
            f"Yeni video hazir\n\n"
            f"Baslik: {metadata['baslik']}\n\n"
            f"Onaylarsan GitHub Actions'ta 'video_yukle' workflow'unu su "
            f"degerlerle calistir:\n"
            f"  video_id: {video_id}\n"
            f"  kaynak_run_id: (bu calistirmanin Actions run numarasi)"
        ),
    )


if __name__ == "__main__":
    calistir()
