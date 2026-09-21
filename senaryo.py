"""Secilen konudan sahne sahne senaryo uretir."""
import json
import anthropic
import config


def senaryo_yaz(konu: dict, sahne_sayisi: int = None) -> dict:
    sahne_sayisi = sahne_sayisi or config.SAHNE_SAYISI
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    prompt = f"""Konu: {konu['konu']}
Aci: {konu['aci']}

Bu konu icin YouTube faceless video senaryosu yaz. Tam olarak {sahne_sayisi} sahneye bol.
Her sahne icin: anlatici metni (seslendirilecek, 2-4 cumle, Turkce) ve o sahnede gosterilecek
gorseli tarif eden kisa bir Ingilizce gorsel arama sorgusu (stok gorsel bulmak icin).

Sadece su JSON formatinda cevap ver:
{{"baslik_taslak": "...", "sahneler": [{{"metin": "...", "gorsel_sorgu": "..."}}, ...]}}"""

    yanit = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(yanit.content[0].text.strip())


if __name__ == "__main__":
    ornek_konu = {"nis": "bilim ve uzay", "konu": "Kara delikler", "aci": "test"}
    print(senaryo_yaz(ornek_konu))
