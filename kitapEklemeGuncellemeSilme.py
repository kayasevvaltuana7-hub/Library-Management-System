import os
from datetime import datetime

class Kitap:
    def __init__(self, isbn, ad, yazar, yayinevi, yayin_yili, stok, konum):
        self.isbn = isbn
        self.ad = ad
        self.yazar = yazar
        self.yayinevi = yayinevi
        self.yayin_yili = yayin_yili
        self.stok = int(stok)
        self.konum = konum


def isbn_gecerli_mi(isbn):
    return isbn.isdigit() and len(isbn) in [10, 13]


def stok_gecerli_mi(stok):
    return stok.isdigit() and int(stok) >= 0


def yayin_yili_gecerli_mi(yil):

    if not yil.isdigit():
        return False

    yil = int(yil)
    mevcut_yil = datetime.now().year

    return 0 < yil <= mevcut_yil


def ozel_karakter_kontrol(text):
    return "|" not in text


def kitaplari_yukle():
    kitaplar = []

    if not os.path.exists("kitaplar.txt"):
        return kitaplar

    with open("kitaplar.txt", "r", encoding="utf-8") as dosya:

        for satir in dosya:

            if satir.strip():

                bilgiler = satir.strip().split('|')

                if len(bilgiler) == 7:
                    kitaplar.append(Kitap(*bilgiler))

    return kitaplar


def kitaplari_kaydet(kitaplar):

    with open("kitaplar.txt", "w", encoding="utf-8") as dosya:

        for k in kitaplar:

            dosya.write(
                f"{k.isbn}|{k.ad}|{k.yazar}|"
                f"{k.yayinevi}|{k.yayin_yili}|"
                f"{k.stok}|{k.konum}\n"
            )


def kitap_ekle(kitaplar, isbn, ad, yazar,
               yayinevi, yayin_yili,
               stok, konum):

    isbn = isbn.strip()
    ad = ad.strip()
    yazar = yazar.strip()
    yayinevi = yayinevi.strip()
    yayin_yili = yayin_yili.strip()
    stok = stok.strip()
    konum = konum.strip()

    if not all([isbn, ad, yazar,
                yayinevi, yayin_yili,
                stok, konum]):

        return False, "Lütfen tüm alanları doldurunuz!"

    alanlar = [isbn, ad, yazar, yayinevi, konum]

    for alan in alanlar:

        if not ozel_karakter_kontrol(alan):
            return False, "'|' karakteri kullanılamaz."

    if not isbn_gecerli_mi(isbn):
        return False, "ISBN 10 veya 13 haneli sayı olmalıdır."

    if not stok_gecerli_mi(stok):
        return False, "Stok negatif olamaz ve sayı olmalıdır."

    if not yayin_yili_gecerli_mi(yayin_yili):
        return False, "Geçerli bir yayın yılı giriniz."

    if any(k.isbn == isbn for k in kitaplar):
        return False, "Bu ISBN numarasına sahip kitap zaten var!"

    try:

        yeni_kitap = Kitap(
            isbn,
            ad,
            yazar,
            yayinevi,
            yayin_yili,
            stok,
            konum
        )

        kitaplar.append(yeni_kitap)

        kitaplari_kaydet(kitaplar)

        return True, "Kitap başarıyla eklendi."

    except ValueError:
        return False, "Sayısal alanlarda hata oluştu."

    except Exception as e:
        return False, f"Ekleme sırasında hata oluştu: {str(e)}"


def kitap_sil(kitaplar, isbn):

    isbn = isbn.strip()

    if not isbn:
        return False, "Lütfen ISBN giriniz!"

    for i, kitap in enumerate(kitaplar):

        if kitap.isbn == isbn:

            del kitaplar[i]

            kitaplari_kaydet(kitaplar)

            return True, "Kitap başarıyla silindi."

    return False, "Belirtilen ISBN bulunamadı."


def kitap_guncelle(kitaplar, isbn,
                   yeni_ad,
                   yeni_yazar,
                   yeni_yayinevi,
                   yeni_yayin_yili,
                   yeni_stok,
                   yeni_konum):

    isbn = isbn.strip()

    if not isbn:
        return False, "ISBN belirtilmelidir!"

    for kitap in kitaplar:

        if kitap.isbn == isbn:

            if yeni_ad:

                yeni_ad = yeni_ad.strip()

                if not ozel_karakter_kontrol(yeni_ad):
                    return False, "Geçersiz karakter kullanıldı."

                kitap.ad = yeni_ad

            if yeni_yazar:

                yeni_yazar = yeni_yazar.strip()

                if not ozel_karakter_kontrol(yeni_yazar):
                    return False, "Geçersiz karakter kullanıldı."

                kitap.yazar = yeni_yazar

            if yeni_yayinevi:

                yeni_yayinevi = yeni_yayinevi.strip()

                if not ozel_karakter_kontrol(yeni_yayinevi):
                    return False, "Geçersiz karakter kullanıldı."

                kitap.yayinevi = yeni_yayinevi

            if yeni_yayin_yili:

                yeni_yayin_yili = yeni_yayin_yili.strip()

                if not yayin_yili_gecerli_mi(yeni_yayin_yili):
                    return False, "Geçersiz yayın yılı."

                kitap.yayin_yili = yeni_yayin_yili

            if yeni_stok:

                yeni_stok = yeni_stok.strip()

                if not stok_gecerli_mi(yeni_stok):
                    return False, "Geçersiz stok değeri."

                kitap.stok = int(yeni_stok)

            if yeni_konum:

                yeni_konum = yeni_konum.strip()

                if not ozel_karakter_kontrol(yeni_konum):
                    return False, "Geçersiz karakter kullanıldı."

                kitap.konum = yeni_konum

            kitaplari_kaydet(kitaplar)

            return True, "Kitap başarıyla güncellendi."

    return False, "Belirtilen ISBN numarasına ait kitap bulunamadı."
