import time

class ShoppingMall:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.shops = []
        self.galleries = []
        self.promotions = []
    
    def add_shop(self, shop):
        self.shops.append(shop)
    
    def add_gallery(self, gallery):
        self.galleries.append(gallery)
    
    def add_promotion(self, promotion):
        self.promotions.append(promotion)

class Shop:
    def __init__(self, name, category, area, rent_price):
        self.name = name
        self.category = category
        self.area = area
        self.rent_price = rent_price
        self.products = []
        self.sellers = []
        self.cash_registers = []
        self.return_policy_days = 14 if category in ["Бытовая техника", "Электроника"] else 0
    
    def add_product(self, product):
        self.products.append(product)
    
    def add_seller(self, seller):
        self.sellers.append(seller)
    
    def add_cash_register(self, cash_register):
        self.cash_registers.append(cash_register)

class Customer:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info
        self.purchases = []
        self.balance = 0
        self.questions = []
    
    def add_funds(self, amount):
        self.balance += amount
    
    def ask_question(self, seller, question):
        self.questions.append({
            'seller': seller.name,
            'question': question,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        })
        return seller.answer_question(question)

class Seller:
    def __init__(self, name, shop, position):
        self.name = name
        self.shop = shop
        self.position = position
        self.rating = 0
        self.answered_questions = []
    
    def answer_question(self, question):
        answers = {
            "цена": "Цена указана на ценнике.",
            "характеристики": "Полные характеристики вы можете найти в описании товара.",
            "наличие": "Да, товар есть в наличии.",
            "гарантия": "Гарантия 1 год на всю технику.",
            "возврат": f"Возврат возможен в течение {self.shop.return_policy_days} дней."
        }
        
        answer = answers.get(question.lower(), 
                   "Я помогу вам с этим вопросом. Давайте подойдем к товару.")
        self.answered_questions.append({
            'question': question,
            'answer': answer,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        })
        return answer
    
    def process_return(self, customer, product, purchase_date):
        if self.shop.return_policy_days == 0:
            return False, "В этом магазине возврат товаров не предусмотрен"
        
        days_passed = (time.time() - time.mktime(time.strptime(purchase_date, "%Y-%m-%d %H:%M:%S"))) / (24 * 3600)
        
        if days_passed > self.shop.return_policy_days:
            return False, f"Срок возврата ({self.shop.return_policy_days} дней) истек"
        
        return True, f"Возврат товара {product.name} оформлен. Деньги будут возвращены на ваш счет."

class Product:
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.specifications = {}
    
    def add_specification(self, key, value):
        self.specifications[key] = value

class CashRegister:
    def __init__(self, shop, number):
        self.shop = shop
        self.number = number
        self.balance = 0
    
    def process_payment(self, amount):
        self.balance += amount
        return True

class Promotion:
    def __init__(self, name, description, discount):
        self.name = name
        self.description = description
        self.discount = discount

class Gallery:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.shops = []
    
    def add_shop(self, shop):
        self.shops.append(shop)