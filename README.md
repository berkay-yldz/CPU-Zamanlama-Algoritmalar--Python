# CPU Scheduling Simülatörü

İşletim Sistemleri dersi için geliştirilmiş CPU zamanlama algoritmaları simülatörü. Web arayüzü üzerinden CSV dosyası yükleyerek CPU zamanlama algoritmalarını test edebilir ve performans metriklerini analiz edebilirsiniz.

## Özellikler

- Web tabanlı arayüz
- CSV dosyası yükleme ve otomatik doğrulama
- FCFS ve Non-Preemptive SJF algoritmaları
- Detaylı performans metrikleri
- Otomatik rapor oluşturma

## Kurulum

**Gereksinimler:** Python 3.8+

```bash
# Paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python app.py
```

Tarayıcıda `http://localhost:5000` adresine gidin.

## Kullanım

1. CSV dosyası hazırlayın (format aşağıda)
2. Web arayüzünde "Dosya Seç" butonuna tıklayın
3. CSV dosyasını seçin ve "Yükle ve Çalıştır" butonuna tıklayın
4. "Oluşan Çıktılar" bölümünden sonuç dosyalarını indirin

## CSV Formatı

| Sütun | Açıklama | Zorunlu | Örnek |
|-------|----------|---------|-------|
| `Process_ID` | Süreç kimliği | + | P001, P002 |
| `Arrival_Time` | Varış zamanı (≥ 0) | + | 0, 2, 4 |
| `CPU_Burst_Time` | CPU patlama süresi (> 0) | + | 4, 7, 10 |
| `Priority` | Öncelik seviyesi | - | high, normal, low |

**Örnek CSV:**
```csv
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P001,0,4,high
P002,2,7,normal
P003,4,10,low
```

## Desteklenen Algoritmalar

- **FCFS** (First Come First Served): İlk gelen process ilk hizmet görür
- **Non-Preemptive SJF** (Shortest Job First): En kısa işe öncelik verir

## Çıktı Formatı

Her algoritma için ayrı `.txt` dosyası oluşturulur. Çıktı dosyaları şunları içerir:

- **Zaman Tablosu**: Her sürecin CPU zamanları
- **Bekleme Süresi**: Maksimum, toplam ve ortalama
- **Tamamlanma Süresi**: Maksimum, toplam ve ortalama (Turnaround Time)
- **Throughput**: T=[50, 100, 150, 200] için tamamlanan süreç sayısı
- **CPU Verimliliği**: Utilization yüzdesi ve detaylı zaman analizi
- **Context Switch Sayısı**: Toplam bağlam değiştirme sayısı

## Proje Yapısı

```
OSproject1/
├── app.py                      # Flask web uygulaması
├── fcfs.py                     # FCFS algoritması
├── nonpreemptive_sjf.py        # Non-Preemptive SJF algoritması
├── requirements.txt            # Python bağımlılıkları
├── data/                       # Örnek CSV dosyaları
├── templates/                  # HTML şablonları
├── uploads/                    # Yüklenen CSV dosyaları
└── outputs/                    # Algoritma çıktı dosyaları
```

## Teknik Detaylar

- **Backend**: Flask, Pandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Kod Kalitesi**: Clean code prensipleri, dokümantasyon
- **Hata Yönetimi**: CSV doğrulama, kullanıcı dostu hata mesajları

## Sınırlamalar

- Şu anda sadece 2 algoritma desteklenmektedir (FCFS ve Non-Preemptive SJF)
- Priority sütunu henüz kullanılmamaktadır

---

**Not**: Bu proje İşletim Sistemleri dersi ödevi kapsamında geliştirilmiştir.
