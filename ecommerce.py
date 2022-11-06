import os
import json

def getJSONdata(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data
def postJSONdata(filename, database):
    with open(filename, "w") as file:
        json.dump(database, file, indent=4, separators=(',', ': ')) 

class Database():
    def __init__(self, data):
        self.data = data
    # Penjual
    def addToko(self, toko, password):
        self.data[toko] = {}
        self.data[toko]["password"] = password
        self.data[toko]["barang"] = {}
    def addBarang(self, toko, barang, stock, harga):
        self.data[toko]["barang"][barang] = {"harga":harga, "stock":stock}
    def editStockBarang(self, toko, barang, stock):
        self.data[toko]["barang"][barang]["stock"] = stock
    def editHargaBarang(self, toko, barang, harga):
        self.data[toko]["barang"][barang]["harga"] = harga
    def getTokoPass(self, toko):
        return self.data[toko]["password"]
    # Pembeli
    def getListToko(self):
        return list(self.data.keys())
    def getListBarang(self,toko):
        return list(self.data[toko]["barang"].keys())
    def getHargaBarang(self, toko, barang):
        return self.data[toko]["barang"][barang]["harga"]
    def getStockBarang(self, toko, barang):
        return self.data[toko]["barang"][barang]["stock"]
    def printKatalog(self, toko):
        tokos = self.getListToko()
        for toko in tokos:
            print(toko)
            barangs = self.getListBarang(toko)
            for barang in barangs:
                print(f">> {barang}")

class Item():
    def __init__(self, nama, toko, harga, jumlah):
        self.nama = nama
        self.toko = toko
        self.harga = harga
        self.jumlah = jumlah
class Keranjang():
    def __init__(self, cart):
        self.cart = cart
    def addToCart(self, toko, barang, harga, jumlah):
        self.cart.append(Item(barang, toko, harga, jumlah))
    def removeFromCart(self, idx):
        self.cart.pop(idx)
    def editJumlah(self, idx, jumlahBaru):
        self.cart[idx].jumlah = jumlahBaru

    def printCart(self):
        for i in range(len(self.cart)):
            print(self.cart[i].nama)
            print(self.cart[i].toko)
            print(self.cart[i].harga)
            print(self.cart[i].jumlah)


database = Database(getJSONdata(os.path.dirname(__file__)+"\\database.json"))
database.addToko("Toko Ganja", "1234")
database.addBarang("Toko Ganja", "Ganja", 10, 100000)
database.addBarang("Toko Ganja", "Sabu-sabu", 20, 200000)
database.addToko("Toko Gaming", "5678")
database.addBarang("Toko Gaming", "Mouse", 5, 60000)
database.addBarang("Toko Gaming", "Keyboard", 2, 150000)
database.addBarang("Toko Gaming", "Speaker", 3, 100000)
database.addToko("Toko Senjata", "0000")
database.addBarang("Toko Senjata", "Ak47", 100, 5000)
postJSONdata(os.path.dirname(__file__)+"\\database.json", database.data)
# cart.addToCart("Toko Ganja", "Ganja", 100)
