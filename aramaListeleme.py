def tum_kitaplari_getir(kitaplar):
    return kitaplar


def kitap_ara_ad(kitaplar, aranacak_ad):

    aranacak_ad = aranacak_ad.lower().strip()

    if not aranacak_ad:
        return []

    return [
        k for k in kitaplar
        if aranacak_ad in k.ad.lower()
    ]


def kitap_ara_yazar(kitaplar, aranacak_yazar):

    aranacak_yazar = aranacak_yazar.lower().strip()

    if not aranacak_yazar:
        return []

    return [
        k for k in kitaplar
        if aranacak_yazar in k.yazar.lower()
    ]


def kitap_ara_yayinevi(kitaplar, aranacak_yayinevi):

    aranacak_yayinevi = aranacak_yayinevi.lower().strip()

    if not aranacak_yayinevi:
        return []

    return [
        k for k in kitaplar
        if aranacak_yayinevi in k.yayinevi.lower()
    ]


def kitap_ara_isbn(kitaplar, aranacak_isbn):

    aranacak_isbn = aranacak_isbn.strip()

    if not aranacak_isbn:
        return []

    return [
        k for k in kitaplar
        if k.isbn == aranacak_isbn
    ]


def kitaplari_tablo_yap(bulunan_kitaplar):

    if not bulunan_kitaplar:
        return "Arama kriterinize uygun herhangi bir kitap bulunamadı.\n"

    tablo_metni = (
        f"{'ISBN':<15} | "
        f"{'KİTAP ADI':<30} | "
        f"{'YAZAR':<25} | "
        f"{'STOK':<5} | "
        f"{'KONUM':<10}\n"
    )

    tablo_metni += "-" * 95 + "\n"

    for k in bulunan_kitaplar:

        ad_gosterim = (
            k.ad[:27] + "..."
            if len(k.ad) > 30
            else k.ad
        )

        yazar_gosterim = (
            k.yazar[:22] + "..."
            if len(k.yazar) > 25
            else k.yazar
        )

        satir = (
            f"{k.isbn:<15} | "
            f"{ad_gosterim:<30} | "
            f"{yazar_gosterim:<25} | "
            f"{k.stok:<5} | "
            f"{k.konum:<10}\n"
        )

        tablo_metni += satir

    return tablo_metni
