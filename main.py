import math
import unittest


class Binary16:
    PRECISION = 16
    BIT_SIGNO = 1
    BIT_EXPONENTE = 5
    BIT_MANTISA = 10
    SESGO = 2 ** (BIT_EXPONENTE - 1) - 1

    def __init__(self, d):
        self.bits = Binary16.dec_to_bin(d)
        self.d = Binary16.bin_to_dec(self.bits)

    def __mul__(self, other):
        a = self.d
        b = other.d
        producto = (a * b)
        return Binary16(producto)

    def __truediv__(self, other):
        a = self.d
        b = other.d
        if (b == 0):
            if (a == float("inf")):
                cociente = float("inf")
            elif (a == float("-inf")):
                cociente = float("-inf")
            else:
                cociente = float("nan")
        elif (b == -0):
            if (a == float("inf")):
                cociente = float("-inf")
            elif (a == float("-inf")):
                cociente = float("inf")
            else:
                cociente = float("nan")
        else:
            cociente = a / b
        return Binary16(cociente)

    def __eq__(self, other):
        return self.bits == other.bits

    def __ne__(self, other):
        return self.bits != other.bits

    @staticmethod
    def dec_to_bin(d):
        bits = [0] * Binary16.PRECISION
        mantisa = 0
        signo = 1
        numero = math.copysign(signo, d)
        if numero < 0:
            bits[0] = 1
            d *= -1
        if d > 6.55e4:  # limite infinito
            for i in range(1, Binary16.BIT_EXPONENTE + 1):
                bits[i] = 1
        elif d < 6.103e-5:  # limite subnormal
            mantisa = d / 2 ** (1 - Binary16.SESGO)
        else:  # numeros normales
            pot = -14
            while d / 2 ** pot > 2:
                pot += 1
            exp = Binary16.SESGO + pot
            exponente = exp
            l = 4
            while exp >= 0 and l >= 0:
                for m in range(1, Binary16.BIT_EXPONENTE + 1):
                    if (exp / (2 ** l)) >= 1:
                        bits[m] = 1
                        exp -= 2 ** l
                    else:
                        bits[m] = 0
                    l -= 1
            mantisa = (d / (2 ** (exponente - Binary16.SESGO))) - 1
        if (d < 6.55e4):
            for j in range(Binary16.BIT_EXPONENTE + 1, Binary16.BIT_EXPONENTE + Binary16.BIT_MANTISA + 1):
                mantisa *= 2
                if (mantisa >= 1):
                    bits[j] = 1
                    mantisa -= 1
                else:
                    bits[j] = 0
            n = 15
            if (mantisa > 0.5):
                while (n >= 1):
                    if bits[n] == 1:
                        bits[n] = 0
                    else:
                        bits[n] = 1
                        break
                    n -= 1
        if (str(d) == "nan"):
            bits = [1] * 16
        return bits

    def bin_to_dec(bits):
        if 0 in bits[1:(Binary16.BIT_EXPONENTE + 1)]:
            I = False
            N = False
        elif 1 in bits[(Binary16.BIT_EXPONENTE + 1): (Binary16.BIT_EXPONENTE + Binary16.BIT_MANTISA + 1)]:
            N = True
            I = False
            d = float("Nan")
        else:
            N = False
            I = True
            d = float("Inf")
        if not (N or I):
            if 1 in bits[1:(Binary16.BIT_EXPONENTE + 1)]:
                m = 1.0
                e = 0
                for j in range(1, Binary16.BIT_EXPONENTE + 1):
                    e += bits[j] * (2 ** (Binary16.BIT_EXPONENTE - j))
            else:
                m = 0.0
                e = 1
            l = -1
            for i in range(Binary16.BIT_EXPONENTE + 1, Binary16.BIT_EXPONENTE + Binary16.BIT_MANTISA + 1):
                m += bits[i] * (2 ** l)
                l -= 1
            d = m * 2 ** (e - Binary16.SESGO)
        d *= (-1) ** bits[0]
        return d


class Test(unittest.TestCase):

    def test_cero(self):
        d = Binary16(0)
        expected = [0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(d.d, expected[0])
        self.assertEqual(d.bits, expected[1])

    def test_infinito(self):
        d = Binary16(99999999999)
        expected = [float("inf"), [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(d.d, expected[0])
        self.assertEqual(d.bits, expected[1])

    def test_minus_infinito(self):
        d = Binary16(-999999999999)
        expected = [float("-inf"), [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(d.d, expected[0])
        self.assertEqual(d.bits, expected[1])

    def test_multiplicacion(self):
        a = Binary16(1)
        b = Binary16(2)
        res = a * b
        self.assertEqual(res.d, 2)

    def test_division(self):
        a = Binary16(1)
        b = Binary16(2)
        res = a / b
        self.assertEqual(res.d, 0.5)

    def test_igualdad(self):
        a = Binary16(1)
        b = Binary16(1)
        self.assertTrue(a == b)

    def test_desigualdad(self):
        a = Binary16(3)
        b = Binary16(4)
        self.assertTrue(a != b)

    def test_limite_precision(self):
        a = Binary16(2.3457)
        b = Binary16(2.3463)
        self.assertEqual(a, b)

    def test_epsilon_de_maquina(self):
        epsilon = 2 ** (-Binary16.BIT_MANTISA)
        a = 2.3457
        b = Binary16(a)
        self.assertTrue(abs((b.d - a) / a) <= (epsilon / 2))

    def test_infinito_x_cero(self):
        a = Binary16(9999999999999)
        b = Binary16(0)
        res = a * b
        self.assertEqual(res.bits, Binary16(float("nan")).bits)

    def test_infinito_x_infinito(self):
        a = Binary16(9999999999999)
        b = Binary16(9999999999999)
        res = a * b
        self.assertEqual = (res.d, float("inf"))

    def test_0_sobre_0(self):
        a = Binary16(0)
        b = Binary16(0)
        res = a / b
        self.assertEqual(res.bits, Binary16(float("nan")).bits)

    def test_inf_sobre_inf(self):
        a = Binary16(9999999999999)
        b = Binary16(9999999999999)
        res = a / b
        self.assertEqual(res.bits, Binary16(float("nan")).bits)

    def test_infinito_sobre_cero(self):
        a = Binary16(9999999999999)
        b = Binary16(0)
        res = a / b
        self.assertEqual(res.bits, Binary16(float("inf")).bits)

    def test_cero_sobre_infinito(self):
        a = Binary16(0)
        b = Binary16(9999999999999)
        res = a / b
        self.assertEqual(res.d, 0)

    def test_igualdad_ceros(self):
        a = Binary16(0.0)
        b = Binary16(-0.0)
        self.assertFalse(a == b)

    def test_desigualdad_nan(self):
        a = Binary16(float("nan"))
        b = Binary16(float("nan"))
        self.assertFalse(a != b)


def test():
    unittest.main()


if __name__ == '__main__':
    test()



