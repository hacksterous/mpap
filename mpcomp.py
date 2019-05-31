from mpmath import *
from mpap import mpap
from ArbitraryPrecision import ArbitraryPrecision
mp.dps=40

x=mpf(100)
y=ArbitraryPrecision(100)
z=mpap(100)

x = (x**7)/(mpf(720))
y = (y**7)/(ArbitraryPrecision(720))
z = (z**7)/(mpap(720))
#print (x)
#print (y)
#print (z)
print ('-----------------------------')

for i in range (20):
	x *= x/(mpf(i+1)*mpf(i+2))
	y *= y/(ArbitraryPrecision(i+1)*ArbitraryPrecision(i+2))
	z *= z/(mpap(i+1)*mpap(i+2))
	#print (x)
	#print (y)
	#print (z)
	m = (z-mpap(str(x)))/z
	print ("i = ", i, "mpap diff = ", m)
	a = (y-int(x))/y
	print ("i = ", i, "ArbPrec diff = ", a)
	print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
