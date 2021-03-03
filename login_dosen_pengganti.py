from tkinter import *
from tkinter import messagebox
import os
import cv2
import sys
import shutil
import random
import numpy as np
from time import sleep
import Halaman_Kedua
import db.db
import datetime

class Eigenfaces(object):    
    #result=None                                         
    faces_count = 1 #jumlah folder s1

    faces_dir = '.'                                                             

    train_faces_count = 6                                                       
    test_faces_count = 1                                                        

    l = train_faces_count * faces_count                                        
    m = 92                                                                      
    n = 112                                                                   
    mn = m * n                                                                 

    """
    Initializing the Eigenfaces model.
    """
    def __init__(self, _faces_dir = '.', _energy = 0.85):
        print('> Initializing started')

        self.faces_dir = _faces_dir
        self.energy = _energy
        self.training_ids = []                                                  

        L = np.empty(shape=(self.mn, self.l), dtype='float64')                  

        cur_img = 0
        for face_id in range(1, self.faces_count + 1):

            training_ids = random.sample(list(range(1, 7)), self.train_faces_count)  
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

    def evaluate_celebrities(self, celebrity_dir='.', NIK_Dosen_Reguler=''):
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
                    euclidean_distance = int(norms[top_id]) 
            f.close()                                                           # close the results file
        print('> Evaluating celebrity matches ended')
        print(euclidean_distance)
        print(NIK_Dosen_Reguler) # NIK Dosen Yang Mau Digantikan
        kode_gambar = NIM +'.jpg'
        print(kode_gambar)
        tup = (
            kode_gambar
        )
        NIK = db.db.dosen_login(kode_gambar) 
        print(NIK) #menampilkan NIK Dosen Pengganti
        #print(NIK)
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
            NIK_Dosen_Reguler,
            Hari
        )
        result = db.db.cek_waktu(tup, self) #Mengecek apakah Dosen masuk di jam yang benar
        Jadwal = db.db.cek_semester() #mengecek tahun ajaran, minggu ke berapa
        print(result) #menampilkan matkul yang dibawakan
        print(Jadwal)
        if result:
            #messagebox.showinfo("Message", "Login Berhasil")
            #self.Halaman_Kedua(result)
            #hal_kedua = Halaman_Kedua.LoginWindow(result)
            dosen_pengganti = NIK[0]
            print(dosen_pengganti)
            tup =(
                result[0],
                result[1],
                result[2],
                Jadwal[1],
                dosen_pengganti
            )
            Hasil = (
                result[0],
                Jadwal[1],
                result[2]
            )
            Pengecekan = db.db.data_login(Hasil, self)
            if Pengecekan:
                Hasil = (
                result[0],
                Jadwal[1],
                result[2]
                )
                print(Hasil)
                Jam_Login = db.db.data_login(Hasil, self)
                Halaman_Kedua.LoginWindow(result, NIK_Dosen_Reguler, Hari, Jam_Login[0], 0, NIK)
            else:
                db.db.data_perkuliahan(tup, self)
                #db.db.data_perkuliahan(result[0], result[1], result[2], str(Jadwal[1]), self)
                Hasil = (
                    result[0],
                    Jadwal[1],
                    result[2]
                )
                print(Hasil)
                Jam_Login = db.db.data_login(Hasil, self)
                Halaman_Kedua.LoginWindow(result, NIK_Dosen_Reguler, Hari, Jam_Login[0], 0, NIK)
                #login_reguler.Destroy(self)
                """result = db.db.dosen_kelas(result)
                print(result[0])"""
                #result = db.db.tes(self)
        else: 
            messagebox.showinfo("Message", "Anda Tidak Memiliki Sesi Kelas")
            login_pengganti(NIK)

class login_pengganti():
    
    def __init__(self, NIK):

        
        self.win = Tk()
        # print('Tes Operan')
        # print(NIK)
        # reset the window and background color
        self.NIK_Dosen_Reguler = NIK # NIK Dosen yang mau digantikan
        self.canvas = Canvas(self.win, width=700, height=250)
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 700 / 2)
        y = int(height / 2 - 250 / 2)
        str1 = "700x250+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        self.label = Label(self.win, text="Login Kelas")
        self.label.config(font=("Courier", 20, 'bold'))
        self.label.place(x=0, y = 0)

        self.label = Label(self.win, text="Berikut langkah-langkah untuk login:")
        self.label.config(font=("Courier", 15, 'bold'))
        self.label.place(x=0, y = 40)

        self.label = Label(self.win, text="1. Tekan Tombol login")
        self.label.config(font=("Courier", 15, 'bold'))
        self.label.place(x=0, y = 65)

        self.label = Label(self.win, text="2. Begitu kamera menyala, tekan huruf 'S' pada keyboard")
        self.label.config(font=("Courier", 15, 'bold'))
        self.label.place(x=0, y = 90)

        self.label = Label(self.win, text="   untuk verifikasi wajah")
        self.label.config(font=("Courier", 15, 'bold'))
        self.label.place(x=0, y = 115)
        
        self.label = Label(self.win, text="3. Untuk batal tekan tombol 'Q' pada keyboard")
        self.label.config(font=("Courier", 15, 'bold'))
        self.label.place(x=0, y = 140)
        
        x, y = 100, 0

        self.button = Button(self.win, text="LOGIN", font='Courier 15 bold', 
        command=self.Foto)
        self.button.place(x=310, y=200)


        # change the title of the window
        self.win.title("LOGIN")

        self.win.mainloop()

    def Foto(self):      
        #a = self.win.focus_get()
        self.win.destroy()
        
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
                    #a.destroy()
                    #self.win.destroy()
                    efaces = Eigenfaces(str(entryString))
                    efaces.evaluate_celebrities(str('wajah_presensi'), str(self.NIK_Dosen_Reguler))
                    break
                
                elif key == ord('q'):
                    webcam.release()
                    cv2.destroyAllWindows()
                    break