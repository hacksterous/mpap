import random
import mpmath.libmp
from mpmath import *
from mpap import mpap
#from ArbitraryPrecision import ArbitraryPrecision
EPS = '1e-94'
mp.dps=100

print ("MPMATH backend is ", mpmath.libmp.BACKEND)
m = 101000000000000000000000
m = random.randint(1000, m)
r1 = random.randint(1000, m)
badCount = 0
for i in range (50):
	x=mpf(r1)
	z=mpap(r1)
	x *= x*(-1) 
	z *= z*(-1)#/(mpap(i+1)*mpap(i+2))
	#print (y)
	#print (repr(z))
	delta = z-mpap(str(x))
	#print ("i = ", i, "mpap diff = ", repr(delta))
	if abs(delta) > mpap(EPS):
		badCount += 1
		#print ("---------------------------------------------- BAD ")
	#print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	m = max(r1, m)
	r1 = random.randint(1000, m)
print ("1. badCount is = ", badCount)

m = random.randint(1000, m)
r1 = random.randint(1000, m)
r2 = random.randint(1000, m)
badCount = 0
for i in range (50):
	x = mpf(r1+i+1)/mpf(r2+i+2)
	z = mpap(r1+i+1)/mpap(r2+i+2)
	#print (x)
	#print (repr(z))
	delta = z-mpap(str(x))
	#print ("i = ", i, "mpap diff = ", repr(delta))
	if abs(delta) > mpap(EPS):
		badCount += 1
		#print ("---------------------------------------------- BAD ")
	#print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	m = max(r1, m)
	r1 = random.randint(1000, m)
	r2 = random.randint(1000, m)
print ("2. badCount is = ", badCount)

m = random.randint(1000, m)
r1 = random.randint(1000, m)
r2 = random.randint(1000, m)
badCount = 0
for i in range (50):
	x = (mpf(r1+i+1)/mpf(r2+i+2))**3
	z = (mpap(r1+i+1)/mpap(r2+i+2))**3
	#print (x)
	#print (repr(z))
	delta = z-mpap(str(x))
	#print ("i = ", i, "mpap diff = ", repr(delta))
	if abs(delta) > mpap(EPS):
		badCount += 1
		#print ("---------------------------------------------- BAD ")
	#print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	m = max(r1, m)
	r1 = random.randint(1000, m)
	r2 = random.randint(1000, m)
print ("3. badCount is = ", badCount)

badCount = 0
for i in range (50):
	r1 = random.randint(5001, 100000)
	r2 = random.randint(1001, 5000)
	a = r1/r2
	print ("a is ", a)
	x = mp.exp(a)
	z = mpap(a).exp()
	print ("x: ", x)
	print ("z: ", repr(z))
	delta = z-mpap(str(x))
	#print ("i = ", i, "mpap diff = ", repr(delta))
	if abs(delta) > mpap(EPS):
		badCount += 1
		print ("---------------------------------------------- BAD ")
	#print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

## NOTE -- MPAP EXP matches with LibBF -- looks like MPMath
## is not using gmpy2 backend correctly
print ("4. EXP. badCount is = ", badCount)

badCount = 0
for i in range (50):
	r1 = random.randint(5001, 1000000)
	r2 = random.randint(1001, 5000)
	a = r1/r2
	print ("a is ", a)
	x = mp.tan(a)
	z = mpap(a).tan()
	print ("x: ", x)
	print ("z: ", repr(z))
	delta = z-mpap(str(x))
	#print ("i = ", i, "mpap diff = ", repr(delta))
	if abs(delta) > mpap(EPS):
		badCount += 1
		print ("---------------------------------------------- BAD ")
	#print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

## NOTE -- MPAP EXP matches with LibBF
print ("4. TAN. badCount is = ", badCount)

