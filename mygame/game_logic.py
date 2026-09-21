import random

class NumberGame:
    def __init__(self, secret_number=None, max_attempts=10):
        # Если секретное число не передано, генерируем случайное от 1 до 100
        if secret_number is None:
            self.secret_number = random.randint(1, 100)
        else:
            self.secret_number = secret_number
            
        self.attempts_left = max_attempts
        self.is_game_over = False

    def make_move(self, guess):
        """
        Делает один ход. 
        Возвращает текстовую подсказку: 'БОЛЬШЕ', 'МЕНЬШЕ', 'УГАДАЛ' или 'ИГРА ОКОНЧЕНА'.
        """
        if self.is_game_over:
            return "ИГРА ОКОНЧЕНА"

        self.attempts_left -= 1

        if guess == self.secret_number:
            self.is_game_over = True
            return "УГАДАЛ"
        
        # Если попытки закончились, завершаем игру
        if self.attempts_left == 0:
            self.is_game_over = True
            return "ИГРА ОКОНЧЕНА"

        if guess < self.secret_number:
            return "БОЛЬШЕ"
        else:
            return "МЕНЬШЕ"