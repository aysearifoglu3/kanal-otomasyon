"""Video icin baslik, aciklama ve etiket uretir."""
import json
import anthropic
import config


def seo_uret(baslik_taslak: str, sahneler_metni: str) -> dict:
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    prompt = f"""Bu YouTube videosu icin tiklanabilir bir baslik, izleyiciyi bilgilendiren
bir aciklama (2-3 paragraf) ve 10-15 SEO etiketi uret.

Taslak baslik: {baslik_taslak}
Video icerigi ozeti: {sahneler_metni[:1500]}

Sadece su JSON formatinda cevap ver:
{{"baslik": "...", "aciklama": "...", "etiketler": ["...", "..."]}}"""

    yanit = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(yanit.content[0].text.strip())
