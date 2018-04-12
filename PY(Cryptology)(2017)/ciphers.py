# -*- coding: utf-8 -*-

abs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesarEncrypt(offset=3, buf="alamakota"):
    res = ''
    for c in buf:
        try:
            i = (abs.index(c) + offset) % 52
            res += abs[i]
        except ValueError:
            res += c
    return res

def caesarDecrypt(offset=3, buf="dodpdnrwd"):
    res = ''
    for c in buf:
        try:
            i = (abs.index(c) - offset) % 52
            res += abs[i]
        except ValueError:
            res += c
    return res

def caesarBrutForce(cstr, word):
	res = ''
	offset = key = 0
	while offset != 52:
		offset += 1
		buff = caesarDecrypt(offset, cstr)
		if buff.find(word) > -1:
			res = buff
			key = offset
		print "For key",offset-1,": ",buff
	if key != 0:
		print "Encrypted word is",res,"for key",key-1
	else:
		print "Key is not found"

def charAsNum(text):
    numseq = []
    for c in text:
        try:
            numseq.append(abs.index(c))
        except ValueError:
            numseq.append(-1)
    return numseq

def vigenereEncrypt(plaintext="If you do not like how it works, please, remove all lines which contain word \"less\"!", key="Cryptoid"):
    key_int = charAsNum(key)
    plaintext_int = charAsNum(plaintext)
    ciphertext = ''
    less = 0
    for i in range(len(plaintext_int)):
        if plaintext_int[i] == -1:
            less+=1
            ciphertext += plaintext[i]
        else:
            value = (plaintext_int[i] + key_int[(i - less) % len(key)]) % 52
            ciphertext += abs[value]
    return ciphertext

def vigenereDecrypt(ciphertext="kw WDN rw qQK JxDs prY zR LHFsv, RCCpLs, zhOFTt tzt oKECH PvqfJ tMCMoqq YFPs \"EsAv\"!", key="Cryptoid"):
    key_int = charAsNum(key)
    ciphertext_int = charAsNum(ciphertext)
    plaintext = ''
    less = 0
    for i in range(len(ciphertext_int)):
        if ciphertext_int[i] == -1:
            less+=1
            plaintext += ciphertext[i]
        else:
            value = (ciphertext_int[i] - key_int[(i - less) % len(key)]) % 52
            plaintext += abs[value]
    return plaintext

def matrixMul(C=[[9,3,4],[7,2,1],[6,5,8]], P=[20,13,8]):
    res = []
    for i in range(len(C)):
        s = 0
        for j in range(len(P)):
            s += C[i][j]*P[j]
        res.append(s)
    return res

# The algorythm below ignores every symbol which does not included in local alphabet
def hillEncrypt(plaintext="unicef", key=[[9,3,4],[7,2,1],[6,5,8]]):
    ciphertext_int = []
    ciphertext = []
    plaintext_int = []
    border = 0
    for c in plaintext:
        try:
            plaintext_int.append(abs.index(c))
        except ValueError:
            pass
    if len(plaintext_int) % len(key) != 0:
        border = (len(plaintext_int) / len(key) + 1) * len(key) - len(plaintext_int)
        for i in range(border):
            plaintext_int.append(0)
    for bnum in range(len(plaintext_int)/len(key)):
        ciphertext_int += [c % 52 for c in matrixMul(key, [c % 52 for c in [plaintext_int[bnum*len(key)+i] for i in range(len(key))]])]
    for i in range(len(ciphertext_int)-border):
        ciphertext.append(abs[ciphertext_int[i]])
    return ''.join(ciphertext)

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    if len(m) == 2:
        return (m[0][0]*m[1][1]-m[0][1]*m[1][0])
    determinant = 0
    for c in range(len(m)):
        determinant += (((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c)))
    return determinant

def modInv(a, mod):
  for i in range(1, mod):
    if (i * a) % mod == 1:
      return i
  raise ValueError(str(a) + " has no inverse mod " + str(mod))

def getMatrixInverse(m, mod):
    cofactors = []
    if len(m)==2:
        return [[(modInv(getMatrixDeternminant(m),mod)*i%mod)%mod for i in [m[1][1],-m[0][1]]],[(modInv(getMatrixDeternminant(m),mod)*i%mod)%mod for i in [-m[1][0],m[0][0]]]]
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            cofactorRow.append((((-1)**(r+c))*getMatrixDeternminant(getMatrixMinor(m,r,c)))%mod)
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = (cofactors[r][c]*modInv(getMatrixDeternminant(m),mod))%mod
    return cofactors

def hillDecrypt(ciphertext="RsPYBu", key=[[9,3,4],[7,2,1],[6,5,8]]):
    return hillEncrypt(ciphertext, getMatrixInverse(key, 52))

print "-*-Manual-*-"
print "\nTo encrypt with Caesar use command: caesarEncrypt(offset, plaintext)"
print "Example result for offset=3 and plaintext=\"alamakota\": ", caesarEncrypt(3, "alamakota")
print "\nTo decrypt with Caesar use command: caesarDecrypt(offset, ciphertext)"
print "Example result for offset=3 and ciphertext=\"dodpdnrwd\": ", caesarDecrypt(3, "dodpdnrwd")
print "\nTo make brute force attack at Caesar use command: caesarBrutForce(ciphertext, keyword)"
print "Example result for ciphertext=\"dodpdnrwd\" and keyword=\"ala\": \n", caesarBrutForce("dodpdnrwd", "ala")
print "\nTo encrypt with Vigenere use command: vigenereEncrypt(plaintext, key)"
print "Example result for plaintext=\"LAREK marek?\" and key=\"KOKOS\": ", vigenereEncrypt("LAREK marek?", "KOKOS")
print "\nTo decrypt with Vigenere use command: vigenereDecrypt(ciphertext, key)"
print "Example result for ciphertext=\"voBsC WObSc?\" and key=\"KOKOS\": ", vigenereDecrypt("voBsC WObSc?", "KOKOS")
print "\nTo encrypt with Hill use command: hillEncrypt(plaintext, key)"
print "Example result for plaintext=\"unicef\" and key=[[9,3,4],[7,2,1],[6,5,8]]: ", hillEncrypt("unicef", [[9,3,4],[7,2,1],[6,5,8]])
print "\nTo decrypt with Hill use command: hillDecrypt(ciphertext, key)"
print "Example result for ciphertext=\"RsPYBu\" and key=[[9,3,4],[7,2,1],[6,5,8]]: ", hillDecrypt(ciphertext="RsPYBu", key=[[9,3,4],[7,2,1],[6,5,8]])

def euklid(n, a):
    ui = 0; uip = 1; vi = 1; vip = 0; ni = n; ai = a; qi = ni / ai; ri = ni % ai; i = 0
    print " i |   ui   |   ui'   |   vi   |   vi'   |   ni   |   ai   |   qi   |   ri   "
    print "_____________________________________________________________________________"
    print "", i, "| ", '%+5s' % ui, "| ", '%+5s' % uip, " | ", '%+5s' % vi, "| ", '%+5s' % vip, " | ", '%+5s' % ni, "| ", '%+5s' % ai, "| ", '%+5s' % qi, "| ", '%+5s' % ri
    while ri:
        i += 1
        uiprev = ui; viprev = vi
        ui = uip - ui * qi; vi = vip - vi * qi
        uip = uiprev; vip = viprev
        ni = ai; ai = ri
        qi = ni / ai
        ri = ni % ai
        print "", i, "| ", '%+5s' % ui, "| ", '%+5s' % uip, " | ", '%+5s' % vi, "| ", '%+5s' % vip, " | ", '%+5s' % ni, "| ", '%+5s' % ai, "| ", '%+5s' % qi, "| ", '%+5s' % ri
    print "V=", ui, "   U=", vi
    print "gcd(", n, ", ", a, ")=", n, "*", ui, "+", vi, "*", a, "=", ui * n + vi * a
    print a, "^-1 mod", n, "=", vi, "mod", n, "=", vi % n

def powerMod(a, k, n):
    xi = 1
    ai = a
    print k, "binary is:", bin(k)[:1:-1]
    print "  i  |   xi   |   ai   |   ti   "
    print "________________________________"
    for i in range(len(bin(k)[2:])):
        print "", '%+3s' % i, "| ", '%+5s' % xi, "| ", '%+5s' % ai, "| ", '%+5s' % bin(k)[:1:-1][i]
        if bin(k)[:1:-1][i] == '1':
            xi = xi * ai % n
        ai = ai * ai % n
    print "", '%+3s' % len(bin(k)[2:]), "| ", '%+5s' % xi, "| "

print "\nTo run euklid algorythm implementation use command: euklid(n, a)"
print "Example result for n=197, a=84: \n", euklid(197, 84)
print "\nTo run power modulo algorythm implementation use command: powerMod(a, k, n)"
print "Example result for a=255, k=521, n=314: \n", powerMod(255, 521, 314)
