from abc import ABC, abstractmethod

# ======================================
# MODELS (Lapisan Model)
# ======================================

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total(self):
        return self.product.price * self.quantity


# ======================================
# REPOSITORY (Lapisan Data)
# ======================================

class ProductRepository:
    def __init__(self):
        self.products = [
            Product(1, "Pulpen", 3000),
            Product(2, "Buku", 5000),
            Product(3, "Penghapus", 2000)
        ]

    def get_all(self):
        return self.products

    def get_by_id(self, pid):
        for p in self.products:
            if p.id == pid:
                return p
        return None


# ======================================
# SERVICES (Lapisan Bisnis)
# ======================================

class IPaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CashPayment(IPaymentProcessor):
    def pay(self, amount):
        print(f"Pembayaran tunai sebesar Rp{amount} berhasil.")


# ✅ Challenge OCP/DIP
class DebitCardPayment(IPaymentProcessor):
    def pay(self, amount):
        print(f"Pembayaran menggunakan Kartu Debit sebesar Rp{amount} berhasil.")


class CartService:
    def __init__(self):
        self.items = []

    def add_item(self, product, qty):
        self.items.append(CartItem(product, qty))

    def get_total(self):
        return sum(item.get_total() for item in self.items)

    def show_cart(self):
        print("\nIsi Keranjang:")
        for item in self.items:
            print(f"{item.product.name} x{item.quantity} = Rp{item.get_total()}")


# ======================================
# ORCHESTRATOR / APP (TIDAK DIUBAH)
# ======================================

class PosApp:
    def __init__(self, repo, cart_service, payment):
        self.repo = repo
        self.cart_service = cart_service
        self.payment = payment

    def run(self):
        while True:
            print("\n=== Sistem Kasir ===")
            print("1. Lihat Produk")
            print("2. Tambah ke Keranjang")
            print("3. Lihat Keranjang")
            print("4. Bayar")
            print("0. Keluar")

            menu = input("Pilih: ")

            if menu == "1":
                self.show_products()
            elif menu == "2":
                self.add_to_cart()
            elif menu == "3":
                self.cart_service.show_cart()
            elif menu == "4":
                self.checkout()
            elif menu == "0":
                print("Terima kasih!")
                break
            else:
                print("Menu tidak valid")

    def show_products(self):
        for p in self.repo.get_all():
            print(f"{p.id}. {p.name} - Rp{p.price}")

    def add_to_cart(self):
        pid = int(input("Masukkan ID Produk: "))
        qty = int(input("Jumlah: "))
        prod = self.repo.get_by_id(pid)

        if prod:
            self.cart_service.add_item(prod, qty)
            print("Berhasil ditambah ke keranjang")
        else:
            print("Produk tidak ditemukan")

    def checkout(self):
        total = self.cart_service.get_total()
        print(f"\nTotal belanja: Rp{total}")
        self.payment.pay(total)


# ======================================
# MAIN PROGRAM (Dependency Injection)
# ======================================

if __name__ == "__main__":
    repo = ProductRepository()
    cart = CartService()

    # ✅ Jangan ubah PosApp, hanya ganti payment di sini
    payment_method = DebitCardPayment()

    app = PosApp(repo, cart, payment_method)
    app.run()
