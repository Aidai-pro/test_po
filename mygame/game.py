import random

def play_game():
    secret_number = random.randint(1, 100)
    max_attempts = 10
    
    print("Я загадал число от 1 до 100. У вас 10 попыток!")
    
    for attempt in range(1, max_attempts + 1):
        guess = int(input(f"Ход {attempt}/10. Введите число: "))
        
        if guess == secret_number:
            print(f"Поздравляем! Вы угадали число за {attempt} ходов.")
            return True
        elif guess < secret_number:
            print("Загаданное число БОЛЬШЕ.")
        else:
            print("Загаданное число МЕНЬШЕ.")
            
    print(f"Игра окончена! Вы исчерпали 10 ходов. Загаданное число было: {secret_number}")
    return False

if __name__ == "__main__":
    play_game()