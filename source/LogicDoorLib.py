""" Definition of logical gates
"""

def Order(Times=[30,20,20]): 
    """
    It takes a list of numbers and returns a list of two sublists. The first one contains the ranks
    corresponding to the expected position of each numbers in the inputed list if it was sorted from the
    smallest to the highest. The second sublist is the sorted version of the inputed list
    
    :param Times: The list of times for each person
    :return: A list of two sublists. The first one contains the ranks corresponding to the expected
    position of each numbers in the inputed list if it was sorted from the smallest to the highest. The
    second sublist is the sorted version of the inputed list.
    
    Examples:
    ---------


    >>> Times=[30,20,20]
    [[3,1,2],[20,20,30]]
    >>> Times=[30,20,10]
    [[3,2,1],[10,20,30]]
    """
    res=[[],[]]
    for i in range(len(Times)):
        j=1
        for k in range(len(Times)):
            if (Times[k]<Times[i]):
                j=j+1
        while (j in res[0]):
            j=j+1
        res[0].append(j) # res[0][i] Order of index i
        res[1].append(0) # res[1][i] Index of the order i
    for i in range(len(Times)):
        res[1][int(res[0][i])-1]=Times[i]
    return res
#print(Order.__doc__)
#print(Order())
#print(Order([30,20,10]))
    
def InOrder(Orders=[1,3,2],Times=[10,20,30]): 
    """
    It takes two lists of numbers and returns a boolean
    The first list contains ordinal numbers.
    The answer is true if the second list is ordered 
    according to the respective orders given in the
    first list.
    
    :param Orders: A list of numbers
    :param Times: The time at which each event occurred
    :return: a boolean.


    Examples:
    ---------

    >>> Orders=[1,3,2],Times=[10,20,30]
    False
    >>> Order([1,3,2],[10,30,20])
    True
    """
    Temp=[Times[int(Orders[i])-1] for i in range(len(Orders))]
    res=True
    for i in range(len(Orders)-1):
        res=(res and (Temp[i]<=Temp[i+1]))
    return res
#print(InOrder.__doc__)
#print(InOrder())
#print(InOrder([1,3,2],[10,30,20]))
    
def RemoveEmpty(ValuesIn=[[],[1],[],[5]],Orders=None,Times=None,IndicesPrincipal=None):
    """
    RemoveEmpty removes sub-lists of 'ValuesIn' and items with the same index in 
    index in the 'Orders', 'Times' and 'IndicesPrincipal' lists
    
    :param ValuesIn: a list of list
    :param Orders: a list of ordinal values
    :param Times: a list of numbers
    :param IndicesPrincipal: a list of numbers
    :return: A list of lists.
     
    Examples:
    ---------
    
    >>> ValuesIn=[[],[1],[],[5]],Orders=None,Times=None,IndicesPrincipal=None
    [[[1],[5]],None,None,None]
    """
    i=0
    n=len(ValuesIn)
    while (i<n):
        if (ValuesIn[i]==[]):
            del(ValuesIn[i])
            if (Orders!=None):
                del(Orders[i])
            if (Times!=None):
                del(Times[i])
            if (IndicesPrincipal!=None):
                del(IndicesPrincipal[i])
            i=i-1
            n=n-1
        i=i+1
    return [ValuesIn,Orders,Times,IndicesPrincipal]
#print(RemoveEmpty.__doc__)
#print(RemoveEmpty([[],[1],[],[5]],[1,2,3,4],[1,2,3,4],[1,0,1,1]))      

   
def Reductible(x=[1,0,1],y=[1,1,0]):
    """
    **Reductible** takes in input two lists of numbers having the same 
    length and return True if they are different on exactly one term
    
    :param x: the first list of numbers
    :param y: the target variable

    Exemples:
    ---------
    
    >>> x=[1,0,1],y=[1,1,0])    
    False  
    >>> x=[1,0,1],y=[1,0,0])
    True
    """
    res=False
    #Temp1=[x[i]-y[i] for i in range(len(x))]
    Temp2=sum([abs(x[i]-y[i]) for i in range(len(x))])
    if (Temp2==1):  #x est reductible par y
        res=True
        #for i in range(len(x)):
            #res.append(max(x[i],y[i])) 
    return res
#print(Reductible.__doc__)
#print(Reductible([1,0,1],[1,1,0]))
#print(Reductible([1,0,1],[1,0,0]))

    
def G_ID(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #Identité
    """
    It takes a list of lists of lists of numbers, and returns the same list of lists of lists of numbers
    
    :param ValuesIn: a list of lists of lists of values. The first list is the list of values for each
    time. The second list is the list of values for each order. The third list is the list of values for
    each index
    :param Orders: a list of lists of integers, each list of integers is a list of indices of the tensor
    to be contracted
    :param Times: a list of times at which the values are given
    :param IndicesPrincipal: The indices of the principal values
    :return: The input values.

    Examples:
    ---------
    
    >>> ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None
    [[[1, 0, 1], [1, 1, 0]], [[0, 1, 0]]]
    """

    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal) 
    return ValuesIn
#print(G_ID())

"""
def G_OR(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):
    res=[]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)
    Temp=ValuesIn.copy()
    for i in range(len(Temp)):
        for j in range(len(Temp[i])):
            if not(Temp[i][j] in res):
                res.append(Temp[i][j])
    return [res]

"""
def G_OR(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):
    """
The function takes as input a list of lists of vectors and returns a list of lists of vectors
    
    :param ValuesIn: a list of list
    :param Orders: a list of ordinal values
    :param Times: a list of numbers
    :param IndicesPrincipal: a list of numbers
    :return: the list of lists of the reductible vectors of the given vectors.
    
    Examples:
    ---------

    >>> [1,0,1],[1,1,0]],[[0,1,0]]   
    [[[1,0,1],[1,1,0]],[[1,0,0]]]
   
    """
    res=[]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    Temp=ValuesIn.copy()
    if (len(Temp)>0):
        res=Temp[0].copy()
        if (len(Temp)>1):
            for i in range(1,len(Temp)): 
                n=len(res)
                Temp1=[]
                # The above code is iterating through the list of lists and printing the values in
                # each list.
                # The above code is finding the reductible vectors of the given vectors.
                for j in range(len(Temp[i])):    
                    for l in range(n):
                        if (Reductible(Temp[i][j],res[l])):
                            Temp2=[]
                            for k in range(len(Temp[i][j])):
                                if (Temp[i][j][k]*res[l][k]==0):
                                    Temp2.append(0)
                                else:
                                    Temp2.append(max(-1,min(1,Temp[i][j][k]+res[l][k])))
                            if not(Temp2 in Temp1):
                                Temp1.append(Temp2)
                        else:
                            if not(res[l] in Temp1):
                                Temp1.append(res[l])
                            if not(Temp[i][j] in Temp1):
                                Temp1.append(Temp[i][j])
                res=Temp1
    return [res]
#print(G_OR())
#print(G_OR([[[1,0,1],[1,1,0]],[[1,0,0]]]))
    
def G_AND(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #AND
    """
    The above code is taking the cartesian product of the list of lists
    
    :param ValuesIn: This is the list of lists of lists of numbers
    :param Orders: a list of ordinal values
    :param Times: a list of numbers
    :param IndicesPrincipal: a list of numbers
    :return: The above code is returning the list of lists.
    
    Examples:
    ---------

    >>> ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]]  
    [[[1,0,1],[1,1,0]],[[1,0,0]]]
   
    """
    res=[]  #res=[[1,0,0],[0,1,0]]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)   #Suppression des portes vides
    Temp=ValuesIn.copy() #Temp=[[[1,0,1],[1,1,0]],[[0,1,0]]]
    if (len(Temp)>0):   #Temp=[[[1,0,1],[1,1,0]],[[0,1,0]]]
        res=Temp[0].copy()  #res=[[1,0,1],[1,1,0]]
        if (len(Temp)>1):   
           # The above code is taking the cartesian product of the list of lists.
            # The above code is iterating through the list of strings and printing the strings in the
            # list.
            # The above code is looping through the list of strings and printing the strings.
            for i in range(1,len(Temp)): 
                n=len(res)
                Temp1=[]
                for j in range(len(Temp[i])):    
                    for l in range(n):
                        Temp2=[]
                        for k in range(len(Temp[i][j])):
                            if (Temp[i][j][k]*res[l][k]!=-1):
                                Temp2.append(max(-1,min(1,Temp[i][j][k]+res[l][k])))
                            else:
                                print("Bad")
                        if ((len(Temp2)==len(Temp[i][j])) and (not(Temp2 in Temp1))):
                            Temp1.append(Temp2)
                res=Temp1
    return [res]
#print(G_AND())
    
def G_NOT(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #NOT
    """
    This function takes a list of lists of lists of integers as input and returns a list of lists of
    integers as output
    
    :param ValuesIn: The input values
    :param Orders: The order of the gates
    :param Times: The time at which the gate is applied
    :param IndicesPrincipal: The indices of the principal values
    :return: the negation of the input.
    
    Exemples:
    -------

    >>> ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]]  
    [[1,0,1],[1,1,0]]
    """
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal) 
    res=ValuesIn.copy()
    l=len(res)
    for i in range(l): #res=[[1,0,1],[1,1,0]]
        ll=len(res[i])
        if (ll==1):
            lll=len(res[i][0])
            if (sum([abs(res[i][0][k]) for k in range(lll)])<=1):
                for j in range(lll):
                    res[i][0][j]=-res[i][0][j]
            else:
                Temp1=[]
                for j in range(lll):
                    if (res[i][0][j]!=0):
                        Temp2=[0 for k in range(lll)]
                        Temp2[j]=res[i][0][j]
                        Temp1.append(G_NOT([[Temp2]])[0])
                res=G_OR(Temp1)
        else:
            res[i]=G_AND([G_NOT([[res[i][j]]])[0] for j in range(ll)])[0]
    return res
#print(G_NOT())
    
def G_PAND(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[0,0,0],IndicesPrincipal=None): #PAND
    """
    This function is a gate that is a combination of the AND gate and the PAND gate
    
    :param ValuesIn: a list of lists of lists of integers. The first list is the list of inputs, the
    second list is the list of values for each input, and the third list is the list of values for each
    input at each time
    :param Orders: a list of the order of each input
    :param Times: a list of the times at which the inputs are applied
    :param IndicesPrincipal: This is a list of indices that you can use to specify which values in
    ValuesIn you want to use
        
    Examples:
    ---------

    >>> ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[0,0,0],IndicesPrincipal=None 
    Porte PAND appellee 1
    [[[1, 1, 1], [1, 1, 0]]]
             
    """
    res=[[]]
    if InOrder(Orders,Times):
        res=G_AND(ValuesIn,Orders,Times,IndicesPrincipal)
        print("Porte PAND appellee 1")
    else:
        print("Porte PAND appellee 2") 
        if (len(ValuesIn)>0):
            n=len(ValuesIn[0][0])
            res[0]=[[0 for i in range(n)]]
            #print(Orders)
            #print(Times)
    return res
#print(G_AND())

def G_FDEP(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #
    """
    It takes a list of lists of lists and returns a list of lists.
    
    :param ValuesIn: a list of lists of lists of integers. Each list of lists of integers represents a
    gate. Each list of integers represents a time. Each integer represents a value
    :param Orders: a list of lists of integers, each list of integers representing a gate
    :param Times: The time at which the gate is applied
    :param IndicesPrincipal: The indices of the principal qubits
    
    Examples:
    ---------

    >>> ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]] 
    [[1,0,1],[1,1,0]]
    """
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    res=[[]]    #res=[[1,0,1],[1,1,0]]
    Temp=ValuesIn.copy()
    if (len(Temp)>0):
        res=[Temp[0].copy()]
        if (len(Temp)>1):
            res=G_OR(G_NOT(res)+[Temp[i] for i in range(1,len(Temp))]) 
    return res
#print(G_FDEP())
    
def G_SPARE(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=[30,20],IndicesPrincipal=[1,0]):   #SPARE
    """
    The function G_SPARE takes as input a list of lists of lists of integers, a list of integers, a
    list of integers and a list of integers. It returns a list of lists of integers
    
    :param ValuesIn: The list of the values of the variables
    :param Orders: The order of the variables in the list
    :param Times: [30,20]
    :param IndicesPrincipal: This is a list of 0s and 1s. The length of this list is the same as the
    length of the list of values. The 1s in this list indicate the values that are to be used in the
    final result. The 0s indicate the values that are to be used in the
    :return: the values of the variables in the order of the times of the variables.
    
    Examples:
    ---------

    >>> ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Times=[30,20],IndicesPrincipal=[1,0]
    [[1,0,1],[1,1,0]]

    """
   # Removing empty values from the list.
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    Temp1=[]
    Temp2=[]
   # Taking the values of the variables in the order of the times of the variables.
    for i in range(len(IndicesPrincipal)):  #IndicesPrincipal=[1,0]
        if (IndicesPrincipal[i]==1):
            Temp1.append(i)
        elif (IndicesPrincipal[i]==0):
            Temp2.append(i)
    Orders=Order(Times)[1]  #Orders=[0,1]
    Temp3=[Orders[i] for i in Temp1]
    Temp4=[Orders[i] for i in Temp2]
    Temp5=ValuesIn.copy()
    res=[]
    for i in range(len(Temp3)): #Temp3=[0,1]
        if (i<len(Temp4)):
            res+=G_AND([Temp5[int(Temp3[i])]]+[Temp5[int(Temp4[i])]])
        else:
            res+=[Temp5[int(Temp3[i])]]
    return res
#print(G_SPARE())

def G_Gen(n=1,ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[30,20,40],IndicesPrincipal=[1,0]):
    """
    G_Gen is a function that returns a list of lists of values of G_Input, G_ID, G_NOT, G_OR, G_AND,
    G_PAND, G_FDEP, G_SPARE
    
    :param n: the number of elements in the list, defaults to 1 (optional)
    :param ValuesIn: the input values of the gate
    :param Orders: The order of the gate
    :param Times: the time of each element
    :param IndicesPrincipal: the index of the main input
    :return: a list of lists.
    
    Examples:
    ---------

    >>> n=1,ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[30,20,40],IndicesPrincipal=[1,0]
    [[[1, 0, 1], [1, 1, 0]], [[0, 1, 0]]]
    """
    if n==0:
        return G_ID(ValuesIn,Orders,Times,IndicesPrincipal)  
    elif n==1:  
        return G_ID(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==2:
        return G_NOT(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==3:
        return G_OR(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==4:
        return G_AND(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==5:
        return G_PAND(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==6:
        return G_FDEP(ValuesIn,Orders,Times,IndicesPrincipal)
    else:
        return G_SPARE(ValuesIn,Orders,Times,IndicesPrincipal)

#print(G_Gen())
        
def ID_G(n=1):  #ID_G
    """
    This function returns the ID of the gate
    
    :param n: the number of inputs to the gate, defaults to 1 (optional)
    :return: The ID of the gate.
    
    Examples:
    ---------

    >>> n=1
    G_ID
    """
    if n==0:
        return "G_Input"
    elif n==1:
        return "G_ID"
    elif n==2:
        return "G_NOT"
    elif n==3:
        return "G_OR"
    elif n==4:
        return "G_AND"
    elif n==5:
        return "G_PAND"
    elif n==6:
        return "G_FDEP"
    else:
        return "G_SPARE"
#print(ID_G())  #ID==


