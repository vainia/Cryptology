PM = int(input("Podaj liczbe pierwrza modulo (PRIME PODULE) "))
GR = int(input("Podaj wartosc generatora (GENERATOR) "))
TA = int(input("Podaj tajemnice Alicji "))
TB = int(input("Podaj tajemnice Boba "))
A=GR**TA%PM
B=GR**TB%PM
print(f"Klucz dzielony Alicji {A}")
print(f"Klucz dzielony Boba {B}")
print(f"Klucz wspolny sesji dla Alicji {B**TA%PM}")
print(f"Klucz wspolny sesji dla Boba {A**TB%PM}")
