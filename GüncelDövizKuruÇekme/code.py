import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import os

def fiyatları_getir(event=None):
    url ="https://www.bloomberght.com/doviz"
    response = requests.get(url)
    if response.status_code == 200 :
        content = response.content
        soup = BeautifulSoup(content,"html.parser")
        div = soup.find("div",{"data-widget-type":"economy-table-type2"})
        if div :
            all_tr = div.find_all("tr",{"class":"border-b"})
            fiyatlar = []
            for tr in all_tr :
                döviz_isim = tr.find("div", {"class": "text-ellipses"})
                if döviz_isim :
                    döviz_isim = döviz_isim.get_text(strip=True)
                    döviz_fiyat = tr.find("span",{"class":"lastPrice"})
                    if döviz_fiyat :
                        döviz_fiyat = döviz_fiyat.get_text(strip=True)
                        fiyatlar.append((döviz_isim,döviz_fiyat))
            return fiyatlar
    else :
        messagebox.showerror("Hata","Döviz Fiyatları Çekilemedi.")
        return None
def hesapla(event=None):
    try:
        tl_miktarı = float(entry.get())
        fiyatlar = fiyatları_getir()
        if fiyatlar :
            for widget in result_canvas_frame.winfo_children():
                widget.destroy()
            for i , (döviz_isim,döviz_fiyat) in enumerate(fiyatlar):
                karsilik_gelen_deger = tl_miktarı / float(döviz_fiyat.replace(",", "."))
                döviz_isim_label = Label(result_canvas_frame,text=döviz_isim,font=("Helvetica",12),anchor="w",bg="#C2B8E9")
                döviz_isim_label.grid(row=i,column=0,padx=10,pady=10,sticky="w")
                döviz_fiyat_label = Label(result_canvas_frame,text=f"{karsilik_gelen_deger:.2f}",font=("Helvetica",12),anchor="e",bg="#C2B8E9")
                döviz_fiyat_label.grid(row=i,column=1,padx=10,pady=10,sticky="e")
            result_canvas.update_idletasks()
            result_canvas.config(scrollregion=result_canvas.bbox("all"))
    except ValueError:
        messagebox.showerror("Hata","Lütfen Geçerli Bir TL Miktarı Giriniz")


root = Tk()
root.title("Döviz Hesaplayıcı")
root.geometry("400x500")
if os.path.exists("icon.ico"):
    root.iconbitmap("icon.ico")
root.configure(bg="#5E5A72")
root.resizable(0,0)
root.bind("<Return>",hesapla) # Enter ile devam etmek için

title_label = Label(root,text="Döviz Hesaplayıcı",font=("Times",24,"bold"),bg="#5E5A72")
entry_frame = Frame(root,bg="#5E5A72")
entry_frame.pack()
entry_label = Label(entry_frame,text="TL Miktarını giriniz :",font=("Times",12,"bold"),bg="#5E5A72")
entry = Entry(entry_frame,bg="#D7D3E6")
hesapla_button = Button(entry_frame,font=("Arial",14,"bold"),text="Hesapla",bg="#9C8F8F",command=hesapla)

title_label.pack(padx=10,pady=10)
entry_label.grid(row=0,column=0)
entry.grid(row=0,column=1)
hesapla_button.grid(row=1,column=0,columnspan=2,pady=20)

result_frame = Frame(root,bg="#C2B8E9",bd=2,relief="ridge")
result_frame.pack(pady=10,expand=True,fill="both") #expand=True, Frame’in bulunduğu boş alanı tamamen kaplamasını sağlar. fill="both" Pencere boyutuna bağlı olarak frame'in kapladığı alanı düzenler.
result_canvas = Canvas(result_frame,bg="#C2B8E9")
result_canvas.pack(side="left",expand=True,fill="both")
scroll_bar = Scrollbar(result_frame,orient="vertical",command=result_canvas.yview) # result_canvas.yview --> Scrollbar hareket ettikçe Canvas widgetını kaydırır.
scroll_bar.pack(side="right",fill="y") # Çubuğun sağda olması için --> side="right" , sağ tarafı kaplaması için --> fill="y"
result_canvas.configure(yscrollcommand=scroll_bar.set) # yscrollcommand -->Text, Listbox, Canvas gibi kaydırılabilir widgetler için vertical scrollbar hareketini kontrol etmek amacıyla kullanılır. scroll_bar.set ise scrollbar hareket ettikçe pozisyonu güncellemek için kullanılır.
result_canvas_frame = Frame(result_canvas,bg="#C2B8E9")
result_canvas.create_window(0,0,window=result_canvas_frame) # canvas.create_window(x, y, window=widget) --> Belirtilen (x, y) koordinatlarına widget adlı Tkinter öğesini ekler.
root.mainloop()
