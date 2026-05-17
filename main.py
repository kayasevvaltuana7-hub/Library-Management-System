import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Projemizin diğer modüllerini import ediyoruz
import girisyetkilendirme
import kitapEklemeGuncellemeSilme
import hesapyonetimi
import oduncİade
import aramaListeleme
import raporlamaİstatistik

#  KÜRESEL VERİ LİSTELERİ
kitaplar_listesi = kitapEklemeGuncellemeSilme.kitaplari_yukle()
kullanicilar_listesi = hesapyonetimi.kullanicilari_yukle()
oduncler_listesi = oduncİade.oduncleri_yukle()
aktif_kullanici = None

#  ANA PENCERE
ana_pencere = tk.Tk()
ana_pencere.title("Kütüphane Yönetim Sistemi")
ana_pencere.geometry("600x600")
ana_pencere.resizable(False, False)

def pencereyi_temizle():
    for widget in ana_pencere.winfo_children():
        widget.destroy()

# GİRİŞ EKRANI TASARIMI 
def giris_ekranini_olustur():
    pencereyi_temizle()
    ana_pencere.geometry("600x600")
    ana_pencere.configure(bg="#2c3e50")
    
    kart_frame = tk.Frame(ana_pencere, bg="white", bd=0, relief="flat")
    kart_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    tk.Label(kart_frame, text="KÜTÜPHANE OTOMASYONU", font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=(25, 2))
    tk.Label(kart_frame, text="Lütfen bilgilerinizi girerek oturum açın", font=("Arial", 9), bg="white", fg="#7f8c8d").pack(pady=(0, 20))
    
    frame_id = tk.Frame(kart_frame, bg="white")
    frame_id.pack(fill="x", padx=40, pady=5)
    
    tk.Label(frame_id, text="Kullanıcı ID", font=("Arial", 9, "bold"), bg="white", fg="#34495e").pack(anchor="w", pady=2)
    entry_kullanici = tk.Entry(frame_id, font=("Arial", 11), bg="#f8f9fa", fg="#2c3e50", bd=1, relief="solid", highlightthickness=0, justify="center")
    entry_kullanici.pack(fill="x", ipady=6)
    
    frame_sifre = tk.Frame(kart_frame, bg="white")
    frame_sifre.pack(fill="x", padx=40, pady=8)
    
    tk.Label(frame_sifre, text="Şifre", font=("Arial", 9, "bold"), bg="white", fg="#34495e").pack(anchor="w", pady=2)
    entry_sifre = tk.Entry(frame_sifre, show="*", font=("Arial", 11), bg="#f8f9fa", fg="#2c3e50", bd=1, relief="solid", highlightthickness=0, justify="center")
    entry_sifre.pack(fill="x", ipady=6)
    
    def giris_islemi():
        global aktif_kullanici
        girilen_id = entry_kullanici.get().strip()
        girilen_sifre = entry_sifre.get().strip()
        
        bulundu = False
        for k in kullanicilar_listesi:
            if k.id == girilen_id and k.sifre == girilen_sifre:
                aktif_kullanici = k
                bulundu = True
                break
                
        if bulundu:
            ana_uygulamayi_baslat()
        else:
            messagebox.showerror("Hata", "Hatalı ID veya Şifre girdiniz!")
            
    btn_giris = tk.Button(kart_frame, text="GİRİŞ YAP", font=("Arial", 10, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white", relief="flat", bd=0, cursor="hand2", command=giris_islemi)
    btn_giris.pack(fill="x", padx=40, pady=25, ipady=6)

# SİDEBAR VE ANA UYGULAMA (Giriş Sonrası)

def ana_uygulamayi_baslat():
    pencereyi_temizle()
    ana_pencere.geometry("1000x600")
    ana_pencere.resizable(True, True)
    
    sidebar = tk.Frame(ana_pencere, bg="#2c3e50", width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    icerik_alani = tk.Frame(ana_pencere, bg="#ecf0f1")
    icerik_alani.pack(side="right", fill="both", expand=True)
    
    def icerigi_temizle():
        for widget in icerik_alani.winfo_children():
            widget.destroy()

    def sayfa_arama():
        icerigi_temizle()
        tk.Label(icerik_alani, text="KİTAP ARA VE LİSTELE", font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2980b9").pack(pady=15)
        
        frame_ust = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_ust.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_ust, text="Kelime:", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        entry_arama = tk.Entry(frame_ust, width=25)
        entry_arama.pack(side="left", padx=5)
        
        combo_kriter = ttk.Combobox(frame_ust, values=["Kitap Adı", "Yazar", "Yayınevi", "ISBN"], state="readonly", width=15)
        combo_kriter.set("Kitap Adı")
        combo_kriter.pack(side="left", padx=5)
        
        frame_liste = tk.Frame(icerik_alani, bg="white")
        frame_liste.pack(fill="both", expand=True, padx=20, pady=10)
        
        scroll_y = tk.Scrollbar(frame_liste)
        scroll_y.pack(side="right", fill="y")
        txt_sonuclar = tk.Text(frame_liste, wrap=tk.NONE, yscrollcommand=scroll_y.set, font=("Courier", 10))
        txt_sonuclar.pack(fill="both", expand=True)
        scroll_y.config(command=txt_sonuclar.yview)

        def ara_islemi():
            kelime = entry_arama.get().strip()
            kriter = combo_kriter.get()
            
            if not kelime:
                bulunanlar = aramaListeleme.tum_kitaplari_getir(kitaplar_listesi)
            else:
                if kriter == "Kitap Adı": bulunanlar = aramaListeleme.kitap_ara_ad(kitaplar_listesi, kelime)
                elif kriter == "Yazar": bulunanlar = aramaListeleme.kitap_ara_yazar(kitaplar_listesi, kelime)
                elif kriter == "Yayınevi": bulunanlar = aramaListeleme.kitap_ara_yayinevi(kitaplar_listesi, kelime)
                elif kriter == "ISBN": bulunanlar = aramaListeleme.kitap_ara_isbn(kitaplar_listesi, kelime)

            txt_sonuclar.config(state=tk.NORMAL)
            txt_sonuclar.delete("1.0", tk.END)
            txt_sonuclar.insert(tk.END, aramaListeleme.kitaplari_tablo_yap(bulunanlar))
            txt_sonuclar.config(state=tk.DISABLED)

        tk.Button(frame_ust, text="Ara / Filtrele", bg="#3498db", fg="white", font=("Arial", 9, "bold"), relief="flat", command=ara_islemi).pack(side="left", padx=10)
        ara_islemi()

    def sayfa_kitap_yonetimi():
        icerigi_temizle()
        tk.Label(icerik_alani, text="KİTAP YÖNETİMİ", font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2980b9").pack(pady=15)
        
        frame_form = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_form.pack(pady=10)
        
        alanlar = ["ISBN", "Kitap Adı", "Yazar", "Yayınevi", "Yayın Yılı", "Stok", "Konum"]
        entry_dict = {}

        for i, alan in enumerate(alanlar):
            tk.Label(frame_form, text=alan + ":", font=("Arial", 10, "bold"), bg="#ecf0f1").grid(row=i, column=0, padx=10, pady=8, sticky="e")
            ent = tk.Entry(frame_form, width=35)
            ent.grid(row=i, column=1, padx=10, pady=8)
            entry_dict[alan] = ent

        def islem_yap(islem_turu):
            global kitaplar_listesi
            v = {k: ent.get() for k, ent in entry_dict.items()}
            
            if islem_turu == "ekle": basari, msj = kitapEklemeGuncellemeSilme.kitap_ekle(kitaplar_listesi, v["ISBN"], v["Kitap Adı"], v["Yazar"], v["Yayınevi"], v["Yayın Yılı"], v["Stok"], v["Konum"])
            elif islem_turu == "sil": basari, msj = kitapEklemeGuncellemeSilme.kitap_sil(kitaplar_listesi, v["ISBN"])
            elif islem_turu == "guncelle": basari, msj = kitapEklemeGuncellemeSilme.kitap_guncelle(kitaplar_listesi, v["ISBN"], v["Kitap Adı"], v["Yazar"], v["Yayınevi"], v["Yayın Yılı"], v["Stok"], v["Konum"])

            if basari:
                messagebox.showinfo("Başarılı", msj)
                for ent in entry_dict.values(): ent.delete(0, tk.END)
                kitaplar_listesi = kitapEklemeGuncellemeSilme.kitaplari_yukle()
            else:
                messagebox.showerror("Hata", msj)

        frame_btn = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_btn.pack(pady=20)
        tk.Button(frame_btn, text="Kitap Ekle", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=12, relief="flat", command=lambda: islem_yap("ekle")).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Güncelle", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), width=12, relief="flat", command=lambda: islem_yap("guncelle")).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Kitap Sil", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=12, relief="flat", command=lambda: islem_yap("sil")).pack(side="left", padx=10)

    def sayfa_odunc_iade():
        icerigi_temizle()
        tk.Label(icerik_alani, text="ÖDÜNÇ VE İADE İŞLEMLERİ", font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2980b9").pack(pady=15)
        
        frame_form = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_form.pack(pady=30)
        
        tk.Label(frame_form, text="Kullanıcı ID:", font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=0, column=0, padx=10, pady=15, sticky="e")
        entry_k_id = tk.Entry(frame_form, width=25, font=("Arial", 11))
        entry_k_id.grid(row=0, column=1, padx=10, pady=15)
        
        tk.Label(frame_form, text="Kitap ISBN:", font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=1, column=0, padx=10, pady=15, sticky="e")
        entry_isbn = tk.Entry(frame_form, width=25, font=("Arial", 11))
        entry_isbn.grid(row=1, column=1, padx=10, pady=15)

        def islem_yap(islem_turu):
            global oduncler_listesi
            if islem_turu == "odunc": basari, msj = oduncİade.kitap_odunc_al(oduncler_listesi, entry_k_id.get(), entry_isbn.get())
            elif islem_turu == "iade": basari, msj = oduncİade.kitap_iade_et(oduncler_listesi, entry_k_id.get(), entry_isbn.get())

            if basari:
                messagebox.showinfo("Başarılı", msj)
                entry_k_id.delete(0, tk.END)
                entry_isbn.delete(0, tk.END)
                oduncler_listesi = oduncİade.oduncleri_yukle()
            else: messagebox.showerror("Hata", msj)

        frame_btn = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Ödünç Ver", bg="#8e44ad", fg="white", font=("Arial", 11, "bold"), width=15, relief="flat", command=lambda: islem_yap("odunc")).pack(side="left", padx=10)
        tk.Button(frame_btn, text="İade Al", bg="#2980b9", fg="white", font=("Arial", 11, "bold"), width=15, relief="flat", command=lambda: islem_yap("iade")).pack(side="left", padx=10)

    def sayfa_raporlar():
        icerigi_temizle()
        tk.Label(icerik_alani, text="SİSTEM RAPORLARI VE ANALİZ", font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2980b9").pack(pady=15)
        
        frame_btn = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_btn.pack(pady=5)
        
        frame_gosterim = tk.Frame(icerik_alani, bg="#ecf0f1")
        frame_gosterim.pack(fill="both", expand=True, padx=20, pady=15)

        def raporu_goster(turu):
            for widget in frame_gosterim.winfo_children():
                widget.destroy()
                
            if turu == "envanter":
                total_kitap = len(kitaplar_listesi)
                total_stok = sum(k.stok for k in kitaplar_listesi)
                total_kullanici = len(kullanicilar_listesi)
                aktif_oduncler = sum(1 for o in oduncler_listesi if o.durum == "aktif")
                
                def kart_olustur(parent, baslik, deger, renk):
                    kart = tk.Frame(parent, bg=renk, bd=0, relief="flat")
                    kart.pack(side="left", fill="both", expand=True, padx=10, pady=20)
                    tk.Label(kart, text=baslik, bg=renk, fg="white", font=("Arial", 11, "bold")).pack(pady=(20, 5))
                    tk.Label(kart, text=str(deger), bg=renk, fg="white", font=("Arial", 28, "bold")).pack(pady=(0, 20))
                
                kart_frame = tk.Frame(frame_gosterim, bg="#ecf0f1")
                kart_frame.pack(fill="x", pady=20)
                
                kart_olustur(kart_frame, "Farklı Kitap", total_kitap, "#3498db")
                kart_olustur(kart_frame, "Toplam Stok", total_stok, "#e67e22")
                kart_olustur(kart_frame, "Kullanıcılar", total_kullanici, "#2ecc71")
                kart_olustur(kart_frame, "Ödünçte Olan", aktif_oduncler, "#e74c3c")
                
            elif turu in ["gecikme", "populer"]:
                txt_rapor = tk.Text(frame_gosterim, wrap=tk.NONE, font=("Courier", 10))
                txt_rapor.pack(fill="both", expand=True)
                
                if turu == "gecikme": 
                    icerik = raporlamaİstatistik.gecikmis_teslim_raporu(oduncler_listesi, kullanicilar_listesi, kitaplar_listesi)
                elif turu == "populer": 
                    icerik = raporlamaİstatistik.en_cok_odunc_alinanlar(oduncler_listesi, kitaplar_listesi)
                
                txt_rapor.insert(tk.END, icerik)
                txt_rapor.config(state=tk.DISABLED)
                
            elif turu == "grafik":
                frekans = {}
                for o in oduncler_listesi:
                    frekans[o.isbn] = frekans.get(o.isbn, 0) + 1
                    
                kitap_dict = {k.isbn: k.ad for k in kitaplar_listesi}
                sirali = sorted(frekans.items(), key=lambda x: x[1], reverse=True)[:5]
                
                if not sirali:
                    tk.Label(frame_gosterim, text="Grafik çizilecek ödünç verisi bulunamadı.", bg="#ecf0f1").pack()
                    return
                
                isimler = [kitap_dict.get(isbn, "Bilinmeyen")[:15] + "..." for isbn, adet in sirali]
                adetler = [adet for isbn, adet in sirali]
                
                fig, ax = plt.subplots(figsize=(7, 4))
                renkler = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6']
                ax.bar(isimler, adetler, color=renkler)
                ax.set_title('En Çok Ödünç Alınan İlk 5 Kitap', fontweight="bold")
                ax.set_ylabel('Ödünç Alınma Sayısı')
                
                canvas = FigureCanvasTkAgg(fig, master=frame_gosterim)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Button(frame_btn, text="Envanter Özeti", bg="#16a085", fg="white", relief="flat", font=("Arial", 10, "bold"), width=15, command=lambda: raporu_goster("envanter")).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Gecikmiş Teslimler", bg="#c0392b", fg="white", relief="flat", font=("Arial", 10, "bold"), width=18, command=lambda: raporu_goster("gecikme")).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Popüler Kitaplar", bg="#f39c12", fg="white", relief="flat", font=("Arial", 10, "bold"), width=15, command=lambda: raporu_goster("populer")).pack(side="left", padx=5)
        tk.Button(frame_btn, text="📊 Grafiği Göster", bg="#8e44ad", fg="white", relief="flat", font=("Arial", 10, "bold"), width=16, command=lambda: raporu_goster("grafik")).pack(side="left", padx=5)
        
        raporu_goster("envanter")

    def cikis_yap():
        global aktif_kullanici
        aktif_kullanici = None
        giris_ekranini_olustur()

    tk.Label(sidebar, text=f"👤 {aktif_kullanici.ad.upper()}\n({aktif_kullanici.rol.capitalize()})", font=("Arial", 12, "bold"), bg="#34495e", fg="white", pady=15).pack(fill="x", pady=(0, 20))

    def menubutonu_olustur(text, command):
        tk.Button(sidebar, text=text, bg="#2c3e50", fg="white", font=("Arial", 11, "bold"), relief="flat", 
                  activebackground="#1abc9c", activeforeground="white", pady=12, command=command).pack(fill="x", pady=1)

    menubutonu_olustur("🔍 Kitap Ara", sayfa_arama)
    
    if aktif_kullanici.rol in ["yonetici", "personel"]:
        menubutonu_olustur("🔄 Ödünç / İade", sayfa_odunc_iade)
        menubutonu_olustur("📚 Kitap Yönetimi", sayfa_kitap_yonetimi)
        
    if aktif_kullanici.rol == "yonetici":
        menubutonu_olustur("📊 Sistem Raporları", sayfa_raporlar)

    tk.Frame(sidebar, bg="#2c3e50").pack(expand=True) 
    tk.Button(sidebar, text="🚪 Çıkış Yap", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat", 
              activebackground="#c0392b", activeforeground="white", pady=12, command=cikis_yap).pack(fill="x", side="bottom")
    
    sayfa_arama()
# Uygulamayı başlatmak için gereken ilk ekranı oluşturuyoruz
giris_ekranini_olustur()
ana_pencere.mainloop()
