from unittest import TestCase


# def add(x, y):
#     return x + y
#
#
# class DummyTest(TestCase):
#     def test_one_plus_one_is_two(self):
#         assert add(1, 1) == 2

# def palindrome(text: str) -> bool:
#     return text[::-1].lower() == text.lower()
#
#
# class PalyndromesTestCase(TestCase):
#     def test_palyndrom(self):
#         assert palindrome('ana')
#
#     def test_palyndrom_other(self):
#         assert not palindrome('peter')

def bouncyExercise(porcentaje: float) -> int:
    def bouncy(num):
        n_incr = False
        n_decr = False
        num_der = num % 10
        num = num // 10

        while num > 0:
            num_izq = num % 10
            if num_izq < num_der:
                n_incr = True
            elif num_izq > num_der:
                n_decr = True
            num_der = num_izq
            num = num // 10
            if n_incr and n_decr:
                return True
        return False

    if porcentaje > 0.99:
        porcentaje = 0.99
    elif porcentaje < 0:
        porcentaje = 0.001
    cont = 0
    i = 99
    while cont < porcentaje * i:
        i = i + 1
        if bouncy(i):
            cont = cont + 1
    return i


class BouncyTestCase(TestCase):
    def test_bouncy_that_percentage_does_not_exceed_99_(self):
        assert bouncyExercise(3) == 1587000

    def test_bouncy_that_percentage_is_not_less_than_0_(self):
        assert bouncyExercise(-1) == 101

    # def test_bouncy_that_percentage_and_num_is_not_string_(self):
    #     assert bouncyExercise('sds', 'sds') == 101
