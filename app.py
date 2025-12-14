"""
CPU Scheduling Simülatörü - Flask Web Uygulaması

CSV dosyası yükleme, CPU zamanlama algoritmalarını çalıştırma ve sonuçları kaydetme.
"""

import os
import io
import datetime
from contextlib import redirect_stdout

import pandas as pd
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for

from fcfs import fcfs
from nonpreemptive_sjf import non_preemptive_sjf


# Klasör ayarları
UYGULAMA_DIZINI = os.path.dirname(os.path.abspath(__file__))
YUKLEME_DIZINI = os.path.join(UYGULAMA_DIZINI, "uploads")
CIKTI_DIZINI = os.path.join(UYGULAMA_DIZINI, "outputs")

os.makedirs(YUKLEME_DIZINI, exist_ok=True)
os.makedirs(CIKTI_DIZINI, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Algoritmalar
ALGORITMALAR = {
    "FCFS": fcfs,
    "Non_Preemptive_SJF": non_preemptive_sjf,
}


def algoritma_calistir_ve_yakala(algoritma_fonksiyonu, df):
    """Algoritmanın print() çıktısını string olarak yakalar."""
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        algoritma_fonksiyonu(df)
    return tampon.getvalue()


def guvenli_dosya_adi(dosya_adi):
    """Dosya adından zararlı karakterleri temizler."""
    izinli = "._-"
    temizlenmis = "".join(h for h in dosya_adi if h.isalnum() or h in izinli)
    return temizlenmis if temizlenmis else "girdi.csv"


def csv_dogrula(df):
    """CSV dosyasının formatını ve verilerini doğrular."""
    gerekli_sutunlar = ["Process_ID", "Arrival_Time", "CPU_Burst_Time"]
    
    if not all(sutun in df.columns for sutun in gerekli_sutunlar):
        eksik = [s for s in gerekli_sutunlar if s not in df.columns]
        return False, f"Eksik sütunlar: {', '.join(eksik)}"
    
    if df[gerekli_sutunlar].isnull().any().any():
        return False, "CSV dosyasında boş değerler bulunmaktadır."
    
    try:
        df["Arrival_Time"] = pd.to_numeric(df["Arrival_Time"], errors='raise')
        df["CPU_Burst_Time"] = pd.to_numeric(df["CPU_Burst_Time"], errors='raise')
        
        if (df["Arrival_Time"] < 0).any() or (df["CPU_Burst_Time"] <= 0).any():
            return False, "Arrival_Time >= 0 ve CPU_Burst_Time > 0 olmalıdır."
    except (ValueError, TypeError):
        return False, "Arrival_Time ve CPU_Burst_Time sayısal değerler olmalıdır."
    
    return True, "CSV dosyası geçerli."


@app.get("/")
def ana_sayfa():
    """Ana sayfa - çıktı dosyalarını listeler."""
    try:
        dosyalar = sorted(
            [f for f in os.listdir(CIKTI_DIZINI) if f.endswith(".txt")],
            reverse=True
        )
    except FileNotFoundError:
        dosyalar = []
    
    return render_template("index.html", dosyalar=dosyalar)


@app.post("/upload")
def csv_yukle():
    """CSV dosyası yükleme ve algoritma çalıştırma."""
    try:
        dosya = request.files.get("csv")

        if not dosya or not dosya.filename:
            flash("Lütfen bir CSV dosyası seçin.", "error")
            return redirect(url_for("ana_sayfa"))

        if not dosya.filename.lower().endswith(".csv"):
            flash("Lütfen geçerli bir CSV dosyası yükleyin.", "error")
            return redirect(url_for("ana_sayfa"))

        dosya_adi = guvenli_dosya_adi(dosya.filename)
        yukleme_yolu = os.path.join(YUKLEME_DIZINI, dosya_adi)
        dosya.save(yukleme_yolu)

        try:
            df = pd.read_csv(yukleme_yolu)
        except Exception as e:
            flash(f"CSV dosyası okunamadı: {str(e)}", "error")
            return redirect(url_for("ana_sayfa"))

        gecerli, mesaj = csv_dogrula(df)
        if not gecerli:
            flash(f"CSV doğrulama hatası: {mesaj}", "error")
            return redirect(url_for("ana_sayfa"))

        zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temel_ad = os.path.splitext(dosya_adi)[0]

        basarili_algoritmalar = []
        for alg_adi, alg_fonk in ALGORITMALAR.items():
            try:
                cikti_metin = algoritma_calistir_ve_yakala(alg_fonk, df.copy())
                cikti_dosya_adi = f"{temel_ad}__{alg_adi}__{zaman_damgasi}.txt"
                cikti_yolu = os.path.join(CIKTI_DIZINI, cikti_dosya_adi)
                
                with open(cikti_yolu, "w", encoding="utf-8") as f:
                    f.write(cikti_metin)
                
                basarili_algoritmalar.append(alg_adi)
            except Exception as e:
                flash(f"{alg_adi} algoritması çalıştırılırken hata oluştu: {str(e)}", "error")

        if basarili_algoritmalar:
            flash(f"Algoritmalar başarıyla çalıştırıldı: {', '.join(basarili_algoritmalar)}", "success")
        else:
            flash("Hiçbir algoritma çalıştırılamadı.", "error")

    except Exception as e:
        flash(f"Beklenmeyen bir hata oluştu: {str(e)}", "error")

    return redirect(url_for("ana_sayfa"))


@app.get("/outputs/<dosya_adi>")
def cikti_indir(dosya_adi):
    """Çıktı dosyası indirme."""
    try:
        return send_from_directory(CIKTI_DIZINI, dosya_adi, as_attachment=True)
    except FileNotFoundError:
        flash("Dosya bulunamadı.", "error")
        return redirect(url_for("ana_sayfa"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
