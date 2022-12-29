# LogicalGateLib
## the function `Order(Times=[])`
Gets a list of numbers and returns a list of two sublists.

The first one contains the ranks corresponding to the 
expected position of each numbers in the inputed list 
if it was sorted from the smallest to the highest.
    
The second sublist is the sorted version of the inputed
list.
        
Examples:
-------
1) Input: [30,20,20]
 Output: [[3,1,2],[20,20,30]]
2) Order([30,20,10])=[[3,2,1],[10,20,30]]
    

    def Order(Times=[30,20,20]): 
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
    
## the function `Order(Orders=[],Times=[])`
Gets two lists of numbers and returns a boolean.
The first list contains ordinal numbers.
    
The answer is true if the second list is ordered 
according to the respective orders given in the
first list.
        
Examples:
-------
1) Input: Orders=[1,3,2]
Times=[10,20,30]
 Output: false
2) InOrder([1,3,2],[10,30,20])=True

  
    def InOrder(Orders=[1,3,2],Times=[10,20,30]): 
    Temp=[Times[int(Orders[i])-1] for i in range(len(Orders))]
    res=True
    for i in range(len(Orders)-1):
        res=(res and (Temp[i]<=Temp[i+1]))
    return res

## the function `def RemoveEmpty(ValuesIn=[],Orders=None,\Times=None,IndicesPrincipal=None)`

Takes as input four arguments:
ValuesIn: a list of list
Orders (default=None): a list of ordinal values
        
Times (default=None): a list of numbers
        
IndicesPrincipal (default=None): a list of numbers
        
When the lists 'Orders', 'Times' and 'IndicesPrincipal' are
non-zero they must be of the same length as the 'ValuesIn' list.

RemoveEmpty removes sub-lists of 'ValuesIn' and items with the same index in 
index in the 'Orders', 'Times' and 'IndicesPrincipal' lists.

Examples:
-------
1) Input: ValuesIn=[[],[1],[],[5]]
Times=None
Orders=None
 Output: false
 IndicesPrincipal=None
2) RemoveEmpty([[],[1],[],[5]],[1,2,3,4],[1,2,3,4],[1,0,1,1])= [[[1], [5]], [1], [2, 4], [0, 1]]
        
        
    def RemoveEmpty(ValuesIn=[[],[1],[],[5]],Orders=None,\
                Times=None,IndicesPrincipal=None):
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


   
## the function `Reductible(x=[],y=[])`

Gets in input two lists of numbers having the same length
and return True if they are different on exactly one term.

Examples:
-------
1) Input: ([1,0,1],[1,1,0])
Output: False
 IndicesPrincipal=None
2) Reductible([1,0,1],[1,0,0])=True        

  
    def Reductible(x=[1,0,1],y=[1,1,0]):
    res=False
    #Temp1=[x[i]-y[i] for i in range(len(x))]
    Temp2=sum([abs(x[i]-y[i]) for i in range(len(x))])
    if (Temp2==1):  #x est reductible par y
        res=True
        #for i in range(len(x)):
            #res.append(max(x[i],y[i])) 
    return res
    

