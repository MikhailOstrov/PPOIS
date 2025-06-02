import tkinter as tk
from tkinter import ttk, messagebox
from controller import ShoppingMallController

class ShoppingMallGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title(f"ТЦ: {controller.mall.name}")
        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Tabs
        self.shops_frame = ttk.Frame(self.notebook)
        self.promotions_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        self.product_details_frame = ttk.Frame(self.notebook)
        self.purchase_frame = ttk.Frame(self.notebook)
        self.promotion_apply_frame = ttk.Frame(self.notebook)
        self.rent_frame = ttk.Frame(self.notebook)
        self.rating_frame = ttk.Frame(self.notebook)
        self.announcement_frame = ttk.Frame(self.notebook)
        self.customer_frame = ttk.Frame(self.notebook)
        self.return_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.shops_frame, text="Магазины")
        self.notebook.add(self.promotions_frame, text="Акции")
        self.notebook.add(self.search_frame, text="Поиск товаров")
        self.notebook.add(self.product_details_frame, text="Детали товара")
        self.notebook.add(self.purchase_frame, text="Покупка")
        self.notebook.add(self.promotion_apply_frame, text="Применить акцию")
        self.notebook.add(self.rent_frame, text="Аренда")
        self.notebook.add(self.rating_frame, text="Оценка сервиса")
        self.notebook.add(self.announcement_frame, text="Оповещения")
        self.notebook.add(self.customer_frame, text="Сменить покупателя")
        self.notebook.add(self.return_frame, text="Возврат")

        self.setup_shops_tab()
        self.setup_promotions_tab()
        self.setup_search_tab()
        self.setup_product_details_tab()
        self.setup_purchase_tab()
        self.setup_promotion_apply_tab()
        self.setup_rent_tab()
        self.setup_rating_tab()
        self.setup_announcement_tab()
        self.setup_customer_tab()
        self.setup_return_tab()

    def setup_shops_tab(self):
        tk.Label(self.shops_frame, text="Список магазинов").pack()
        self.shops_text = tk.Text(self.shops_frame, height=20, width=50)
        self.shops_text.pack()
        tk.Button(self.shops_frame, text="Обновить", command=self.update_shops).pack()
        self.update_shops()

    def update_shops(self):
        self.shops_text.delete(1.0, tk.END)
        for i, shop in enumerate(self.controller.get_shops(), 1):
            self.shops_text.insert(tk.END, f"{i}. {shop.name} ({shop.category})\n")
            self.shops_text.insert(tk.END, f"   Площадь: {shop.area} кв.м, Аренда: {shop.rent_price} руб/мес\n")
            self.shops_text.insert(tk.END, f"   Продавцов: {len(shop.sellers)}, Товаров: {len(shop.products)}\n")
            self.shops_text.insert(tk.END, f"   Политика возврата: {shop.return_policy_days} дней\n\n")

    def setup_promotions_tab(self):
        tk.Label(self.promotions_frame, text="Текущие акции").pack()
        self.promotions_text = tk.Text(self.promotions_frame, height=10, width=50)
        self.promotions_text.pack()
        tk.Button(self.promotions_frame, text="Обновить", command=self.update_promotions).pack()
        self.update_promotions()

    def update_promotions(self):
        self.promotions_text.delete(1.0, tk.END)
        promotions = self.controller.get_promotions()
        if not promotions:
            self.promotions_text.insert(tk.END, "Активные акции отсутствуют\n")
            return
        for i, promo in enumerate(promotions, 1):
            self.promotions_text.insert(tk.END, f"{i}. {promo.name} - {promo.description}\n")
            self.promotions_text.insert(tk.END, f"   Скидка: {promo.discount}%\n\n")

    def setup_search_tab(self):
        tk.Label(self.search_frame, text="Поиск товаров").pack()
        tk.Label(self.search_frame, text="Тип поиска:").pack()
        self.search_type = tk.StringVar(value="name")
        tk.Radiobutton(self.search_frame, text="По названию", variable=self.search_type, value="name").pack()
        tk.Radiobutton(self.search_frame, text="По категории", variable=self.search_type, value="category").pack()
        tk.Label(self.search_frame, text="Запрос:").pack()
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack()
        tk.Button(self.search_frame, text="Искать", command=self.perform_search).pack()
        self.search_results = tk.Text(self.search_frame, height=15, width=50)
        self.search_results.pack()

    def perform_search(self):
        query = self.search_entry.get()
        results = self.controller.search_products(self.search_type.get(), query)
        self.search_results.delete(1.0, tk.END)
        if not results:
            self.search_results.insert(tk.END, "Товары не найдены\n")
            return
        for i, (product, shop) in enumerate(results, 1):
            self.search_results.insert(tk.END, f"{i}. {product.name} в магазине '{shop.name}'\n")
            self.search_results.insert(tk.END, f"   Цена: {product.price} руб, Остаток: {product.quantity} шт\n")
            self.search_results.insert(tk.END, f"   Категория: {product.category}\n\n")

    def setup_product_details_tab(self):
        tk.Label(self.product_details_frame, text="Название товара:").pack()
        self.product_name_entry = tk.Entry(self.product_details_frame)
        self.product_name_entry.pack()
        tk.Button(self.product_details_frame, text="Показать детали", command=self.show_product_details).pack()
        self.product_details_text = tk.Text(self.product_details_frame, height=15, width=50)
        self.product_details_text.pack()

    def show_product_details(self):
        product_name = self.product_name_entry.get()
        result = self.controller.get_product_details(product_name)
        self.product_details_text.delete(1.0, tk.END)
        if not result:
            self.product_details_text.insert(tk.END, "Товар не найден\n")
            return
        product, shop = result
        self.product_details_text.insert(tk.END, f"Товар: {product.name}\n")
        self.product_details_text.insert(tk.END, f"Магазин: {shop.name}\n")
        self.product_details_text.insert(tk.END, f"Цена: {product.price} руб\n")
        self.product_details_text.insert(tk.END, f"Остаток: {product.quantity} шт\n")
        self.product_details_text.insert(tk.END, f"Категория: {product.category}\n")
        if product.specifications:
            self.product_details_text.insert(tk.END, "\nХарактеристики:\n")
            for key, value in product.specifications.items():
                self.product_details_text.insert(tk.END, f"- {key}: {value}\n")
        if product.category == "Бытовая техника":
            self.product_details_text.insert(tk.END, "\nТиповые характеристики:\n")
            self.product_details_text.insert(tk.END, "- Гарантия: 2 года\n")
            self.product_details_text.insert(tk.END, "- Страна производства: зависит от модели\n")
            if "стиральная" in product.name.lower():
                self.product_details_text.insert(tk.END, "- Количество оборотов: 1200 об/мин\n")
                self.product_details_text.insert(tk.END, "- Режимы стирки: хлопок, синтетика, деликатная\n")
            elif "холодильник" in product.name.lower():
                self.product_details_text.insert(tk.END, "- Объем: 300 л\n")
                self.product_details_text.insert(tk.END, "- Класс энергопотребления: A++\n")

    def setup_purchase_tab(self):
        tk.Label(self.purchase_frame, text="Название товара:").pack()
        self.purchase_product_entry = tk.Entry(self.purchase_frame)
        self.purchase_product_entry.pack()
        tk.Label(self.purchase_frame, text="Количество:").pack()
        self.quantity_entry = tk.Entry(self.purchase_frame)
        self.quantity_entry.pack()
        tk.Label(self.purchase_frame, text="Продавец (опционально):").pack()
        self.seller_entry = tk.Entry(self.purchase_frame)
        self.seller_entry.pack()
        tk.Button(self.purchase_frame, text="Купить", command=self.perform_purchase).pack()
        self.purchase_result = tk.Text(self.purchase_frame, height=5, width=50)
        self.purchase_result.pack()

    def perform_purchase(self):
        product_name = self.purchase_product_entry.get()
        quantity = self.quantity_entry.get()
        seller_name = self.seller_entry.get() or None
        try:
            quantity = int(quantity)
            success, message, _ = self.controller.make_purchase(product_name, quantity, seller_name)
            self.purchase_result.delete(1.0, tk.END)
            self.purchase_result.insert(tk.END, f"{message}\n")
            if success:
                self.purchase_result.insert(tk.END, f"Остаток на счете: {self.controller.current_customer.balance} руб\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом")

    def setup_promotion_apply_tab(self):
        tk.Label(self.promotion_apply_frame, text="Индекс покупки:").pack()
        self.promotion_purchase_index = tk.Entry(self.promotion_apply_frame)
        self.promotion_purchase_index.pack()
        tk.Label(self.promotion_apply_frame, text="Название акции:").pack()
        self.promotion_name_entry = tk.Entry(self.promotion_apply_frame)
        self.promotion_name_entry.pack()
        tk.Button(self.promotion_apply_frame, text="Применить", command=self.apply_promotion).pack()
        self.promotion_result = tk.Text(self.promotion_apply_frame, height=5, width=50)
        self.promotion_result.pack()

    def apply_promotion(self):
        try:
            purchase_index = int(self.promotion_purchase_index.get())
            promotion_name = self.promotion_name_entry.get()
            success, message = self.controller.apply_promotion(purchase_index, promotion_name)
            self.promotion_result.delete(1.0, tk.END)
            self.promotion_result.insert(tk.END, message + "\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Индекс покупки должен быть числом")

    def setup_rent_tab(self):
        tk.Label(self.rent_frame, text="Название магазина:").pack()
        self.rent_name_entry = tk.Entry(self.rent_frame)
        self.rent_name_entry.pack()
        tk.Label(self.rent_frame, text="Категория:").pack()
        self.rent_category_entry = tk.Entry(self.rent_frame)
        self.rent_category_entry.pack()
        tk.Label(self.rent_frame, text="Площадь (кв.м):").pack()
        self.rent_area_entry = tk.Entry(self.rent_frame)
        self.rent_area_entry.pack()
        tk.Label(self.rent_frame, text="Срок аренды (месяцев):").pack()
        self.rent_months_entry = tk.Entry(self.rent_frame)
        self.rent_months_entry.pack()
        tk.Button(self.rent_frame, text="Арендовать", command=self.perform_rent).pack()
        self.rent_result = tk.Text(self.rent_frame, height=10, width=50)
        self.rent_result.pack()

    def perform_rent(self):
        try:
            name = self.rent_name_entry.get()
            category = self.rent_category_entry.get()
            area = float(self.rent_area_entry.get())
            months = int(self.rent_months_entry.get())
            success, rent_info = self.controller.rent_space(name, category, area, months)
            self.rent_result.delete(1.0, tk.END)
            if success:
                self.rent_result.insert(tk.END, "Аренда оформлена!\n")
                self.rent_result.insert(tk.END, f"Магазин: {rent_info['shop']}\n")
                self.rent_result.insert(tk.END, f"Срок: {rent_info['months']} месяцев\n")
                self.rent_result.insert(tk.END, f"Общая стоимость: {rent_info['total_cost']} руб\n")
                self.rent_result.insert(tk.END, f"Дата начала: {rent_info['start_date']}\n")
                self.rent_result.insert(tk.END, f"Дата окончания: {rent_info['end_date']}\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Площадь и срок должны быть числами")

    def setup_rating_tab(self):
        tk.Label(self.rating_frame, text="Индекс покупки:").pack()
        self.rating_purchase_index = tk.Entry(self.rating_frame)
        self.rating_purchase_index.pack()
        tk.Label(self.rating_frame, text="Оценка (1-5):").pack()
        self.rating_entry = tk.Entry(self.rating_frame)
        self.rating_entry.pack()
        tk.Button(self.rating_frame, text="Оценить", command=self.perform_rating).pack()
        self.rating_result = tk.Text(self.rating_frame, height=5, width=50)
        self.rating_result.pack()

    def perform_rating(self):
        try:
            purchase_index = int(self.rating_purchase_index.get())
            rating = int(self.rating_entry.get())
            success, message = self.controller.rate_seller(purchase_index, rating)
            self.rating_result.delete(1.0, tk.END)
            self.rating_result.insert(tk.END, message + "\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Индекс и оценка должны быть числами")

    def setup_announcement_tab(self):
        tk.Label(self.announcement_frame, text="Сообщение:").pack()
        self.announcement_entry = tk.Entry(self.announcement_frame)
        self.announcement_entry.pack()
        tk.Button(self.announcement_frame, text="Отправить", command=self.send_announcement).pack()
        self.announcement_result = tk.Text(self.announcement_frame, height=5, width=50)
        self.announcement_result.pack()

    def send_announcement(self):
        message = self.announcement_entry.get()
        success, result = self.controller.send_announcement(message)
        self.announcement_result.delete(1.0, tk.END)
        self.announcement_result.insert(tk.END, result + "\n")

    def setup_customer_tab(self):
        tk.Label(self.customer_frame, text="Имя покупателя:").pack()
        self.customer_name_entry = tk.Entry(self.customer_frame)
        self.customer_name_entry.pack()
        tk.Label(self.customer_frame, text="Контактная информация:").pack()
        self.customer_contact_entry = tk.Entry(self.customer_frame)
        self.customer_contact_entry.pack()
        tk.Label(self.customer_frame, text="Баланс:").pack()
        self.customer_balance_entry = tk.Entry(self.customer_frame)
        self.customer_balance_entry.pack()
        tk.Button(self.customer_frame, text="Сменить покупателя", command=self.change_customer).pack()
        self.customer_result = tk.Text(self.customer_frame, height=5, width=50)
        self.customer_result.pack()

    def change_customer(self):
        try:
            name = self.customer_name_entry.get()
            contact = self.customer_contact_entry.get()
            balance = float(self.customer_balance_entry.get())
            success, message = self.controller.change_customer(name, contact, balance)
            self.customer_result.delete(1.0, tk.END)
            self.customer_result.insert(tk.END, message + "\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Баланс должен быть числом")

    def setup_return_tab(self):
        tk.Label(self.return_frame, text="Индекс покупки:").pack()
        self.return_purchase_index = tk.Entry(self.return_frame)
        self.return_purchase_index.pack()
        tk.Button(self.return_frame, text="Оформить возврат", command=self.process_return).pack()
        self.return_result = tk.Text(self.return_frame, height=5, width=50)
        self.return_result.pack()

    def process_return(self):
        try:
            purchase_index = int(self.return_purchase_index.get())
            success, message = self.controller.process_return(purchase_index)
            self.return_result.delete(1.0, tk.END)
            self.return_result.insert(tk.END, message + "\n")
            if success:
                self.return_result.insert(tk.END, f"Новый баланс: {self.controller.current_customer.balance} руб\n")
        except ValueError:
            messagebox.showerror("Ошибка", "Индекс покупки должен быть числом")

if __name__ == "__main__":
    from main import initialize_mall
    root = tk.Tk()
    mall = initialize_mall()
    controller = ShoppingMallController(mall)
    app = ShoppingMallGUI(root, controller)
    root.mainloop()