import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="python"
)

cursor = con.cursor()

#make a function to access the db
def user_login(tup):
    try:
        cursor.execute("SELECT * FROM `user` WHERE `username`=%s AND `password`=%s",tup)
        return (cursor.fetchone())
    except:
        return False

def nama_dosen():
    try:
        cursor.execute("SELECT NIK, Nama_Dosen FROM `daftar_dosen`")
        return (cursor.fetchall())
    except:
        return False

def dosen_login(kode):
    try:
        cursor.execute("SELECT NIK FROM daftar_dosen WHERE Gambar='" + kode + "'")
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False

def Verifikasi_dosen(kode):
    try:
        cursor.execute("SELECT Nama_Dosen FROM daftar_dosen WHERE Gambar='" + kode + "'")
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False

def Verifikasi_pengganti(kode):
    try:
        cursor.execute("SELECT NIK FROM daftar_dosen WHERE Gambar='" + kode + "'")
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False        

def Verifikasi_mahasiswa(kode):
    try:
        cursor.execute("SELECT NIM FROM mahasiswa WHERE Gambar='" + kode + "'")
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False

def Verifikasi_Matkul(tup, self):
    try:
        cursor.execute("SELECT * FROM daftar_krs_mahasiswa WHERE NIM=%s AND Nama_Matkul=%s", tup)
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False

def mahasiswa_login(kode): #Mengambil NIM Mahasiswa melalui verifikasi wajah
    try:
        cursor.execute("SELECT * FROM mahasiswa WHERE Gambar='" + kode + "'")
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False

def cek_krs_mahasiswa(tup, self): #mengecek apakah mahasiswa benar mengambil matkul tersebut
    try:
        cursor.execute("SELECT * FROM daftar_krs_mahasiswa WHERE Kode_Matkul=%s AND NIM=%s", tup)
        #NIK = cursor.fetchone()
        #print(NIK)
        return (cursor.fetchone())
    except:
        return False

#Mengambil value Tahun akademik, semester dan minggu ke berapa
def cek_semester():
    try:
        cursor.execute("SELECT Tahun_Akademik, Minggu, Semester FROM jadwal_perkuliahan WHERE NOW() BETWEEN Jadwal_Pertemuan_1 AND Jadwal_Pertemuan_2")
        return (cursor.fetchone())
    except:
        return False

#Mengecek apakah dosen benar dosen itu yang mengajar dan apakah memiliki sesi kelas pada hari itu
#mengembalikan nilai yang akan ditampilkan di bagian atas halaman_kedua
def cek_waktu(tup, self):
    try:
        cursor.execute("SELECT Kode_Matkul,Nama_Matkul,Nama_Dosen, Hari, Kelas, Ruang, Jam_Mulai, Jam_Selesai FROM daftar_matakuliah WHERE NOW() BETWEEN Jam_Mulai AND Jam_Selesai AND NIK=%s AND Hari=%s", tup)
        #cursor.execute("SELECT Kode_Matkul,Nama_Matkul,Nama_Dosen, Hari, Kelas, Ruang FROM daftar_matakuliah WHERE NOW() BETWEEN Jam_Mulai AND Jam_Selesai AND NIK=%s", tup)
        #NIK = cursor.fetchone()
        #print(NIK)
        self.Matkul = cursor.fetchone()
        return (self.Matkul)
    except:
        return False

"""def tes_waktu(tup, self):
    try:
        #cursor.execute("SELECT Kode_Matkul,Nama_Matkul,Nama_Dosen, Hari, Kelas, Ruang FROM daftar_matakuliah WHERE NOW() BETWEEN Jam_Mulai AND Jam_Selesai AND NIK=%s AND Hari=%s", tup)
        cursor.execute("UPDATE daftar_matakuliah SET Kode_Matkul = 'MKB-2' WHERE NOW() BETWEEN Jam_Mulai AND Jam_Selesai AND NIK=%s", tup)
        #NIK = cursor.fetchone()
        #print(NIK)
        self.Matkul = cursor.fetchone()
        return (self.Matkul)
    except:
        return False"""

#Dosen masuk ke dalam sistem presensi
def data_perkuliahan(tup, self):
#def data_perkuliahan(kode, nama, dosen, minggu, self):
    cursor.execute("INSERT INTO daftar_perkuliahan (Kode_Matkul, Nama_Matkul, Nama_Dosen, Pertemuan, tanggal_login, Login, Dosen_Pengganti) VALUES (%s,%s,%s,%s,NOW(),NOW(),%s)", tup)
    #cursor.execute("INSERT INTO daftar_perkuliahan (Kode_Matkul, Nama_Matkul, Nama_Dosen, Pertemuan, tanggal_login, Login) VALUES ('{}','{}','{}','{}',NOW(),NOW())").format(kode,nama,dosen,minggu)
    #NIK = cursor.fetchone()
    #print(NIK)
    con.commit()
    return True

#Mengambil jam dosen masuk ke dalam sistem presensi
def data_login(tup,self):
    try:
        cursor.execute("SELECT Login FROM daftar_perkuliahan WHERE Kode_Matkul = %s AND Pertemuan = %s AND Nama_Dosen = %s", tup)
        return (cursor.fetchone())
    except:
        return False

def data_Materi(tup,self):
    try:
        cursor.execute("SELECT Materi_Perkuliahan FROM daftar_perkuliahan WHERE Kode_Matkul = %s AND Pertemuan = %s AND Nama_Dosen = %s", tup)
        return (cursor.fetchone())
    except:
        return False

#Dosen keluar dari sistem presensi
def dosen_logout(tup, self):
    cursor.execute("UPDATE daftar_perkuliahan SET Logout = NOW(), Materi_Perkuliahan = %s WHERE Kode_Matkul=%s AND Pertemuan=%s AND Nama_Dosen = %s", tup)
    #NIK = cursor.fetchone()
    #print(NIK)
    con.commit()
    return True

#Menampilkan tabel kehadiran mahasiswa
def show_absensi(kode, self):
#def show_absensi():
    try:
        cursor.execute("SELECT NIM, Nama FROM daftar_krs_mahasiswa WHERE Kode_Matkul ='" + kode + "'")
        #cursor.execute("SELECT * FROM daftar_presensi_mahasiswa")
        #fetch all fetch all the data
        return cursor.fetchall()
    except: 
        return False
    

def cancel_kehadiran(tup):
    cursor.execute("UPDATE daftar_presensi_mahasiswa SET kode_absensi = 9 WHERE NIM=%s AND Kode_Matkul=%s AND Pertemuan=%s", tup)
    con.commit()
    return True

#Mengecek apakah mahasiswa sudah presensi, jika ya maka tercentang
def cek_presensi(tup, self):
    try:
        cursor.execute("SELECT * FROM `daftar_presensi_mahasiswa` WHERE `NIM`=%s AND `Kode_Matkul`=%s AND Pertemuan=%s",tup)
        return (cursor.fetchone())
    except:
        return False

#Mencatat kehadiran mahasiswa
def pencatatan_presensi(tup, self):
    cursor.execute("INSERT INTO daftar_presensi_mahasiswa (NIM, Nama, Kode_Matkul, Nama_Matkul, Tanggal_Presensi, Jam_Presensi, Pertemuan, kode_absensi) VALUES (%s,%s,%s,%s,NOW(),NOW(),%s,1)", tup)
    #NIK = cursor.fetchone()
    #print(NIK)
    con.commit()
    return True

def tes(self):
    print(self.Matkul)
