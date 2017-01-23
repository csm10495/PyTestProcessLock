import pytest
import time

def test_a(constantObj):
    constantObj['safePrint']('test a stuff')
    
def test_b(constantObj, sync):
    sPrint = constantObj['safePrint']
    
    sPrint('in b')
    sPrint('about to be done with b')
    
def test_c(constantObj):
    constantObj['safePrint']('test c stuff')
    time.sleep(.2)    
    
def test_d(constantObj):
    constantObj['safePrint']('test d stuff')
    time.sleep(.4)
