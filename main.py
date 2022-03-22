import math *
import unittest

class Binary16:

    PRECISION = 16
    N_EXPONENTE = 5
    SESGO = 2**(Binary16.N_EXPONENTE) - 1
    def __init__(self, d):
        self.d = d
        self.bits = Binary16.bin_to_dec(self.d)

    def __mul__(self, other): #faltan todos los casos con problemas
        producto = (self.d * other.d)
        return Binary16(pasar_a_decimal(producto)) #dudas sobre a que se refiere esto

    def __divmod__(self, other):
        cociente = self.d/other.d
        return Binary16(pasar_a_decimal(cociente))

    def __eq__(self, other):
        if(self.d==other.d):
            print("Los números son iguales") #se supone que tiene q hacer esto la función?
            else:
                print("Los números son distintos")
        return

    def __ne__(self, other):
        if(self.d!=other.d):
            print("Los números son distintos")
            else:
                print("Los números son iguales")
        return
        

    @staticmethod
    def bin_to_dec(numero): #esto tiene un tab de mas?
        """
        Con un staticmethod no hace falta inicializar la clase para invocarlo
        Simplemente basta con hacer Binary16.bin_to_dec(numero)
        Otra opcion es no utilizar staticmethod y en vez de numero pasar self, y reemplzar
        cada aparicion de numero por self.d
        :param numero:
        :return:
        """
        bits=[0]*Binary16.PRECISION
        mantisa=0
        if numero<0 :
            bits[0]=1
            numero*=-1
        if numero>6.55e4 : #marcamos el limite para infinito
            for i in range(1,6):
                bits[i]=1
        elif numero<6.103e-5: #marcamos el limite para subnormal
            mantisa=numero/2**(1-sesgo)
        else: #numeros normales
            pot=-14
            while numero//2**pot>2:
              pot+=1
            exp=sesgo+pot
            exponente=exp
            l=4
            while exp>=0 and l>=0:
              for m in range (1,6):
                if (exp/(2**l))>=1:
                  bits [m]=1
                  exp-=2**l
                else:
                  bits[m]=0
                l-=1
            mantisa=(d/(2**(exponente-sesgo)))-1
        for j in range(6,16) :
            mantisa*=2
            if (mantisa>=1):
                bits[j]=1
                mantisa-=1
            else:
                bits[j]=0


class Test(unittest.TestCase):

    def __init__(self):
        super()

    def test_cero(self):
        """
        Aca testeo una clase que es bonita
        """
        d = Binary16(0)

        self.assertEqual(d.d, 0)
        self.asserEqual(d.bits, [0,0,0,0,0,0... etc]) #en esto hay q poner todo exacto

    def test_infinito(self):
        d = Binary16(99999999999)

        self.assertEqual(d.d, '+inf')
        self.assertEqual(d.d, [111111111111])

    def test_minus_infinito(self):
        d = Binary16(99999999999)

        expected = [-inf , [1231231412414]]
        self.assertEqual(d.d, expected[0])
        self.assertEqual(d.d, expected[1]))

    def test_multiplication(self):
        d = Binary16(1)
        c = Binary16(2)

        res = c*d

        self.assertEqual(res.d, 2)

    def test_mas_cosas(self):
        pass


def test():
    unittest.main()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
