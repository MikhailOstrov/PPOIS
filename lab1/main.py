from entities import *
from operations import *
from admin_interface import AdminInterface

def initialize_mall():
    mall = ShoppingMall("МегаVМолл", "ул. Центральная, 123")
    
    # Создаем галереи
    cosmetics_gallery = Gallery("Галерея косметики", 1)
    electronics_gallery = Gallery("Галерея Электроники", 2)
    food_gallery = Gallery("Галерея Еды", 3)
    mall.add_gallery(cosmetics_gallery)
    mall.add_gallery(electronics_gallery)
    mall.add_gallery(food_gallery)
    
    
    # Создаем и наполняем магазины
    electronics = Shop("ТехноМир", "Бытовая техника", 200, 80000)
    
    # Добавляем товары с характеристиками
    washing_machine = Product("Стиральная машина LG", 45000, 5, "Бытовая техника")
    washing_machine.add_specification("Количество оборотов", "1200 об/мин")
    washing_machine.add_specification("Режимы стирки", "Хлопок, Синтетика, Деликатная")
    washing_machine.add_specification("Гарантия", "2 года")
    
    fridge = Product("Холодильник Samsung", 60000, 3, "Бытовая техника")
    fridge.add_specification("Объем", "300 л")
    fridge.add_specification("Класс энергопотребления", "A++")
    
    electronics.add_product(washing_machine)
    electronics.add_product(fridge)
    electronics.add_seller(Seller("Иванова Мария", electronics, "Консультант"))
    
    grocery = Shop("Продуктовый рай", "Продукты", 150, 50000)
    milk = Product("Молоко Простоквашино", 80, 100, "Молочные продукты")
    grocery.add_product(milk)
    grocery.add_seller(Seller("Петров Иван", grocery, "Кассир"))
    
    # Создаем магазины косметики
    perfume_shop = Shop("Ароматы мира", "Парфюмерия", 120, 60000)
    makeup_shop = Shop("Красота", "Декоративная косметика", 100, 45000)
    
    # Добавляем товары в парфюмерный магазин
    perfume1 = Product("Chanel №5", 8500, 15, "Парфюмерия")
    perfume1.add_specification("Объем", "50 мл")
    perfume1.add_specification("Тип аромата", "Цветочный")
    perfume1.add_specification("Страна производства", "Франция")
    
    perfume2 = Product("Dior Sauvage", 7500, 12, "Парфюмерия")
    perfume2.add_specification("Объем", "60 мл")
    perfume2.add_specification("Тип аромата", "Древесный")
    perfume2.add_specification("Страна производства", "Франция")
    
    perfume_shop.add_product(perfume1)
    perfume_shop.add_product(perfume2)
    perfume_shop.add_seller(Seller("Смирнова Ольга", perfume_shop, "Парфюмер"))
    
    # Добавляем товары в магазин декоративной косметики
    lipstick = Product("Помада L'Oreal", 1200, 30, "Декоративная косметика")
    lipstick.add_specification("Цвет", "Красный")
    lipstick.add_specification("Тип", "Матовый")
    
    mascara = Product("Тушь Maybelline", 900, 25, "Декоративная косметика")
    mascara.add_specification("Эффект", "Увеличение объема")
    mascara.add_specification("Водостойкая", "Да")
    
    makeup_shop.add_product(lipstick)
    makeup_shop.add_product(mascara)
    makeup_shop.add_seller(Seller("Кузнецова Анна", makeup_shop, "Визажист"))
    
    # Добавляем магазины в галереи и ТЦ
    food_gallery.add_shop(grocery)
    electronics_gallery.add_shop(electronics)
    cosmetics_gallery.add_shop(perfume_shop)
    cosmetics_gallery.add_shop(makeup_shop)
    
    mall.add_shop(grocery)
    mall.add_shop(electronics)
    mall.add_shop(perfume_shop)
    mall.add_shop(makeup_shop)
    
    # Добавляем кассы
    electronics.add_cash_register(CashRegister(electronics, 1))
    grocery.add_cash_register(CashRegister(grocery, 1))
    perfume_shop.add_cash_register(CashRegister(perfume_shop, 1))
    makeup_shop.add_cash_register(CashRegister(makeup_shop, 1))
    
    # Добавляем акции
    mall.add_promotion(Promotion(
        "Летняя распродажа", 
        "Скидки на всю технику", 
        15
    ))
    mall.add_promotion(Promotion(
        "Утренние скидки", 
        "Скидки на продукты до 11 утра", 
        10
    ))
    mall.add_promotion(Promotion(
        "Красота без границ", 
        "Скидки на всю косметику 20%", 
        20
    ))
    mall.add_promotion(Promotion(
        "Парфюмерный день", 
        "Скидки на парфюмерию 25% по пятницам", 
        25
    ))
    
    return mall

if __name__ == "__main__":
    mall = initialize_mall()
    
    try:
        interface = AdminInterface(mall)
        interface.run()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Работа программы завершена")