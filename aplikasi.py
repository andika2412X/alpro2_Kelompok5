import csv
import os
import hashlib
import webbrowser
import time
from tabulate import tabulate  # Menggunakan pustaka tabulate untuk tampilan tabel
from manim import *

# Menentukan path penyimpanan dengan format yang benar
folder_path = r"D:\new\[TFN]\Alpro-1_k5\tubes"
file_transaksi = os.path.join(folder_path, "data_transaksi.csv")
file_member = os.path.join(folder_path, "data_member.csv")
file_admin = os.path.join(folder_path, "data_admin.csv")
file_barang = os.path.join(folder_path, "data_barang.csv")

# Membuat folder jika belum ada
os.makedirs(folder_path, exist_ok=True)

# Fungsi untuk mengenkripsi password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk menampilkan animasi selamat datang
def tampilkan_animasi_kasir():
    os.system("manim -pql kasir_animasi.py KasirAnimasi")

# Fungsi untuk menampilkan animasi transaksi berhasil
def tampilkan_animasi_transaksi():
    os.system("manim -pql transaksi.py TransaksiBerhasil")

# Fungsi untuk menambahkan member baru dengan nomor telepon sebagai primary key dan password
def tambah_member():
    nomor_telepon = input("Masukkan nomor telepon member: ")
    nama_member = input("Masukkan nama member: ")
    password = input("Masukkan password member: ")
    saldo = float(input("Masukkan saldo awal: "))
    level = "0"

    encrypted_password = hash_password(password)

    with open(file_member, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nomor_telepon, nama_member, encrypted_password, saldo, level])
    
    print(f"Member {nama_member} ({nomor_telepon}) berhasil ditambahkan dengan saldo Rp{saldo}!")

# Fungsi untuk mengganti password member
def ganti_password():
    nomor_telepon = input("Masukkan nomor telepon Anda: ")
    password_lama = input("Masukkan password lama: ")

    # Baca data member
    member_data = baca_member()
    if nomor_telepon not in member_data:
        print("Member tidak ditemukan!")
        return
    
    # Verifikasi password lama
    if member_data[nomor_telepon]["password"] != hash_password(password_lama):
        print("Password lama salah! Tidak dapat mengubah password.")
        return
    
    # Minta password baru
    password_baru = input("Masukkan password baru: ")
    member_data[nomor_telepon]["password"] = hash_password(password_baru)
    simpan_member(member_data)

    print("Password berhasil diperbarui!")


def tambah_admin():
    ID = input("Masukkan ID: ")
    password = input("Masukkan password member: ")

    encrypted_password = hash_password(password)

    with open(file_admin, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ID, encrypted_password])
    
    print(f"id ({ID}) berhasil ditambahkan!")

# Fungsi untuk menghapus member
def hapus_member():
    nomor_telepon = input("Masukkan nomor telepon member yang ingin dihapus: ")
    password = input("Masukkan password member: ")

    # Baca data member
    member_data = baca_member()
    if nomor_telepon not in member_data:
        print("Member tidak ditemukan!")
        return
    
    # Verifikasi password
    if member_data[nomor_telepon]["password"] != hash_password(password):
        print("Password salah! Akun tidak dapat dihapus.")
        return
    
    # Hapus akun dari data
    del member_data[nomor_telepon]
    simpan_member(member_data)

    print(f"Akun dengan nomor {nomor_telepon} berhasil dihapus!")

def hapus_admin():
    ID = input("Masukkan nomor telepon member yang ingin dihapus: ")
    password = input("Masukkan password member: ")

    # Baca data member
    admin_data = baca_admin()
    if ID not in admin_data:
        print("Member tidak ditemukan!")
        return
    
    # Verifikasi password
    if admin_data[ID]["password"] != hash_password(password):
        print("Password salah! Akun tidak dapat dihapus.")
        return
    
    # Hapus akun dari data
    del admin_data[ID]
    simpan_member(admin_data)

    print(f"Akun dengan nomor {ID} berhasil dihapus!")

# Fungsi untuk memverifikasi password saat member ingin melakukan transaksi
def verifikasi_member(nomor_telepon, password):
    member_data = baca_member()
    if nomor_telepon not in member_data:
        print("Member tidak ditemukan!")
        return False
    
    if member_data[nomor_telepon]["password"] != hash_password(password):
        print("Password salah!")
        return False
    
    return True

def verifikasi_admin(ID, password):
    admin_data = baca_admin()
    if ID not in admin_data:
        print("Member tidak ditemukan!")
        return False
    
    if admin_data[ID]["password"] != hash_password(password):
        print("Password salah!")
        return False
    
    return True

# Fungsi untuk menambahkan saldo member dengan verifikasi password
def tambah_saldo():
    nomor_telepon = input("Masukkan nomor telepon member yang ingin menambah saldo: ")

    member_data = baca_member()
    if nomor_telepon not in member_data:
        print("Member tidak ditemukan!")
        return False

    saldo_tambahan = int(input("Masukkan jumlah saldo yang ingin ditambahkan: "))
    member_data = baca_member()
    member_data[nomor_telepon]["saldo"] += saldo_tambahan
    simpan_member(member_data)

    print(f"Saldo member {member_data[nomor_telepon]['nama']} berhasil ditambahkan! Saldo sekarang: Rp{member_data[nomor_telepon]['saldo']}")

def kurang_saldo():
    nomor_telepon = input("Masukkan nomor telepon member yang ingin menambah saldo: ")

    member_data = baca_member()
    if nomor_telepon not in member_data:
        print("Member tidak ditemukan!")
        return False

    saldo_kurang = int(input("Masukkan jumlah saldo yang ingin dikurang: "))
    member_data = baca_member()
    member_data[nomor_telepon]["saldo"] -= saldo_kurang
    simpan_member(member_data)

    print(f"Saldo member {member_data[nomor_telepon]['nama']} berhasil dikurangi! Saldo sekarang: Rp{member_data[nomor_telepon]['saldo']}")

def tambah_barang():
    nama_barang = input("Masukkan nama barang: ")
    harga = int(input("Masukkan harga barang: "))

    with open(file_barang, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nama_barang, harga])
    
    print(f"Barang {nama_barang} berhasil ditambahkan dengan harga Rp{harga}!")

def baca_barang():
    barang_data = {}
    if os.path.exists(file_barang):
        with open(file_barang, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    barang_data[row[0]] = row[1]  # Menyimpan nama barang sebagai key dan harga sebagai value
    return barang_data

# Fungsi untuk membeli barang dengan nomor telepon dan password
keranjang = []  # Keranjang sebagai daftar sementara sebelum checkout

# Fungsi untuk menambahkan barang ke keranjang
def tambah_ke_keranjang():
    tampilkan_barang()
    nama_barang = input("Masukkan nama barang yang ingin ditambahkan ke keranjang: ")

    # Cek apakah barang tersedia
    barang_data = baca_barang()
    if nama_barang not in barang_data:
        print("Barang tidak ditemukan!")
        return
    
    jumlah = int(input("Masukkan jumlah barang: "))
    harga = barang_data[nama_barang]
    total = jumlah * int(harga)

    keranjang.append({"nama_barang": nama_barang, "jumlah": jumlah, "harga": harga, "total": total})
    print(f"{jumlah} {nama_barang} ditambahkan ke keranjang! Total: Rp{total}")

# Fungsi untuk menampilkan isi keranjang
def tampilkan_keranjang():
    if not keranjang:
        print("Keranjang masih kosong!")
        return
    
    print("\n=== Isi Keranjang ===")
    print(tabulate([[item["nama_barang"], item["jumlah"], item["harga"], item["total"]] for item in keranjang], 
                   headers=["Nama Barang", "Jumlah", "Harga", "Total"], tablefmt="grid"))
    print("=====================")

# Fungsi untuk menghapus satu barang dari keranjang
def hapus_satu_barang_keranjang():
    if not keranjang:
        print("Keranjang masih kosong!")
        return
    
    tampilkan_keranjang()
    nama_barang = input("Masukkan nama barang yang ingin dihapus: ")

    # Cari barang dalam keranjang
    for item in keranjang:
        if item["nama_barang"].lower() == nama_barang.lower():
            keranjang.remove(item)
            print(f"Barang '{nama_barang}' berhasil dihapus dari keranjang!")
            return
    
    print(f"Barang '{nama_barang}' tidak ditemukan dalam keranjang.")

# Fungsi untuk menghapus semua barang di keranjang
def hapus_keranjang():
    global keranjang
    if not keranjang:
        print("Keranjang sudah kosong!")
        return
    
    keranjang.clear()
    print("Keranjang berhasil dikosongkan!")

# Fungsi untuk checkout dan membayar
def checkout():
    nomor_telepon = input("Masukkan nomor telepon member untuk pembayaran: ")
    password = input("Masukkan password member: ")

    # Verifikasi member
    member_data = baca_member()
    if nomor_telepon not in member_data:
        print("Member tidak ditemukan!")
        return
    if member_data[nomor_telepon]["password"] != hash_password(password):
        print("Password salah!")
        return
    
    saldo = member_data[nomor_telepon]["saldo"]
    harga = sum(item["total"] for item in keranjang)

    if member_data[nomor_telepon]["level"] == 0:
        diskon = harga * 0
    elif member_data[nomor_telepon]["level"] <= 1:
        diskon = harga * 0.01
    elif member_data[nomor_telepon]["level"] <= 10:
        diskon = harga * 0.05
    else:
        diskon = harga * 0.1

    total_harga = harga - diskon

    if total_harga > saldo:
        print(f"Saldo tidak mencukupi! Total belanja Rp{total_harga}, saldo tersedia Rp{saldo}")
        return

    # Simpan transaksi
    with open(file_transaksi, mode='a', newline='') as file:
        writer = csv.writer(file)
        for item in keranjang:
            writer.writerow([nomor_telepon, item["nama_barang"], item["jumlah"], item["harga"], item["total"]])

    # Kurangi saldo member
    member_data[nomor_telepon]["saldo"] -= total_harga
    member_data[nomor_telepon]["level"] += 1
    simpan_member(member_data)
    tampilkan_animasi_transaksi()

    # Kosongkan keranjang
    keranjang.clear()

    print(f"Checkout berhasil! Total belanja Rp{total_harga}. Sisa saldo: Rp{member_data[nomor_telepon]['saldo']}")

def login():
    ID = input("Masukkan ID: ")
    password = input("Masukkan password admin: ")

    # Verifikasi admin
    admin_data = baca_admin()
    if ID not in admin_data:
        print("admin tidak ditemukan!")
        time.sleep(3)
        main()
    if admin_data[ID]["password"] != hash_password(password):
        print("Password salah!")
        time.sleep(3)
        main()

# Fungsi untuk membaca data member
def baca_member():
    member_data = {}
    if os.path.exists(file_member):
        with open(file_member, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    nomor_telepon, nama, password, saldo, level = row
                    member_data[nomor_telepon] = {"nama": nama, "password": password, "saldo": float(saldo), "level": int(level)}
    return member_data

def baca_admin():
    admin_data = {}
    if os.path.exists(file_admin):
        with open(file_admin, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    ID, password = row
                    admin_data[ID] = {"password": password,}
    return admin_data

# Fungsi untuk menyimpan kembali data member (update saldo)
def simpan_member(member_data):
    with open(file_member, mode='w', newline='') as file:
        writer = csv.writer(file)
        for nomor_telepon, data in member_data.items():
            writer.writerow([nomor_telepon, data["nama"], data["password"], data["saldo"], data["level"]]) 

def simpan_admin(admin_data):
    with open(file_admin, mode='w', newline='') as file:
        writer = csv.writer(file)
        for nomor_telepon, data in admin_data.items():
            writer.writerow([nomor_telepon, data["nama"], data["password"], data["saldo"]])

def tampilkan_member():
    member_data = baca_member()
    
    if not member_data:
        print("Belum ada member yang terdaftar.")
        return

    print("\n=== Daftar Member ===")
    print(tabulate([[nomor, data["nama"], data["saldo"]] for nomor, data in member_data.items()], 
                   headers=["Nomor Telepon", "Nama Member", "Saldo"], tablefmt="grid"))
    print("=====================")

def tampilkan_barang():
    if not os.path.exists(file_barang):
        print("Belum ada barang yang tersedia.")
        return

    with open(file_barang, mode='r') as file:
        reader = csv.reader(file)
        data = [row for row in reader if row]

    if not data:
        print("Belum ada barang yang tersedia.")
        return

    print("\n=== Daftar Barang ===")
    print(tabulate(data, headers=["Nama Barang", "Harga"], tablefmt="grid"))
    print("=====================")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar
    print("Selamat datang di Mesin Kasir!")
    while True:
        print("\nPilihan:")
        print("1.admin")
        print("2.user")
        print("0. Keluar")
        pilihan = input("Pilih opsi (1/2/0): ")
        if pilihan == '1':
            login()
            admin()
        elif pilihan == '2':
            mesin_kasir()
        elif pilihan == 'Admin#1234':
            tambah_admin()
        elif pilihan == '0':
            time.sleep(2)
            print("Terima kasih telah menggunakan mesin kasir!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

# Fungsi utama
def mesin_kasir():
    os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar
    tampilkan_animasi_kasir()
    print("=== Mesin Kasir ===")
    while True:
        print("\nPilihan:")
        print("1. Tambah barang ke keranjang")
        print("2. Tampilkan isi keranjang")
        print("3. Hapus satu barang dari keranjang")
        print("4. Hapus semua barang di keranjang")
        print("5. Checkout & bayar")
        print("0. Keluar")
        print("peringatan!, jangan pernah memasukan angka 666")
        pilihan = input("Pilih opsi (1/2/3/4/5/0): ")
        

        if pilihan == '1':
            os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar
            tambah_ke_keranjang()
        elif pilihan == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== Isi Keranjang ===")
            tampilkan_keranjang()
        elif pilihan == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            hapus_satu_barang_keranjang()
        elif pilihan == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            hapus_keranjang()
        elif pilihan == '5':
            checkout()
        elif pilihan == '666':
            os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar
            print("Anda telah memasukkan angka 666, yang merupakan angka terlarang!")
            print("apakah anda ingin melanjutkan? (1 untuk ya, 0 untuk tidak)")
            lanjut = input("Masukkan pilihan (1/0): ")
            if lanjut == '1':
                # URL YouTube
                youtube_url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
                # Buka browser dan masuk ke YouTube
                webbrowser.open(youtube_url)
            elif lanjut == '0':
                print("Anda memilih untuk tidak melanjutkan.")
                return
            else:
                print("Pilihan tidak valid, kembali ke menu utama.")
        elif pilihan == '0':
            time.sleep(2)
            print("Terima kasih telah menggunakan mesin kasir!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

def admin():
    os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar
    print("=== Mesin Kasir - ADMIN ===")
    while True:
        print("\nPilihan:")
        print("1. Tambah member")
        print("2. Hapus member")
        print("3. Ganti password member")
        print("4. Tambah saldo member")
        print("5. Kurang saldo member")
        print("6. Tambah barang")
        print("7. Tampilkan daftar member")
        print("8. Tampilkan daftar barang")
        print("0. Keluar")
        pilihan = input("Pilih opsi (1/2/3/4/5/6/7/8/0): ")

        if pilihan == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            tambah_member()
        elif pilihan == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            hapus_member()
        elif pilihan == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            ganti_password()
        elif pilihan == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            tambah_saldo()
        elif pilihan == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            kurang_saldo()
        elif pilihan == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            tambah_barang()
        elif pilihan == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== Daftar Member ===")
            tampilkan_member()
        elif pilihan == '8':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== Daftar Barang ===")
            tampilkan_barang()
        elif pilihan == '0':
            time.sleep(2)
            print("Terima kasih telah menggunakan mesin kasir!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

# Menjalankan aplikasi
main()
