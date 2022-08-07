
"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go
#from numpy import matlib # importer le module matlib 

import sympy
import networkx as nx
import  matplotlib.pyplot  as  plt

from DFT2HD2ReliabilityR.DefaultTreeLib import *

"""
Construction des coupes minimales
"""

Cuts={} # dictionary of cuts
class Cut:  # cut class
    NCut=0      # Number of cuts
    def __init__(self,Tree=DefaultTree(2),IndivIndex=[0]):  # cut class
        self.id=id(self)                             # id of the cut
        Cuts[str(self.id)]=self                     # add the cut to the dictionary
        self.__class__.NCut+=1                    # increase the number of cuts
        self.Tree=Tree                          # fault tree
        self.IndIndex=IndivIndex            # list of indices of the components
        self.NComponent=len(self.IndIndex)  # number of components
        self.NNode=0                      # number of nodes
        self.Node={}                  # list of nodes
        self.NCut=0                     # number of cuts
        self.Cut=[]                 # list of cuts
        self.RelMat=[[],[],[],[],[],[],[],[]]   # list of relations
        #[[NumRel],[Node i],[Node j],[Door],[Orders],[Times],[IndicesPrincipal],[Result]]
        
    def __del__(self):      # delete the cut
        self.__class__.NCut-=1  # decrease the number of cuts
        
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):  # return the inorder of the cut
        res=True                             # return the inorder of the cut
        i=0                                 # index of the first node
        while ((res==True) and (i<min(len(xx),len(yy)))):   # while the inorder is correct
            res=(res and (xx[i]<=yy[i]))    # check the inorder
            i=i+1                       # increase the index
        return res                        # return the inorder of the cut
    
    def Leaves(self):   # return the leaves of the cut
        Temp1=self.Tree.Leaves()    # return the leaves of the tree
        #print("\n DT leaves")  # print the leaves of the tree
        #print(Temp1)
        n=len(Temp1)         # number of leaves
        res=[]              # list of leaves
        for i in range(n):  # for each leaf
            Leaf=[]        # list of leaves
            #Temp2=self.Tree.Node[Temp1[i]]
            #print("\n Raw leaf :")
            #print(Temp2)
            #print(self.IndIndex)
            #print(self.NComponent)
            for k in range(self.NComponent):    # for each component
                Temp3=[0 for l in range(self.NComponent)]   # list of components
                Temp3[k]=1                              # set the component
                #print("\n Cutomized leaf :")
                #print(Temp3)
                Leaf+=[[Temp3]]
            #if (Leaf!=[]):
            res.append([Temp1[i],Leaf]) # add the leaf to the list
            #print("\n Leaf:")
            #print(Leaf)
        return res               # return the leaves of the cut

    def CollectCut(self):   # return the cut
        Temp1=self.Leaves()   # return the leaves of the cut
        #print("\n Customized DT Leaves")
        #print(Temp1)
        Temp2=self.Tree.IdxTable            # return the index table of the tree
        #print("\n Index Table")
        #print(Temp2)
        #[[NumRel],[Node i],[Node j]]
        Temp3=self.Tree.RelMat            # return the relations of the tree
        #print("\n Tree.RelMat")
        #print(Temp3)
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        for i in range(len(Temp1)): # for each leaf
            self.NNode+=1          # increase the number of nodes
            self.Node[Temp1[i][0]]=Temp1[i][1]  # add the leaf to the list of nodes
            #self.Cut=P_Gen(3,[self.Cut]+Temp1[i][1])[0]
            #self.NCut=len(self.Cut)
        #print("\n Nodes")
        #print(self.Node)   
        for i in range(len(Temp2[0])):  # for each relation
            #[[NumRel],[Node i],[Node j],[Door],[Orders],[Times],[IndicesPrincipal],[Result]]
            self.RelMat[0].append(Temp2[0][i])      # add the relation number    
            self.RelMat[1].append(Temp2[1][i])    # add the node i
            self.RelMat[2].append(Temp2[2][i])      # add the node j
            self.RelMat[3].append(Temp3[0][i])    # add the door
            self.RelMat[4].append(Temp3[3][i])  # add the orders
            self.RelMat[5].append(Temp3[4][i])  # add the times
            self.RelMat[6].append(Temp3[5][i])  # add the indices principal
            for x in self.Tree.Node:    # for each node
                if (self.Tree.IdxNode(x) in self.Node): # if the node is in the cut
                    y=self.Tree.Node[self.RelMat[1][-1]]    # return the node i
                    Test=(x!=y) and (self.InOrder2(x,y))    # check the inorder
                    Test=(Test and (self.Tree.AdjMat[self.Tree.IdxNode(y)][self.Tree.IdxNode(x)]==0))   # check the adjacency
                    Test=(Test and (self.Tree.AdjMat[self.Tree.IdxNode(x)][self.Tree.IdxNode(y)]==0))   # check the adjacency
                    if (Test):      
                        self.Node[self.RelMat[1][-1]]+=self.Node[self.Tree.IdxNode(x)]
                        #print("\n Added vertice")
                        #print([self.Tree.IdxNode(x),self.Node[self.Tree.IdxNode(x)]])
            #print("\n Actualised vertice")
            #print([self.RelMat[1][-1],self.Node[self.RelMat[1][-1]]])
            #print("\n Door")
            #print(ID_P(self.RelMat[3][-1]))
            #print("\n Input")
            #print(self.Node[self.RelMat[1][-1]])
            #print("\n P_Gen gives")
            #print(P_Gen(self.RelMat[3][-1],self.Node[self.RelMat[1][-1]],self.RelMat[4][-1],self.RelMat[5][-1],self.RelMat[6][-1])[0])
            if not(self.RelMat[2][-1] in self.Node):    # if the node is not in the cut
                self.NNode+=1       # increase the number of nodes
                self.Node[self.RelMat[2][-1]]=P_Gen(self.RelMat[3][-1],self.Node[self.RelMat[1][-1]],self.RelMat[4][-1],self.RelMat[5][-1],self.RelMat[6][-1])
                #self.Cut=P_Gen(3,[self.Cut]+self.Node[self.RelMat[2][-1]])[0]
                #self.NCut=len(self.Cut)
                """
                if (self.Node[self.RelMat[2][-1]]==[[]]):
                    print("Here Bad")
                    print(self.RelMat[3][-1])
                    print(self.Node[self.RelMat[1][-1]])
                """
            self.RelMat[7]+=self.Node[self.RelMat[2][-1]]
            
        
        #print("\n RelMat in CollectCut in ")
        #print(self.RelMat)
        
        self.Cut=self.RelMat[7][-1]
        self.NCut=len(self.Cut)

"""
MyTree=DefaultTree(3)
MyTree.NewRelation(3,[1,1,0],[0,0,1])

MyCut=Cut(MyTree,[0])
print(MyCut.NComponent)
print(MyCut.Tree.Node)
print(MyCut.Leaves())

MyCut.CollectCut()
print(MyCut.NCut)
print(MyCut.Cut)

print(MyCut.RelMat)
print(MyCut.NNode)
print(MyCut.Node)

"""

"""
Construction des liens minimaux
"""

Links={}    # dictionnary of links  with the number of links
class Link: # class of links    #[[NumRel],[Node i],[Node j]]
    NLink=0     # number of links   
    def __init__(self,Tree=DefaultTree(2),IndivIndex=[0]):  # constructor
        self.id=id(self)    # id of the link
        Links[str(self.id)]=self    # add the link to the dictionnary
        self.__class__.NLink+=1  # increase the number of links
        self.Tree=Tree  # tree of the link
        self.IndIndex=IndivIndex    # index of the individual
        self.NComponent=len(self.IndIndex)  # number of components

        self.NNode=0    # number of nodes
        self.Node={}    # list of nodes
        self.NLink=0    # number of links
        self.Link=[]    # list of links
        self.NMinLink=0   # number of minimal links
        self.MinLink=[]  # list of minimal links
        
        def InOrder3(xx=[1,0,1],yy=[0,-1,-1]):  # function to check the inorder of the nodes
            #print([xx,yy])
            res=True
            i=0
            while ((res==True) and (i<min(len(xx),len(yy)))):   # while the inorder is correct and the number of nodes is less than the number of nodes of the tree (the last node is not in the tree)
                if (xx[i]*yy[i]!=0):    # if the inorder is not correct
                    res=(res and (xx[i]<=yy[i]))    # check the inorder
                i=i+1   # increase the index
            return res  # return the result
        
        def TrueVal1(xx=[1,0],yy=[0,-1]):   # function to check the inorder of the nodes
            res=xx.copy()   # copy the list
            if InOrder3(xx,yy):   # if the inorder is correct
                i=0 
                while (i<min(len(xx),len(yy))):  # while the number of nodes is less than the number of nodes of the tree (the last node is not in the tree)
                    if (xx[i]*yy[i]==0) and (xx[i]+yy[i]!=0):
                        res[i]=1
                    i=i+1
            return res
        
        def TrueVal2(xx=[1,0],yy=[[0,-1]]):
            res=xx.copy()
            i=0
            while (i<len(yy)):
                res=TrueVal1(res,yy[i])
                i=i+1
                #print(res)
            return res
        
        #print(TrueVal2([0,1,0],[[0,-1,0],[0,0,-1]]))
        self.Cut=Cut(self.Tree,self.IndIndex)
        self.Cut.CollectCut() 
        
        for x in self.Cut.Cut:
            for i in range(len(x)):
                x[i]=-x[i]
        
        if (self.Cut.Cut!=[]):
            temp=P_NOT([self.Cut.Cut])
            if (temp!=[]):
                self.Link=temp[0]
        else:
            temp=[]
            for i in range(self.NComponent):
                tempBis=[0 for j in range(self.NComponent)]
                tempBis[i]=1
                temp.append(tempBis)
            self.Link=temp
            #print("Here")
            #print(self.Link)
        
        self.NLink=len(self.Link)   # number of links
        
        #print("\n Minimal Cuts: ")
        #print(self.Cut.Cut)
        
        #print("\n Raw set of Links: ")
        #print(self.Link)
        
    def __del__(self):
        self.__class__.NLink-=1
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):  # function to check the inorder of the nodes
        res=True
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))):   # while the inorder is correct and the number of nodes is less than the number of nodes of the tree (the last node is not in the tree)
            res=(res and (xx[i]<=yy[i]))
            i=i+1
        return res      

    def CollectLink(self):  # function to collect the links
        #Temp=self.Node.copy()
        #nn=len(Temp)     
        def InOrder3(xx=[1,0],yy=[0,-1]):   # function to check the inorder of the nodes
            res=True
            i=0
            while ((res==True) and (i<min(len(xx),len(yy)))):
                if (xx[i]*yy[i]!=0):
                    res=(res and (xx[i]<=yy[i]))
                i=i+1
            return res
        
        def InOrder4(xx=[1,0],yy=[[0,-1],[-1,0]]):  # function to check the inorder of the nodes
            res=False
            i=0
            while (not(res) and (i<len(yy))):
                res=(res or InOrder3(xx,yy[i]))
                i=i+1
            return res
        
        Order=[]    # list of inorder
        for y in self.Link: # for each link
            if not(y in [self.Node[k] for k in self.Node.keys()]):
                self.Node[self.NNode]=y
                self.NNode+=1
                Order.append(0)
                for x in self.Link:
                    if ((x!=y)and(self.InOrder2(x,y))):
                        Order[-1]+=1
                if (Order[-1]==0):
                    if not(y in self.MinLink):
                        self.MinLink.append(y)
                        self.NMinLink+=1
                        #print("\n Minimal Links step")
                        #print(self.MinLink)
        """
        kkk=0
        while ((len(Temp)>0)and(kkk<0)):#and(kkk<10)
            kkk+=1
            print(kkk)
            #print("\n Links")
            #print(Temp)
            for l in Temp.keys():
                Son={}
                for k in range(len(Temp[l])):
                    Sonl=Temp[l].copy()
                    if (Sonl[k]>-1):
                        Sonl[k]=-1
                        if not(InOrder4(Sonl,self.Cut.Cut)):
                            Son[nn]=Sonl
                            nn+=1
                #print("\n Son:")
                #print(Son)
                Temp1=Temp.copy()
                if (Son=={}):
                    if not(Temp1[l] in self.MinLink):
                        self.MinLink.append(Temp1[l])
                        self.NMinLink+=1
                        print("\n Minimal Links step")
                        print(self.MinLink)
                    del[Temp1[l]]
                else:
                    for k in Son.keys():
                        Temp1[k]=Son[k]
            Temp=Temp1.copy()
        """   
"""
MyTree=DefaultTree(3)
MyTree.NewRelation(3,[1,1,0],[0,0,1])

MyLink=Link(MyTree,2)

MyLink.CollectLink()

print(MyLink.NLink)
print(MyLink.Link)

print(MyLink.NMinLink)
print(MyLink.MinLink)
"""

"""
Construction du diagramme de Hasse et Calcul du polynôme de fiabilité
"""

def One(x):     # function to check if x is a one
    return 1
            
DownHasseDiagrams={}    # dictionary of the down hasse diagrams
class DownHasseDiagram: # class of the down hasse diagrams
    NDownHasseDiagram=0     # number of down hasse diagrams
    
    def __init__(self,Tree=DefaultTree(2),IndivIndex=[0],IndivLabel=[0],IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1):   # constructor
        self.id=id(self)    # id of the down hasse diagram  
        DownHasseDiagrams[str(self.id)]=self    # adding the down hasse diagram to the dictionary
        self.__class__.NDownHasseDiagram+=1  # incrementing the number of down hasse diagrams
        self.Tree=Tree  # tree of the down hasse diagram
        self.IndIndex=IndivIndex    # index of the individuals  of the down hasse diagram
        self.IndLabel=IndivLabel    # label of the individuals of the down hasse diagram
        self.IndFiabVal=IndivReliabilityVal   # reliability value of the individuals of the down hasse diagram  
        self.IndFiabFunc=IndivReliabilityFunc   # reliability function of the individuals of the down hasse diagram
        self.NComponent=len(self.IndLabel)  # number of components of the down hasse diagram
        self.Time=t # time of the down hasse diagram
        self.Option=Option  # option of the down hasse diagram
        self.Times=[0 for i in range(self.NComponent)]  # list of times of the down hasse diagram
        self.Order=[0 for i in range(self.NComponent)]  # list of orders of the down hasse diagram
        self.IndicesPrincipal=[1 for i in range(self.NComponent)]       # list of indices of the principal components of the down hasse diagram    
        self.NNode=0    # number of nodes of the down hasse diagram
        self.Node={}    # dictionary of the nodes of the down hasse diagram
        self.NCut=0    # number of cuts of the down hasse diagram
        self.Cut=[]   # list of cuts of the down hasse diagram
        
        MyCut=Cut(self.Tree,self.IndIndex)  # cut of the down hasse diagram 
        MyCut.CollectCut()  # collecting the cuts of the down hasse diagram
        self.MinCut=MyCut.Cut   # minimal cuts of the down hasse diagram
        
        #print("\n Minimal Cuts")
        #print(MyCut.Cut)
        
        
        for i in range(len(self.MinCut)):   # for each minimal cut
            self.Node[i]=self.MinCut[i].copy()  # adding the nodes of the cut to the down hasse diagram
            self.Cut.append(self.MinCut[i].copy())  # adding the cut to the down hasse diagram
            self.NNode+=1   # incrementing the number of nodes of the down hasse diagram
            self.NCut+=1    # incrementing the number of cuts of the down hasse diagram

        self.NodeGeneration=[self.MinCut]   # list of the nodes of the down hasse diagram
        
        while (self.NodeGeneration[-1]!=[[1 for j in range(self.NComponent)]]): # while the last node of the list of nodes is not the last node
            Leaves=[]   # list of leaves of the last node of the list of nodes
            for Leaf in self.NodeGeneration[-1]:    
                
                for k in range(len(Leaf)):
                    NewLeaf=Leaf.copy()
                    if (NewLeaf[k]<1):
                        NewLeaf[k]+=1
                        if (not(NewLeaf in Leaves) and not(NewLeaf in self.Cut)):
                            Leaves.append(NewLeaf.copy())
                            self.Node[len(self.Node)]=NewLeaf.copy()
                            self.Cut.append(NewLeaf.copy())
                            self.NNode+=1
                            self.NCut+=1
            self.NodeGeneration.append(Leaves) 
            #print("\n New generation")
            #print(self.NodeGeneration[-1])

        #print("\n All cuts generated")
        
        """
        def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):
            i=min(len(xx),len(yy))-1
            while ((xx[i]==yy[i]) and (i>=0)):
                #print((xx,yy))
                i=i-1
            if (i<0):
                res=True
            else:
                res=(xx[i]<yy[i])
            return res
        
        """
        def InOrder2(x=[0,0,1],y=[0,1]):    # function to check if x is in order of y
            res=True
            if (x!=None) and (y!=None):
                for i in range(min(len(x),len(y))):
                    res=res and (x[i]<=y[i])
            return res
        
        self.AdjMat={i:[0 for j in range(len(self.Node))] for i in self.Node.keys()}  # adjacency matrix of the down hasse diagram
        for i in self.Node.keys():
            for j in self.Node.keys():
                if ((i!=j) and InOrder2(self.Node[i],self.Node[j])):
                    self.AdjMat[i][j]=1
        
        def UpdateGeneration(): # function to update the generation of the down hasse diagram   
            kk=min([sum(self.MinCut[i]) for i in range(len(self.MinCut))])
            depth=self.NComponent-kk+1
            #print("\n Depth:")
            #print(depth)
            temp=[[] for i in range(depth)]
            #print("\n Nodes:")
            #print(self.Node)
            for i in self.Node.keys():
                j=sum(self.Node[i])
                temp[depth+kk-j-1].append(i)
                #print("\n Generations:")
                #print(temp)
            self.NodeGeneration=temp.copy()          
            
        self.WeightTable=[[],[],[],[],[]] # weight table of the down hasse diagram
        #[[Index],[minimalité], [poids], [coef poly fiab], [code coupe]]
        
        def InitWeight():   # function to initialize the weight table of the down hasse diagram 
            for i in self.Node.keys():
                self.WeightTable[0].append(i)
                self.WeightTable[3].append(0)
                self.WeightTable[4].append(self.Node[i])
                if (self.Node[i] in self.MinCut):
                    self.WeightTable[1].append(1)
                    self.WeightTable[2].append(1)
                else:
                    self.WeightTable[1].append(0)
                    self.WeightTable[2].append(0)
                    for j in self.Node.keys():
                        if (i!=j) and InOrder2(self.Node[j],self.Node[i]) and (self.Node[j] in self.MinCut):
                            self.WeightTable[2][-1]+=1
            #print("\n Current weights")
            #print(self.WeightTable[2])
            #print("\n Current Nodes")
            #print(self.Node)
        
        def UpdatePolyDeFiab(): # function to update the polynomial of defiability of the down hasse diagram
            UpdateGeneration()
            for i in range(len(self.NodeGeneration)-1,-1,-1):   # for each generation
                for j in self.NodeGeneration[i]:
                    if ((self.Node[j] in self.MinCut)):# and (self.WeightTable[2][j]==1)):
                        self.WeightTable[3][j]+=1
                        #print("\n Leaf Adding")
                        #print(self.Node[j])
                    while ((self.WeightTable[2][j]>1)): # while the number of cuts of the node is greater than 1
                        for k in self.Node.keys():
                            if InOrder2(self.Node[j],self.Node[k]):
                                self.WeightTable[2][k]-=1
                                if (k==j):
                                    self.WeightTable[3][k]-=1
                                    #print("\n Branch removal")
                                    #print(self.WeightTable[2])
                    while ((self.WeightTable[2][j]<1)): # while the number of cuts of the node is less than 1
                        for k in self.Node.keys():
                            if InOrder2(self.Node[j],self.Node[k]):
                                self.WeightTable[2][k]+=1
                                if (k==j):
                                    self.WeightTable[3][k]+=1
                                    #print("\n Branch addition")
                                    #print(self.WeightTable[2])
            #print("\n The sum of weights should be nonegative and less than the number of leaves")
            #print(sum(self.WeightTable[3]))
        
        InitWeight()    # initialize the weight table of the down hasse diagram
        UpdatePolyDeFiab()  # update the polynomial of defiability of the down hasse diagram
        #print("Unreliability polynomial")

    def __del__(self):  # destructor
        self.__class__.NDownHasseDiagram-=1
        
    def GetPolyFiab(self):  # function to get the polynomial of defiability of the down hasse diagram
        #R=[sympy.Symbol("R"+str(self.IndIndex[i])) for i in range(self.NComponent)]
        R=self.IndLabel     # list of the variables of the polynomial of defiability
        if (self.Option==1):    # if the option is 1, the polynomial of defiability is the polynomial of reliability
            R2=[[self.IndFiabVal[i][j] for j in range(len(self.Time))] for i in range(self.NComponent)]
        else:
            R2=[[self.IndFiabFunc[i](self.Time[j]) for j in range(len(self.Time))] for i in range(self.NComponent)]
        P=0
        P2=[0 for k in range(len(self.Time))]
        for i in self.WeightTable[0]:
            Temp=1
            Temp2=[1 for k in range(len(self.Time))]
            for j in range(self.NComponent):
                if (self.WeightTable[4][i][j]==1):
                    Temp*=1-R[j]
                    for k in range(len(self.Time)):
                        Temp2[k]*=1-R2[j][k]
                    #print("\n Temp ")
                    #print(Temp)
                    #print("\n Temp2 ")
                    #print(Temp2)
                elif (self.WeightTable[4][i][j]==-1):
                    Temp*=R[j]
                    for k in range(len(self.Time)):
                        Temp2[k]*=R2[j][k]
                    #print("\n Temp ")
                    #print(Temp)
                    #print("\n Temp2 ")
                    #print(Temp2)
            P+=self.WeightTable[3][i]*Temp
            for k in range(len(self.Time)):
                P2[k]+=self.WeightTable[3][i]*Temp2[k]
            #print("\n Temp ")
            #print(Temp)
            #print("\n Temp2 ")
            #print(Temp2)
            #print("\n current R2 ")
            #print(P2)
            #print("\n Les coefficient ")
        #print(self.WeightTable[3])
        #print("\n Reliability polynomial R= ")
        return [sympy.simplify(sympy.expand(1-P)),[1-P2[k] for k in range(len(self.Time))]] # return the polynomial of defiability and the polynomial of reliability
    
    def ViewGraph(self,Dir=None):   # function to view the down hasse diagram
        G=nx.DiGraph()
        for i in self.AdjMat.keys():
            for j in range(len(self.AdjMat[i])):
                if (self.AdjMat[i][j]==1):
                    G.add_edge(str(sum([(self.Node[j][kk])*(2**kk) for kk in range(len(self.Node[j]))])),\
                    str(sum([(self.Node[i][kk])*(2**kk) for kk in range(len(self.Node[i]))])))
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))

        #print(G.adj)
        #fig=plt.figure(figsize=(5,5))
        plt.subplots(figsize=(10, 10))
        plt.clf() # Efface le contenu de la figure courante
        nx.draw_networkx(G,pos=nx.circular_layout(G),node_size=(10**4)/2)
        #nx.draw(G)
        #nx.draw(G,pos=nx.circular_layout(G),node_color='r',edge_color='b')
        plt.axis('off')
        #plt.grid(False)
        if (Dir!=None):
            plt.savefig(Dir+"HD.png")
            plt.savefig(Dir+"HD.pdf",format="pdf")
        plt.show()

"""
MyTree=DefaultTree(3)
MyTree.NewRelation(3,[1,1,0],[0,0,1])
MyTree.ViewGraph(Dir)

MyDownHasseDiagram=DownHasseDiagram(MyTree,[0,1],[0,1],[[1],[1]],[One,One],[0],1)

print(MyDownHasseDiagram.NComponent)
print(MyDownHasseDiagram.Node)


print(MyDownHasseDiagram.MinCut)

print(MyDownHasseDiagram.NCut)
print(MyDownHasseDiagram.Cut)

print(MyDownHasseDiagram.NNode)
print(MyDownHasseDiagram.Node)

print(MyDownHasseDiagram.NodeGeneration)

print(MyDownHasseDiagram.AdjMat)

print(MyDownHasseDiagram.WeightTable)

MyDownHasseDiagram.ViewGraph(Dir)

print(MyDownHasseDiagram.GetPolyFiab())
"""

UpHasseDiagrams={} # dictionary of the up hasse diagrams
class UpHasseDiagram:   # class of the up hasse diagram
    NUpHasseDiagram=0       # number of up hasse diagrams
    
    def __init__(self,Tree=DefaultTree(2),IndivIndex=[0],IndivLabel=[0],IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1): # constructor
        self.id=id(self) # id of the up hasse diagram
        UpHasseDiagrams[str(self.id)]=self   # add the up hasse diagram to the dictionary
        self.__class__.NUpHasseDiagram+=1   # increment the number of up hasse diagrams
        self.Tree=Tree  # tree of the up hasse diagram
        self.IndIndex=IndivIndex    # list of the indices of the individuals of the up hasse diagram
        self.IndLabel=IndivLabel    # list of the labels of the individuals of the up hasse diagram
        self.IndFiabVal=IndivReliabilityVal   # list of the values of the individuals of the up hasse diagram
        self.IndFiabFunc=IndivReliabilityFunc   # list of the functions of the individuals of the up hasse diagram
        self.NComponent=len(self.IndLabel)  # number of components of the up hasse diagram
        self.Time=t # time of the up hasse diagram
        self.Option=Option  # option of the up hasse diagram
        self.Times=[0 for i in range(self.NComponent)]  # list of the times of the up hasse diagram
        self.Order=[0 for i in range(self.NComponent)]  # list of the orders of the up hasse diagram
        self.IndicesPrincipal=[1 for i in range(self.NComponent)]   # list of the indices of the principal components of the up hasse diagram
        self.NNode=0    # number of nodes of the up hasse diagram
        self.Node={}            # dictionary of the nodes of the up hasse diagram
        self.NLink=0    # number of links of the up hasse diagram
        self.Link=[]    # list of the links of the up hasse diagram
        
        MyLink=Link(self.Tree,self.IndIndex)    # create a link of the up hasse diagram
        MyLink.CollectLink()    # collect the links of the up hasse diagram
        
        self.MinLink=MyLink.MinLink # minimum link of the up hasse diagram
        self.NMinLink=MyLink.NMinLink   # number of minimum links of the up hasse diagram
        
        print("\n Minimal Links")     # print the minimal links
        print(self.MinLink)   # print the minimal links
        
        for i in range(len(self.MinLink)):  # for each minimal link
            self.Node[i]=self.MinLink[i].copy()
            self.Link.append(self.MinLink[i].copy())
            self.NNode+=1
            self.NLink+=1
            
        self.NodeGeneration=[self.MinLink]  # list of the generations of the up hasse diagram
        
        #print("\n UpHasseDiagram called line 630")
        #print([self.MinLink,[[1 for j in range(self.NComponent)]]])
        xx=max([len(self.MinLink[ii]) for ii in range(len(self.MinLink))])-self.NComponent  # number of missing components
        #print(xx)
        if (xx==0): # if there is no missing components
            #print([self.MinLink,[[1 for j in range(self.NComponent)]]])
            while (self.NodeGeneration[-1]!=[[1 for j in range(self.NComponent)]]):
                Leaves=[]
                for Leaf in self.NodeGeneration[-1]:
                    for k in range(len(Leaf)):
                        NewLeaf=Leaf.copy()
                        if (NewLeaf[k]<1):
                            NewLeaf[k]+=1
                            if (not(NewLeaf in Leaves) and not(NewLeaf in self.Link)):
                                Leaves.append(NewLeaf.copy())
                                self.Node[len(self.Node)]=NewLeaf.copy()
                                self.Link.append(NewLeaf.copy())
                                self.NNode+=1
                                self.NLink+=1
                self.NodeGeneration.append(Leaves) 
                #print("\n New generation")
                #print(self.NodeGeneration[-1])
        #print("\n All Links generated")
        
        """ 
        def InOrder2(xx=[1, 1, 0, 0],yy=[1, 0, 0, 0]):
            i=min(len(xx),len(yy))-1
            while ((xx[i]==yy[i]) and (i>=0)):
                #print((xx,yy))
                i=i-1
            if (i<0):
                res=True
            else:
                res=(xx[i]<yy[i])
            return res
        
        
        def InOrder2(xx=[1,3,2],yy=[1,2,30]):
            i=min(len(xx),len(yy))-1
            while ((xx[i]==yy[i]) and (i>=0)):
                #print((xx,yy))
                i=i-1
            if (i<0):
                res=True
            else:
                res=(xx[i]<yy[i])
            return res
        """
        
        def InOrder2(x=[0,0,1],y=[0,1]):    # function to determine if x is in order of y
            res=True    # result of the function
            if (x!=None) and (y!=None): # if x and y are not None
                for i in range(min(len(x),len(y))):
                    res=res and (x[i]<=y[i])
            return res
        
        self.AdjMat={i:[0 for j in range(len(self.Node))] for i in self.Node.keys()}    # adjacency matrix of the up hasse diagram   
        for i in self.Node.keys():
            for j in self.Node.keys():
                if ((i!=j) and InOrder2(self.Node[i],self.Node[j])):
                    self.AdjMat[i][j]=1
        
        def UpdateGeneration(): # function to update the generation of the up hasse diagram
            kk=min([sum(self.MinLink[i]) for i in range(len(self.MinLink))])
            depth=self.NComponent-kk+1
            temp=[[] for i in range(depth)]
            #print("\n Nodes:")
            #print(self.Node)
            for i in self.Node.keys():
                j=sum(self.Node[i])
                temp[depth+kk-j-1].append(i)
                #print("\n Generations:")
                #print(temp)
            self.NodeGeneration=temp.copy()          
            
        self.WeightTable=[[],[],[],[],[]]
        #[[Index],[minimalité], [poids], [coef poly fiab], [code coupe]]
        
        def InitWeight():   # function to initialize the weight table of the up hasse diagram
            for i in self.Node.keys():  # for each node of the up hasse diagram
                self.WeightTable[0].append(i)
                self.WeightTable[3].append(0)
                self.WeightTable[4].append(self.Node[i])
                if (self.Node[i] in self.MinLink):
                    self.WeightTable[1].append(1)
                    self.WeightTable[2].append(1)
                else:
                    self.WeightTable[1].append(0)
                    self.WeightTable[2].append(0)
                    for j in self.Node.keys():
                        if (i!=j) and InOrder2(self.Node[j],self.Node[i]) and (self.Node[j] in self.MinLink):
                            self.WeightTable[2][-1]+=1
            #print("\n Current weights")
            #print(self.WeightTable[2])
        
        def UpdatePolyFiab():   # function to update the polynomial of fiability of the up hasse diagram
            UpdateGeneration()  # update the generation of the up hasse diagram
            #print("Generations")
            #print(self.NodeGeneration)
            for i in range(len(self.NodeGeneration)-1,-1,-1):   # for each generation of the up hasse diagram
                for j in self.NodeGeneration[i]:
                    if ((self.Node[j] in self.MinLink) and (self.WeightTable[2][j]==1)):
                        self.WeightTable[3][j]+=1
                        #print("\n Leaf Adding")
                        #print(j)
                        #print(self.Node[j])
                    while ((self.WeightTable[2][j]>1)):
                        for k in self.Node.keys():
                            if InOrder2(self.Node[j],self.Node[k]):
                                #print(self.Node[j],self.Node[k])
                                #print("True 1 ?")
                                self.WeightTable[2][k]-=1
                                if (k==j):
                                    self.WeightTable[3][k]-=1
                                #print("\n Branch removal")
                                #print(self.WeightTable[2])
                    while ((self.WeightTable[2][j]<1)):
                        for k in self.Node.keys():
                            if InOrder2(self.Node[j],self.Node[k]):
                                #print(self.Node[j],self.Node[k])
                                #print("True 2 ?")
                                self.WeightTable[2][k]+=1
                                if (k==j):
                                    self.WeightTable[3][k]+=1
                                #print("\n Branch addition")
                                #print(self.WeightTable[2])
            #print("\n The sum of weights should be nonegative and less than the number of leaves")
            #print(self.WeightTable[3])
            #print(sum(self.WeightTable[3]))
            #print(len(self.NodeGeneration[-1]))
        
        InitWeight()
        
        UpdatePolyFiab()
        #print("Reliability polynomial")
        
    def __del__(self):
        self.__class__.NUpHasseDiagram-=1
        
    def GetPolyFiab(self):  # function to get the polynomial of fiability of the up hasse diagram
        #R=[sympy.Symbol("R"+str(self.IndIndex[i])) for i in range(self.NComponent)]
        R=self.IndLabel
        if (self.Option==1):
            R2=[[self.IndFiabVal[i][j] for j in range(len(self.Time))] for i in range(self.NComponent)]
        else:
            R2=[[self.IndFiabFunc[i](self.Time[j]) for j in range(len(self.Time))] for i in range(self.NComponent)]
        
        
        P=0  # polynomial of fiability
        P2=[0 for k in range(len(self.Time))]       # polynomial of fiability
        for i in self.WeightTable[0]:   # for each node of the up hasse diagram
            Temp=1  # temporary variable
            Temp2=[1 for k in range(len(self.Time))]    # temporary variable
            for j in range(self.NComponent):
                if (self.WeightTable[4][i][j]==1):
                    Temp*=R[j]
                    for k in range(len(self.Time)):
                        Temp2[k]*=R2[j][k]
                elif (self.WeightTable[4][i][j]==-1):
                    Temp*=1-R[j]
                    for k in range(len(self.Time)):
                        Temp2[k]*=1-R2[j][k]
            P+=self.WeightTable[3][i]*Temp
            for k in range(len(self.Time)):
                P2[k]+=self.WeightTable[3][i]*Temp2[k]
        #print("\n Les poids")
        print(R2)
        #print(len(self.WeightTable))
        #print(self.WeightTable[0])
        #print(self.WeightTable[2])
        #print(self.WeightTable[3])
        #print("\n Reliability polynomial R= ")
        #print(P2)
        #return [sympy.simplify(sympy.expand(P)),P2]
        return [P,P2]
    
    def ViewGraph(self,Dir=None): # function to view the up hasse diagram
        G=nx.DiGraph()
        for i in self.AdjMat.keys():
            for j in range(len(self.AdjMat[i])):
                if (self.AdjMat[i][j]==1):
                    G.add_edge(str(sum([(self.Node[j][kk])*(2**kk) for kk in range(len(self.Node[j]))])),\
                    str(sum([(self.Node[i][kk])*(2**kk) for kk in range(len(self.Node[i]))])))
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))

        #print(G.adj)
        #fig=plt.figure(figsize=(5,5))
        plt.subplots(figsize=(10, 10))
        plt.clf() # Efface le contenu de la figure courante
        nx.draw_networkx(G,pos=nx.circular_layout(G),node_size=(10**4)/2)
        #nx.draw(G)
        #nx.draw(G,pos=nx.circular_layout(G),node_color='r',edge_color='b')
        plt.axis('off')
        #plt.grid(False)
        if (Dir!=None):
            plt.savefig(Dir+"HD.png")
            plt.savefig(Dir+"HD.pdf",format="pdf")
        plt.show()

"""
MyTree=DefaultTree(3)
MyTree.NewRelation(3,[1,1,0],[0,0,1])
MyTree.ViewGraph(Dir)

MyUpHasseDiagram=UpHasseDiagram(MyTree,[0,1],[0,1],[[1],[1]],[One,One],[0],1)


print(MyUpHasseDiagram.NComponent)
print(MyUpHasseDiagram.Node)


print(MyUpHasseDiagram.MinCut)

print(MyUpHasseDiagram.NCut)
print(MyUpHasseDiagram.Cut)

print(MyUpHasseDiagram.NNode)
print(MyUpHasseDiagram.Node)

print(MyUpHasseDiagram.NodeGeneration)

print(MyUpHasseDiagram.AdjMat)

print(MyUpHasseDiagram.WeightTable)

MyUpHasseDiagram.ViewGraph(Dir)

print(MyUpHasseDiagram.GetPolyFiab())
"""

"""
Dir="E:/Pedagogie/Encadrement/EncadrementEnsai/MasterRThese/20192020/TadieBenjaulys/"
MyTree=DefaultTree(12)
MyTree.NewRelation(3,[0,1,1,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0])
MyTree.NewRelation(3,[0,0,0,0,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,1,0,0,0])
MyTree.NewRelation(4,[0,0,0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,1,0,0])
MyTree.NewRelation(3,[1,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0])
MyTree.NewRelation(1,[0,0,0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0,1])

#MyTree.ViewGraph(Dir)

MyDownHasseDiagram=DownHasseDiagram(MyTree,[k for k in range(7)],[k for k in range(7)],[[1] for k in range(7)],[One for k in range(7)],[0],1)
print(MyDownHasseDiagram.GetPolyFiab())

MyUpHasseDiagram=UpHasseDiagram(MyTree,[k for k in range(7)],[k for k in range(7)],[[1] for k in range(7)],[One for k in range(7)],[0],1)
#print(MyUpHasseDiagram.Node)
print(MyUpHasseDiagram.GetPolyFiab())
#print(MyUpHasseDiagram.MinLink)

#MyDownHasseDiagram.ViewGraph(Dir)
#MyUpHasseDiagram.ViewGraph(Dir)

"""