class BankAccount:
    def __init__(self, owner: str, account_number: str):
        self.owner = owner
        self.account_number = account_number
        self.balance = 0.0

    def deposit(self, amount: float) -> None:
        """Пополнение счёта."""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Снятие средств со счёта."""
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля.")
        if amount > self.balance:
            raise ValueError("Недостаточно средств на счете.")
        self.balance -= amount

    def transfer(self, target_account: 'BankAccount', amount: float) -> None:
        """Перевод средств на другой счёт."""
        if not isinstance(target_account, BankAccount):
            raise TypeError("Получатель должен быть объектом BankAccount.")
        
        # Запомним баланс на случай ошибки, хотя сперва валидируем
        self.withdraw(amount)
        target_account.balance += amount

    def get_balance(self) -> float:
        """Получение текущего баланса."""
        return self.balance

    def is_empty(self) -> bool:
        """Проверка, является ли счёт пустым."""
        return self.balance == 0.0