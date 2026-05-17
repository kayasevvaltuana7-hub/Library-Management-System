import os

class Kullanici:
    def __init__(self, id, ad, sifre, rol):
        self.id = id
        self.ad = ad
        self.sifre = sifre
        self.rol = rol


def ozel_karakter_kontrol_kullanici(text):
    return "|" not in text


def rol_gecerli_mi(rol):
    gecerli_roller = ["yonetici", "personel", "ogrenci"]
    return rol in gecerli_roller


def kullanicilari_yukle():
    kullanicilar = []

    if not os.path.exists("kullanicilar.txt"):
        return kullanicilar

    with open("kullanicilar.txt", "r", encoding="utf-8") as dosya:

        for satir in dosya:

            if satir.strip():

                bilgiler = satir.strip().split('|')

                if len(bilgiler) == 4:
                    kullanicilar.append(Kullanici(*bilgiler))

    return kullanicilar


def kullanicilari_kaydet(kullanicilar):

    with open("kullanicilar.txt", "w", encoding="utf-8") as dosya:

        for k in kullanicilar:

            dosya.write(
                f"{k.id}|{k.ad}|{k.sifre}|{k.rol}\n"
            )


def kullanici_ekle(kullanicilar, id, ad, sifre, rol):

    id = id.strip()
    ad = ad.strip()
    sifre = sifre.strip()
    rol = rol.strip().lower()

    if not all([id, ad, sifre, rol]):
        return False, "Lütfen tüm alanları doldurunuz!"

    alanlar = [id, ad, sifre, rol]

    for alan in alanlar:

        if not ozel_karakter_kontrol_kullanici(alan):
            return False, "'|' karakteri kullanılamaz."

    if not rol_gecerli_mi(rol):
        return False, "Geçersiz rol! (yonetici, personel, ogrenci olmalıdır)"

    if any(k.id == id for k in kullanicilar):
        return False, "Bu ID numarasına sahip kullanıcı zaten var!"

    try:

        yeni_kullanici = Kullanici(
            id,
            ad,
            sifre,
            rol
        )

        kullanicilar.append(yeni_kullanici)

        kullanicilari_kaydet(kullanicilar)

        return True, "Kullanıcı başarıyla eklendi."

    except Exception as e:
        return False, f"Ekleme sırasında hata oluştu: {str(e)}"


def kullanici_sil(kullanicilar, id):

    id = id.strip()

    if not id:
        return False, "Lütfen ID giriniz!"

    for i, kullanici in enumerate(kullanicilar):

        if kullanici.id == id:

            del kullanicilar[i]

            kullanicilari_kaydet(kullanicilar)

            return True, "Kullanıcı başarıyla silindi."

    return False, "Belirtilen ID bulunamadı."


def kullanici_guncelle(kullanicilar, id,
                       yeni_ad,
                       yeni_sifre,
                       yeni_rol):

    id = id.strip()

    if not id:
        return False, "ID belirtilmelidir!"

    for kullanici in kullanicilar:

        if kullanici.id == id:

            if yeni_ad:

                yeni_ad = yeni_ad.strip()

                if not ozel_karakter_kontrol_kullanici(yeni_ad):
                    return False, "Geçersiz karakter kullanıldı."

                kullanici.ad = yeni_ad

            if yeni_sifre:

                yeni_sifre = yeni_sifre.strip()

                if not ozel_karakter_kontrol_kullanici(yeni_sifre):
                    return False, "Geçersiz karakter kullanıldı."

                kullanici.sifre = yeni_sifre

            if yeni_rol:

                yeni_rol = yeni_rol.strip().lower()

                if not rol_gecerli_mi(yeni_rol):
                    return False, "Geçersiz rol girildi."

                kullanici.rol = yeni_rol

            kullanicilari_kaydet(kullanicilar)

            return True, "Kullanıcı başarıyla güncellendi."

    return False, "Belirtilen ID numarasına ait kullanıcı bulunamadı."
