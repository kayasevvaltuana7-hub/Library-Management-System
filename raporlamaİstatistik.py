import os
from datetime import datetime

def genel_envanter_ozeti(kitaplar, kullanicilar, oduncler):
    total_kitap_cesidi = len(kitaplar)
    total_stok = sum(k.stok for k in kitaplar)
    total_kullanici = len(kullanicilar)
    
    aktif_oduncler = sum(1 for o in oduncler if o.durum == "aktif")
    
    rapor = (
        f"=========================================\n"
        f"           GENEL ENVANTER ÖZETİ          \n"
        f"=========================================\n"
        f"Toplam Farklı Kitap Çeşidi : {total_kitap_cesidi}\n"
        f"Toplam Fiziksel Kitap Stoğu: {total_stok}\n"
        f"Toplam Kayıtlı Kullanıcı   : {total_kullanici}\n"
        f"Şu An Ödünçte Olan Kitap   : {aktif_oduncler}\n"
        f"-----------------------------------------\n"
    )
    return rapor


def gecikmis_teslim_raporu(oduncler, kullanicilar, kitaplar):
    bugun = datetime.now()
    gecikmis_kayitlar = []
    
    kullanici_dict = {k.id: k.ad for k in kullanicilar}
    kitap_dict = {k.isbn: k.ad for k in kitaplar}
    
    for o in oduncler:
        if o.durum == "aktif":
            try:
                iade_tarihi = datetime.strptime(o.iade_tarihi, "%Y-%m-%d")
                if bugun > iade_tarihi:
                    gecikme_gunu = (bugun - iade_tarihi).days
                    kullanici_adi = kullanici_dict.get(o.kullanici_id, f"Bilinmeyen (ID: {o.kullanici_id})")
                    kitap_adi = kitap_dict.get(o.isbn, f"Bilinmeyen (ISBN: {o.isbn})")
                    
                    gecikmis_kayitlar.append({
                        "kullanici": kullanici_adi,
                        "kitap": kitap_adi,
                        "gecikme": gecikme_gunu,
                        "tarih": o.iade_tarihi
                    })
            except ValueError:
                continue
                
    if not gecikmis_kayitlar:
        return "Gecikmiş teslim kaydı bulunmamaktadır.\n"
        
    rapor = (
        f"================================================================================\n"
        f"                           GECİKMİŞ TESLİM KAYITLARI                            \n"
        f"================================================================================\n"
        f"{'KULLANICI':<20} | {'KİTAP ADI':<30} | {'BEKLENEN TARİH':<15} | {'GECİKME'}\n"
        f"--------------------------------------------------------------------------------\n"
    )
    
    for kayit in gecikmis_kayitlar:
        kitap_gosterim = kayit["kitap"][:27] + "..." if len(kayit["kitap"]) > 30 else kayit["kitap"]
        rapor += f"{kayit['kullanici']:<20} | {kitap_gosterim:<30} | {kayit['tarih']:<15} | {kayit['gecikme']} Gün\n"
        
    rapor += f"--------------------------------------------------------------------------------\n"
    return rapor


def en_cok_odunc_alinanlar(oduncler, kitaplar, limit=5):
    frekans = {}
    for o in oduncler:
        frekans[o.isbn] = frekans.get(o.isbn, 0) + 1
        
    kitap_dict = {k.isbn: k.ad for k in kitaplar}
    sirali_populerlik = sorted(frekans.items(), key=lambda x: x[1], reverse=True)
    
    if not sirali_populerlik:
        return "Henüz sistemde ödünç alma işlemi gerçekleştirilmemiş.\n"
        
    rapor = (
        f"=========================================\n"
        f"         EN ÇOK ÖDÜNÇ ALINAN KİTAPLAR     \n"
        f"=========================================\n"
    )
    
    for i, (isbn, adet) in enumerate(sirali_populerlik[:limit], 1):
        kitap_adi = kitap_dict.get(isbn, f"Bilinmeyen Kitap (ISBN: {isbn})")
        rapor += f"{i}. {kitap_adi:<25} -> {adet} kez ödünç alındı.\n"
        
    rapor += f"-----------------------------------------\n"
    return rapor
