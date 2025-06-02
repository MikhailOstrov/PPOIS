import unittest
import time
from entities import *
from operations import *
from controller import ShoppingMallController

class TestShoppingMall(unittest.TestCase):
    def setUp(self):
        self.mall = ShoppingMall("Тестовый Молл", "ул. Тестовая, 1")
        self.shop = Shop("Тестовый Магазин", "Бытовая техника", 100, 30000)
        self.mall.add_shop(self.shop)
        self.product = Product("Тестовый Товар", 100, 10, "Тесты")
        self.shop.add_product(self.product)
        self.customer = Customer("Тестовый Покупатель", "test@example.com")
        self.customer.add_funds(1000)
        self.seller = Seller("Тестовый Продавец", self.shop, "Консультант")
        self.shop.add_seller(self.seller)
        self.cash = CashRegister(self.shop, 1)
        self.shop.add_cash_register(self.cash)
        self.controller = ShoppingMallController(self.mall)

    def test_product_search(self):
        results = self.controller.search_products("name", "тестовый")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].name, "Тестовый Товар")

    def test_purchase(self):
        success, message, _ = self.controller.make_purchase("Тестовый Товар", 2, "Тестовый Продавец")
        self.assertTrue(success)
        self.assertEqual(self.product.quantity, 8)
        self.assertEqual(self.controller.current_customer.balance, 99800)
        self.assertEqual(len(self.controller.current_customer.purchases), 1)

    def test_question_answer(self):
        answer = self.customer.ask_question(self.seller, "цена")
        self.assertIn("Цена указана на ценнике", answer)
        self.assertEqual(len(self.customer.questions), 1)
        self.assertEqual(len(self.seller.answered_questions), 1)

    def test_product_return(self):
        self.controller.make_purchase("Тестовый Товар", 1, "Тестовый Продавец")
        success, message = self.controller.process_return(0)
        self.assertTrue(success)
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.controller.current_customer.balance, 100000)

    def test_return_policy(self):
        non_return_shop = Shop("Продукты", "Продукты", 50, 20000)
        self.assertEqual(non_return_shop.return_policy_days, 0)
        self.assertEqual(self.shop.return_policy_days, 14)

    def test_product_specifications(self):
        tv = Product("Телевизор", 50000, 5, "Электроника")
        tv.add_specification("Диагональ", "55 дюймов")
        self.assertEqual(tv.specifications["Диагональ"], "55 дюймов")

if __name__ == "__main__":
    unittest.main()