import numbers as num


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, num.Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other
    
    def neg_coefs(self):
        coefs = (-1*x for x in self.coefficients)
        return *coefs,

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            other_coef = other.neg_coefs()
            other_poly = Polynomial(other_coef)
            return self + other_poly
        elif isinstance(other, num.Number):
            other_num = -other
            return self + other_num
        else:
            return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, Polynomial):
            other_coef = other.neg_coefs()
            other_poly = Polynomial(other_coef)
            sub_poly = self + other_poly

        elif isinstance(other, num.Number):
            other_num = -other
            sub_poly = self + other_num
        sub_coefs = sub_poly.neg_coefs()
        return Polynomial(sub_coefs)
            
    
    def __mul__(self,other):
        if isinstance(other,Polynomial):
            s = list(self.coefficients)
            o = list(other.coefficients)
            res = [0]*(len(s)+len(o)-1)
            for o1,i1 in enumerate(s):
                for o2,i2 in enumerate(o):
                    res[o1+o2] += i1*i2
            return Polynomial(tuple(res))
        elif isinstance(other, num.Number):
            coefs = (other*x for x in self.coefficients)
            tup_coefs = *coefs,
            return Polynomial(tup_coefs)
        else:
            return NotImplemented
    
    def __rmul__(self,other):
        return self * other
    
    def __pow__(self, other):
       if not isinstance(other, num.Integral):
           raise AssertionError('Exponent can only be an integer!')
       elif other == 1:
           return self
       else:
           exp_poly = self
           for i in range(1,other):
               exp_poly = self * exp_poly
           return exp_poly

    def __call__(self,scalar):
        if not isinstance(scalar, num.Number):
           raise AssertionError('Function can only be evaluated for a real number.')
        else:
            value = 0
            list_coeff = list(self.coefficients)
            for i in list_coeff:
                idx = list_coeff.index(i)
                value +=  (scalar**idx)*i
            return value
        