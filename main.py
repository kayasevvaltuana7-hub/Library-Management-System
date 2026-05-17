
import tkinter as tk

# Dosyaları main fonksiyonunda import ile topluyoruz
import girisyetkilendirme 
import kitapEklemeGuncellemeSilme
import hesapyonetimi
import oduncİade
import aramaListeleme
import raporlamaİstatistik

# Arayüz penceremizi oluşturup şekilsel ve biçimsel özelliklerini belirliyoruz.
root=tk.Tk()
root.title("Kütüphane Yönetim Sistemi")
root.geometry("500x600")

lbl_kullanici = tk.Label(root, text="Kullanıcı Adı:")
lbl_kullanici.pack(pady=5)
entry_kullanici = tk.Entry(root)
entry_kullanici.pack(pady=5)

lbl_sifre = tk.Label(root, text="Şifre:")
lbl_sifre.pack(pady=5)
entry_sifre = tk.Entry(root, show="*")
entry_sifre.pack(pady=5)

btn_giris = tk.Button(root, text="Giriş Yap", command=giris_yap)
btn_giris.pack(pady=15)

# Programın sürekli açık kalmasını sağlayan ana döngümüz
root.mainloop()
