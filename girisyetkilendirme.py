class Kullanici:
    def __init__(self, id, ad, sifre, rol):
        self.id = id
        self.ad = ad
        self.sifre = sifre
        self.rol = rol


def kullanicilari_yukle():
    kullanicilar = []

    try:
        with open("kullanicilar.txt", "r", encoding="utf-8") as dosya:
            for satir in dosya:
                id, ad, sifre, rol = satir.strip().split('|')
                kullanicilar.append(Kullanici(id, ad, sifre, rol))

    except FileNotFoundError:
        print("kullanicilar.txt dosyası bulunamadı.")

    return kullanicilar


def giris_yap(kullanicilar):
    girilen_id = input("ID giriniz: ")
    girilen_sifre = input("Şifre giriniz: ")

    for kullanici in kullanicilar:
        if kullanici.id == girilen_id and kullanici.sifre == girilen_sifre:
            return kullanici

    return None


def menu_goster(kullanici):
    print(f"\nHoş geldin {kullanici.ad}")

    if kullanici.rol == "yonetici":
        print("Yönetici menüsü")
        print("1. Kitap ekle")
        print("2. Kitap sil")
        print("3. Kullanıcı ekle")

    elif kullanici.rol == "personel":
        print("Personel menüsü")
        print("1. Kitap ödünç ver")
        print("2. Kitap iade al")

    elif kullanici.rol == "ogrenci":
        print("Öğrenci menüsü")
        print("1. Kitap ara")
        print("2. Kitap ödünç al")

