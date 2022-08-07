"""
Definition des portes
"""

def Order(Times=[30,20,20]): #Ordre des portes
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
        res[1][int(res[0][i])-1]=i
    return res
#print(Order())
#print(Order([30,20,10]))
    
def InOrder(Orders=[1,3,2],Times=[10,20,30]): #Ordre des portes
    Temp=[Times[int(Orders[i])-1] for i in range(len(Orders))]
    res=True
    for i in range(len(Orders)-1):
        res=(res and (Temp[i]<=Temp[i+1]))
    return res
#print(InOrder())
#print(InOrder([1,3,2],[10,30,20]))
    
def RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal):    #Suppression des portes vides
    i=0
    n=len(ValuesIn)
    while (i<n):
        if (ValuesIn[i]==[]):
            del(ValuesIn[i])
            if (Times!=None):
                del(Times[i])
            if (IndicesPrincipal!=None):
                del(IndicesPrincipal[i])
            i=i-1
            n=n-1
        i=i+1
    return [ValuesIn,Orders,Times,IndicesPrincipal]
#print(RemoveEmpty([[],[1],[],[5]],[1],[1,2,3,4],[1,0,1,1]))      
    
def Reductible(x,y):   #x est reductible par y
    res=False
    #Temp1=[x[i]-y[i] for i in range(len(x))]
    Temp2=sum([abs(x[i]-y[i]) for i in range(len(x))])
    if (Temp2==1):  #x est reductible par y
        res=True
        #for i in range(len(x)):
            #res.append(max(x[i],y[i])) 
    return res
#print(Reductible([1,0,1],[1,1,0]))
#print(Reductible([1,0,1],[1,0,0]))
    
def P_ID(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #Identité
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)
    return ValuesIn
#print(P_ID())

"""
def P_OR(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):
    res=[]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)
    Temp=ValuesIn.copy()
    for i in range(len(Temp)):
        for j in range(len(Temp[i])):
            if not(Temp[i][j] in res):
                res.append(Temp[i][j])
    return [res]
"""
def P_OR(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):  #OR
    res=[]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    Temp=ValuesIn.copy()
    if (len(Temp)>0):
        res=Temp[0].copy()
        if (len(Temp)>1):
            for i in range(1,len(Temp)): 
                n=len(res)
                Temp1=[]
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
#print(P_OR())
#print(P_OR([[[1,0,1],[1,1,0]],[[1,0,0]]]))
    
def P_AND(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #AND
    res=[]  #res=[[1,0,0],[0,1,0]]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)   #Suppression des portes vides
    Temp=ValuesIn.copy() #Temp=[[[1,0,1],[1,1,0]],[[0,1,0]]]
    if (len(Temp)>0):   #Temp=[[[1,0,1],[1,1,0]],[[0,1,0]]]
        res=Temp[0].copy()  #res=[[1,0,1],[1,1,0]]
        if (len(Temp)>1):   
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
#print(P_AND())
    
def P_NOT(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #NOT
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
                        Temp1.append(P_NOT([[Temp2]])[0])
                res=P_OR(Temp1)
        else:
            res[i]=P_AND([P_NOT([[res[i][j]]])[0] for j in range(ll)])[0]
    return res
#print(P_NOT())
    
def P_PAND(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[0,0,0],IndicesPrincipal=None): #PAND
    res=[[]]
    if InOrder(Orders,Times):
        res=P_AND(ValuesIn,Orders,Times,IndicesPrincipal)
        print("Porte PAND appellee 1")
    else:
        print("Porte PAND appellee 2") 
        if (len(ValuesIn)>0):
            n=len(ValuesIn[0][0])
            res[0]=[[0 for i in range(n)]]
            #print(Orders)
            #print(Times)
    return res
#print(P_AND())
    
def P_FDEP(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):    #FDEP
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    res=[[]]    #res=[[1,0,1],[1,1,0]]
    Temp=ValuesIn.copy()
    if (len(Temp)>0):
        res=[Temp[0].copy()]
        if (len(Temp)>1):
            res=P_OR(P_NOT(res)+[Temp[i] for i in range(1,len(Temp))])
    return res
#print(P_FDEP())
    
def P_SPARE(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=[30,20],IndicesPrincipal=[1,0]):   #SPARE
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    Temp1=[]
    Temp2=[]
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
            res+=P_AND([Temp5[int(Temp3[i])]]+[Temp5[int(Temp4[i])]])
        else:
            res+=[Temp5[int(Temp3[i])]]
    return res
#print(P_SPARE())

def P_Gen(n=1,ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[30,20,40],IndicesPrincipal=[1,0]):   #GEN
    if n==0:
        return P_ID(ValuesIn,Orders,Times,IndicesPrincipal)  
    elif n==1:  
        return P_ID(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==2:
        return P_NOT(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==3:
        return P_OR(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==4:
        return P_AND(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==5:
        return P_PAND(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==6:
        return P_FDEP(ValuesIn,Orders,Times,IndicesPrincipal)
    else:
        return P_SPARE(ValuesIn,Orders,Times,IndicesPrincipal)

#print(P_Gen())
        
def ID_P(n=1):  #ID_P
    if n==0:
        return "P_Input"
    elif n==1:
        return "P_ID"
    elif n==2:
        return "P_NOT"
    elif n==3:
        return "P_OR"
    elif n==4:
        return "P_AND"
    elif n==5:
        return "P_PAND"
    elif n==6:
        return "P_FDEP"
    else:
        return "P_SPARE"
#print(ID_P())  #ID_P