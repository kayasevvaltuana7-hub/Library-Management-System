import os
from datetime import datetime, timedelta

class Odunc:
    def __init__(self, kullanici_id, isbn, odunc_tarihi, iade_tarihi, durum):
        self.kullanici_id = kullanici_id
        self.isbn = isbn
        self.odunc_tarihi = odunc_tarihi
        self.iade_tarihi = iade_tarihi
        self.durum = durum


def oduncleri_yukle():
    oduncler = []

    if not os.path.exists("odunc.txt"):
        return oduncler

    with open("odunc.txt", "r", encoding="utf-8") as dosya:

        for satir in dosya:

            if satir.strip():

                bilgiler = satir.strip().split('|')

                if len(bilgiler) == 5:
                    oduncler.append(Odunc(*bilgiler))

    return oduncler


def oduncleri_kaydet(oduncler):

    with open("odunc.txt", "w", encoding="utf-8") as dosya:

        for o in oduncler:

            dosya.write(
                f"{o.kullanici_id}|{o.isbn}|{o.odunc_tarihi}|"
                f"{o.iade_tarihi}|{o.durum}\n"
            )


def kitap_odunc_al(oduncler, kullanici_id, isbn, sure_gun=15):

    kullanici_id = kullanici_id.strip()
    isbn = isbn.strip()

    if not all([kullanici_id, isbn]):
        return False, "Kullanıcı ID ve ISBN girilmelidir!"

    for o in oduncler:

        if o.kullanici_id == kullanici_id and o.isbn == isbn and o.durum == "aktif":
            return False, "Bu kitap kullanıcıda zaten mevcut!"

    try:

        bugun = datetime.now()
        iade_zamani = bugun + timedelta(days=int(sure_gun))

        odunc_str = bugun.strftime("%Y-%m-%d")
        iade_str = iade_zamani.strftime("%Y-%m-%d")

        yeni_odunc = Odunc(
            kullanici_id,
            isbn,
            odunc_str,
            iade_str,
            "aktif"
        )

        oduncler.append(yeni_odunc)

        oduncleri_kaydet(oduncler)

        return True, "Kitap başarıyla ödünç verildi."

    except Exception as e:
        return False, f"İşlem sırasında hata oluştu: {str(e)}"


def kitap_iade_et(oduncler, kullanici_id, isbn):

    kullanici_id = kullanici_id.strip()
    isbn = isbn.strip()

    if not all([kullanici_id, isbn]):
        return False, "Kullanıcı ID ve ISBN girilmelidir!"

    for o in oduncler:

        if o.kullanici_id == kullanici_id and o.isbn == isbn and o.durum == "aktif":

            o.durum = "iade_edildi"

            bugun = datetime.now()
            beklenen_iade = datetime.strptime(o.iade_tarihi, "%Y-%m-%d")

            fark = (bugun - beklenen_iade).days

            oduncleri_kaydet(oduncler)

            if fark > 0:
                return True, f"Kitap iade edildi ancak {fark} gün gecikme var!"
            
            return True, "Kitap zamanında başarıyla iade edildi."

    return False, "Bu kullanıcıya ait aktif ödünç kaydı bulunamadı."
