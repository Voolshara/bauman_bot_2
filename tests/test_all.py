from src.main import phone_validation, ready_validation


def test_plus():
    assert phone_validation('+7(999)-999-99-99')

def test_no_plus():
    assert phone_validation('89999999999')

def test_ready_he():
    assert ready_validation("Готов\n08.08.2022")

def test_ready_she():
    assert ready_validation("Готова\n12.05.1999")