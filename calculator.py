"""
Консольный калькулятор с историей операций.

Итоговый проект (Кейс 1). Поддерживает сложение, вычитание, умножение и
деление двух чисел (целых и дробных), сохраняет историю вычислений в CSV-файл
и позволяет её просматривать. Обрабатывает ошибки ввода и деление на ноль.

Функции get_number() и divide() сгенерированы с помощью ИИ-инструмента —
см. ai_prompts.md для промптов и пояснений.
"""

import csv
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.csv")


# ---------------------------------------------------------------------------
# Математические операции
# ---------------------------------------------------------------------------

def add(a: float, b: float) -> float:
    """Возвращает сумму a и b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Возвращает разность a и b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Возвращает произведение a и b."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Выполняет деление a на b.

    :param a: Делимое.
    :param b: Делитель.
    :raises ZeroDivisionError: если b равно нулю.
    :return: Результат деления a на b.
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль невозможно. Введите ненулевой делитель.")
    return a / b


# ---------------------------------------------------------------------------
# Ввод и валидация
# ---------------------------------------------------------------------------

def get_number(prompt: str) -> float:
    """
    Запрашивает у пользователя ввод числа и валидирует его.

    Поддерживает целые и дробные числа, а также дробные числа,
    записанные через запятую (например, "3,14"). Повторяет запрос
    ввода до тех пор, пока пользователь не введёт корректное число.

    :param prompt: Текст приглашения для ввода.
    :return: Введённое пользователем число в виде float.
    """
    while True:
        raw_value = input(prompt).strip()
        normalized_value = raw_value.replace(",", ".")
        try:
            return float(normalized_value)
        except ValueError:
            print(f'Ошибка: "{raw_value}" не является числом. Попробуйте снова (например: 3.14 или 7).')


# ---------------------------------------------------------------------------
# История операций
# ---------------------------------------------------------------------------

def ensure_history_file() -> None:
    """Создаёт CSV-файл истории с заголовком, если он ещё не существует."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["datetime", "operation", "operand_a", "operand_b", "result"])


def save_to_history(operation: str, a: float, b: float, result: float) -> None:
    """Добавляет одну запись об операции в CSV-файл истории."""
    ensure_history_file()
    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            operation,
            a,
            b,
            result,
        ])


def show_history() -> None:
    """Выводит содержимое истории операций в читаемом виде."""
    if not os.path.exists(HISTORY_FILE):
        print("\nИстория операций пока пуста.\n")
        return

    with open(HISTORY_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("\nИстория операций пока пуста.\n")
        return

    print("\n--- История операций ---")
    for row in rows:
        print(
            f"{row['datetime']} | {row['operand_a']} {row['operation']} {row['operand_b']} "
            f"= {row['result']}"
        )
    print("------------------------\n")


# ---------------------------------------------------------------------------
# Основной цикл программы
# ---------------------------------------------------------------------------

OPERATIONS = {
    "1": ("+", add),
    "2": ("-", subtract),
    "3": ("*", multiply),
    "4": ("/", divide),
}

MENU_TEXT = """
========== КОНСОЛЬНЫЙ КАЛЬКУЛЯТОР ==========
1. Сложение (+)
2. Вычитание (-)
3. Умножение (*)
4. Деление (/)
5. Показать историю операций
0. Выход
=============================================
"""


def run_calculation(operation_key: str) -> None:
    """Выполняет выбранную операцию: запрашивает операнды, считает результат,
    обрабатывает ошибки и сохраняет успешный результат в историю."""
    symbol, func = OPERATIONS[operation_key]

    a = get_number("Введите первое число: ")
    b = get_number("Введите второе число: ")

    try:
        result = func(a, b)
    except ZeroDivisionError as e:
        print(f"Ошибка: {e}")
        return

    print(f"Результат: {a} {symbol} {b} = {result}")
    save_to_history(symbol, a, b, result)


def main() -> None:
    """Главный цикл программы: показывает меню и обрабатывает выбор пользователя."""
    ensure_history_file()

    while True:
        print(MENU_TEXT)
        choice = input("Выберите пункт меню: ").strip()

        if choice == "0":
            print("Работа программы завершена.")
            break
        elif choice in OPERATIONS:
            run_calculation(choice)
        elif choice == "5":
            show_history()
        else:
            print("Ошибка: некорректный пункт меню. Введите число от 0 до 5.")


if __name__ == "__main__":
    main()
