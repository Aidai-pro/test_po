import flet as ft
from game_logic import NumberGame

def main(page: ft.Page):
    page.title = "Игра «Угадай число»"
    page.window.width = 450
    page.window.height = 450
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    game = NumberGame()

    title_label = ft.Text("Угадай число от 1 до 100", size=20, weight=ft.FontWeight.BOLD)
    attempts_label = ft.Text(f"Осталось попыток: {game.attempts_left}", size=16)
    result_label = ft.Text("Введите число и нажмите 'Проверить'", size=16, color="blue")
    
    input_field = ft.TextField(hint_text="Число...", width=150, text_align=ft.TextAlign.CENTER)

    def check_guess(e):
        if not input_field.value or not input_field.value.isdigit():
            result_label.value = "Введите корректное число!"
            result_label.color = "orange"
            page.update()
            return

        guess = int(input_field.value)
        result = game.make_move(guess)
        input_field.value = ""

        attempts_label.value = f"Осталось попыток: {game.attempts_left}"

        if result == "УГАДАЛ":
            result_label.value = f"Поздравляем! Вы угадали число {game.secret_number}!"
            result_label.color = "green"
            btn_submit.disabled = True
        elif result == "ИГРА ОКОНЧЕНА":
            result_label.value = f"Игра окончена! Загаданное число: {game.secret_number}"
            result_label.color = "red"
            btn_submit.disabled = True
        elif result == "БОЛЬШЕ":
            result_label.value = "Загаданное число БОЛЬШЕ ⬆️"
            result_label.color = "blue"
        elif result == "МЕНЬШЕ":
            result_label.value = "Загаданное число МЕНЬШЕ ⬇️"
            result_label.color = "blue"

        page.update()

    def restart_game(e):
        nonlocal game
        game = NumberGame()
        attempts_label.value = f"Осталось попыток: {game.attempts_left}"
        result_label.value = "Новая игра началась! Введите число."
        result_label.color = "blue"
        btn_submit.disabled = False
        input_field.value = ""
        page.update()

    btn_submit = ft.Button("Проверить", on_click=check_guess)
    btn_restart = ft.Button("Начать заново", on_click=restart_game)

    page.add(
        title_label,
        attempts_label,
        input_field,
        ft.Row([btn_submit, btn_restart], alignment=ft.MainAxisAlignment.CENTER),
        result_label
    )

if __name__ == "__main__":
    ft.run(main)