#########################################################
# mpap
# Minimalistic Python port of ArbitraryPrecision
# Targeted for MicroPython on microcontrollers
# with a few tweaks 
# (c) 2019 Anirban Banerjee <anirbax@gmail.com>
#########################################################
# ArbitraryPrecision
# a simple, efficient arbitrary precision arithmetic library
# for python 3+
# 
# (c) 2018 Haipeng Lin <jimmie.lin@gmail.com>
#
# Originally written for Computational Physics Course
# HW-2, Peking University, School of Physics, Fall 2017
#
#########################################################
import math
MPAPERRORFLAG = ''
PRECISION = 50
class mpap ():
    # Supported maximum precision digits.
    Precision = PRECISION

    # Internal Representation of significant digits + sign.
    Mantissa = None

    # Internal Representation of (Integer) Exponent of 10,
    # e.g. 6.283012 = [Mantissa = 6283012, Exponent = 6]
    #      0.097215 = [Mantissa = 97215  , Exponent = -2]
    # This exponent IS the scientific notation exponent.
    # Contrary to intuition, Mantissa * 10eExponent is NOT this number it
    # To reconstruct this number, take the first number and insert "." divider in 0-1 pos
    # e.g. 9.7215e-2, this is the actual number.
    # This is implied in later calculations, beware!
    Exponent = 0

    #True is positive, False is negative
    Sign = 1

    ImagMantissa = 0 
    ImagExponent = 0

    # __init__
    # Initialization Function
    # If a non-integer float type is passed to Mantissa, then this number will be converted
    # to our internal representation.
    #
    # (!!) IF YOU PASS A INTEGER TO mantissa there are two possible behaviors.
    # Your int may be interpreted
    # as a literal integer (InternalAware = False) or interpreted as internal representation of significant
    # digits, so 142857 = 1.42857x10^0 = 1.42857.
    # By default, we assume you are NOT aware of the Internal structures. This keeps consistency with float support
    # for mantissa.

    # Set InternalAware = True to interpret as internal representation.
    
    # (!) Non-Integer Exponents passed to __init__ are currently unsupported.
    def __init__(self, Mantissa, Exponent = 0, Precision = PRECISION, InternalAware = False, \
        ImagMantissa = 0, ImagExponent = 0):

        #print ("Mantissa is ", Mantissa, "Exponent is ", Exponent)
        if(isinstance(Mantissa, mpap)):
            #print (" -- is already of type mpap!")
            self.Mantissa = Mantissa.Mantissa
            self.Exponent = Mantissa.Exponent
            return

        if type (Precision) != int:
            self.Mantissa = 0
            self.Exponent = 0
            MPAPERRORFLAG = "Illegal precision."
            return

        if Precision < 6:
            self.Precision = 6
        else:
            self.Precision = Precision

        #print (" float of mantissa is --", float(Mantissa))
        try:
            #catch inf in Mantissa and illegal format in Exponent
            if type(Mantissa) == float:
                #print ("--------------------------------FLOAT")
                if str(float(Mantissa)) == 'inf' or str(float(Mantissa)) == '-inf' or \
                    str(float(Exponent)) == 'inf' or str(float(Exponent)) == '-inf':
                    raise OverflowError
            Exponent = int(Exponent)
        except (ValueError, OverflowError):
            #print ("Raised error --")
            self.Mantissa = 0
            self.Exponent = 0
            MPAPERRORFLAG = "Illegal mantissa or exponent. \nHint: use strings to hold large numbers!"
            return

        if (type(Mantissa) == float or type(Mantissa) == str):
            #if (type(Mantissa) == str):
                #print ("STR")
                #print ("FLOAT or STR")
            # String rep of mantissa, useful for reuse (strings are immutable), also UnSigned variant
            strMan = str(Mantissa)
            #print ("strMan is ", strMan)
            strManUS = strMan.replace('-', '')
            # Extract all significant digits
            if('e' in strMan): # Oops, too small; have to expand notation
                # Something like 1e-07... significant digits are before e, then 
                # extract the second part and add it to exponent accumulator
                strManParts = strMan.split('e')
                try:
                    self.Mantissa = int(strManParts[0].replace('.', ''))
                    #print ("self.Mantissa is ", self.Mantissa)
                    Exponent += int(strManParts[1])
                except (ValueError, OverflowError):
                    self.Mantissa = 0
                    self.Exponent = 0
                    MPAPERRORFLAG = "Illegal mantissa or exponent."
                    return
                #print ("Exponent is ", Exponent)
            else:
                self.Mantissa = int(strMan.replace('.', ''))

            #print ("abs(float(Mantissa)) is ", abs(float(Mantissa)))
            #print ("abs is ", (abs(float(Mantissa)) < 1))
            # Count exponent for scientific notation
            
            #print ("find . is ", strManUS.find('.'))
            #print ("int part is ", int(strManUS[:strManUS.find('.')]))
            isFraction = (strManUS.find('.') > -1 and int(strManUS[:strManUS.find('.')]) == 0)
            #print ("isFraction is ", isFraction)
            if (abs(float(Mantissa)) < 1) or isFraction == True:
                #print ("LT 1: strManUS is ", strManUS)
                #-inf and +inf comparisons will be handled
                #by Python
                #print ("strMan is ", strMan)
                if(float(Mantissa) == 0) and self.Mantissa == 0:
                    #number is 0, .0, 0.0, 0. etc
                    self.Mantissa = 0
                    self.Exponent = 0
                    Exponent = 0
                else:
                    #number is a fraction
                    for i in range(len(strManUS)):
                        if(strManUS[i] == '.'):
                            continue
                        if(strManUS[i] != '0'):
                            break
                        Exponent = Exponent - 1
            else:
                #print ("GTE 1: strManUS is ", strManUS)
                Exponent = Exponent - 1 # 1.42857 is 1.425847e0
                for i in range(len(strManUS)):
                    if(strManUS[i] == 'e' or  strManUS[i] == '.'):
                        break
                    Exponent = Exponent + 1

            self.Exponent = Exponent
            #print ("2. Exponent is ", Exponent)

        else:
            #print ("INIT -- seeing Mantissa = ", Mantissa)
            #handle integer parameters only
            if(Mantissa == 0):
                self.Mantissa = 0
                self.Exponent = 0
            else:
                self.Mantissa = Mantissa
                if(InternalAware):
                    self.Exponent = Exponent
                    #print ("passed InternalAware exponent is ", Exponent)
                else:
                    self.Exponent = Exponent + len(str(Mantissa).replace('-', '')) - 1
            
        #endif

        #M=10, E=1 and M=1, E=1 both indicate the same number,
        #however, the different values of mantissa will be a problem
        #in numeric comparisons, so reduce to the form M=1, E=1
        #print ("self.Mantissa is ", self.Mantissa)
        #print ("type of self.Mantissa is ", type(self.Mantissa))
        MantissaStr = str(self.Mantissa)
        i = 0
        while MantissaStr[-1:] == '0' and \
                self.Mantissa != 0:
            MantissaStr = MantissaStr[:-1]
            i += 1
        #print ("i is ", i, "MantissaStr is ", MantissaStr)
        self.Mantissa = int (MantissaStr)

        #zero value has sign 0
        self.Sign = (1 if self.Mantissa > 0 else (0 if self.Mantissa == 0 and self.Exponent == 0 else -1))
        #print ("=============================Sign is ", self.Sign)
    #enddef init

    ########  Query Functions ########
    # bool isInt
    # Is "Integer"?
    def isInt(self):
        # 123456 --> (123456, 5)
        return len(str(self.Mantissa).replace('-', '')) <= self.Exponent + 1

    ########  Output Functions  ########
    #int int
    def int(self, preserveType = False):
        # 123456 (123456, 5)
        s = str(self.Mantissa).replace('-', '')
        if self.Exponent < 0:
            s = '0'
        else:
            lenS =len(s)
            #fill up with requisite number of 0s on the right
            s = s + '0'*(self.Exponent + 1 - lenS)
            #take as many required by the Exponent (add 1 more
            #since canonical form is always #.##....e###
            s = s[0:(self.Exponent + 1)]

        if preserveType == True:
            #convert to an integer, but return the mpap() version
            return mpap(s) * self.Sign
        else:
            return int(s) * self.Sign

    def __int__ (self):
        return self.int()

    def float (self):
        s = str(self.Mantissa)
        return float(('-' if self.Sign == -1 else '') + s[0:1] + '.' + s[1:] + 'e' + str(self.Exponent))

    # __repr__
    # Official Object Representation
    def __repr__(self):
        return "mpap(Mantissa = " + str(self.Mantissa) + ", Exponent = " + str(self.Exponent) + \
                ", Precision = " + str(self.Precision) + ", InternalAware = True)"

    # __str__
    # Pretty-Printed Representation of a number
    def __str__(self):
        if self.isInt():
            return str(int(self))
        elif len(str(self.Mantissa)) - 1 > self.Exponent and self.Exponent >= 0:
            #do not return as 1.23e45
            strAbsSelfMantissa = str(abs(self.Mantissa))
            decPoint = self.Exponent + 1
            return ('-' if self.Mantissa < 0 else '') + strAbsSelfMantissa[:decPoint] + '.' + strAbsSelfMantissa[decPoint:]
        else:
            strAbsSelfMantissa = str(abs(self.Mantissa))
            frac = strAbsSelfMantissa[1:]
            # mpap(1, -3) is 1.0e-3 and not 1.e-3
            if frac == '':
                frac = '0'
            strAbsSelfMantissa = strAbsSelfMantissa[0] + '.' + frac
            return ('-' if self.Mantissa < 0 else '') + strAbsSelfMantissa + "e" + str(self.Exponent)

    # return number in the form of
    # Mantissa = ###.#######, Exponent = ###*3
    # returns new mantissa as a string with adecimal point
    # and the exponent as an integer
    def sci(self):
        #print(repr(self), "sign is ", self.Sign)
        strMantissa = str(self.Mantissa)
        strMantissa = strMantissa.replace('-', '')
        lenStrMantissa = len(strMantissa)
        diff = self.Exponent - lenStrMantissa + 1
        #if  diff > 0:
        strMantissa = strMantissa + '0'*diff
        #print ("----- A. strMantissa=", strMantissa)
        expo = self.Exponent
        multfac = self.Exponent % 3 + 1
        expo = (self.Exponent // 3) * 3
        #print ("----- multfac=", multfac)
        #print ("----- lenStrMantissa=", lenStrMantissa)
        #print ("----- B. strMantissa[multfac:]=", strMantissa[multfac:])
        man = ('-' if (self.Sign == -1) else '') + strMantissa[:multfac] + '.' + strMantissa[multfac:]
        # handle the case when mantissa string is like '123.' -- add a zero at end
        if man[-1:] == '.':
            man += '0'
        #print (man)
        return man, expo

    def floor(self):
        i = self.int(preserveType = True)
        return i if self.Sign >= 0 else i-1

    #########  Modification Functions  ########
    def __neg__(self):
        return mpap(Mantissa = (-1) * self.Mantissa, Exponent = self.Exponent, InternalAware = True)

    #integer division (self // other)
    def __floordiv__ (self, other):
        if(not isinstance(other, mpap)):
            return self // mpap(other)
        #for negative numbers, round downwards, not towards 0
        res = (self / other).floor()
        #print ("__floordiv__: res is ", res)
        return res

    # __mod__ (self % other)
    def __mod__ (self, other):
        if(not isinstance(other, mpap)):
            return self % mpap(other)
        other = (self / other - self // other) * other
        return other

    def __abs__(self):
        if(self.Sign == 1):
            return self
        else:
            return -self

    #########  Comparison Functions  ########
    # __eq__ (self == other)
    def __eq__(self, other):
        if(not isinstance(other, mpap)):
            return self == mpap(other)
        #print ("self is -------------", self.__repr__())
        #print ("other is -------------", other.__repr__())
        return self.Mantissa == other.Mantissa and self.Exponent == other.Exponent

    # __hash__
    # Returns the unique Integer hash of object
    def __hash__(self):
        return hash((self.Mantissa, self.Exponent))

    # __ne__ (self != other)
    def __ne__(self, other):
        return not self == other

    # __lt__ (self < other)
    # Supports comparing with numbers too.
    def __lt__(self, other):
        if(not isinstance(other, mpap)):
            return self < mpap(other)

        if((self.Sign == -1 or self.Sign == 0) and other.Sign == 1):
            #Man = 0 and Exp = 0 means Sign is 0
            return True
        if(self.Sign == -1 and other.Sign == -1):
            return -other < -self

        #print ("self.Sign=", self.Sign)
        #print ("other.Sign=", other.Sign)
        # Now they are all positive & same
        if self.Exponent < other.Exponent and other.Sign != 0:
            return True
        if self.Exponent > other.Exponent and self.Sign != 0:
            return False

        # Now they're the same exponent
        # You cannot directly compare mantissas, because they contain precision digits
        # e.g. 1.42857 -> (142857, 0), 1.482562 (1428562, 0)
        # You have to align them and compare, so... the key is to align
        mSelf = self.Mantissa
        mOther = other.Mantissa
        if(len(str(self.Mantissa)) < len(str(other.Mantissa))):
            mSelf = mSelf * 10**(len(str(other.Mantissa)) - len(str(self.Mantissa)))
        elif(len(str(self.Mantissa)) > len(str(other.Mantissa))):
            mOther = mOther * 10**(len(str(self.Mantissa)) - len(str(other.Mantissa)))

        return mSelf < mOther

    # __le__ (self <= other)
    def __le__(self, other):
        return self == other or self < other

    # __gt__ (self > other)
    def __gt__(self, other):
        return not self < other and not self == other

    # __ge__ (self >= other)
    def __ge__(self, other):
        return self == other or self > other

    #########  Arithmetic Functions  ########
    def __add__(self, other):
        # To perform arithmetic add, we have to align the bits so that they are
        # aligned to the SMALLEST significant position, e.g.
        # 142.857 (142857, 2) + 3.45678 (345678, 0)
        # MinExpPos: 2-6+1=-3, 0-6+1=-5
        if(not isinstance(other, mpap)):
            return self + mpap(other)

        #print('self = ', self.__repr__(), 'other = ', other.__repr__())

        # Calculate Minimum Exponents for Alignment
        minESelf  = 1 + self.Exponent - len(str(self.Mantissa).replace('-', ''))
        minEOther = 1 + other.Exponent - len(str(other.Mantissa).replace('-', ''))

        # Save copies of mantissas
        mSelf   = self.Mantissa
        mOther  = other.Mantissa

        # Borrowed Exponents for Calculation
        bECalc = max(-minESelf, -minEOther)
        #print ('minESelf = ', minESelf)
        #print ('minEOther = ', minEOther)
        #print ('bECalc = ', bECalc)

        # Check which we borrowed, and return to the other
        if(minESelf < minEOther):
            mOther = mOther * 10**(minEOther + bECalc)
        else:
            mSelf  = mSelf * 10**(minESelf + bECalc)

        # # Given minExpPos, e.g. 142.857 is -3, 3.45678 is -5, diff is 2
        # # 14285700 & 345678
        # # 142.85700
        # #   3.45678
        # # ----------

        mSum = mOther + mSelf
        eSum = len(str(mSum).replace('-', '')) - 1 - bECalc
        #print(mSelf, mOther, mSum, eSum, minESelf, minEOther, bECalc)

        #M=100, E=1 and M=10, E=1 both indicate the same number,
        #however, the different values of mantissa will be a problem
        #in numeric comparisons of mantissas, so reduce to the form M=10, E=1
        mSumStr = str(mSum)
        i = 0
        #print ("mSumStr = ", mSumStr)
        while mSumStr[-1:] == '0' and i <= eSum and mSum != 0:
            mSumStr = mSumStr[:-1]
            i += 1

        # cut Mantissa to target precision
        if(len(str(mSum)) > self.Precision):
            mSum = int(mSumStr[0:self.Precision])
        else:
            mSum = int(mSumStr)

        result = mpap(Mantissa = mSum, Exponent = eSum, InternalAware = True)

        #print("result =", result.__repr__())

        return result

    # __sub__ (self - other)
    def __sub__(self, other):
        return self + (-other)

    # __mul__ (self * other)
    def __mul__(self, other):
        # To perform arithmetic multiplication, the exponents are multiplied together
        # and the mantissa are aligned and multiplied together.
        # This means we need to align all problems like this:
        # 1.42951e-5 (142951, -5) x 8.37e4 (837, 4) = 142951 x e(-5-5) x 837 x e(4-2)
        #print ("__mul__ ----> type(other) is ", type(other))
        #print("len self is ", len(str(self)))
        #print("len other is ", len(str(other)))
        #print ("type of other is ", type(other))
        if(not isinstance(other, mpap)):
            #print ("calling __mul__ recursively...")
            #r = self * mpap(other)
            #print (" ----- finished calling __mul__ recursively...")
            #print ("-- r is " , r)
            return self * mpap(other)

        self.Sign = self.Sign * other.Sign

        #print ("__mul__ ----> other.Mantissa is ", other.Mantissa)
        # Calculate "Borrowed" Exponents for Alignment -- always len() - 1 after removing the sign digit
        bESelf  = len(str(self.Mantissa).replace('-', '')) - 1
        bEOther = len(str(other.Mantissa).replace('-', '')) - 1

        # Copies of mantissas
        mSelf    = self.Mantissa
        #print ("mSelf is ", mSelf)
        mOther   = other.Mantissa
        #print ("mOther is ", mOther)

        iProduct = mSelf * mOther # this is an INTEGER part, not an actual Mantissa number!
        # Convert this iProduct to a internal representation
        # Check how many numbers the product can ReTurn to the Exponent (RTE)
        rteProduct = len(str(iProduct).replace('-', '')) - 1
        
        # ...and return it
        mProduct = iProduct
        eProduct = self.Exponent + other.Exponent + rteProduct - bESelf - bEOther
        
        #M=100, E=1 and M=10, E=1 both indicate the same number,
        #however, the different values of mantissa will be a problem
        #in numeric comparisons, so reduce to the form M=10, E=1
        #print ("1 -- mProduct is ", mProduct, "type of mProduct is ", type(mProduct))
        #print ("1 -- eProduct is ", eProduct, "type of eProduct is ", type(eProduct))
        mProductStr = str(mProduct)
        #print ("1a -- mProductStr is ", mProductStr)
        i = 0
        while mProductStr[-1:] == '0' and \
                i <= eProduct and mProduct != 0:
            #print ("A -- mProductStr is ", mProductStr)
            mProductStr = mProductStr[:-1]
            i += 1

        #print ("~~~~~~~~~~~~~mProduct is ", mProductStr)
        # cut Mantissa to target precision
        if(len(mProductStr) > self.Precision):
            mProduct = int(mProductStr[0:self.Precision])
        else:
            mProduct = int(mProductStr)
        #print ("Mantissa is ", mProduct, "Exponent is ", eProduct)
        return mpap(Mantissa = mProduct, Exponent = eProduct, InternalAware = True)

    # __truediv__ (self / other)
    # Implements "true" division
    def __truediv__(self, other):
        if(not isinstance(other, mpap)):
            return self / mpap(other)
        if other == 0:
            MPAPERRORFLAG = "Division by zero."
            return mpap(0)
        #print ("self.Sign is ", self.Sign, "other.Sign is ", other.Sign)
        #print ()
        #print ("--------------------------------------------------------")
        #print ("self is ", self.__repr__(), "other is ", other.__repr__())

        self.Sign = self.Sign * other.Sign

        #print ("self.Sign is ", self.Sign, "other.Sign is ", other.Sign)
        #print ("self.Sign is ", self.Sign)

        # Calculate "Borrowed" Exponents for Alignment -- always len() - 1 after removing the sign digit
        bESelf  = len(str(self.Mantissa).replace('-', '')) - 1
        bEOther = len(str(other.Mantissa).replace('-', '')) - 1
        #print ("bESelf is ", bESelf, "bEOther is ", bEOther)
        bEPrecision = 0 # Borrowed Exponent for Precision Division

        # Copies of mantissas
        mSelf    = abs(self.Mantissa)
        mOther   = abs(other.Mantissa)
        #print ("mSelf is ", mSelf, "mOther is ", mOther)

        # Until we reach desired precision... or when we have exhausted the divisor
        # The signs are all absolute
        opSelf   = mSelf % mOther
        #print ("opSelf is ", opSelf)
        opResult = (str(mSelf // mOther)) if mSelf // mOther != 0 else ''
        #print ("opResult is ", opResult)
        while(len(opResult.lstrip('0')) < (self.Precision*2) and opSelf != 0):
            #NOTE: anirb -- we compute double the precision digits required
            opSelf = opSelf * 10
            bEPrecision += 1
            opResult = opResult + (str(opSelf // mOther))
            #print ("loop: opResult is ", opResult)
            opSelf = opSelf % mOther

        opResult = opResult.lstrip('0')

        if(len(opResult) == 0):
            return mpap(0)

        bDiv = int(opResult) * self.Sign
        rteDiv = len(opResult) - 1

        #print(self, other)
        #print(mSelf, mOther, opSelf, opResult)
        #print(self.Exponent, other.Exponent, rteDiv, bESelf, bEOther, bEPrecision)
        eDiv = self.Exponent - other.Exponent + rteDiv - bESelf + bEOther - bEPrecision
        return mpap(Mantissa = bDiv, Exponent = eDiv, InternalAware = True)

    # __lshift__ (self << other)
    def __lshift__ (self, other):
        if(not isinstance(other, mpap)):
            return self << mpap(other)
        return self * mpap(2) ** other

    # __rshift__ (self >> other)
    def __rshift__ (self, other):
        if(not isinstance(other, mpap)):
            return self >> mpap(other)
        return self // mpap(2) ** other

    # logical functions on int() of mpap()
    def __xor__ (self, other):
        if(not isinstance(other, mpap)):
            return self ^ mpap(other)
        return mpap(int(self) ^ int(other))

    def __or__ (self, other):
        if(not isinstance(other, mpap)):
            return self | mpap(other)
        return mpap(int(self) | int(other))

    def __and__ (self, other):
        if(not isinstance(other, mpap)):
            return self & mpap(other)
        return mpap(int(self) & int(other))

    def __invert__ (self):
        return mpap(~int(self))

    def __not__ (self):
        return mpap(0 if self == 0 else 1)

    # __pow__ (self ** other)
    def __pow__(self, other):
        #print ("other is ", other)
        if(not isinstance(other, mpap)):
            return self ** mpap(other)
        if (self.Sign == -1 and other.Exponent < 0):
            MPAPERRORFLAG = "Complex result is not implemented."
            return mpap (0)

        if(not other.isInt()):
            #print ("B. other is ", other)
            return self.generic_pow (other)
        else:
            rResult = self
            if(other == 0):
                if(self == 0):
                    raise ValueError("mpap: 0**0 has no mathematical significance")
                return mpap(1)

            if(other < 0):
                return mpap(1) / (self ** (-other))
            else:
                #print ("other is ", other)
                #for i in range(1, other.Mantissa):
                for i in range(1, int(other)):
                    #print ("--- __pow__ -- i is ", i)
                    rResult = rResult * self
                return rResult

    # sgn(self)
    def sgn(self):
        return self.Sign

    def generic_pow (self, other):
        return (other*self.log()).exp()

    def log (self):
        if self.Precision < 15:
            return mpap(math.log(self.float()))
        if self.Exponent > 100:
            ### DO NOT USE for mpaps with exponent smaller than 100! ###
            t = self.Exponent - 1
            self = mpap(self.Mantissa, Exponent = 1)
            return self.logsmall() + mpap(10).logsmall() * t
        else:
            #print ("1. self is now ", self)
            return self.logsmall()

    def logt (self):
        ## Taylor's series tweaked for better convergence
        ## See https://stackoverflow.com/questions/27179674/examples-of-log-algorithm-using-arbitrary-precision-maths
        if (self <= 0):
            MPAPERRORFLAG = "I give up!"
            return mpap (0)
        x = (self-1)/(self+1)
        z = x * x
        log = mpap(0)
        k = 0
        k = 1
        while x > mpap(1, -self.Precision):
            log += x * 2 / k
            x *= z
            k+=2
        return log

    def pi(self):
        # Pi using Chudnovsky's algorithm
        #NOTE: anirb: bug in floordiv has been fixed 30May2019
        K, M, L, X, S = mpap(6), mpap(1), mpap(13591409), mpap(1), mpap(13591409)
        maxK = self.Precision
        for i in range(1, maxK+1):
            M = (K**3 - K*16) * M // i**3 
            L += 545140134
            X *= -262537412640768000
            S += M * L / X
            K += 12
        pi = mpap(10005).sqrt() * 426880 / S
        return pi * self

    def logsmall (self):
        #print ("self is -------------", self.__repr__())
        # return something for the special case.
        #print ("2. self is now ", self)
        if (self <= 0):
            #print ("self is ---LT 0------", self.__repr__())
            MPAPERRORFLAG = "I give up!"
            return mpap (0)
 
        # Precondition x to make 1.2 < x < 1.5
        f = 1 #mul adjustment (power of 0.5)
        s = 0 #subtraction adjustment (multiplier of 1.6)
        if self == 1.0:
            #print ("self is EQ 1.0 -------------", self.__repr__())
            return mpap (0)

        if self < 1.1:
            i = 0
            while self < 1.4:
                s += 1
                self = self * 1.6
                #print ("3. self is now ", self)
                i += 1
                if i > 100000:
                    break
        if self > 1.8:
            i = 0
            while self > 1.5:  #for large numbers
                f *= 2
                self = self.sqrt()
                i += 1
                if i > 100000:
                    break

            #if we have reduced to too low a value
            i = 0
            while self < 1.1:
                s += 1
                self = self * 1.6
                #print ("self is now ", self)
                i += 1
                if i > 100000:
                    break

        if self < 1.1:
            print ("Value too low for logt!")
            MPAPERRORFLAG = "WARNING: Value too low for logt!"

        #print (self.__repr__())
        return self.logt() * f  - mpap(1.6).logt() * s
      

    def bitcount (self):
        #print ("bitcount: x is", x)
        return int(math.log(int(self), 2)+2)

    def x10p (self, x):
        # multiply by 10^x, where x is an integer
        return mpap(self.Mantissa, self.Exponent+int(x), InternalAware=True)

    def sqrt (self):
        #Use isqrt(x*10^Precision)/isqrt(10^Precision)
        #n = self.x10p(self.Precision*2).fisqrt()
        #d = mpap(1).x10p(self.Precision*2).fisqrt()
        #print ("n is ", n)
        #print ("d is ", d)
        return self.x10p(self.Precision*2).isqrt()/mpap(1).x10p(self.Precision*2).isqrt()

    def isqrt(self):
        if self.Mantissa == 1 and (self.Exponent % 2) == 0:
            #even power of ten, make use of our base-10 advantage
            #print ("make use of our base-10 advantage")
            return mpap (1, Exponent = (self.Exponent // 2), InternalAware = True, Precision=self.Precision)
        elif self.Precision < 15:
            #use built-in float 
            #print ("use built-in float")
            return mpap(math.sqrt(int(self)), Precision=self.Precision)

        x = int(self)
        #print ("isqrt: x is", x)

        ####### From libmath #######
        bc = self.bitcount()
        guard_bits = 10
        x <<= 2*guard_bits
        bc += 2*guard_bits
        bc += (bc&1)
        hbc = bc//2
        startprec = min(50, hbc)
        # Newton iteration for 1/sqrt(x), with floating-point starting value
        r = int(2.0**(2*startprec) * (x >> (bc-2*startprec)) ** -0.5)
        pp = startprec
        for p in self.giant_steps(startprec, hbc):
            # r**2, scaled from real size 2**(-bc) to 2**p
            r2 = (r*r) >> (2*pp - p)
            # x*r**2, scaled from real size ~1.0 to 2**p
            xr2 = ((x >> (bc-p)) * r2) >> p
            # New value of r, scaled from real size 2**(-bc/2) to 2**p
            r = (r * ((3<<p) - xr2)) >> (pp+1)
            pp = p
        # (1/sqrt(x))*x = sqrt(x)
        return mpap((r*(x>>hbc)) >> (p+guard_bits))

    def giant_steps(self, start, target, n=2):
        ## Return a list of integers ~=
         
        ## [start, n*start, ..., target/n^2, target/n, target]
         
        ## but conservatively rounded so that the quotient between two
        ## successive elements is actually slightly less than n.
         
        ## With n = 2, this describes suitable precision steps for a
        ## quadratically convergent algorithm such as Newton's method;
        ## with n = 3 steps for cubic convergence (Halley's method), etc.
         
        ##     >>> giant_steps(50,1000)
        ##     [66, 128, 253, 502, 1000]
        ##     >>> giant_steps(50,1000,4)
        ##     [65, 252, 1000]
        
        L = [target]
        while L[-1] > start*n:
            L = L + [L[-1]//n + 2]
        return L[::-1]

    def exp (self):
        if abs(self) < 2000:
            return self.expsmall()
        else:
            # use exp(x) = exp(x-m*log(2)) * 2^m where m = floor(x/log(2)).
            m = (self/(mpap(2).log())).floor()
            #print ("m is ", m)
            return (self - m * mpap(2).log()).expsmall() * mpap(2)**m

    def digits(self):
        return len(str(int(self)))

    def expsmall(self):
        # Compute exp(x) as a fixed-point number. Works for any x,
        # but for speed should have |x| < 1. For an arbitrary number,
        # use exp(x) = exp(x-m*log(2)) * 2^m where m = floor(x/log(2)).

        # e(x)  = 1 + x**1/1! + x**2/2! + x**3/3! + x**4/4! + ...
        #       = 1 + x**2/2! + x**4/4! + ... even terms
        #           + x**3/3! + x**5/5! + ... odd terms
        #       = 1 + x**2/2! + x**4/4! + ... even terms
        #           + x* (x**2/3! + x**4/5! + ... ) odd terms
        x = self
        s0 = s1 = mpap(1)
        k = 2
        a = x*x
        while a > mpap(1, Exponent=-self.Precision):
            a /= k; s0 += a; k += 1
            a /= k; s1 += a; k += 1
            a *= x*x
               
        s1 = s1*x
        s = s0 + s1
        return s

    def sin (self):
        if self == 0:
            return mpap(0)
        else:
            #print ("sine sign is ", self.cos(cosine=False).Sign)
            return self.cos(cosine=False)

    def tan (self):
        c = self.cos()
        if c != 0:
            return self.cos(cosine=False)/c
        else:
            MPAPERRORFLAG = "Tangent is undefined."
            return mpap(0)

    def cos (self, cosine=True):
        #x = x mod 2PI
        x = self % (mpap(2).pi())
        #print ("x is now ", x)
        x2 = -x*x
        t = mpap(1)
        c = mpap(1)
        n = mpap(2)
        while abs(t) > mpap(1, -self.Precision):
            if cosine == True:
                #cosine
                t *= x2/(n*(n-1))
            else:
                #sine
                t *= x2/((n+1)*n)
            n += 2
            c += t
        if cosine == False:
            #sine
            c *= x
        return c

    def acos (self):
        return self.asin(acosine=True)

    def asin (self, acosine=False):
        if abs(self) > 1:
            return mpap(0)
            MPAPERRORFLAG = "Domain error."
        x = self
        x2 = x*x
        t = mpap(1)
        v = mpap(1)
        i = 2
        while abs(t) > mpap(1, -self.Precision):
            t *= x2*(i-1)/i
            #print (repr(t))
            v += t/(i+1)
            i += 2
        v *= x
        return mpap(1).pi()/2 - v if acosine==True else v

    def atan (self):
        x = self
        m = 1
        if self < 0:
            x = -x
            m = -1
        a = mpap(0)
        f = 0
        if x > 0.2:
            a = mpap(0.2).atan()
        while x > 0.2:
            f += 1
            x = (x - 0.2)/(x * 0.2 + 1)
        v = x
        x2 = -x * x
        n = x
        t = mpap(1)
        i = 3
        while abs(t) > mpap (1, -self.Precision):
            n *= x2
            t = n/i
            v += t
            i += 2
        
        return (v + a*f)*m

    def endian(self, boundary=8):
        #print ("self is ", repr(self))
        boundary = int(boundary)
        if boundary == 0:
            boundary = 8;
        copy = self
        result = mpap(0)
        while copy != 0:
            result <<= boundary
            #result |= (copy & int('0b'+'1'*boundary))
            result |= (copy & ((1<<boundary)-1))
            copy >>= boundary

        #print ("result is ", repr(result))
        return result

    
    def factors (self):
        n = int(self)

        if n == 0:
            self.result = 0
    
        self.result = set()
        self.result |= {int(1), n}
    
        def all_multiples(result, n, factor):
            z = n
            f = int(factor)
            while z % f == 0:
                result |= {f, z // f}
                f += factor
            return result
        
        self.result = all_multiples(self.result, n, 2)
        self.result = all_multiples(self.result, n, 3)
        
        for i in range(1, math.sqrt(n) + 1, 6):
            i1 = i + 1
            i2 = i + 5
            if not n % i1:
                self.result |= {int(i1), n // i1}
            if not n % i2:
                self.result |= {int(i2), n // i2}

        print (self.result)
        return mpap(1)

