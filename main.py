import folium
import webbrowser
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager # Yeni Dosya Yöneticisi
from kivymd.toast import toast
from kivy.core.window import Window
from kivy.utils import platform
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

# Pencere boyutu (Sadece PC testleri için)
if platform != 'android':
    Window.size = (360, 640)

# --- Matematik Fonksiyonları ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return R * (2 * atan2(sqrt(a), sqrt(1-a)))

def get_speed_color(speed_kmh):
    if speed_kmh < 2: return 'red'
    elif speed_kmh < 15: return 'orange'
    elif speed_kmh < 40: return 'blue'
    else: return 'green'

class GpsMobilApp(MDApp):
    def build(self):
        self.title = "Gelişmiş Mobil GPS"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        screen = MDScreen()

        # Başlık
        screen.add_widget(MDLabel(
            text="🗺️ Mobil Rota Analizi",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.92},
            font_style="H5", theme_text_color="Primary"
        ))

        # Harita Stili Butonu
        self.secilen_stil = "CartoDB dark_matter"
        self.stil_butonu = MDRaisedButton(
            text=f"Görünüm: {self.secilen_stil}",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            size_hint=(0.85, None),
            on_release=self.menu_ac
        )
        screen.add_widget(self.stil_butonu)

        stiller = ["CartoDB dark_matter", "OpenStreetMap", "CartoDB Positron", "Esri.WorldImagery"]
        menu_items = [{"viewclass": "OneLineListItem", "text": i, "on_release": lambda x=i: self.menu_secim(x)} for i in stiller]
        self.menu = MDDropdownMenu(caller=self.stil_butonu, items=menu_items, width_mult=4)

        # Dosya Adı
        self.dosya_adi_input = MDTextField(
            hint_text="Çıktı Dosya Adı",
            text="Rota_Analiz",
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            size_hint=(0.85, None),
        )
        screen.add_widget(self.dosya_adi_input)

        # Başlat Butonu
        screen.add_widget(MDRaisedButton(
            text="📂 DOSYA SEÇ VE ÇİZ",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.85, None),
            md_bg_color=(0, 0.7, 0, 1),
            on_release=self.dosya_yoneticisini_ac
        ))

        # Bilgi Ekranı
        self.lbl_bilgi = MDLabel(
            text="Log dosyasını seçmeye hazır...",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            theme_text_color="Custom",
            text_color=(0.3, 0.3, 0.3, 1),
            font_style="Caption"
        )
        screen.add_widget(self.lbl_bilgi)

        # Dosya Yöneticisi Ayarları
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )

        return screen

    def menu_ac(self, button): self.menu.open()
    def menu_secim(self, text_item):
        self.secilen_stil = text_item
        self.stil_butonu.text = f"Görünüm: {text_item}"
        self.menu.dismiss()

    # --- Dosya Yöneticisi Fonksiyonları ---
    def dosya_yoneticisini_ac(self, instance):
        path = os.path.expanduser("~") # Başlangıç klasörü
        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_manager()
        if path.endswith(".txt"):
            toast(f"Dosya Seçildi: {os.path.basename(path)}")
            self.harita_yap(path)
        else:
            toast("Lütfen .txt uzantılı bir dosya seçin!")

    def exit_manager(self, *args):
        self.file_manager.close()

    # --- Harita Oluşturma ---
    def harita_yap(self, dosya_yolu):
        self.lbl_bilgi.text = "⏳ İşleniyor..."
        klasor = os.path.dirname(dosya_yolu)
        cikti_adi = self.dosya_adi_input.text.strip() + ".html"
        cikis_yolu = os.path.join(klasor, cikti_adi)
        
        TIME_FORMAT = "%Y-%m-%d %H:%M:%S" 

        koordinatlar = []
        zamanlar = []

        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                for satir in f:
                    satir = satir.strip()
                    if not satir: continue
                    p = satir.split(',')
                    if len(p) >= 3:
                        try:
                            t_obj = datetime.strptime(p[0].strip(), TIME_FORMAT)
                            lat, lon = float(p[1]), float(p[2])
                            if abs(lat) <= 90: 
                                koordinatlar.append([lat, lon])
                                zamanlar.append(t_obj)
                        except ValueError: continue
            
            if len(koordinatlar) < 2:
                self.lbl_bilgi.text = "⚠️ Yetersiz veri!"
                return

            m = folium.Map(location=koordinatlar[0], zoom_start=15, tiles=self.secilen_stil)
            toplam_mesafe = 0
            
            for i in range(len(koordinatlar) - 1):
                loc1, loc2 = koordinatlar[i], koordinatlar[i+1]
                t1, t2 = zamanlar[i], zamanlar[i+1]
                mesafe = calculate_distance(loc1[0], loc1[1], loc2[0], loc2[1])
                sure = (t2 - t1).total_seconds()
                toplam_mesafe += mesafe
                hiz = 0
                if sure > 0.001: hiz = (mesafe / sure) * 3.6
                
                folium.PolyLine([loc1, loc2], color=get_speed_color(hiz), weight=5, opacity=0.9).add_to(m)

            toplam_sure_dk = (zamanlar[-1] - zamanlar[0]).total_seconds() / 60
            ozet = f"Mesafe: {toplam_mesafe/1000:.2f} km"

            folium.Marker(koordinatlar[0], popup="BAŞLANGIÇ", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(koordinatlar[-1], popup=f"BİTİŞ<br>{ozet}", icon=folium.Icon(color="red")).add_to(m)
            
            folium.LayerControl().add_to(m)

            m.save(cikis_yolu)
            
            # Android'de tarayıcıyı açma
            webbrowser.open("file://" + os.path.realpath(cikis_yolu))
            self.lbl_bilgi.text = f"✅ Hazır! {cikti_adi}"
            toast("Harita oluşturuldu ve tarayıcıda açılıyor.")

        except Exception as e:
            self.lbl_bilgi.text = f"Hata: {e}"

if __name__ == '__main__':
    GpsMobilApp().run()