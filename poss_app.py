from abc import ABC, abstractmethod

# =========================
# MODELS
# =========================

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.id}. {self.name} - Rp{self.price}"


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total(self):
        return self.product.price * self.quantity


# =========================
# REPOSITORY
# =========================

class ProductRepository:
    def __init__(self):
        self.products = [
            Product(1, "Pulpen", 3000),
            Product(2, "Buku", 5000),
            Product(3, "Penghapus", 2000),
        ]

    def get_all(self):
        return self.products

    def get_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None


# =========================
# SERVICES
# =========================

class IPaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CashPayment(IPaymentProcessor):
    def pay(self, amount):
        print(f"Pembayaran tunai sebesar Rp{amount} berhasil.")


class DebitCardPayment(IPaymentProcessor):   # Challenge OCP/DIP
    def pay(self, amount):
        print(f"Pembayaran menggunakan Kartu Debit sebesar Rp{amount} berhasil.")


class CartService:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        # jika quantity <= 0 maka ignore
        if quantity <= 0:
            raise ValueError("Quantity harus > 0")
        self.items.append(CartItem(product, quantity))

    def get_total(self):
        return sum(item.get_total() for item in self.items)

    def show_cart(self):
        if not self.items:
            print("\nKeranjang kosong.")
            return
        print("\nIsi Keranjang:")
        for item in self.items:
            print(f"- {item.product.name} x{item.quantity} = Rp{item.get_total()}")
        print(f"Total: Rp{self.get_total()}")


# =========================
# ORCHESTRATOR / APP
# =========================

class PosApp:
    def __init__(self, product_repo, cart_service, payment_processor):
        self.product_repo = product_repo
        self.cart_service = cart_service
        self.payment_processor = payment_processor

    def run(self):
        while True:
            print("\n=== Sistem Kasir ===")
            print("1. Lihat Produk")
            print("2. Tambah ke Keranjang")
            print("3. Lihat Keranjang")
            print("4. Bayar")
            print("0. Keluar")

            menu = input("Pilih menu: ").strip()

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
                print("Menu tidak valid. Masukkan 1/2/3/4/0.")

    def show_products(self):
        products = self.product_repo.get_all()
        print("\nDaftar Produk:")
        for p in products:
            print(p)

    def add_to_cart(self):
        try:
            product_id_str = input("Masukkan ID produk: ").strip()
            qty_str = input("Jumlah: ").strip()

            product_id = int(product_id_str)
            quantity = int(qty_str)

            product = self.product_repo.get_by_id(product_id)
            if product:
                try:
                    self.cart_service.add_item(product, quantity)
                    print("Produk berhasil ditambahkan ke keranjang.")
                except ValueError as ve:
                    print("Error:", ve)
            else:
                print("Produk tidak ditemukan.")
        except ValueError:
            print("Input harus berupa angka (contoh: 1 dan 2).")

    def checkout(self):
        total = self.cart_service.get_total()
        if total == 0:
            print("Keranjang kosong. Tambahkan produk dulu.")
            return
        print(f"\nTotal belanja: Rp{total}")
        # panggil payment processor
        self.payment_processor.pay(total)
        # Kosongkan keranjang setelah bayar
        self.cart_service.items = []
        print("Transaksi selesai. Keranjang dikosongkan.")


# =========================
# MAIN PROGRAM (DI)
# =========================

if __name__ == "__main__":
    product_repo = ProductRepository()
    cart_service = CartService()

    # Challenge: ganti metode pembayaran di sini
    payment_method = DebitCardPayment()  # atau CashPayment()

    app = PosApp(product_repo, cart_service, payment_method)
    app.run()
