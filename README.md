## Minimalistic Python Arbitrary Precision Library

MPAP is a small arbitrary precision math library based on [ArbitraryPrecision](https://github.com/jimmielin/ArbitraryPrecision)

Like AP, MPAP is based on an internal representation using mantissa and exponent and adds an additional sign.
Mantissa, sign and exponent for imaginary component is not currently used.

The Mantissa is always stored as the smallest possible integer, i.e., zeroes to the right are trimmed. 
The number 1000 is stored as: 
```
>>> from mpap import mpap
>>> mpap(1000)
mpap(Mantissa = 1, Exponent = 3, InternalAware = True)
```
The number 10001 is stored as:
```
>>> mpap(1001)
mpap(Mantissa = 1001, Exponent = 3, InternalAware = True)
```
*In the internal representation, the decimal point is always after the leftmost digit.*
See more details below.

Floats are rounded to the precision supported by the Python implementation (CPython double precision below:)
```
>>> mpap(1000.342353465654765786787978978)
mpap(Mantissa = 1000342353465655, Exponent = 3, InternalAware = True)
```

MPAP can convert floats to numbers:

```
>>> mpap(1.2)/mpap(1001e234560)
mpap(Mantissa = 
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880119880
1198801198801198801198801198801198801198801198801198801198801198801198801198801198, Exponent = -234563, 
InternalAware = True)
```
Precision is automatically increased upto a hard maximum limit of 1000 (can be changed in `mpap.py`).

Floats directly passed to MPAP will be limited by Python implementation's native precision:
```
>>> mpap(1.234567891234567891234567)
mpap(Mantissa = 1234567891234568, Exponent = 0, InternalAware = True)
```
Higher precision floats must be passed as strings:
```
>>> mpap('1.234567891234567891234567')
mpap(Mantissa = 1234567891234567891234567, Exponent = 0, InternalAware = True)
```

### The *InternalAware* parameter passed to MPAP
When InternalAware is *False*, the Mantissa is interpreted as a literal number. The default value
for InternalAware is *False*.
```
>>> mpap(1393821, InternalAware=False)
mpap(Mantissa = 1393821, Exponent = 6, InternalAware = True)
```
In the above case, the value of the number is 1393821, i.e., 1.393821e6
```
>>> mpap(1393821, InternalAware=True)
mpap(Mantissa = 1393821, Exponent = 0, InternalAware = True)
```
In this case, the value of the number is 1.393821, i.e., 1.393821e0


### Functions supported

Mathematical functions supported are: sine, cosine, tangent and inverse function of these; exponential (base of natural logarithm),
natural logarithm, square root, integer square root and pi (using Chudnovsky series).
