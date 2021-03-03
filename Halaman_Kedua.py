from tkinter import *
from tkinter import messagebox
import db.db
import os
import cv2
import sys
import shutil
import random
import numpy as np
import datetime
from time import sleep
from tkinter.ttk import Treeview

class LoginWindow():

    def __init__(self, result, NIK, Hari, Jam, Count, NIK_Pengganti):

        if(Count == 1): 
            self.win.destroy()
        #Halaman yang berisi tabel mahasiswa, tombol untuk presensi dan lain-lain
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=1300, height=600)
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 1300 / 2)
        y = int(height / 2 - 600 / 2)
        str1 = "1300x600+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        #self.win.resizable(width=False, height=False)

        x, y = 60, 0

        Akademik = db.db.cek_semester()
        print(Akademik)
        self.Akademik = Akademik

        self.Hari = Hari
        self.NIK = NIK
        self.result = result
        self.Jam = Jam
        self.NIK_Pengganti = NIK_Pengganti

        self.label = Label(self.win, text='Tahun Akademik :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=0, y = 0)

        self.label = Label(self.win, text=Akademik[0])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=140, y = 0)

        self.label = Label(self.win, text='Semester :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=220, y = 0)

        self.label = Label(self.win, text=Akademik[2])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=300, y = 0)

        self.label = Label(self.win, text='Mata Kuliah :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=0, y = 25)

        self.label = Label(self.win, text=result[0]) #Tampilkan Kode Mata Kuliah
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=140, y = 25)
        self.Kode_Matkul = result[0]
        
        self.Nama_Matakuliah = result[1]
        self.label = Label(self.win, text=result[1]) #Tampilkan Nama Mata Kuliah
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=220, y = 25)
        
        self.label = Label(self.win, text='Kelas :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=420, y = 25)

        self.Nama_Kelas = result[4]
        self.label = Label(self.win, text=result[4])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=470, y = 25)

        self.label = Label(self.win, text='Ruang : ')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=500, y = 25)

        self.Nama_Ruang = result[5]
        self.label = Label(self.win, text=result[5])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 25)

        self.label = Label(self.win, text='Hari/Jam :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=0, y = 50)

        self.label = Label(self.win, text=result[3])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=140, y = 50)

        #self.label = Label(self.win, text=result[6])
        self.label = Label(self.win, text=result[6]) #Tampilkan Jam kelas mulai
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=220, y = 50)

        self.label = Label(self.win, text=result[7]) #Tampilkan Jam Kelas Selesai
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=280, y = 50)

        self.label = Label(self.win, text='Login :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=370, y = 50)

        self.label = Label(self.win, text=Jam)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=420, y = 50)

        self.label = Label(self.win, text='Logout :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=490, y = 50)

        def cidClock():    
            c_time = datetime.datetime.now().strftime("%H:%M:%S")
            clock.config(text=c_time)
            clock.after(100,cidClock)
            
        clock = Label(self.win, font=("times", 12))
        clock.place(x=560 , y=50)
        cidClock()
        """self.label = Label(self.win, text='10:00:00')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=560, y = 50)"""

        self.label = Label(self.win, text='Dosen :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=0, y = 75)

        self.Nama_Dosen = result[2]
        self.label = Label(self.win, text=result[2])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=140, y = 75)

        self.label = Label(self.win, text='Pertemuan Ke :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=420, y = 75)

        self.Pertemuan_Ke = Akademik[1]
        self.label = Label(self.win, text=Akademik[1])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=520, y = 75)

        Materi = Akademik[1] - 1 #Mencari materi pertemuan sebelumnya

        self.label = Label(self.win, text='Materi Sebelumnya :')
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=0, y = 100)

        tup = (
            result[0],
            Materi,
            result[2]
        )
        
        Materi_Sebelumnya = db.db.data_Materi(tup,self)
        if Materi_Sebelumnya:
            self.label = Label(self.win, text=Materi_Sebelumnya[0])
            self.label.config(font=("Times New Roman", 12))
            self.label.place(x=140, y = 100)
        else: 
            self.label = Label(self.win, text='')
            self.label.config(font=("Times New Roman", 12))
            self.label.place(x=140, y = 100)

        self.label = Label(self.win, text='Ketik Materi Perkuliahan Saat Ini!')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=140, y = 150)
        

        self.text = Text(self.win, height=2, width = 120)
        #self.text.config(state="disabled",font=("Times New Roman", 20))
        self.text.place(x=140, y=175)
        #self.text.pack()

        
        self.Data_Kehadiran = (
            result[0],  #mengambil kode matkul
            result[1], #mengambil nama matkul
            Akademik[1]
        )

        self.button = Button(self.win, text="Tekan Ini \n Untuk Selesai \n Kuliah", font=('Times New Roman bold',12), 
        command=self.Halaman_Konfirmasi, bg="blue", fg="white")
        self.button.place(x=0, y=150)

        self.button = Button(self.win, text="Tekan Tombol Ini \n Untuk Mulai \n Presensi", font=('Times New Roman bold',12), 
        command=self.Foto, bg="red", fg="white")
        self.button.place(x=0, y=230)

        self.tr = Treeview(self.win, columns=('A', 'B', 'C', 'D', 'E'), selectmode="extended")
        #heading key + text
        # self.tr.heading('#0', text='NO')
        # self.tr.column('#0', minwidth=0, width=40, stretch=NO)
        self.tr.heading('#0', text='NIM')
        self.tr.column('#0', minwidth=0, width=100, stretch=NO)
        self.tr.heading('#1', text='Nama')
        self.tr.column('#1', minwidth=0, width=300, stretch=NO)
        self.tr.heading('#2', text='Hadir')
        self.tr.column('#2', minwidth=0, width=70, stretch=NO)
        self.tr.heading('#3', text='Keterangan')
        self.tr.column('#3', minwidth=0, width=300, stretch=NO)
        self.tr.heading('#4', text='Cancel')
        self.tr.column('#4', minwidth=0, width=150, stretch=NO)

        j = 0
        Count = 1
        #for i in db.db.show_absensi(Kode_Matkul, self):
        Mahasiswa = db.db.show_absensi(result[0], self)
        print (Mahasiswa)
        for i in Mahasiswa:
            #if i[3] == 9:   #Jika Absensi sudah di cancel
            Cek_Data = (
                i[0],
                result[0],
                Akademik[1]
            )
            print('tesssssss')
            #print(Cek_Data)
            Dapat_Data = db.db.cek_presensi(Cek_Data, self)
            print(Dapat_Data)
            if Dapat_Data:
                if Dapat_Data[8] != 9:
                    self.tr.insert('', index=j, text=i[0], values=(i[1], '☑', '', 'Cancel Kehadiran'))
                    # self.tr.insert('', index=j, text=Count, values=(i[0], i[1], '☑', '', 'Cancel Kehadiran'))
                else:
                    self.tr.insert('', index=j, text=i[0], values=(i[1], '☐', '', 'Kehadiran Dicancel'))
            else:
                self.tr.insert('', index=j, text=i[0], values=(i[1], '☐', '', ''))
                # self.tr.insert('', index=j, text=Count, values=(i[0], i[1], '☐', '', ''))
            """elif i[3] == 1:
                self.tr.insert('', index=j, text=i[0], values=(i[1], i[2], '☑', i[4], 'Cancel Kehadiran'))
            else:
                self.tr.insert('', index=j, text=i[0], values=(i[1], i[2], '☐', i[4], ''))"""
            j+=1 
            Count+=1

        # create action on selected row
        self.tr.bind('<Button-1>', self.actions)
        self.tr.place(x=0, y=320)
        
        print(result[0])
        print(result)
        #print('ssssss')

        # change the title of the window
        self.win.title("PRESENSI KEHADIRAN MAHASISWA")

        self.win.mainloop()

    def Halaman_Konfirmasi(self):
        
        self.Materi = self.text.get(1.0, END)
        self.win.destroy()
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=1300, height=600)
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 1300 / 2)
        y = int(height / 2 - 600 / 2)
        str1 = "1300x600+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        #self.win.resizable(width=False, height=False)

        x, y = 60, 0

        """self.img = PhotoImage(file='images/logo2.png')
        self.label = Label(self.win, image=self.img)
        self.label.place(x = x, y = 0)"""

        self.label = Label(self.win, text='Nama Dosen :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 0)

        self.label = Label(self.win, text=self.Nama_Dosen)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 0)

        self.label = Label(self.win, text='Tanggal :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 25)
        
        now = datetime.datetime.today().strftime('%Y-%m-%d')
        self.label = Label(self.win, text=now)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 25)

        self.label = Label(self.win, text='Jam Mulai :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 50)

        self.label = Label(self.win, text=self.Jam)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 50)
        print('TESSS JAM')
        print(self.Jam)

        self.label = Label(self.win, text='Jam Selesai :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 75)

        def cidClock():    
            c_time = datetime.datetime.now().strftime("%H:%M:%S")
            clock.config(text=c_time)
            clock.after(100,cidClock)
            
        clock = Label(self.win, font=("times", 12))
        clock.place(x=550 , y=75)
        cidClock()

        self.label = Label(self.win, text='Durasi :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 100)
        #Jam = datetime.datetime.strftime(self.Jam, '%H:%M').time()
        #Jam2 = int(Jam)
        #print(Jam2)
        Jam = str(self.Jam)
        print(Jam)
        Ambil_Waktu = ''
        if Jam[1] != ':':
            Ambil_Waktu = (Jam[0] + Jam[1] + '.' + Jam[3] + Jam[4])
        else :
            Ambil_Waktu = ('0' + Jam[0] + '.' + Jam[2] + Jam[3])
        print('Tes Jam')
        print(Ambil_Waktu)
        Convert_Waktu = float(Ambil_Waktu)
        #Convert_Jam = Convert_Waktu / 3600
        print(Convert_Waktu)
        #Convert_Jam = str(Convert_Jam)
        #Convert_Jam = (Convert_Jam[0] + Convert_Jam[1])
        #Convert_Jam = int(Convert_Jam)

        def cidClock():    
            #c_time = datetime.datetime.now().strftime("%H:%M:%S")
             
            #c_time = datetime.datetime.now() - datetime.timedelta(hours=Convert_Jam)
            c_time = datetime.datetime.now() - datetime.timedelta(hours=Convert_Waktu)
            c_time = c_time.strftime("%H:%M:%S")
            clock.config(text=c_time)
            clock.after(100,cidClock)
            
        clock = Label(self.win, font=("times", 12))
        clock.place(x=550 , y=100)
        cidClock()

        self.label = Label(self.win, text='Pertemuan Ke :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 125)

        self.label = Label(self.win, text=self.Akademik[1])
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 125)

        self.label = Label(self.win, text='Ruang :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 150)

        self.label = Label(self.win, text=self.Nama_Ruang)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 150)

        self.label = Label(self.win, text='Kelas :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=400, y = 175)

        self.label = Label(self.win, text=self.Nama_Kelas)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=550, y = 175)

        self.button = Button(self.win, text="PRESENSI KELAS", font=('Times New Roman bold',12), 
        command=self.Kembali, bg="yellow", fg="black")
        self.button.config(width = 50, height = 2)
        self.button.place(x=550, y=400)

        self.count = 1
        self.button = Button(self.win, text="LOGOUT", font=('Times New Roman bold',12), 
        command= self.Halaman_Log_Out, bg="red", fg="white")
        self.button.config(width = 50, height = 2)
        self.button.place(x=550, y=460)

        self.win.title("KONFIRMASI PERKULIAHAN")
        self.win.mainloop()

    def Halaman_Log_Out(self):

        self.win.destroy()
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=600, height=600)
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 600 / 2)
        str1 = "600x600+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        #self.win.resizable(width=False, height=False)

        x, y = 60, 0

        self.label = Label(self.win, text=self.Nama_Dosen)
        self.label.config(font=("Times New Roman bold", 18))
        self.label.place(x=0, y = 0)

        self.label = Label(self.win, text='Mata Kuliah :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 50)

        self.label = Label(self.win, text=self.Nama_Matakuliah)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=100, y = 50)

        self.label = Label(self.win, text='Pertemuan Ke :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 75)

        self.label = Label(self.win, text=self.Pertemuan_Ke)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=100, y = 75)

        self.label = Label(self.win, text='Tanggal :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 100)

        now = datetime.datetime.today().strftime('%Y-%m-%d')
        self.label = Label(self.win, text=now)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=100, y = 100)

        self.label = Label(self.win, text='Jam :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 125)

        self.label = Label(self.win, text=self.Jam)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=100, y = 125)

        self.label = Label(self.win, text='s/d')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=160, y = 125)

        def cidClock():    
            c_time = datetime.datetime.now().strftime("%H:%M:%S")
            clock.config(text=c_time)
            clock.after(100,cidClock)
            
        clock = Label(self.win, font=("times", 12))
        clock.place(x=185 , y=125)
        cidClock()

        self.label = Label(self.win, text='Durasi :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 150)
        Jam = str(self.Jam)
        print(Jam)
        Ambil_Waktu = ''
        if Jam[1] != ':':
            Ambil_Waktu = (Jam[0] + Jam[1] + '.' + Jam[3] + Jam[4])
        else :
            Ambil_Waktu = ('0' + Jam[0] + '.' + Jam[2] + Jam[3])
        print('Tes Jam')
        print(Ambil_Waktu)
        Convert_Waktu = float(Ambil_Waktu)
        print(Convert_Waktu)

        def cidClock():    
            c_time = datetime.datetime.now() - datetime.timedelta(hours=Convert_Waktu)
            c_time = c_time.strftime("%H Jam %M Menit %S Detik")
            clock.config(text=c_time)
            clock.after(100,cidClock)
            
        clock = Label(self.win, font=("times", 12))
        clock.place(x=100 , y=150)
        cidClock()

        self.label = Label(self.win, text='Materi :')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 175)

        self.label = Label(self.win, text=self.Materi)
        self.label.config(font=("Times New Roman", 12))
        self.label.place(x=100, y = 175)

        self.label = Label(self.win, text='Untuk Log Out Silahkan Verifikasi Wajah Sekali Lagi')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 250)

        self.label = Label(self.win, text='KONFIRMASI')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 275)

        self.label = Label(self.win, text='Dosen')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=0, y = 300)

        if self.count == 1 or self.count == 2:
            self.button = Button(self.win, text="Verifikasi", font=('Times New Roman bold',12), 
            command=self.Verifikasi)
            self.button.config(width = 10, height = 2)
            self.button.place(x=0, y=325)
        else: 
            self.label = Label(self.win, text='☑')
            self.label.config(font=("Times New Roman bold", 12))
            self.label.place(x=0, y = 325)

        self.label = Label(self.win, text='Mahasiswa 1')
        self.label.config(font=("Times New Roman bold", 12))
        self.label.place(x=100, y = 300)

        if self.count == 1 or self.count == 3:
            self.button = Button(self.win, text="Verifikasi", font=('Times New Roman bold',12), 
            command=self.Verifikasi2)
            self.button.config(width = 10, height = 2)
            self.button.place(x=100, y=325)
        else:
            self.label = Label(self.win, text='☑')
            self.label.config(font=("Times New Roman bold", 12))
            self.label.place(x=100, y = 325)

        self.button = Button(self.win, text="Batal", font=('Times New Roman bold',12), 
        command=self.Kembali)
        self.button.config(width = 10, height = 2)
        self.button.place(x=0, y=400)

        if self.count == 4:
            self.button = Button(self.win, text="Simpan", font=('Times New Roman bold',12), 
            command=self.Log_Out)
            self.button.config(width = 10, height = 2)
            self.button.place(x=100, y=400)

        """self.button = Button(self.win, text="LOGOUT", font=('Times New Roman bold',12), 
        command=self.Log_Out, bg="red", fg="white")
        self.button.config(width = 50, height = 2)
        self.button.place(x=550, y=460)"""

        self.win.title("LOG OUT")
        self.win.mainloop()

    def Verifikasi(self): #Verifikasi Wajah Dosen

        Data_Verifikasi_Dosen = (
            self.Nama_Dosen
        )
        """print(self.NIK)
        print('sssssksoakasoksaoksa')
        self.win.destroy()
        #db.db.tes_waktu(self.NIK, self)
        tup = (
            self.NIK,
            self.Hari
        )
        result = db.db.cek_waktu(tup, self)
        LoginWindow(result, self.NIK, self.Hari, self.Jam)"""
        key = cv2.waitKey(1)
        webcam = cv2.VideoCapture(0)
        sleep(2)
        entryString = 'Dosen'
        if(entryString == 'Dosen'):
            while True:
                check, frame = webcam.read()
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('s'): 
                    cv2.imwrite(filename='./wajah_presensi/6.jpg', img=frame)
                    webcam.release()
                    print("Processing image...")
                    img_ = cv2.imread('./wajah_presensi/6.jpg', cv2.IMREAD_ANYCOLOR)
                    print("Converting RGB image to grayscale...")
                    gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                    print("Converted RGB image to grayscale...")
                    print("Resizing image to 92x112 scale...")
                    img_ = cv2.resize(img_,(92,112))
                    print("Resized...")
                    img_resized = cv2.imwrite(filename='./wajah_presensi/6.jpg', img=img_)
                    print("Image saved!")
                    if not os.path.exists('Results'): 
                        os.makedirs('Results')
                    else:
                        shutil.rmtree('Results')                                               
                        os.makedirs('Results')
                    
                    cv2.destroyAllWindows()
                    #self.win.destroy()
                    efaces = self.Eigenfaces2(entryString)
                    efaces = self.evaluate_celebrities2('wajah_presensi') 
                    break
                
                elif key == ord('q'):
                    webcam.release()
                    cv2.destroyAllWindows()
                    break

    def Verifikasi2(self):

        print(self.result) #Mengoper kode, nama matkul, hari, ruang, kelas
        print('tesss data kehadiran')
        print(self.Data_Kehadiran)
        """print(self.NIK)
        print('sssssksoakasoksaoksa')
        self.win.destroy()
        #db.db.tes_waktu(self.NIK, self)
        tup = (
            self.NIK,
            self.Hari
        )
        result = db.db.cek_waktu(tup, self)
        LoginWindow(result, self.NIK, self.Hari, self.Jam)"""
        key = cv2.waitKey(1)
        webcam = cv2.VideoCapture(0)
        sleep(2)
        entryString = 'Mahasiswa'
        if(entryString == 'Mahasiswa'):
            while True:
                check, frame = webcam.read()
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('s'): 
                    cv2.imwrite(filename='./wajah_presensi/6.jpg', img=frame)
                    webcam.release()
                    print("Processing image...")
                    img_ = cv2.imread('./wajah_presensi/6.jpg', cv2.IMREAD_ANYCOLOR)
                    print("Converting RGB image to grayscale...")
                    gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                    print("Converted RGB image to grayscale...")
                    print("Resizing image to 92x112 scale...")
                    img_ = cv2.resize(img_,(92,112))
                    print("Resized...")
                    img_resized = cv2.imwrite(filename='./wajah_presensi/6.jpg', img=img_)
                    print("Image saved!")
                    if not os.path.exists('Results'): 
                        os.makedirs('Results')
                    else:
                        shutil.rmtree('Results')                                               
                        os.makedirs('Results')
                    
                    cv2.destroyAllWindows()
                    #self.win.destroy()
                    efaces = self.Eigenfaces3(entryString)
                    efaces = self.evaluate_celebrities3('wajah_presensi') 
                    break
                
                elif key == ord('q'):
                    webcam.release()
                    cv2.destroyAllWindows()
                    break

    def Foto(self):

        print(self.result) #Mengoper kode, nama matkul, hari, ruang, kelas
        print('tesss data kehadiran')
        print(self.Data_Kehadiran)
        """print(self.NIK)
        print('sssssksoakasoksaoksa')
        self.win.destroy()
        #db.db.tes_waktu(self.NIK, self)
        tup = (
            self.NIK,
            self.Hari
        )
        result = db.db.cek_waktu(tup, self)
        LoginWindow(result, self.NIK, self.Hari, self.Jam)"""
        key = cv2.waitKey(1)
        webcam = cv2.VideoCapture(0)
        sleep(2)
        entryString = 'Mahasiswa'
        if(entryString == 'Mahasiswa'):
            while True:
                check, frame = webcam.read()
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('s'): 
                    cv2.imwrite(filename='./wajah_presensi/6.jpg', img=frame)
                    webcam.release()
                    print("Processing image...")
                    img_ = cv2.imread('./wajah_presensi/6.jpg', cv2.IMREAD_ANYCOLOR)
                    print("Converting RGB image to grayscale...")
                    gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                    print("Converted RGB image to grayscale...")
                    print("Resizing image to 92x112 scale...")
                    img_ = cv2.resize(img_,(92,112))
                    print("Resized...")
                    img_resized = cv2.imwrite(filename='./wajah_presensi/6.jpg', img=img_)
                    print("Image saved!")
                    if not os.path.exists('Results'): 
                        os.makedirs('Results')
                    else:
                        shutil.rmtree('Results')                                               
                        os.makedirs('Results')
                    
                    cv2.destroyAllWindows()
                    #self.win.destroy()
                    efaces = self.Eigenfaces(entryString)
                    efaces = self.evaluate_celebrities('wajah_presensi') 
                    break
                
                elif key == ord('q'):
                    webcam.release()
                    cv2.destroyAllWindows()
                    break

    def Kembali(self): #Kembali ke halaman presensi

        result =(
            self.result[0],
            self.result[1],
            self.Nama_Dosen,
            self.Hari,
            self.Nama_Kelas,
            self.Nama_Ruang,
            self.result[6],
            self.result[7]
        )
        tup = (
            self.result[0],
            self.Pertemuan_Ke,
            self.Nama_Dosen
        )
        self.win.destroy()
        now = datetime.datetime.now()
        x = LoginWindow(result, self.Nama_Dosen, self.Hari, self.Jam, 0, self.NIK_Pengganti)

    def Log_Out(self): #Untuk Log Out Dosen

        tup = (
            self.Materi,
            self.Kode_Matkul,
            self.Pertemuan_Ke,
            self.Nama_Dosen
        )
        db.db.dosen_logout(tup, self)
        self.win.destroy()

    def actions(self,e):
        # get the value of selected row
        tt = self.tr.focus()

        #get the column id
        col = self.tr.identify_column(e.x)
        #print(col)
        #print(self.tr.item(tt))

        tup = (
            self.tr.item(tt).get('text'), 
            self.Kode_Matkul,
            self.Pertemuan_Ke,
        )

        print(tup)
        print('tes tuppp')
        if col == "#4":
            res = messagebox.askyesno("Message", "Do you want to cancel?")
            if res:
                rs = db.db.cancel_kehadiran(tup)
                if rs:
                    messagebox.showinfo("Message", "Data Cancel Succesfully")
                    # self.Kembali
                    # self.win.destroy()
                    # z = ShowPresensi()
                    # z.add_frame()
                    result =(
                        self.result[0],
                        self.result[1],
                        self.Nama_Dosen,
                        self.Hari,
                        self.Nama_Kelas,
                        self.Nama_Ruang,
                        self.result[6],
                        self.result[7]
                    )
                    tup = (
                        self.result[0],
                        self.Pertemuan_Ke,
                        self.Nama_Dosen
                    )
                    self.win.destroy()
                    now = datetime.datetime.now()
                    x = LoginWindow(result, self.Nama_Dosen, self.Hari, self.Jam, 0, self.NIK_Pengganti)
            # else:
            #     self.win.destroy()
            #     z = ShowPresensi()
            #     z.add_frame()

    faces_count = 1 #jumlah folder s1

    faces_dir = '.'                                                             

    train_faces_count = 5                                                       
    test_faces_count = 1                                                        

    l = train_faces_count * faces_count                                        
    m = 92                                                                      
    n = 112                                                                   
    mn = m * n 

    def Eigenfaces(self, _faces_dir = '.', _energy = 0.85):
        print('> Initializing started')

        self.faces_dir = _faces_dir
        self.energy = _energy
        self.training_ids = []                                                  

        L = np.empty(shape=(self.mn, self.l), dtype='float64')                  

        cur_img = 0
        for face_id in range(1, self.faces_count + 1):

            training_ids = random.sample(list(range(1, 6)), self.train_faces_count)  
            self.training_ids.append(training_ids)                              

            for training_id in training_ids:
                path_to_img = os.path.join(self.faces_dir,
                        's' + str(face_id), str(training_id) + '.jpg')          

                img = cv2.imread(path_to_img, 0)                                
                img_col = np.array(img, dtype='float64').flatten()              

                L[:, cur_img] = img_col[:]                                     
                cur_img += 1

        self.mean_img_col = np.sum(L, axis=1) / self.l                          

        for j in range(0, self.l):                                             
            L[:, j] -= self.mean_img_col[:]

        C = np.matrix(L.transpose()) * np.matrix(L)                             # instead of computing the covariance matrix as
        C /= self.l                                                             # L*L^T, we set C = L^T*L, and end up with way
                                                                                # smaller and computentionally inexpensive one
                                                                                # we also need to divide by the number of training
                                                                                # images


        self.evalues, self.evectors = np.linalg.eig(C)                          # eigenvectors/values of the covariance matrix
        sort_indices = self.evalues.argsort()[::-1]                             # getting their correct order - decreasing
        self.evalues = self.evalues[sort_indices]                               # puttin the evalues in that order
        self.evectors = self.evectors[:,sort_indices]                             # same for the evectors

        evalues_sum = sum(self.evalues[:])                                      # include only the first k evectors/values so
        evalues_count = 0                                                       # that they include approx. 85% of the energy
        evalues_energy = 0.0
        for evalue in self.evalues:
            evalues_count += 1
            evalues_energy += evalue / evalues_sum

            if evalues_energy >= self.energy:
                break

        self.evalues = self.evalues[0:evalues_count]                            # reduce the number of eigenvectors/values to consider
        self.evectors = self.evectors[:,0:evalues_count]

        #self.evectors = self.evectors.transpose()                                # change eigenvectors from rows to columns (Should not transpose) 
        self.evectors = L * self.evectors                                       # left multiply to get the correct evectors
        norms = np.linalg.norm(self.evectors, axis=0)                           # find the norm of each eigenvector
        self.evectors = self.evectors / norms                                   # normalize all eigenvectors

        self.W = self.evectors.transpose() * L                                  # computing the weights

        print('> Initializing ended')

    """
    Classify an image to one of the eigenfaces.
    """
    def classify(self, path_to_img):
        img = cv2.imread(path_to_img, 0)                                        # read as a grayscale image
        img_col = np.array(img, dtype='float64').flatten()                      # flatten the image
        img_col -= self.mean_img_col                                            # subract the mean column
        img_col = np.reshape(img_col, (self.mn, 1))                             # from row vector to col vector

        S = self.evectors.transpose() * img_col                                 # projecting the normalized probe onto the
                                                                                # Eigenspace, to find out the weights

        diff = self.W - S                                                       # finding the min ||W_j - S||
        norms = np.linalg.norm(diff, axis=0)

        closest_face_id = np.argmin(norms)                                      # the id [0..240) of the minerror face to the sample
        return int(closest_face_id / self.train_faces_count) + 1                   # return the faceid (1..40)

    def evaluate_celebrities(self, celebrity_dir='.'):
        print('> Evaluating celebrity matches started')
        for img_name in os.listdir(celebrity_dir):                              # go through all the celebrity images in the folder
            path_to_img = os.path.join(celebrity_dir, img_name)

            img = cv2.imread(path_to_img, 0)                                    # read as a grayscale image
            img_col = np.array(img, dtype='float64').flatten()                  # flatten the image
            img_col -= self.mean_img_col                                        # subract the mean column
            img_col = np.reshape(img_col, (self.mn, 1))                         # from row vector to col vector

            S = self.evectors.transpose() * img_col                             # projecting the normalized probe onto the
                                                                                # Eigenspace, to find out the weights

            diff = self.W - S                                                   # finding the min ||W_j - S||
            norms = np.linalg.norm(diff, axis=0)
            top5_ids = np.argpartition(norms, 1)[:1]                           # first five elements: indices of top 5 matches in AT&T set

            name_noext = os.path.splitext(img_name)[0]                          
            result_dir = os.path.join('results', name_noext)                    
            os.makedirs(result_dir)                                             
            result_file = os.path.join(result_dir, 'results.txt')               
            euclidean_distance = 0 #mengukur jarak euclidean terdekat
            NIM = ''
            f = open(result_file, 'w')                                          
            for top_id in top5_ids:
                face_id = (top_id // self.train_faces_count) + 1                 
                subface_id = self.training_ids[face_id-1][top_id % self.train_faces_count]    
                path_to_img = os.path.join(self.faces_dir,
                        's' + str(face_id), str(subface_id) + '.jpg')          
                NIM = str(subface_id)
                shutil.copyfile(path_to_img,                                    
                        os.path.join(result_dir, str(subface_id) + '.jpg'))
                f.write('id: %3d, score: %.6f\n' % (top_id, norms[top_id]))     # write the id and its score to the results file
                f.write('%.6f' % (norms[top_id]))
                if int(norms[top_id]) >= euclidean_distance:
                    euclidean_distance = int(norms[top_id]) #Nilai result, jika diatas 2000 maka gambar tidak dikenali
            f.close()                                                           # close the results file
        print('> Evaluating celebrity matches ended')
        print(euclidean_distance)
        kode_gambar = NIM +'.jpg'
        print(kode_gambar)
        # if euclidean_distance <= 5000:
        tup = (
            kode_gambar
        )
        NIM = db.db.mahasiswa_login(kode_gambar) 
        #for i in db.db.dosen_login(kode_gambar):
            #print(i[0])
            #NIK = i[0]
        #print(NIK)
        if NIM: #Mengecek apakah benar wajah mahasiswa
            print('tessssssss NIM')
            print(NIM) #menampilkan NIM mahasiswa
            tup = (
                self.Data_Kehadiran[0],
                NIM[0]
            )
            Verifikasi_KRS = db.db.cek_krs_mahasiswa(tup, self) #Mengecek apakah mahasiswa mengambil matkul tersebut
            print('cekkk KRS')
            print(Verifikasi_KRS)
            if Verifikasi_KRS:
                tup = (
                    Verifikasi_KRS[3],
                    Verifikasi_KRS[4],
                    Verifikasi_KRS[1],
                    Verifikasi_KRS[2],
                    self.Data_Kehadiran[2]
                )
                cek_data = (
                    NIM[0], #Mendapatkan NIM
                    Verifikasi_KRS[1], #Mendapatkan Kode Matkul
                    self.Data_Kehadiran[2] #Mendapatkan Pertemuan
                )
                Pengecekan = db.db.cek_presensi(cek_data, self) #Mengecek mahasiswa sudah presensi atau belum
                if Pengecekan:
                    messagebox.showinfo("Message", "Anda sudah presensi")
                    self.win.destroy()
                    now = datetime.datetime.now()
                    result =(
                        Verifikasi_KRS[1],
                        self.Nama_Matakuliah,
                        self.Nama_Dosen,
                        self.Hari,
                        self.Nama_Kelas,
                        self.Nama_Ruang,
                        now,
                        now
                    )
                    x = LoginWindow(result, self.NIK, self.Hari, self.Jam, 0, self.NIK_Pengganti)
                else:
                    db.db.pencatatan_presensi(tup, self)
                    messagebox.showinfo("Message", "Presensi Berhasil")
                    self.win.destroy()
                    now = datetime.datetime.now()
                    result =(
                        Verifikasi_KRS[1],
                        self.Nama_Matakuliah,
                        self.Nama_Dosen,
                        self.Hari,
                        self.Nama_Kelas,
                        self.Nama_Ruang,
                        now,
                        now
                    )
                    x = LoginWindow(result, self.NIK, self.Hari, self.Jam, 0, self.NIK_Pengganti) #Merefresh halaman presensi
            else:
                messagebox.showinfo("Message", "NIM Tidak Terdaftar")
        else:
            messagebox.showinfo("Message", "Wajah Tidak Dikenali")
        # else:
        #     messagebox.showinfo("Message", "Wajah Tidak Dikenali")

    def Eigenfaces2(self, _faces_dir = '.', _energy = 0.85):
        print('> Initializing started')

        self.faces_dir = _faces_dir
        self.energy = _energy
        self.training_ids = []                                                  

        L = np.empty(shape=(self.mn, self.l), dtype='float64')                  

        cur_img = 0
        for face_id in range(1, self.faces_count + 1):

            training_ids = random.sample(list(range(1, 6)), self.train_faces_count)  
            self.training_ids.append(training_ids)                              

            for training_id in training_ids:
                path_to_img = os.path.join(self.faces_dir,
                        's' + str(face_id), str(training_id) + '.jpg')          

                img = cv2.imread(path_to_img, 0)                                
                img_col = np.array(img, dtype='float64').flatten()              

                L[:, cur_img] = img_col[:]                                     
                cur_img += 1

        self.mean_img_col = np.sum(L, axis=1) / self.l                          

        for j in range(0, self.l):                                             
            L[:, j] -= self.mean_img_col[:]

        C = np.matrix(L.transpose()) * np.matrix(L)                             # instead of computing the covariance matrix as
        C /= self.l                                                             # L*L^T, we set C = L^T*L, and end up with way
                                                                                # smaller and computentionally inexpensive one
                                                                                # we also need to divide by the number of training
                                                                                # images


        self.evalues, self.evectors = np.linalg.eig(C)                          # eigenvectors/values of the covariance matrix
        sort_indices = self.evalues.argsort()[::-1]                             # getting their correct order - decreasing
        self.evalues = self.evalues[sort_indices]                               # puttin the evalues in that order
        self.evectors = self.evectors[:,sort_indices]                             # same for the evectors

        evalues_sum = sum(self.evalues[:])                                      # include only the first k evectors/values so
        evalues_count = 0                                                       # that they include approx. 85% of the energy
        evalues_energy = 0.0
        for evalue in self.evalues:
            evalues_count += 1
            evalues_energy += evalue / evalues_sum

            if evalues_energy >= self.energy:
                break

        self.evalues = self.evalues[0:evalues_count]                            # reduce the number of eigenvectors/values to consider
        self.evectors = self.evectors[:,0:evalues_count]

        #self.evectors = self.evectors.transpose()                                # change eigenvectors from rows to columns (Should not transpose) 
        self.evectors = L * self.evectors                                       # left multiply to get the correct evectors
        norms = np.linalg.norm(self.evectors, axis=0)                           # find the norm of each eigenvector
        self.evectors = self.evectors / norms                                   # normalize all eigenvectors

        self.W = self.evectors.transpose() * L                                  # computing the weights

        print('> Initializing ended')

    """
    Classify an image to one of the eigenfaces.
    """
    def classify2(self, path_to_img):
        img = cv2.imread(path_to_img, 0)                                        # read as a grayscale image
        img_col = np.array(img, dtype='float64').flatten()                      # flatten the image
        img_col -= self.mean_img_col                                            # subract the mean column
        img_col = np.reshape(img_col, (self.mn, 1))                             # from row vector to col vector

        S = self.evectors.transpose() * img_col                                 # projecting the normalized probe onto the
                                                                                # Eigenspace, to find out the weights

        diff = self.W - S                                                       # finding the min ||W_j - S||
        norms = np.linalg.norm(diff, axis=0)

        closest_face_id = np.argmin(norms)                                      # the id [0..240) of the minerror face to the sample
        return int(closest_face_id / self.train_faces_count) + 1                   # return the faceid (1..40)

    def evaluate_celebrities2(self, celebrity_dir='.'):
        print('> Evaluating celebrity matches started')
        for img_name in os.listdir(celebrity_dir):                              # go through all the celebrity images in the folder
            path_to_img = os.path.join(celebrity_dir, img_name)

            img = cv2.imread(path_to_img, 0)                                    # read as a grayscale image
            img_col = np.array(img, dtype='float64').flatten()                  # flatten the image
            img_col -= self.mean_img_col                                        # subract the mean column
            img_col = np.reshape(img_col, (self.mn, 1))                         # from row vector to col vector

            S = self.evectors.transpose() * img_col                             # projecting the normalized probe onto the
                                                                                # Eigenspace, to find out the weights

            diff = self.W - S                                                   # finding the min ||W_j - S||
            norms = np.linalg.norm(diff, axis=0)
            top5_ids = np.argpartition(norms, 1)[:1]                           # first five elements: indices of top 5 matches in AT&T set

            name_noext = os.path.splitext(img_name)[0]                          
            result_dir = os.path.join('results', name_noext)                    
            os.makedirs(result_dir)                                             
            result_file = os.path.join(result_dir, 'results.txt')               
            euclidean_distance = 0 #mengukur jarak euclidean terdekat
            NIK = ''
            f = open(result_file, 'w')                                          
            for top_id in top5_ids:
                face_id = (top_id // self.train_faces_count) + 1                 
                subface_id = self.training_ids[face_id-1][top_id % self.train_faces_count]    
                path_to_img = os.path.join(self.faces_dir,
                        's' + str(face_id), str(subface_id) + '.jpg')          
                NIK = str(subface_id)
                shutil.copyfile(path_to_img,                                    
                        os.path.join(result_dir, str(subface_id) + '.jpg'))
                f.write('id: %3d, score: %.6f\n' % (top_id, norms[top_id]))     # write the id and its score to the results file
                f.write('%.6f' % (norms[top_id]))
                if int(norms[top_id]) >= euclidean_distance:
                    euclidean_distance = int(norms[top_id]) #Nilai result, jika diatas 2000 maka gambar tidak dikenali
            f.close()                                                           # close the results file
        print('> Evaluating celebrity matches ended')
        print(euclidean_distance)
        kode_gambar = NIK +'.jpg'
        print(kode_gambar)
        #if euclidean_distance <= 5000:
        tup = (
            kode_gambar
        )
        print(self.NIK_Pengganti)
        print('aaaaaaaaaaaaaaaaaaaa')
        if self.NIK_Pengganti == 0: #Jika tidak ada dosen pengganti
            print('tes gagal')
            Hasil_Verifikasi = db.db.Verifikasi_dosen(kode_gambar) 
            #for i in db.db.dosen_login(kode_gambar):
                #print(i[0])
                #NIK = i[0]
            #print(NIK)
            if self.Nama_Dosen == Hasil_Verifikasi[0]: #Jika benar wajah dosen
                if self.count == 1: #Jika mahasiswa dan dosen belum verifikasi wajah
                    self.count = 3
                    self.win.destroy
                    x =  self.Halaman_Log_Out()
                elif self.count == 2: #Jika mahasiswa sudah verifikasi wajah tetapi dosen belum
                    self.count = 4
                    self.win.destroy
                    x =  self.Halaman_Log_Out()
            else:
                messagebox.showinfo("Message", "Wajah Tidak Dikenali")
        else: #Jika ada dosen pengganti
            Hasil_Verifikasi2 = db.db.Verifikasi_pengganti(kode_gambar) 
            print('tes berhasil')
            #for i in db.db.dosen_login(kode_gambar):
                #print(i[0])
                #NIK = i[0]
            #print(NIK)
            if self.NIK_Pengganti[0] == Hasil_Verifikasi2[0]: #Jika benar wajah dosen
                if self.count == 1: #Jika mahasiswa dan dosen belum verifikasi wajah
                    self.count = 3
                    self.win.destroy
                    x =  self.Halaman_Log_Out()
                elif self.count == 2: #Jika mahasiswa sudah verifikasi wajah tetapi dosen belum
                    self.count = 4
                    self.win.destroy
                    x =  self.Halaman_Log_Out()
            else:
                messagebox.showinfo("Message", "Wajah Tidak Dikenali")
        # else:
        #     messagebox.showinfo("Message", "Wajah Tidak Dikenali")

    def Eigenfaces3(self, _faces_dir = '.', _energy = 0.85):
        print('> Initializing started')

        self.faces_dir = _faces_dir
        self.energy = _energy
        self.training_ids = []                                                  

        L = np.empty(shape=(self.mn, self.l), dtype='float64')                  

        cur_img = 0
        for face_id in range(1, self.faces_count + 1):

            training_ids = random.sample(list(range(1, 6)), self.train_faces_count)  
            self.training_ids.append(training_ids)                              

            for training_id in training_ids:
                path_to_img = os.path.join(self.faces_dir,
                        's' + str(face_id), str(training_id) + '.jpg')          

                img = cv2.imread(path_to_img, 0)                                
                img_col = np.array(img, dtype='float64').flatten()              

                L[:, cur_img] = img_col[:]                                     
                cur_img += 1

        self.mean_img_col = np.sum(L, axis=1) / self.l                          

        for j in range(0, self.l):                                             
            L[:, j] -= self.mean_img_col[:]

        C = np.matrix(L.transpose()) * np.matrix(L)                             # instead of computing the covariance matrix as
        C /= self.l                                                             # L*L^T, we set C = L^T*L, and end up with way
                                                                                # smaller and computentionally inexpensive one
                                                                                # we also need to divide by the number of training
                                                                                # images


        self.evalues, self.evectors = np.linalg.eig(C)                          # eigenvectors/values of the covariance matrix
        sort_indices = self.evalues.argsort()[::-1]                             # getting their correct order - decreasing
        self.evalues = self.evalues[sort_indices]                               # puttin the evalues in that order
        self.evectors = self.evectors[:,sort_indices]                             # same for the evectors

        evalues_sum = sum(self.evalues[:])                                      # include only the first k evectors/values so
        evalues_count = 0                                                       # that they include approx. 85% of the energy
        evalues_energy = 0.0
        for evalue in self.evalues:
            evalues_count += 1
            evalues_energy += evalue / evalues_sum

            if evalues_energy >= self.energy:
                break

        self.evalues = self.evalues[0:evalues_count]                            # reduce the number of eigenvectors/values to consider
        self.evectors = self.evectors[:,0:evalues_count]

        #self.evectors = self.evectors.transpose()                                # change eigenvectors from rows to columns (Should not transpose) 
        self.evectors = L * self.evectors                                       # left multiply to get the correct evectors
        norms = np.linalg.norm(self.evectors, axis=0)                           # find the norm of each eigenvector
        self.evectors = self.evectors / norms                                   # normalize all eigenvectors

        self.W = self.evectors.transpose() * L                                  # computing the weights

        print('> Initializing ended')

    """
    Classify an image to one of the eigenfaces.
    """
    def classify3(self, path_to_img):
        img = cv2.imread(path_to_img, 0)                                        # read as a grayscale image
        img_col = np.array(img, dtype='float64').flatten()                      # flatten the image
        img_col -= self.mean_img_col                                            # subract the mean column
        img_col = np.reshape(img_col, (self.mn, 1))                             # from row vector to col vector

        S = self.evectors.transpose() * img_col                                 # projecting the normalized probe onto the
                                                                                # Eigenspace, to find out the weights

        diff = self.W - S                                                       # finding the min ||W_j - S||
        norms = np.linalg.norm(diff, axis=0)

        closest_face_id = np.argmin(norms)                                      # the id [0..240) of the minerror face to the sample
        return int(closest_face_id / self.train_faces_count) + 1                   # return the faceid (1..40)

    def evaluate_celebrities3(self, celebrity_dir='.'):
        print('> Evaluating celebrity matches started')
        for img_name in os.listdir(celebrity_dir):                              # go through all the celebrity images in the folder
            path_to_img = os.path.join(celebrity_dir, img_name)

            img = cv2.imread(path_to_img, 0)                                    # read as a grayscale image
            img_col = np.array(img, dtype='float64').flatten()                  # flatten the image
            img_col -= self.mean_img_col                                        # subract the mean column
            img_col = np.reshape(img_col, (self.mn, 1))                         # from row vector to col vector

            S = self.evectors.transpose() * img_col                             # projecting the normalized probe onto the
                                                                                # Eigenspace, to find out the weights

            diff = self.W - S                                                   # finding the min ||W_j - S||
            norms = np.linalg.norm(diff, axis=0)
            top5_ids = np.argpartition(norms, 1)[:1]                           # first five elements: indices of top 5 matches in AT&T set

            name_noext = os.path.splitext(img_name)[0]                          
            result_dir = os.path.join('results', name_noext)                    
            os.makedirs(result_dir)                                             
            result_file = os.path.join(result_dir, 'results.txt')               
            euclidean_distance = 0 #mengukur jarak euclidean terdekat
            NIM = ''
            f = open(result_file, 'w')                                          
            for top_id in top5_ids:
                face_id = (top_id // self.train_faces_count) + 1                 
                subface_id = self.training_ids[face_id-1][top_id % self.train_faces_count]    
                path_to_img = os.path.join(self.faces_dir,
                        's' + str(face_id), str(subface_id) + '.jpg')          
                NIM = str(subface_id)
                shutil.copyfile(path_to_img,                                    
                        os.path.join(result_dir, str(subface_id) + '.jpg'))
                f.write('id: %3d, score: %.6f\n' % (top_id, norms[top_id]))     # write the id and its score to the results file
                f.write('%.6f' % (norms[top_id]))
                if int(norms[top_id]) >= euclidean_distance:
                    euclidean_distance = int(norms[top_id]) #Nilai result, jika diatas 2000 maka gambar tidak dikenali
            f.close()                                                           # close the results file
        print('> Evaluating celebrity matches ended')
        print(euclidean_distance)
        kode_gambar = NIM +'.jpg'
        print(kode_gambar)
        #if euclidean_distance <= 5000:
        tup = (
            kode_gambar
        )
        Hasil_Verifikasi_NIM = db.db.Verifikasi_mahasiswa(kode_gambar) #Verifikasi wajah mahasiswa untuk mendapatkan NIM 
        #for i in db.db.dosen_login(kode_gambar):
            #print(i[0])
            #NIK = i[0]
        #print(NIK)
        tup = (
            Hasil_Verifikasi_NIM[0],
            self.Nama_Matakuliah
        )
        Hasil_Verifikasi_Matkul = db.db.Verifikasi_Matkul(tup, self) #Verifikasi apakah mahasiswa tersebut mengambil mata kuliah tersebut
        if Hasil_Verifikasi_Matkul: #Jika benar
            if self.count == 1: #Jika mahasiswa dan dosen belum verifikasi wajah
                self.count = 2
                self.win.destroy
                x =  self.Halaman_Log_Out()
            elif self.count == 3: #Jika dosen sudah verifikasi wajah tetapi mahasiswa belum
                self.count = 4
                self.win.destroy
                x =  self.Halaman_Log_Out()
        else:
            messagebox.showinfo("Message", "NIM Tidak terdaftar")
        # else:
        #     messagebox.showinfo("Message", "Wajah Tidak Dikenali")

if __name__ == "__main__":
    now = datetime.datetime.now()
    result =(
        'MKB-1',
        'RTI',
        'abc',
        'Kamis',
        'T',
        '1.8',
        now,
        now
    )
    tup = (
        'MKB-1',
        2,
        'abc'
    )
    Jam = db.db.data_login(tup, SEL_FIRST)
    x = LoginWindow(result, '123', 'Kamis', Jam, 0, 0)