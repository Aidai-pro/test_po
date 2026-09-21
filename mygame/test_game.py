import unittest
from game_logic import NumberGame

class TestNumberGame(unittest.TestCase):

    def test_correct_guess(self):
        """Проверяем, что игра отвечает 'УГАДАЛ', если число совпало."""
        game = NumberGame(secret_number=50, max_attempts=10)
        result = game.make_move(50)
        self.assertEqual(result, "УГАДАЛ")
        self.assertTrue(game.is_game_over)

    def test_guess_smaller_number(self):
        """Проверяем подсказку 'БОЛЬШЕ'."""
        game = NumberGame(secret_number=50, max_attempts=10)
        result = game.make_move(20)
        self.assertEqual(result, "БОЛЬШЕ")
        self.assertFalse(game.is_game_over)

    def test_guess_larger_number(self):
        """Проверяем подсказку 'МЕНЬШЕ'."""
        game = NumberGame(secret_number=50, max_attempts=10)
        result = game.make_move(80)
        self.assertEqual(result, "МЕНЬШЕ")
        self.assertFalse(game.is_game_over)

    def test_game_over_after_10_attempts(self):
        """Проверяем завершение игры после 10 попыток."""
        game = NumberGame(secret_number=50, max_attempts=10)
        for _ in range(9):
            game.make_move(1)
        self.assertFalse(game.is_game_over)

        result = game.make_move(1)
        self.assertEqual(result, "ИГРА ОКОНЧЕНА")
        self.assertTrue(game.is_game_over)

if __name__ == "__main__":
    unittest.main()