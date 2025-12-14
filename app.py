import os
import io
import datetime
from contextlib import redirect_stdout

import pandas as pd
from flask import Flask, render_template, request, send_from_directory

from fcfs import fcfs
from nonpreemptive_sjf import non_preemptive_sjf


# -------------------------------
# KLASÖR AYARLARI
# -------------------------------

UYGULAMA_DIZINI = os.path.dirname(os.path.abspath(__file__))
YUKLEME_DIZINI = os.path.join(UYGULAMA_DIZINI, "uploads")
CIKTI_DIZINI = os.path.join(UYGULAMA_DIZINI, "outputs")

os.makedirs(YUKLEME_DIZINI, exist_ok=True)
os.makedirs(CIKTI_DIZINI, exist_ok=True)

app = Flask(__name__)

# -------------------------------
# KULLANILACAK ALGORİTMALAR
# -------------------------------

ALGORITMALAR = {
    "FCFS": fcfs,
    "Non_Preemptive_SJF": non_preemptive_sjf,
}

# -------------------------------
# ALGORİTMA ÇIKTISINI YAKALAMA
# -------------------------------

def algoritma_calistir_ve_yakala(algoritma_fonksiyonu, veri_cercevesi):
    """
    Algoritmanın print() ile bastığı çıktıyı string olarak yakalar
    """
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        algoritma_fonksiyonu(veri_cercevesi)
    return tampon.getvalue()


# -------------------------------
# DOSYA ADI TEMİZLEME
# -------------------------------

def guvenli_dosya_adi(dosya_adi):
    izinli = "._-"
    return "".join(h for h in dosya_adi if h.isalnum() or h in izinli) or "girdi.csv"


# -------------------------------
# ANA SAYFA
# -------------------------------

@app.get("/")
def ana_sayfa():
    cikti_dosyalari = sorted(
        [f for f in os.listdir(CIKTI_DIZINI) if f.endswith(".txt")],
        reverse=True
    )
    return render_template("index.html", dosyalar=cikti_dosyalari)


# -------------------------------
# CSV YÜKLEME
# -------------------------------

@app.post("/upload")
def csv_yukle():
    dosya = request.files.get("csv")

    if not dosya or not dosya.filename.lower().endswith(".csv"):
        return "Lütfen geçerli bir CSV dosyası yükleyin.", 400

    dosya_adi = guvenli_dosya_adi(dosya.filename)
    yukleme_yolu = os.path.join(YUKLEME_DIZINI, dosya_adi)
    dosya.save(yukleme_yolu)

    # CSV → DataFrame
    df = pd.read_csv(yukleme_yolu)

    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temel_ad = os.path.splitext(dosya_adi)[0]

    # Algoritmaları çalıştır
    for alg_adi, alg_fonk in ALGORITMALAR.items():
        cikti_metin = algoritma_calistir_ve_yakala(alg_fonk, df.copy())

        cikti_dosya_adi = f"{temel_ad}__{alg_adi}__{zaman_damgasi}.txt"
        cikti_yolu = os.path.join(CIKTI_DIZINI, cikti_dosya_adi)

        with open(cikti_yolu, "w", encoding="utf-8") as f:
            f.write(cikti_metin)

    return "Algoritmalar başarıyla çalıştırıldı.", 200


# -------------------------------
# ÇIKTI DOSYASI İNDİRME
# -------------------------------

@app.get("/outputs/<dosya_adi>")
def cikti_indir(dosya_adi):
    return send_from_directory(CIKTI_DIZINI, dosya_adi, as_attachment=True)


# -------------------------------
# UYGULAMAYI BAŞLAT
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
