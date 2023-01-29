from src.main import phone_validation


def test_plus():
    assert phone_validation('+7(999)-999-99-99')

def test_no_plus():
    assert phone_validation('89999999999')


