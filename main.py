import math *
import unittest

class Binary16:

    PRECISION = 16
    N_EXPONENTE = 5
    SESGO = 2**(Binary16.N_EXPONENTE-1) - 1
    def __init__(self, d):
        self.d = d
        self.bits = Binary16.dec_to_bin(self.d)

    def __mul__(self, other): #faltan todos los casos con problemas: 
        a = bin_to_dec(self.bits) 
        b = bin_to_dec(other.bits)
        producto = (a * b)
        return Binary16(dec_to_bin(producto))

    def __divmod__(self, other):
        a = bin_to_dec(self.bits)
        b = bin_to_dec(other.bits)
        cociente = a/b
        return Binary16(dec_to_bin(cociente))

    def __eq__(self, other):
        if(self.d==other.d):
            vf1 = True
            print("Los números son iguales") #se supone que tiene q hacer esto la función?
            else:
                vf1 = False
                print("Los números son distintos")
        return vf1

    def __ne__(self, other):
        if(self.d!=other.d):
            vf2 = True
            print("Los números son distintos")
            else:
                vf2 = False
                print("Los números son iguales")
        return vf2
        

    @staticmethod
    def dec_to_bin(numero):
        """
        Con un staticmethod no hace falta inicializar la clase para invocarla
        Simplemente basta con hacer Binary16.bin_to_dec(numero)
        Otra opcion es no utilizar staticmethod y en vez de numero pasar self, y reemplzar
        cada aparicion de numero por self.d
        :param numero:
        :return:
        """
        bits=[0]*Binary16.PRECISION
        mantisa=0
        signo=1
        numero=math.copysign(signo,d)
        if numero<0 :
            bits[0]=1
            d*=-1
        if d>6.55e4 : #marcamos el limite para infinito
            for i in range(1,6):
                bits[i]=1
        elif d<6.103e-5: #marcamos el limite para subnormal
            mantisa=d/2**(1-sesgo)
        else: #numeros normales
            pot=-14
            while d//2**pot>2:
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
        n=15
        if (mantisa>0.5):
            while (n>=1):
                if bits[n]==1:
                    bits[n]=0
                else:
                    bits[n]=1
                    break
                n-=1
        if(str(d)=="nan"):
          bits=[1]*16
        return bits
                
                
    def bin_to_dec(bits):
      if 0 in bits[1:6]:
        I=False
        N=False
      elif 1 in bits[6:16]:
        N=True
        I=False
        d=float("Nan")
      else:
        N=False
        I=True
        d=float("Inf")
      if not (N or I):
        if 1 in bits[1:6]:
          m=1.0
          e=0
          for j in range(1,6):
            e+=bits[j]*(2**(j-1))
        else:
          m=0.0
          e=1
        l=-1
        for i in range(6,16):
          m+=bits[i]*(2**l)
          l-=1
        d=m*2**(e-Binary16.SESGO)
      d*=(-1)**bits[0]
      return d

class Test(unittest.TestCase):

    def __init__(self):
        super() #what is this

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
