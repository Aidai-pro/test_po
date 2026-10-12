import pytest
from student import get_result

# 1. Проверка правильных ответов и граничных значений
@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        # Границы результата "Отлично"
        (90, 80, "Отлично"),
        (100, 100, "Отлично"),
        # Спуск рейтинга из-за низкой посещаемости
        (95, 79, "Хорошо"),
        (90, 60, "Зачёт"),
        (90, 59, "Незачёт"),
        # Границы результата "Хорошо"
        (70, 70, "Хорошо"),
        (89, 79, "Хорошо"),
        # Границы результата "Зачёт"
        (50, 60, "Зачёт"),
        (69, 69, "Зачёт"),
        # Границы результата "Незачёт"
        (49, 100, "Незачёт"),
        (100, 59, "Незачёт"),
        (0, 0, "Незачёт"),
        # Выход за допустимые пределы (0–100)
        (-1, 80, "Некорректный балл"),
        (101, 80, "Некорректный балл"),
        (80, -1, "Некорректная посещаемость"),
        (80, 101, "Некорректная посещаемость"),
    ],
)
def test_get_result_valid_and_boundaries(score, attendance, expected):
    assert get_result(score, attendance) == expected


# 2. Проверка ошибок типов для score через pytest.raises()
@pytest.mark.parametrize(
    "invalid_score, attendance",
    [
        ("90", 80),
        (None, 80),
        ([90], 80),
    ],
)
def test_score_type_error(invalid_score, attendance):
    with pytest.raises(TypeError, match="Баллы должны быть числом"):
        get_result(invalid_score, attendance)


# 3. Проверка ошибок типов для attendance через pytest.raises()
@pytest.mark.parametrize(
    "score, invalid_attendance",
    [
        (90, "80"),
        (90, None),
        (90, [80]),
    ],
)
def test_attendance_type_error(score, invalid_attendance):
    with pytest.raises(TypeError, match="Посещаемость должна быть числом"):
        get_result(score, invalid_attendance)