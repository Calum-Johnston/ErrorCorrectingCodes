import random
import numpy

#function simulation
#input: numbers r, N and p where r>=2, N>=1 and 0<=p<=1
#output: Something
def simulation(r, N, p):
    count = 1; successes = 0; failures = 0; errors = 0
    print(">>> r = %d; N = %d; p = %f" % (r, N, p))
    while(count <= N):
        print(">>> Simulation(" , r , "," , N , "," , p , ")")
        print("*** Experiment", count,"of", N ,"***")
        
        #Generate Message
        m = randomMessage(r)
        print("\n* Source *")
        print("Message")
        print("m =", m)
        
        #Encode message
        c = encoder(m, r)
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
        c = syndrome(v, r)
        print("\nCodeword estimate")
        print("hatc = ", c)
        
        #Retrieve message
        newm = retrieveMessage(c, r)
        print("\nMessage estimate")
        print("hatm =", newm)
        
        if(newm == m):
            successes += 1
        else:
            failures += 1
        
        count += 1
    print("\n*** End of experiments ***")
    print("\nSuccesses:", successes)
    print("Failures:", failures)
    print("Errors:", errors)
    print("\nExperimental DEP:", (successes/N) * 100)

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
def encoder(m, r):
    G = numpy.matrix(hammingGeneratorMatrix(r))
    
    identityMatrix = numpy.matrix(numpy.identity(2**r-1))
    additionalColumn = numpy.ones((2**r-1, 1), dtype=int)
    M = numpy.append(identityMatrix, additionalColumn, axis=1)

    extG = (G * M) % 2
    
    message = numpy.matrix(m)
    codeword =(message * extG) % 2
    
    return codeword



#function BSC
#input: a String c (codeword) and the crossover probability p
#output: the array v (representing a vector)
def BSC(c, p):
    codeword = numpy.squeeze(numpy.asarray(c))
    v = codeword
    num = 1 / p
    for i in range(0, len(codeword) - 1):
        if(random.randint(1, num) == 1):
            if(codeword[i] == 0):
                v[i] = 1
            elif(codeword[i] == 1):
                v[i] = 0
        else:
            v[i] == codeword[i]
    vector = numpy.matrix(v)
    return vector
        


#function syndrome
#input: an array v (vector)
#output: C, or a decoder failure
def syndrome(v, r):
    H = numpy.matrix(parityCheckMatrix(r))
    
    additionalRow = numpy.zeros((1, r), dtype=int)
    newH = numpy.append(H, additionalRow, axis=0)
    
    additionalColumn = numpy.ones(((2**r), 1),dtype=int)
    H = numpy.append(newH, additionalColumn
                     , axis=1)
    
    syn = (v * H) % 2
    pos = int(vectorToDecimal(syn))
    v = numpy.array(v)
    print("syndrome =", syn)
    print("i =", pos)

    if(pos != 0):
        if(v[0][pos - 1] == 0):
            v[0][pos - 1] = 1
        elif(v[0][pos - 1] == 1):
            v[0][pos - 1] = 0
            
    return v


    
#function retrieveMessage
#input: the codeword C
#output: M, the estimate of the message
def retrieveMessage(c, r):
    pos = 1
    message = []
    while(pos < 2**r):
        c[0][pos - 1] = 3
        pos = pos * 2
    c[0][2**r-1] = 3
    for i in range(0, 2**r):
        if(c[0][i] == 3):
            continue
        message.append(int(c[0][i]))
    return message
        
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
def  vectorToDecimal(n):
    arr = numpy.squeeze(numpy.asarray(n))
    count = 0
    number = 0
    for i in range(len(arr) - 2, -1, -1):
        number += (2**count) * arr[i]
        count += 1
    return number


simulation(3, 10, 0.1)
