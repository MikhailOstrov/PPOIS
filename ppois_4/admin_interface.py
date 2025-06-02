from controller import ShoppingMallController

class AdminInterface:
    def __init__(self, mall):
        self.controller = ShoppingMallController(mall)
        self.commands = {
            "1": ("Просмотреть все магазины", self.view_shops),
            "2": ("Просмотреть текущие акции", self.view_promotions),
            "3": ("Поиск товаров", self.search_products),
            "4": ("Просмотреть детали товара", self.view_product_details),
            "5": ("Совершить покупку", self.make_purchase),
            "6": ("Участие в акции", self.apply_promotion),
            "7": ("Аренда пространства", self.rent_space),
            "8": ("Оценить сервис", self.rate_service),
            "9": ("Отправить оповещение", self.send_announcement),
            "10": ("Сменить покупателя", self.change_customer),
            "11": ("Обработать возврат товара", self.process_return),
            "0": ("Выход", self.exit)
        }

    def run(self):
        print("\n=== Панель администратора торгового центра ===")
        print(f"ТЦ: {self.controller.mall.name}, Адрес: {self.controller.mall.address}\n")
        
        while True:
            self.show_menu()
            choice = input("Выберите действие: ").strip()
            if choice in self.commands:
                self.commands[choice][1]()
            else:
                print("Неверный ввод. Попробуйте снова.")

    def show_menu(self):
        print("\n=== Меню администратора ===")
        print(f"Текущий покупатель: {self.controller.current_customer.name}")
        for key, (description, _) in self.commands.items():
            print(f"{key}. {description}")

    def view_shops(self):
        print("\n=== Список магазинов ===")
        for i, shop in enumerate(self.controller.get_shops(), 1):
            print(f"{i}. {shop.name} ({shop.category})")
            print(f"   Площадь: {shop.area} кв.м, Аренда: {shop.rent_price} руб/мес")
            print(f"   Продавцов: {len(shop.sellers)}, Товаров: {len(shop.products)}")
            print(f"   Политика возврата: {shop.return_policy_days} дней")

    def view_promotions(self):
        print("\n=== Текущие акции ===")
        promotions = self.controller.get_promotions()
        if not promotions:
            print("Активные акции отсутствуют")
            return
        for i, promo in enumerate(promotions, 1):
            print(f"{i}. {promo.name} - {promo.description}")
            print(f"   Скидка: {promo.discount}%")

    def search_products(self):
        print("\n=== Поиск товаров ===")
        search_type = input("Искать по: 1 - названию, 2 - категории: ").strip()
        if search_type == "1":
            query = input("Введите название товара: ").strip()
            results = self.controller.search_products("name", query)
        elif search_type == "2":
            query = input("Введите категорию товара: ").strip()
            results = self.controller.search_products("category", query)
        else:
            print("Неверный выбор")
            return
        if not results:
            print("Товары не найдены")
            return
        print("\n=== Результаты поиска ===")
        for i, (product, shop) in enumerate(results, 1):
            print(f"{i}. {product.name} в магазине '{shop.name}'")
            print(f"   Цена: {product.price} руб, Остаток: {product.quantity} шт")
            print(f"   Категория: {product.category}")

    def view_product_details(self):
        print("\n=== Просмотр деталей товара ===")
        product_name = input("Введите название товара: ").strip()
        result = self.controller.get_product_details(product_name)
        if not result:
            print("Товар не найден")
            return
        product, shop = result
        print(f"\n=== Детали товара: {product.name} ===")
        print(f"Магазин: {shop.name}")
        print(f"Цена: {product.price} руб")
        print(f"Остаток: {product.quantity} шт")
        print(f"Категория: {product.category}")
        if product.specifications:
            print("\nХарактеристики:")
            for key, value in product.specifications.items():
                print(f"- {key}: {value}")
        elif product.category == "Бытовая техника":
            print("\nТиповые характеристики:")
            print("- Гарантия: 2 года")
            print("- Страна производства: зависит от модели")
            if "стиральная" in product.name.lower():
                print("- Количество оборотов: 1200 об/мин")
                print("- Режимы стирки: хлопок, синтетика, деликатная")
            elif "холодильник" in product.name.lower():
                print("- Объем: 300 л")
                print("- Класс энергопотребления: A++")

    def make_purchase(self):
        print("\n=== Совершение покупки ===")
        product_name = input("Введите название товара: ").strip()
        quantity = input("Введите количество: ").strip()
        try:
            quantity = int(quantity)
            print("\nДоступные продавцы:")
            result = self.controller.get_product_details(product_name)
            if not result:
                print("Товар не найден")
                return
            _, shop = result
            if shop.sellers:
                for i, s in enumerate(shop.sellers, 1):
                    print(f"{i}. {s.name} ({s.position})")
                choice = input("Выберите продавца (Enter - без продавца): ").strip()
                seller_name = None
                if choice and choice.isdigit() and 0 < int(choice) <= len(shop.sellers):
                    seller_name = shop.sellers[int(choice)-1].name
            else:
                seller_name = None
            success, message, _ = self.controller.make_purchase(product_name, quantity, seller_name)
            print(message)
            if success:
                print(f"Остаток на счете: {self.controller.current_customer.balance} руб")
        except ValueError:
            print("Количество должно быть числом")

    def apply_promotion(self):
        print("\n=== Участие в акции ===")
        promotions = self.controller.get_promotions()
        if not promotions:
            print("Нет доступных акций")
            return
        print("Доступные акции:")
        for i, promo in enumerate(promotions, 1):
            print(f"{i}. {promo.name} - {promo.description} ({promo.discount}%)")
        choice = input("Выберите акцию: ").strip()
        if not choice.isdigit() or not 0 < int(choice) <= len(promotions):
            print("Неверный выбор")
            return
        promo = promotions[int(choice)-1]
        if not self.controller.current_customer.purchases:
            print("У вас нет покупок для применения акции")
            return
        print("Ваши покупки:")
        for i, purchase in enumerate(self.controller.current_customer.purchases, 1):
            print(f"{i}. {purchase['product']} - {purchase['total_price']} руб")
        p_choice = input("Выберите покупку: ").strip()
        if not p_choice.isdigit() or not 0 < int(p_choice) <= len(self.controller.current_customer.purchases):
            print("Неверный выбор")
            return
        success, message = self.controller.apply_promotion(int(p_choice)-1, promo.name)
        print(message)

    def rent_space(self):
        print("\n=== Аренда торгового пространства ===")
        name = input("Название магазина: ").strip()
        category = input("Категория товаров: ").strip()
        try:
            area = float(input("Площадь (кв.м): ").strip())
            months = int(input("Срок аренды (месяцев): ").strip())
            success, rent_info = self.controller.rent_space(name, category, area, months)
            if success:
                print("\n=== Информация об аренде ===")
                print(f"Магазин: {rent_info['shop']}")
                print(f"Срок: {rent_info['months']} месяцев")
                print(f"Общая стоимость: {rent_info['total_cost']} руб")
                print(f"Дата начала: {rent_info['start_date']}")
                print(f"Дата окончания: {rent_info['end_date']}")
                confirm = input("\nПодтвердить аренду? (да/нет): ").strip().lower()
                if confirm == "да":
                    print("Аренда оформлена! Магазин добавлен в торговый центр.")
        except ValueError:
            print("Площадь и срок должны быть числами")

    def rate_service(self):
        print("\n=== Оценка сервиса ===")
        if not self.controller.current_customer.purchases:
            print("У вас нет покупок для оценки")
            return
        print("Ваши покупки с продавцами:")
        purchases_with_sellers = [
            (i, p) for i, p in enumerate(self.controller.current_customer.purchases, 1) 
            if p.get('seller')
        ]
        if not purchases_with_sellers:
            print("В ваших покупках нет информации о продавцах")
            return
        for i, p in purchases_with_sellers:
            print(f"{i}. {p['product']} - продавец {p['seller']}")
        choice = input("Выберите покупку для оценки: ").strip()
        if not choice.isdigit() or not 0 < int(choice) <= len(purchases_with_sellers):
            print("Неверный выбор")
            return
        try:
            rating = int(input("Оцените сервис (1-5): ").strip())
            success, message = self.controller.rate_seller(int(choice)-1, rating)
            print(message)
            if success:
                purchase = purchases_with_sellers[int(choice)-1][1]
                seller_name = purchase['seller']
                seller = next((s for shop in self.controller.get_shops() for s in shop.sellers if s.name == seller_name), None)
                if seller:
                    print(f"Текущий рейтинг продавца: {seller.rating:.1f}")
        except ValueError:
            print("Оценка должна быть числом")

    def send_announcement(self):
        message = input("Введите оповещение для всех посетителей: ").strip()
        success, result = self.controller.send_announcement(message)
        print("\n=== ОБЪЯВЛЕНИЕ ТОРГОВОГО ЦЕНТРА ===")
        print(result)

    def change_customer(self):
        name = input("Введите имя нового покупателя: ").strip()
        contact = input("Введите контактную информацию: ").strip()
        try:
            balance = float(input("Введите баланс покупателя: ").strip())
            success, message = self.controller.change_customer(name, contact, balance)
            print(message)
        except ValueError:
            print("Баланс должен быть числом")

    def process_return(self):
        print("\n=== Обработка возврата товара ===")
        if not self.controller.current_customer.purchases:
            print("У покупателя нет покупок")
            return
        print("Список покупок:")
        for i, purchase in enumerate(self.controller.current_customer.purchases, 1):
            print(f"{i}. {purchase['product']} - {purchase['date']}")
        choice = input("Выберите покупку для возврата: ").strip()
        if not choice.isdigit() or not 0 < int(choice) <= len(self.controller.current_customer.purchases):
            print("Неверный выбор")
            return
        try:
            success, message = self.controller.process_return(int(choice)-1)
            print(message)
            if success:
                print(f"Новый баланс: {self.controller.current_customer.balance} руб")
        except ValueError:
            print("Индекс покупки должен быть числом")

    def exit(self):
        print("Выход из панели администратора")
        raise SystemExit