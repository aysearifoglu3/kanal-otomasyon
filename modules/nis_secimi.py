"""Nis ve konu secimi: LLM'e nis listesinden bir konu ve aci sectirir."""
import json
import anthropic
import config


def konu_sec() -> dict:
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    nis_metni = "\n".join(f"- {n}" for n in config.NIS_LISTESI)

    prompt = f"""Asagidaki nis listesinden bir tanesini sec ve YouTube'da yuzsuz (faceless)
bir kanal icin ilgi cekici, spesifik bir video konusu oner.

Nis listesi:
{nis_metni}

Sadece su JSON formatinda cevap ver, baska hicbir sey yazma:
{{"nis": "...", "konu": "...", "aci": "video bu konuyu hangi aciodan ele alacak, 1 cumle"}}"""

    yanit = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    metin = yanit.content[0].text.strip()
    return json.loads(metin)


if __name__ == "__main__":
    print(konu_sec())
