from discount_service import DiscountModule, InvalidCardError

passed = failed = 0


def check(name, actual, expected):
    global passed, failed
    ok = actual == expected
    passed += ok
    failed += not ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {actual!r} (ожидалось {expected!r})")


def expect_invalid(name, value):
    global passed, failed
    try:
        res = dm.apply_student_discount(value)
        failed += 1
        print(f"[FAIL] {name}: нет ошибки, вернулось {res!r}")
    except InvalidCardError as e:
        passed += 1
        print(f"[PASS] {name}: {e}")
    except Exception as e:  
        failed += 1
        print(f"[FAIL] {name}: неожиданное {type(e).__name__}: {e}")


dm = DiscountModule()

print("--- Позитивные сценарии ---")
check("Тест 1: действующий билет", dm.apply_student_discount("12345678"), 15.0)
check("Тест 2: другой действующий билет", dm.apply_student_discount("20240001"), 15.0)
check("Тест 3: билет с ведущими нулями", dm.apply_student_discount("00123456"), 15.0)
check("Тест 4: билет не найден в базе", dm.apply_student_discount("99999999"), 0.0)

print("--- Негативные сценарии (стресс-тест) ---")
expect_invalid("Тест 5: текст вместо цифр 'ABC-123'", "ABC-123")
expect_invalid("Тест 6: пустая строка", "")
expect_invalid("Тест 7: None", None)
expect_invalid("Тест 8: число вместо строки", 12345678)
expect_invalid("Тест 9: пробелы по краям", " 12345678 ")
expect_invalid("Тест 10: юникод-цифры", "１２３４５６７８")
expect_invalid("Тест 11: отрицательное число", "-1234567")
expect_invalid("Тест 12: слишком короткий", "1234")
expect_invalid("Тест 13: слишком длинная строка (5000 симв.)", "9" * 5000)
expect_invalid("Тест 14: подчёркивания", "1_234_567")

print(f"\nИтого: {passed} PASS, {failed} FAIL")
raise SystemExit(1 if failed else 0)
