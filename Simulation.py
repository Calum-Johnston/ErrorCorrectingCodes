import random
import numpy
import math

#function randomMessage
#input: a number r
#output: a String m with length r
def randomMessage(r):
    message = []
    length = 2**r - r - 1
    for i in range(0, length):
        message.append(random.randint(0, 1))
    return message



#function encoder
#input: a String m
#output: a String c representing the codeword
def encoder(m):
    r = math.floor(math.log2(len(m))) + 1

    G = numpy.matrix(hammingGeneratorMatrix(r))   

    identityMatrix = numpy.matrix(numpy.identity(2**r-1))
    additionalColumn = numpy.ones((2**r-1, 1), dtype=int)
    M = numpy.append(identityMatrix, additionalColumn, axis=1)

    extG = (G * M) % 2
    
    m = numpy.matrix(m)
    c = (m * extG) % 2

    c = (c.A1).astype(int)

    return c



#function BSC
#input: a String c (codeword) and the crossover probability p
#output: the array v (representing a vector)
def BSC(c, p):
    v = c
    num = 1 / p
    for i in range(0, len(c) - 1):
        if(random.randint(1, num) == 1):
            v[i] = (v[i] + 1) % 2
    return v
        


#function syndrome
#input: an array v (vector)
#output: C, or a decoder failure
def syndrome(v):
    r = math.floor(math.log2(v.size)) 
    v = numpy.matrix(v)
    
    H = numpy.matrix(parityCheckMatrix(r))
    
    additionalRow = numpy.zeros((1, r), dtype=int)
    additionalColumn = numpy.ones(((2**r), 1),dtype=int)
    
    tempH = numpy.append(H, additionalRow, axis=0) 
    H = numpy.append(tempH, additionalColumn, axis=1)
    
    syn = (v * H) % 2
    syn = syn.A1
    pos = int(vectorToDecimal(syn))
    C = v.A1
    
    print("syndrome =", syn)
    print("i =", pos)

    if(pos != 0):
        C[pos - 1] = (C[pos - 1] + 1) % 2
    
    #Checks if a failure has occurred, if so, makes the first digit of the array 2
    if(syn[r] == 0) and (pos != 0):
        C[0] = 2
    
    return C


    
#function retrieveMessage
#input: the codeword C
#output: M, the estimate of the message
def retrieveMessage(c):
    m = []
    for i in range(0, c.size):
        pos = i + 1
        if not(math.log2(pos) == math.floor(math.log2(pos))):
               m.append(c[i])
    return m


        
#function HammingG
#input: a number r
#output: G, the generator matrix of the (2^r-1,2^r-r-1) Hamming code
def hammingGeneratorMatrix(r):
    n = 2**r-1
    
    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose    
    G = [list(i) for i in zip(*G)]

    return G



#function parityCheckMatrix
#input: a number r
#output: H, the transposed parity check matrix of the (2^r-1,2^r-r-1) Hamming code
def parityCheckMatrix(r):
    
    #construct H'
    H = []
    for i in range(1, 2**r):
        H.append(decimalToVector(i,r))
    H = numpy.matrix(H)

    return H
        


#function decimalToVector
#input: numbers n and r (0 <= n<2**r)
#output: a string v of r bits representing n
def decimalToVector(n,r): 
    v = []
    for s in range(r):
        v.insert(0,n%2)
        n //= 2
    return v



#function vectorToDecimal
#input: numbers n
#output: an integer v representing binary value n
def vectorToDecimal(n):
    count = 0
    number = 0
    for i in range(len(n) - 2, -1, -1):
        number += (2**count) * n[i]
        count += 1
    return number



#function simulation
#input: numbers r, N and p where r>=2, N>=1 and 0<=p<=1
#output: Something
def simulation(r, N, p):
    count = 1; successes = 0; failures = 0; errors = 0
    print(">>> r = %d; N = %d; p = %.2f" % (r, N, p))
    while(count <= N):
        print("\n>>> Simulation(%d, %d, %.2f)" % (r, N, p))
        print("*** Experiment %d of %d ***" % (count, N))
        
        #Generate Message
        m = randomMessage(r)
        print("\n* Source *")
        print("Message")
        print("m =", m)
        
        #Encode message
        c = encoder(m)
        print("\nCodeword")
        print("c =", c)
        
        #Transmit codeword
        v = BSC(c, p)
        print("\n* Channel *")
        print("Recieved vector")
        print("v =", v)
        
        #Decode codeword
        print("\n* Destination *")
        print("Decoding by syndrome")
        c = syndrome(v)
        if(c[0] == 2):
            failures += 1
            print("\nDecoding failure")
        else:
            print("\nCodeword estimate")
            print("hatc = ", c)
        
            #Retrieve message
            newm = retrieveMessage(c)
            print("\nMessage estimate")
            print("hatm =", newm)
    
            if(newm == m):
                successes += 1
                print("\nDecoding success")
            else:
                errors += 1
                print("\nDecoding error")
        
        count += 1
    print("\n*** End of experiments ***")
    print("\nSuccesses:", successes)
    print("Failures:", failures)
    print("Errors:", errors)
    print("\nExperimental DEP:", (errors/N))
        
    

simulation(12, 1, 0.01)
