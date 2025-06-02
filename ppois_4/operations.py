import time
from entities import *

class ProductSearch:
    @staticmethod
    def search_by_name(mall, product_name):
        results = []
        for shop in mall.shops:
            for product in shop.products:
                if product_name.lower() in product.name.lower():
                    results.append((product, shop))
        return results
    
    @staticmethod
    def search_by_category(mall, category):
        results = []
        for shop in mall.shops:
            for product in shop.products:
                if category.lower() in product.category.lower():
                    results.append((product, shop))
        return results

class PurchaseOperation:
    @staticmethod
    def make_purchase(customer, product, shop, quantity, seller=None):
        if product.quantity < quantity:
            return False, "Недостаточно товара на складе", None
        
        total_price = product.price * quantity
        if customer.balance < total_price:
            return False, "Недостаточно средств на счете", None
        
        if not shop.cash_registers:
            return False, "В магазине нет доступных касс", None
        
        cash_register = shop.cash_registers[0]
        if cash_register.process_payment(total_price):
            product.quantity -= quantity
            customer.balance -= total_price
            purchase_record = {
                'product': product.name,
                'product_obj': product,
                'quantity': quantity,
                'total_price': total_price,
                'shop': shop.name,
                'shop_obj': shop,
                'seller': seller.name if seller else None,
                'date': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            customer.purchases.append(purchase_record)
            return True, "Покупка успешно совершена", purchase_record
        else:
            return False, "Ошибка при обработке платежа", None

class ReturnOperation:
    @staticmethod
    def return_product(customer, purchase_index):
        if purchase_index < 0 or purchase_index >= len(customer.purchases):
            return False, "Неверный индекс покупки"
        
        purchase = customer.purchases[purchase_index]
        shop = purchase['shop_obj']
        product = purchase['product_obj']
        
        if shop.return_policy_days == 0:
            return False, "В этом магазине возврат товаров не предусмотрен"
        
        seller_name = purchase['seller']
        seller = next((s for s in shop.sellers if s.name == seller_name), None)
        
        if not seller:
            return False, "Продавец не найден"
        
        success, message = seller.process_return(
            customer,
            product,
            purchase['date']
        )
        
        if success:
            customer.balance += purchase['total_price']
            product.quantity += purchase['quantity']
            customer.purchases.pop(purchase_index)
        
        return success, message

class PromotionOperation:
    @staticmethod
    def apply_promotion(purchase, promotion):
        discount_amount = purchase['total_price'] * promotion.discount / 100
        purchase['total_price'] -= discount_amount
        purchase['applied_promotion'] = promotion.name
        return purchase

class RentOperation:
    @staticmethod
    def rent_space(mall, shop, months):
        total_cost = shop.rent_price * months
        return {
            'shop': shop.name,
            'months': months,
            'total_cost': total_cost,
            'start_date': time.strftime("%Y-%m-%d"),
            'end_date': time.strftime("%Y-%m-%d", time.localtime(time.time() + months * 30 * 24 * 3600))
        }

class ServiceRating:
    @staticmethod
    def rate_seller(seller, rating):
        if 1 <= rating <= 5:
            seller.rating = (seller.rating + rating) / 2
            return True, "Рейтинг обновлен"
        return False, "Рейтинг должен быть от 1 до 5"