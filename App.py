import json

def getJSONdata(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data
def syncJSONdata(filename, database):
    with open(filename, "w") as file:
        json.dump(database, file) 

class Item():
    def __init__(self, nama, toko, harga):
        self.nama = nama
        self.toko = toko
        self.harga = harga
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
        return list(self.data[toko].keys())

database = Database(getJSONdata("database.json"))
# database = Database({})

# def printDict(s):
#     print(json.dumps(s, indent=2))
# database.addToko("Toko C", "12345678")
# # printDict(database.data)
# database.addBarang("Toko C", "Ganja", 300, 1000000)
# # printDict(database.data)
# database.editStockBarang("Toko C", "Ganja", 400)
# # printDict(database.data)
# database.editHargaBarang("Toko C", "Ganja", 2000000)
# printDict(database.data)
syncJSONdata("database.json", json.dumps(database.data))

# def homepage_penjual():
#     print("0. Login\n1. Daftar")
#     inp = input("Login atau daftar?\n")

# def homepage_pembeli():
#     pass
# def homepage():
#     print("-- HOMEPAGE --\n0. Penjual\n1. Pembeli")
#     inp = input("Anda penjual atau pembeli?\n")
#     if(inp == "0"):
#         homepage_penjual()
#     elif(inp == "1"):
#         homepage_pembeli()
#     else:
#         print("Invalid Input")
#         homepage()

# homepage()
        

































