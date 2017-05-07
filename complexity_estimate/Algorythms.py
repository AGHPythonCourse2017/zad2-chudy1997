def exampleLOGN(a):
    i = 0
    while i<len(a):
        i = 2*i+1
        for j in range(1,100):
            j=(2*j+1-1)/2

def exampleN(a):
    for i in range(1,len(a)):
        for j in range(1,100):
            j=(2*j+1-1)/2

def exampleNLOGN(a):
    for i in range(1,len(a)):
        j = 0
        while j < len(a):
            j = 2 * j + 1
            for k in range(1, 100):
                k = (2 * k + 1 - 1) / 2

def exampleNN(a):
    for passnum in range(len(a) - 1, 0, -1):
        for i in range(passnum):
            if a[i] > a[i + 1]:
                temp = a[i]
                a[i] = a[i + 1]
                a[i + 1] = temp

def exampleNNN(a):
    for i in range(1,len(a)):
        for j in range(1, len(a)):
            for k in range(1, len(a)):
                l=i*2+j*3+k*4
