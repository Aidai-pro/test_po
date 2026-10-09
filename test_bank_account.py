import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Метод вызывается перед каждым тестом."""
        self.acc1 = BankAccount("Алексей", "ACC123")
        self.acc2 = BankAccount("Мария", "ACC456")

    def test_initial_state(self):
        """Проверка начального состояния счёта."""
        self.assertEqual(self.acc1.owner, "Алексей")
        self.assertEqual(self.acc1.account_number, "ACC123")
        self.assertEqual(self.acc1.get_balance(), 0.0)
        self.assertTrue(self.acc1.is_empty())

    def test_deposit_success(self):
        """Успешное пополнение счёта."""
        self.acc1.deposit(100.0)
        self.assertEqual(self.acc1.get_balance(), 100.0)
        self.assertFalse(self.acc1.is_empty())

    def test_deposit_invalid_amount(self):
        """Пополнение на отрицательную или нулевую сумму должно вызывать ошибку."""
        with self.assertRaises(ValueError):
            self.acc1.deposit(-50.0)
        with self.assertRaises(ValueError):
            self.acc1.deposit(0.0)

    def test_withdraw_success(self):
        """Успешное снятие средств."""
        self.acc1.deposit(200.0)
        self.acc1.withdraw(50.0)
        self.assertEqual(self.acc1.get_balance(), 150.0)

    def test_withdraw_insufficient_funds(self):
        """Снятие суммы, превышающей баланс."""
        self.acc1.deposit(50.0)
        with self.assertRaises(ValueError):
            self.acc1.withdraw(100.0)
        self.assertEqual(self.acc1.get_balance(), 50.0)  # Баланс не изменился

    def test_withdraw_invalid_amount(self):
        """Снятие отрицательной суммы."""
        with self.assertRaises(ValueError):
            self.acc1.withdraw(-10.0)

    def test_transfer_success(self):
        """Успешный перевод денег между счетами."""
        self.acc1.deposit(300.0)
        self.acc1.transfer(self.acc2, 100.0)

        self.assertEqual(self.acc1.get_balance(), 200.0)
        self.assertEqual(self.acc2.get_balance(), 100.0)

    def test_transfer_failed_insufficient_funds(self):
        """Неудачный перевод: недостаточно средств."""
        self.acc1.deposit(50.0)
        with self.assertRaises(ValueError):
            self.acc1.transfer(self.acc2, 100.0)

        # Состояние обоих счетов не должно измениться
        self.assertEqual(self.acc1.get_balance(), 50.0)
        self.assertEqual(self.acc2.get_balance(), 0.0)


if __name__ == '__main__':
    unittest.main()