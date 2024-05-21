import tkinter as tk
from tkinter import ttk, Canvas, messagebox, NO
from PIL import ImageTk, Image, ImageEnhance
from mydatabase import *


WINDOW_TITLE = "Rezervasyon Takip Sistemi"


window = tk.Tk()
window.geometry('1920x1080')
window.title(WINDOW_TITLE)
window.minsize(800, 600)

image = Image.open("hotelfoto.jpg")
image = image.convert("RGBA")
image.putalpha(130)
enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(0.4)
image.save("hotel.png")

bg_image = Image.open("hotel.png")
bg_image = bg_image.resize((1920, 1080))
bg_image = ImageTk.PhotoImage(bg_image)


def initialize_tab_control(window):
    tab_control = ttk.Notebook(window)
    tab_control.pack(fill="both", expand=True)
    return tab_control


def create_and_add_tab(tab_control, tab_title):
    tab = tk.Frame(tab_control)
    tab_control.add(tab, text=tab_title)
    return tab


def create_popup(item_details):
    popup = tk.Toplevel()
    popup.title("Öğe Detayları")

    # Pop-up pencere boyutlarını ayarla
    popup.geometry("400x300")

    # Ekran boyutlarını al
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Pop-up pencere boyutlarını al
    window_width = 400
    window_height = 300

    # Pop-up pencereyi ekranın ortasına yerleştir
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    popup.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Pop-up pencere içeriğini oluştur
    tk.Label(popup, text="Voucher No:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(popup, text=item_details[0], anchor="w").grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(popup, text="Check-In:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(popup, text=item_details[1], anchor="w").grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(popup, text="Check-Out:", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Label(popup, text=item_details[2], anchor="w").grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(popup, text="Mail Adresi:", anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Label(popup, text=item_details[3], anchor="w").grid(row=3, column=1, padx=10, pady=5, sticky="w")


def update_treeview(imlec, treeview):
    imlec.execute('SELECT * FROM InfoTb')
    info = imlec.fetchall()
    info.reverse()
    treeview.delete(*treeview.get_children())
    for i in info:
        treeview.insert("", "end", values=(i[0], i[1], i[2], i[3]))


def on_treeview_double_click(event):
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item[0], "values")
        create_popup(item_values)


def is_input_digit(answer):
    if answer.isdigit():  # Girilen değer bir tam sayı mı kontrol et
        return True
    elif answer == "":  # Girilen değer boş mu kontrol et
        return False
    else:
        return False


tab_control = initialize_tab_control(window)
tab1 = create_and_add_tab(tab_control, "Sekme 1")
tab2 = create_and_add_tab(tab_control, "Sekme 2")

canvas1 = Canvas(tab1)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg_image, anchor="nw")

canvas2 = Canvas(tab2)
canvas2.pack(fill="both", expand=True)
canvas2.create_image(0, 0, image=bg_image, anchor="nw")

minimum_konaklama_label = tk.Label(tab1, text="Minimum Konaklama Süresi Giriniz")
minimum_konaklama_label.place(x=75, y=70, width=190, height=25)

minimum_konaklama_input = tk.Entry(tab1)
minimum_konaklama_input.place(x=100, y=100, width=150, height=25)


def get_min_stay():
    answer = messagebox.askyesno("UYARI", "Yaptığınız seçimden emin misiniz?")
    if answer:
        min_konaklama = minimum_konaklama_input.get()  # MIN_STAY CONSTANTI OVERRIDE EDİLECEK
        is_input_valid = is_input_digit(min_konaklama)
        if is_input_valid:
            print("Kullanıcıdan alınan input: ", min_konaklama)
        else:
            print("Geçersiz input!")
            messagebox.showwarning("GEÇERSİZ GİRİŞ", "Lütfen sadece sayı giriniz.")
    else:
        print("Alınamadı")


button = tk.Button(tab1, text="Kaydet", command=get_min_stay)
button.place(x=275, y=100, width=150, height=25)

treeview = ttk.Treeview(tab1, height=15)
treeview.pack(fill="x")

treeview["columns"] = ("Voucher No", "Check-In", "Check-Out", "Mail Adresi")
treeview.column("#0", width=0, stretch=NO)
treeview.column("Voucher No", anchor="center", width=150)
treeview.column("Check-In", anchor="center", width=150)
treeview.column("Check-Out", anchor="center", width=150)
treeview.column("Mail Adresi", anchor="center", width=150)

treeview.heading("#0", text="")
treeview.heading("Voucher No", text="Voucher No")
treeview.heading("Check-In", text="Check-In")
treeview.heading("Check-Out", text="Check-Out")
treeview.heading("Mail Adresi", text="Mail Adresi")

treeview.bind("<Double-1>", on_treeview_double_click)

update_treeview(imlec, treeview)


window.mainloop()
