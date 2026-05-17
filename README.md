````md id="cq6vdc"
# Kütüphane Envanter Yönetim Sistemi

Python programlama dili kullanılarak geliştirilen bu proje, temel kütüphane işlemlerinin dijital ortamda yönetilmesini amaçlamaktadır. Sistem; kitap yönetimi, kullanıcı işlemleri, ödünç alma/iade süreçleri ve yetkilendirme mekanizmalarını kapsamaktadır.

---

## Proje Hakkında

Kütüphane Envanter Yönetim Sistemi, kullanıcıların ve kitap kayıtlarının düzenli bir şekilde yönetilmesini sağlayan konsol tabanlı bir uygulamadır. Proje kapsamında;

- Kitap ekleme, silme ve güncelleme,
- Kullanıcı yönetimi,
- Ödünç alma ve iade işlemleri,
- Rol tabanlı yetkilendirme,
- Dosya tabanlı veri saklama,
- Arama, filtreleme ve raporlama

işlemleri gerçekleştirilebilmektedir.

---

## Özellikler

### Kullanıcı Girişi ve Yetkilendirme
- Güvenli giriş sistemi
- Rol bazlı erişim kontrolü
- Yönetici, personel ve öğrenci rolleri

### Kitap Yönetimi
- Yeni kitap ekleme
- Kitap bilgilerini güncelleme
- Kitap silme işlemleri
- Stok ve uygunluk takibi

### Kullanıcı Yönetimi
- Kullanıcı hesabı oluşturma
- Kullanıcı bilgilerini güncelleme
- Hesap silme işlemleri

### Ödünç Alma ve İade Sistemi
- Kitap ödünç verme
- Kitap iade alma
- Teslim tarihi kontrolü
- Gecikmiş iade yönetimi

### Arama ve Listeleme
- ISBN ile arama
- Kitap adına göre arama
- Yazara göre filtreleme
- Detaylı listeleme işlemleri

### Raporlama ve İstatistik
- En çok ödünç alınan kitaplar
- Gecikmiş teslim kayıtları
- Genel envanter özeti

---

## Kullanılan Teknolojiler

- Python
- Dosya İşlemleri
- Yapısal Programlama
- Git & GitHub

---

## Proje Yapısı

```bash
Library-Inventory-System/
│
├── data/
│   ├── books.txt
│   ├── users.txt
│   └── loans.txt
│
├── src/
│   ├── main.py
│   ├── auth.py
│   ├── book_operations.py
│   ├── user_operations.py
│   └── loan_operations.py
│
└── README.md
````

---

## Veri Saklama Yapısı

Projede tüm veriler `.txt` dosyaları içerisinde saklanmaktadır.

Örnek kitap kaydı:

```txt id="68cq1r"
9789753638029;Suç ve Ceza;Dostoyevski;Can Yayınları;12
```

---

## Kurulum

```bash id="o79u0d"
git clone https://github.com/kullaniciadi/library-inventory-system.git
cd library-inventory-system
```

---

## Projeyi Çalıştırma

```bash id="x2q6ak"
python main.py
```

---

## Projenin Amacı

Bu proje ile birlikte aşağıdaki konularda uygulamalı deneyim kazanılması hedeflenmiştir:

* Veri yapıları kullanımı
* Dosya işlemleri
* Yetkilendirme sistemleri
* Modüler yazılım geliştirme
* Sürüm kontrol sistemleri
* Takım çalışması ve GitHub kullanımı

---

## Geliştiriciler

* Çınar YILDIRIM
* Şevval Tuana KAYA
* Rabia Nur KUZÇALI
* Eren PULAT

---

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

```
```
