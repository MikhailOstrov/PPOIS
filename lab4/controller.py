from entities import *
from operations import *

class ShoppingMallController:
    def __init__(self, mall):
        self.mall = mall
        self.current_customer = Customer("Администратор", "admin@mymall.com")
        self.current_customer.add_funds(100000)

    def get_shops(self):
        return self.mall.shops

    def get_promotions(self):
        return self.mall.promotions

    def search_products(self, search_type, query):
        if search_type == "name":
            return ProductSearch.search_by_name(self.mall, query)
        elif search_type == "category":
            return ProductSearch.search_by_category(self.mall, query)
        return []

    def get_product_details(self, product_name):
        results = ProductSearch.search_by_name(self.mall, product_name)
        if results:
            return results[0]
        return None

    def make_purchase(self, product_name, quantity, seller_name=None):
        results = ProductSearch.search_by_name(self.mall, product_name)
        if not results:
            return False, "Товар не найден", None
        product, shop = results[0]
        seller = None
        if seller_name:
            seller = next((s for s in shop.sellers if s.name == seller_name), None)
        return PurchaseOperation.make_purchase(self.current_customer, product, shop, quantity, seller)

    def apply_promotion(self, purchase_index, promotion_name):
        promotion = next((p for p in self.mall.promotions if p.name == promotion_name), None)
        if not promotion:
            return False, "Акция не найдена"
        if purchase_index < 0 or purchase_index >= len(self.current_customer.purchases):
            return False, "Неверный индекс покупки"
        purchase = self.current_customer.purchases[purchase_index]
        updated_purchase = PromotionOperation.apply_promotion(purchase, promotion)
        return True, f"Акция '{promotion.name}' применена. Новая цена: {updated_purchase['total_price']} руб"

    def rent_space(self, name, category, area, months):
        rent_price = area * 500
        new_shop = Shop(name, category, area, rent_price)
        rent_info = RentOperation.rent_space(self.mall, new_shop, months)
        self.mall.add_shop(new_shop)
        return True, rent_info

    def rate_seller(self, purchase_index, rating):
        if purchase_index < 0 or purchase_index >= len(self.current_customer.purchases):
            return False, "Неверный индекс покупки"
        purchase = self.current_customer.purchases[purchase_index]
        seller_name = purchase.get('seller')
        if not seller_name:
            return False, "В этой покупке нет информации о продавце"
        seller = None
        for shop in self.mall.shops:
            seller = next((s for s in shop.sellers if s.name == seller_name), None)
            if seller:
                break
        if not seller:
            return False, "Продавец не найден"
        return ServiceRating.rate_seller(seller, rating)

    def send_announcement(self, message):
        return True, f"Оповещение отправлено: {message}"

    def change_customer(self, name, contact, balance):
        self.current_customer = Customer(name, contact)
        self.current_customer.add_funds(balance)
        return True, f"Текущий покупатель изменен на: {name}"

    def process_return(self, purchase_index):
        return ReturnOperation.return_product(self.current_customer, purchase_index)