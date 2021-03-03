from tkinter import *
from tkinter import messagebox
import login_dosen_reguler
import login_dosen_pengganti
import subprocess
import db.db
import datetime

class LoginWindow:

    def __init__(self):

        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=400, height=500)
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 400 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "400x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        x, y = 60, 0

        self.img = PhotoImage(file='images/logo.png')
        self.label = Label(self.win, image=self.img)
        self.label.place(x = x, y = y)
        
        self.button = Button(self.win, text="Jadwal Reguler? \nKlik Disini", font='Courier 20 bold', 
        command=self.halaman_login1)
        self.button.place(x=60, y=200)

        self.button = Button(self.win, text="Dosen Pengganti? \nKlik Disini", font='Courier 20 bold', 
        command=self.halaman_login2)
        self.button.place(x=50, y=300)

        # change the title of the window
        self.win.title("PROGRAM PENCATATAN KEHADIRAN")

        self.win.mainloop()

    def halaman_login1(self):
        self.win.destroy()
        #masuk ke menu presensi
        x = login_dosen_reguler.login_reguler()
    
    def halaman_login2(self):
        self.win.destroy()

        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=800, height=500)
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 800 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "800x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        #self.win.resizable(width=False, height=False)

        x, y = 60, 0

        self.label = Label(self.win, text="PILIH DOSEN YANG AKAN DIGANTIKAN")
        self.label.config(font=("Courier bold", 20))
        self.label.place(x=130, y = 0)

        self.Nama_Dosen = db.db.nama_dosen()

        OPTIONS = ()

        for i in self.Nama_Dosen:
            OPTIONS = self.Nama_Dosen

        self.variable = StringVar(self.win)
        self.variable.set(OPTIONS[0])

        self.w = OptionMenu(self.win, self.variable, *OPTIONS)
        self.w.config(font=("Courier bold", 12))
        self.w.place(x=130, y=50)

        self.button = Button(self.win, text="BATAL", font='Courier 20 bold', 
        command=self.Batal)
        self.button.place(x=200, y=400)

        self.button = Button(self.win, text="PILIH", font='Courier 20 bold', 
        command=self.verifikasi_pengganti)
        self.button.place(x=500, y=400)

        # change the title of the window
        self.win.title("Kuliah Pengganti")

        self.win.mainloop()

    def Batal(self):
        self.win.destroy()
        x = LoginWindow()

    def verifikasi_pengganti(self):
        
        Dosen_Yang_Digantikan = self.variable.get() #Mendapatkan value dosen yang digantikan
        NIK_Dosen = str(Dosen_Yang_Digantikan[2] + Dosen_Yang_Digantikan[3] + Dosen_Yang_Digantikan[4])
        print(NIK_Dosen)
        now = datetime.datetime.now()
        Hari = ""
        #print(now.strftime("%A"))
        if now.strftime("%A") == "Monday":
            Hari = "Senin"
        elif now.strftime("%A") == "Tuesday":
            Hari = "Selasa"
        elif now.strftime("%A") == "Wednesday":
            Hari = "Rabu"
        elif now.strftime("%A") == "Thursday":
            Hari = "Kamis"
        elif now.strftime("%A") == "Friday":
            Hari = "Jumat"
        elif now.strftime("%A") == "Saturday":
            Hari = "Sabtu"
        elif now.strftime("%A") == "Sunday":
            Hari = "Minggu"
        tup = (
            NIK_Dosen,
            Hari
        )
        result = db.db.cek_waktu(tup, self) #Mengecek apakah Dosen masuk di jam yang benar
        Jadwal = db.db.cek_semester() #mengecek tahun ajaran, minggu ke berapa
        print(result) #menampilkan matkul yang dibawakan
        print(Jadwal)
        if result:
            self.win.destroy() 
            x = login_dosen_pengganti.login_pengganti(NIK_Dosen)
        else:
            messagebox.showinfo("Message", "Saat Ini Tidak Ada Sesi Kelas")

if __name__ == "__main__":
    #data = subprocess.check_output("netsh wlan show interfaces")
    #print(data)
    #if b': connected' in subprocess.check_output("netsh wlan show interfaces"): #Mengecek jika connect ke wifi
    x = LoginWindow()
    #else: print('Anda harus mematikan WIFI')
