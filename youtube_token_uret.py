"""TEK SEFERLIK kurulum scripti: YouTube OAuth token'ini yerel bilgisayarinda uretir.
GitHub Actions icinde tarayici acilamadigi icin bu adim senin bilgisayarinda yapilmali,
sonra ciktiyi GitHub secret olarak eklersin.

Kullanim:
  1. Google Cloud Console'dan client_secrets.json indir, proje kokune koy.
  2. python youtube_token_uret.py  calistir, tarayicidan Google hesabinla giris yap.
  3. Olusan youtube_token.json dosyasini base64'e cevir ve GitHub secret'a ekle:
       macOS/Linux: base64 -i youtube_token.json | pbcopy
       (pbcopy yoksa: base64 -i youtube_token.json > token_b64.txt, dosyayi ac kopyala)
     GitHub repo -> Settings -> Secrets and variables -> Actions -> New secret
       Ad: YOUTUBE_TOKEN_B64
     Ayni sekilde client_secrets.json'i da base64'leyip YOUTUBE_CLIENT_SECRETS_B64
     secret'ina ekle.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def uret():
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("youtube_token.json", "w") as f:
        f.write(creds.to_json())
    print("youtube_token.json olusturuldu. README'deki base64 adimina gec.")


if __name__ == "__main__":
    uret()
