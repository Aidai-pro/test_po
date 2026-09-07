import unittest
from game_logic import NumberGame

class TestNumberGame(unittest.TestCase):

    def test_correct_guess(self):
        """Проверяем, что игра отвечает 'УГАДАЛ', если число совпало."""
        # Создаем игру и фиксируем секретное число (например, 50)
        game = NumberGame(secret_number=50, max_attempts=10)
        
        result = game.make_move(50)
        
        # Проверяем равенство значений
        self.assertEqual(result, "УГАДАЛ")
        self.assertTrue(game.is_game_over)

    def test_guess_smaller_number(self):
        """Проверяем, что игра подсказывает 'БОЛЬШЕ', если ввели слишком маленькое число."""
        game = NumberGame(secret_number=50, max_attempts=10)
        
        result = game.make_move(20)
        
        self.assertEqual(result, "БОЛЬШЕ")
        self.assertFalse(game.is_game_over)

    def test_guess_larger_number(self):
        """Проверяем, что игра подсказывает 'МЕНЬШЕ', если ввели слишком большое число."""
        game = NumberGame(secret_number=50, max_attempts=10)
        
        result = game.make_move(80)
        
        self.assertEqual(result, "МЕНЬШЕ")
        self.assertFalse(game.is_game_over)

    def test_game_over_after_10_attempts(self):
        """Проверяем, что игра завершается ровно после 10 неверных попыток."""
        game = NumberGame(secret_number=50, max_attempts=10)
        
        # Делаем 9 неверных ходов
        for _ in range(9):
            game.make_move(1)
            
        self.assertFalse(game.is_game_over)  # На 9 ходу игра еще идет

        # Делаем 10-й неверный ход
        result = game.make_move(1)
        
        self.assertEqual(result, "ИГРА ОКОНЧЕНА")
        self.assertTrue(game.is_game_over)  # На 10 ходу игра закончилась

# Эта строчка позволяет запустить тесты напрямую из файла
if __name__ == "__main__":
    unittest.main()