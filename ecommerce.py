import os
import json

class Database():
    # CONSTRUCTOR
    def __init__(self, filename):
        self.filename = filename
        self.data = self.getJSONdata(self.filename)

    # EDIT DATABASE
    def addToko(self, toko, password):
        self.data[toko] = {}
        self.data[toko]["password"] = password
        self.data[toko]["barang"] = {}
        self.postJSONdata(self.filename, self.data)
    def addBarang(self, toko, barang, stock, harga):
        self.data[toko]["barang"][barang] = {"harga":harga, "stock":stock}
        self.postJSONdata(self.filename, self.data)
    def editStockBarang(self, toko, barang, stock):
        self.data[toko]["barang"][barang]["stock"] = stock
        self.postJSONdata(self.filename, self.data)
    def editHargaBarang(self, toko, barang, harga):
        self.data[toko]["barang"][barang]["harga"] = harga
        self.postJSONdata(self.filename, self.data)
    def removeToko(self, toko):
        del self.data[toko]
        self.postJSONdata(self.filename, self.data)
    def removeBarang(self, toko, barang):
        del self.data[toko]["barang"][barang]
        self.postJSONdata(self.filename, self.data)
    
    # GET INFO
    def getTokoPass(self, toko):
        return self.data[toko]["password"]
    def getListToko(self):
        return list(self.data.keys())
    def getListBarang(self,toko):
        return list(self.data[toko]["barang"].keys())
    def getHargaBarang(self, toko, barang):
        return self.data[toko]["barang"][barang]["harga"]
    def getStockBarang(self, toko, barang):
        return self.data[toko]["barang"][barang]["stock"]

    # SYNC JSONFILE
    def getJSONdata(self, filename):
        f = open(filename)
        data = json.load(f)
        f.close()
        return data
    def postJSONdata(self, filename, database):
        with open(filename, "w") as file:
            json.dump(database, file, indent=4, separators=(',', ': '), sort_keys=True) 

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
