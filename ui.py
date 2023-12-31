import os
import msvcrt
import ecommerce as ec
from datetime import date

# DEKLARASI DATABASE DAN KERANJANG
db = ec.Database(os.path.dirname(__file__)+"\\database.json")
cr = ec.Keranjang([])

# try:
# PRINT UI DENGAN SELECTOR
def printOpsi(text, opsi, **kwargs):
    cursor = 0
    while(True):
        os.system("cls")
        print(text)
        for i in range(len(opsi)):
            print(f"{i}. {opsi[i]}", end="")
            if(cursor == i):
                print(" <",end="")
            print()
        inp = msvcrt.getch()
        if(inp == b'H' and cursor>0):
            cursor -= 1
        elif(inp == b'P' and cursor<len(opsi)-1):
            cursor += 1
        elif(inp == b'\r'):
            break
    crsrOutput = kwargs.get("crsrOutput", False)
    if(crsrOutput):
        return cursor
    return opsi[cursor]

# SISTEM KERANJANG
def beliBarang(toko, barang):
    os.system("cls")
    harga = db.getHargaBarang(toko, barang)
    stock = db.getStockBarang(toko, barang)
    print(f"Stock Tersedia: {stock}")
    jumlah = int(input("Jumlah Barang yang Dibeli: "))
    if(jumlah<0 or jumlah > stock):
        x = printOpsi("Jumlah melebihi stock atau kurang dari 0.", ["Coba Lagi", "Kembali"])
        if(x == "Coba Lagi"):
            beliBarang(toko, barang)
        elif (x == "Kembali"):
            pilihBarang(toko)
    else:
        cr.addToCart(toko, barang, harga, jumlah)
        pilihBarang(toko)
def pilihToko():
    os.system("cls")
    toko = printOpsi("Berikut List Toko: ", ["Kembali"]+db.getListToko())
    if(toko == "Kembali"):
        homepagePembeli()
    else:
        pilihBarang(toko)
def pilihBarang(toko):
    os.system("cls")
    opsi = (db.getListBarang(toko))
    for i in range(len(opsi)):
        opsi[i] += f" Rp{db.getHargaBarang(toko, opsi[i])}"
    barang = printOpsi(f"List Barang {toko}: ", ["Kembali"]+opsi).rsplit(" ",1)[0]
    if(barang == "Kembali"):
        homepagePembeli()
    else:
        harga = db.getHargaBarang(toko, barang)
        stock = db.getStockBarang(toko, barang)
        x = printOpsi(f"{barang}:\nHarga:{harga}\nStock:{stock}", ["Beli", "Kembali"])
        if(x == "Beli"):
            beliBarang(toko, barang)
        elif(x == "Kembali"):
            pilihBarang(toko)
def editJumlah(idx):
    os.system("cls")
    item = cr.cart[idx]
    print(f"Jumlah sekarang: {item.jumlah}")
    print(f"Stock barang tersedia: {db.getStockBarang(item.toko, item.nama)}")
    jumlahBaru = int(input("Jumlah baru yang diinginkan: "))
    if(0<=jumlahBaru and jumlahBaru <= db.getStockBarang(item.toko, item.nama)):
        item.jumlah = jumlahBaru
        lihatKeranjang()
    else:
        x = printOpsi("Jumlah melebihi stock atau invalid", ["Coba Lagi", "Kembali"])
        if(x == "Coba Lagi"):
            editJumlah(idx)
        else:
            lihatKeranjang()
def editBarangKeranjang(idx):
    x = printOpsi(f"{cr.cart[idx].nama}", ["Edit Jumlah", "Hapus Barang", "Kembali"])
    if(x == "Edit Jumlah"):
        editJumlah(idx)
    elif(x == "Hapus Barang"):
        cr.removeFromCart(idx)
        lihatKeranjang()
    elif(x == "Kembali"):
        lihatKeranjang()
def lihatKeranjang():
    listKeranjang = []
    for item in cr.cart:
        listKeranjang.append(f"{item.nama} {item.toko} Rp{item.harga} x{item.jumlah}")
    x = printOpsi("Keranjang: ", ["Kembali"]+listKeranjang, crsrOutput=True)
    if(x == 0):
        homepagePembeli()
    else:
        editBarangKeranjang(x-1)

# SISTEM CHECKOUT PEMBELI
def printInvoice(krnjng, alamat):
    os.system("cls")
    now = date.today()
    invID = f"INV/{now.strftime('%d%m%Y%H%M%S')}"
    invoice = ""
    invoice += " --- INVOICE PEMBELIAN ---\n"
    invoice += f"{invID}\n"
    invoice += f"Tanggal Pembelian: {now.strftime('%d/%m/%Y')}\n"
    invoice += f"Alamat Pembelian: {alamat}\n"
    invoice += krnjng
    
    path = f"{os.path.dirname(__file__)}\\invoices" # Get path buat output invoice
    if not os.path.exists(path): # Cek apakah folder invoices ada
        os.makedirs(path)        # Kalo gk ada, buat baru
    with open(f"{path}\\{now.strftime('%d%m%Y%H%M%S')}.txt", 'w') as f: # Buat invoice
        f.write(invoice) # Buat invoice dengan isi string invoice
def updateStock():
    for item in cr.cart:
        stockbaru = db.getStockBarang(item.toko, item.nama) - item.jumlah
        db.editStockBarang(item.toko, item.nama, stockbaru)
def checkout():
    title = "Keranjang:\n"
    totalHarga = 0
    for i in range(len(cr.cart)):
        item = cr.cart[i]
        title += f"{i+1}. {item.nama} {item.toko} Rp{item.harga} x{item.jumlah}\n"
        totalHarga += item.harga*item.jumlah
    title += f"Total Harga: Rp{totalHarga}"
    x = printOpsi(title, ["Ok", "Kembali"])
    if(x == "Ok"):
        os.system("cls")
        alamat = input("Alamat pengiriman (Gratis Ongkir): ")
        printInvoice(title, alamat)
        updateStock()
        homepage()
    else:
        homepagePembeli()

# HOMEPAGE PEMBELI
def homepagePembeli():
    menu = printOpsi("Selamat Datang!", ["List Toko", "Keranjang", "Checkout", "Kembali"])
    if menu == "List Toko":
        pilihToko()
    elif menu == "Keranjang":
        lihatKeranjang()
    elif menu == "Checkout":
        checkout()
    elif menu == "Kembali":
        homepage()

# SISTEM PAGE PENJUAL
def editKatalog(toko):
    os.system("cls")
    barangs = db.getListBarang(toko)
    barang = printOpsi(f"List Barang", barangs)
    x = printOpsi(f"{barang}:\nHarga:{db.getHargaBarang(toko,barang)}\nStock:{db.getStockBarang(toko, barang)}", ["Edit Harga", "Edit Stock", "Remove Barang", "Kembali"])
    os.system("cls")
    if x == "Edit Harga":
        print(f"Harga sekarang: {db.getHargaBarang(toko, barang)}")
        newHarga = int(input("Harga Baru: "))
        db.editHargaBarang(toko, barang, newHarga)
    elif x == "Edit Stock":
        print(f"Stock sekarang: {db.getStockBarang(toko, barang)}")
        newStock = int(input("Stock Baru: "))
        db.editStockBarang(toko, barang, newStock)
    elif x == "Remove Barang":
        db.removeBarang(toko, barang)
    homepagePenjual(toko)
def tambahBarang(toko):
    os.system("cls")
    newBarang = input("Nama barang baru: ")
    if(newBarang == "Kembali"):
        x = printOpsi(f"Nama barang invalid", ["Coba lagi", "Kembali"])
        if(x == "Coba lagi"):
            tambahBarang(toko)
        elif(x == "Kembali"):
            homepagePenjual(toko)
    elif(newBarang in db.getListBarang(toko)):
        x = printOpsi(f"{newBarang} sudah ada di Katalog", ["Coba lagi", "Kembali"])
        if(x == "Coba lagi"):
            tambahBarang(toko)
        elif(x == "Kembali"):
            homepagePenjual(toko)
    else:
        newHarga = int(input("Harga Barang: "))
        newStock = int(input("Stock Barang: "))
        db.addBarang(toko, newBarang, newStock, newHarga)
        homepagePenjual(toko)
def homepagePenjual(toko):
    x = printOpsi(f"Selamat datang {toko}", ["Edit Katalog", "Tambah Barang", "Remove Toko", "Log Out"])
    if x == "Edit Katalog":
        editKatalog(toko)
    elif x == "Tambah Barang":
        tambahBarang(toko)
    elif x == "Log Out":
        homepage()
    elif x == "Remove Toko":
        db.removeToko(toko)
        homepage()

# SISTEM LOGIN DAN SINGUP AKUN PENJUAL
def signIn():
    toko = input("Nama Toko: ")
    password = input("Password Toko: ")
    db.addToko(toko, password)
    LoginPage()
def logIn():
    os.system("cls")
    toko = input("Nama Toko: ")
    password = input("Password Toko: ")
    if (toko in db.getListToko() and password == db.getTokoPass(toko)):
        homepagePenjual(toko)
    else:
        x = printOpsi("Nama Toko atau Password Invalid\nCoba lagi?", ["Ya", "Tidak"])
        if(x == "Ya"):
            logIn()
        elif(x == "Tidak"):
            LoginPage()
def LoginPage():
    x = printOpsi("Pilih:", ["Sign In", "Log In", "Kembali"])
    if x == "Sign In":
        signIn()
    elif x == "Log In":
        logIn()
    elif x == "Kembali":
        homepage()

# HOMEPAGE
def homepage():
    x = printOpsi("Selamat Datang!", ["Penjual", "Pembeli", "Exit"])
    if x == "Penjual":
        LoginPage()
    elif x == "Pembeli":
        homepagePembeli()
homepage()
# except:
#     homepage()