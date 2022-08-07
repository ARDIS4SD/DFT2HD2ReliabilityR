"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go

import sympy
import networkx as nx
import  matplotlib.pyplot  as  plt

from DFT2HD2ReliabilityR.LogicDoorLib import *
from DFT2HD2ReliabilityR.DefaultTreeLib import *
from DFT2HD2ReliabilityR.HasseDiagramLib import *

"""
Construction de l'arbre de défaillance
"""

DefaultTreeRs={} # fault tree dictionary
class DefaultTreeR: # fault tree class
    NDefaultTreeR=0      # The number of fault tree
    def __init__(self,n,IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1): # n: number of nodes 
        self.id=id(self)
        DefaultTreeRs[str(self.id)]=self
        self.__class__.NDefaultTreeR+=1
        self.Option=Option
        self.IndFiabVal=IndivReliabilityVal
        self.IndFiabFunc=IndivReliabilityFunc
        self.Time=t
        if (self.Option==1):
            self.NComponent=len(self.IndFiabVal) # The number of component(s) of the system
        else:
            self.NComponent=len(self.IndFiabFunc) # The number of component(s) of the system
        #print("\n self.NComponent Start in DefaultTreeR")
        #print(self.NComponent)
        self.NNode=n # The number of nodes of the fault tree
        self.Node=[]    # The list of nodes of the fault tree
        self.SubTree={} # The dictionary of subtrees of the fault tree
        
        for i in range(self.NNode): # The list of nodes of the fault tree
            self.SubTree[i]=None    # The dictionary of subtrees of the fault tree
            
        self.Reliability={} # The dictionary of reliability of the fault tree
        self.Label=[]
        self.AdjMat={}#matlib.zeros((n, n))
        self.RelMat=[[],[],[],[],[],[]] 
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        self.IdxTable=[[],[],[]] 
        #[[NumRel],[Node i],[Node j]]
    
    def __del__(self):  # destructor
        self.__class__.NDefaultTreeR-=1
    
    def IdxNode(self,Indices=None): # Indices: list of indices of nodes
        res=None
        if (Indices in self.Node):
            res=0
            while (self.Node[res]!=Indices):
                res=res+1
        return res
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):  # xx: list of indices of nodes, yy: list of indices of nodes
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
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):
        res=True
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))):
            #print((xx,yy))
            res=(res and (xx[i]<=yy[i]))
            i=i+1
        return res
    
    print(InOrder2())
    """
    
    def Leaves(self):   # Returns the list of leaves of the fault tree
        res=[]
        for j in range(len(self.AdjMat)):
            Temp=0
            for i in range(len(self.AdjMat)):
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
                    if (self.InOrder2(self.Node[i],self.Node[j])):
                        Temp+=1
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(j)
        return res
    
    def Root(self): # Returns the index of the root of the fault tree
        res=[]
        for i in self.AdjMat.keys():
            Temp=0
            for j in range(len(self.AdjMat)):
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
                    if (self.InOrder2(self.Node[i],self.Node[j])):
                        Temp+=1
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(i)
        return res
    
    def Update(self):   # Updates the adjacency matrix of the fault tree
        n=len(self.RelMat[0])
        if (n>0):
            Test=(len(self.Node)<=self.NNode-2)
            Test=Test or ((self.RelMat[1][-1] in self.Node) and (self.RelMat[2][-1] in self.Node))
            Test=Test or ((not(self.RelMat[1][-1] in self.Node) or not(self.RelMat[2][-1] in self.Node)) and (len(self.Node)<=self.NNode-1))
            if not(Test):   # If the last node is not a leaf
                #print("Update Test No")
                del(self.RelMat[0][-1])
                del(self.RelMat[1][-1])
                del(self.RelMat[2][-1])
                del(self.RelMat[3][-1])
                del(self.RelMat[4][-1])
                del(self.RelMat[5][-1])
            else:   # If the last node is a leaf
                if not(self.RelMat[1][-1] in self.Node):    # If the last node is a leaf and the last node is not in the list of nodes
                    self.Node.append(self.RelMat[1][-1])
                    self.Label.append(ID_P(1))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if not(self.RelMat[2][-1] in self.Node):    # If the last node is a leaf and the last node is not in the list of nodes
                    self.Node.append(self.RelMat[2][-1])
                    self.Label.append(ID_P(self.RelMat[0][-1]))
                    for i in range(len(self.Node)-1):   # If the last node is a leaf and the last node is not in the list of nodes
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if (self.RelMat[0][-1]>=0): # If the last node is a leaf and the last node is in the list of nodes
                    self.IdxTable[0].append(n-1)
                    self.IdxTable[1].append(self.IdxNode(self.RelMat[1][-1]))
                    self.IdxTable[2].append(self.IdxNode(self.RelMat[2][-1]))
                    self.AdjMat[self.IdxTable[1][-1]][self.IdxTable[2][-1]]=1
                #print("Update Test Ok")
                #print(self.Node)
   
    def Sort(self):         # Sorts the list of nodes of the fault tree
        Temp1=[]
        Temp2=[]
        for i in range(len(self.IdxTable[0])):    # Sorts the list of indices of the nodes
            j=0
            for k in range(len(self.IdxTable[0])):  # Sorts the list of indices of the nodes
                #if (self.InOrder2(self.RelMat[2][k],self.RelMat[1][i]) and (self.IdxTable[2][k]!=self.IdxTable[1][i])):
                Test=(self.AdjMat[self.IdxNode(self.RelMat[2][k])][self.IdxNode(self.RelMat[1][i])]==1)
                Test=Test or (self.InOrder2(self.RelMat[2][k],self.RelMat[1][i]))
                Test=Test and (self.IdxTable[2][k]!=self.IdxTable[1][i])
                if Test:
                    j=j+1
            while (j in Temp1):
                j=j+1
            Temp1.append(j)
            Temp2.append(0)
        for i in range(len(self.IdxTable[0])):
            Temp2[int(Temp1[i])]=i
        Temp3=[[],[],[]]
        Temp4=[[],[],[],[],[],[]]
        for i in range(len(self.IdxTable[0])):
            Temp3[0].append(i)
            Temp3[1].append(self.IdxTable[1][int(Temp2[i])])
            Temp3[2].append(self.IdxTable[2][int(Temp2[i])])
            Temp4[0].append(self.RelMat[0][int(Temp2[i])])
            Temp4[1].append(self.RelMat[1][int(Temp2[i])])
            Temp4[2].append(self.RelMat[2][int(Temp2[i])])
            Temp4[3].append(self.RelMat[3][int(Temp2[i])])
            Temp4[4].append(self.RelMat[4][int(Temp2[i])])
            Temp4[5].append(self.RelMat[5][int(Temp2[i])])
        self.IdxTable=Temp3.copy()
        self.RelMat=Temp4.copy()
        #print("\n Sort Called in DefaultTreeR")
        #print(self.RelMat)
        
    def NewRelation(self,Port=1,IndicesIn=None,IndicesOut=None,Orders=None,Times=None,IndicesPrincipal=None):   # Creates a new relation in the fault tree
        if (IndicesIn!=None) and (IndicesOut!=None): 
            if (len(IndicesIn)<=self.NNode) and (len(IndicesOut)<=self.NNode):
                self.RelMat[0].append(Port)
                self.RelMat[1].append(IndicesIn)
                self.RelMat[2].append(IndicesOut)
                self.RelMat[3].append(Orders)
                self.RelMat[4].append(Times)
                self.RelMat[5].append(IndicesPrincipal)
                #print("\n NewRelation Called in DefaultTreeR")
                #print(self.RelMat)
                self.Update()
                self.Sort()
        #print(self.RelMat)
            
        
    def AutoCompletion(self):   # Automatically completes the fault tree
        nn=len(self.Node)
        for i in range(nn):
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn):
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    self.NewRelation(1,self.Node[i],self.Node[j],None,None,None)
        """
        mm=self.NNode
        for i in range(nn):
            for j in range(mm):
                Temp=[0 for k in range(mm)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]):
                    if not(Temp in self.Node):
                        if (len(self.Node)==self.NNode):
                            self.NNode+=1
                    self.NewRelation(1,Temp,self.Node[i],None,None,None)
        """
               
    def RecursiveStruturation(self):    # Recursive structurer of the fault tree
        ##self.AutoCompletion()
        #print("\n RecursiveStruturation in DefaultTreeR")
        #print("\n Nodes in RecursiveStruturation in DefaultTreeR")
        #print(self.Node)
        for i in range(len(self.IdxTable[0])):  # For each node
            Temp=self.IdxTable[2][i]
            #print("\n AdjMat: ")
            #print(self.AdjMat)
            nSon=0
            #print("\n Sons: ")
            for j in range(len(self.IdxTable[0])): #in range(len(self.Node)):
                if ((self.IdxTable[1][j]!=Temp) and (self.IdxTable[2][j]==Temp)):
                    nSon+=1#self.AdjMat[j][Temp]
                    #print((self.IdxTable[1][j],self.IdxTable[2][j]))
            #print(nSon)
            self.SubTree[Temp]=DefaultTree(nSon+1)  # Creates a new subtree with nSon+1 nodes   
            for j in range(len(self.IdxTable[0])):
                if (self.IdxTable[2][j]==Temp):
                    Temp1=self.RelMat[0][self.IdxTable[0][j]]
                    Temp2=self.RelMat[1][self.IdxTable[0][j]]
                    Temp3=self.RelMat[2][self.IdxTable[0][j]]
                    Temp4=self.RelMat[3][self.IdxTable[0][j]]
                    Temp5=self.RelMat[4][self.IdxTable[0][j]]
                    Temp6=self.RelMat[5][self.IdxTable[0][j]]
                    self.SubTree[Temp].NewRelation(Temp1,Temp2,Temp3,Temp4,Temp5,Temp6)
                    #print("\n NewRelation ")
                    #print(Temp1,Temp2,Temp3,Temp4,Temp5,Temp6)
                    #print("SubTree's Nodes ")
                    #print(self.SubTree[Temp].Node)
        
    def Generation(self):   # Generates the fault tree      
        #print("\n Generation called in DefaultTreeR")
        Temp1={i:self.Node[i] for i in range(len(self.Node))}   # Creates a dictionary with the nodes as keys and the indices as values
        Temp2={}
        res=[self.Leaves().copy()]
        #print("\n New generation")
        #print(res[-1])
        for i in res[0]:
            Temp2[i]=self.Node[i].copy()
            del(Temp1[i])
        while (Temp1!={}):  # While there are nodes to be generated (i.e. there are nodes in Temp1)
            Leaves=[]
            for j in Temp1.keys():
                Cond=True
                for  i in range(len(self.Node)):
                    if (((self.AdjMat[i][j]==1) or (self.InOrder2(self.Node[i],\
                         self.Node[j]))) and (i!=j)):
                        Cond=Cond and (i in Temp2.keys())
                if Cond :
                    Leaves.append(j)
            for k in Leaves:    # For each leaf in Leaves   
                Temp2[k]=self.Node[k].copy()
                del(Temp1[k])
            res.append(Leaves)
            #print("\n New generation")
            #print(res[-1])
        #print("\n All cuts generated")
        return(res)
    
    def RecursiveReliability(self):  # Recursive reliability of the fault tree  (not used)  
        #print("\n RecursiveReliability called in DefaultTreeR")
        self.RecursiveStruturation()
        Temp=self.Generation()
        #print("\n All generations")
        #print(Temp)
        
        def LeafReliability(Generation,i,Option):   # Recursive reliability of the leaf i in the generation Generation  (not used)
            #print("\n LeafReliability called in DefautTreeR")
            R=[]
            R2=[]
            for j in range(self.NComponent):    # For each component    
                if (self.Node[Generation[i]][j]==1):
                    R.append(sympy.Symbol("R"+str(j)))
                    if (Option==1): # If the option is 1, the reliability is the probability of the component
                        """
                        print("\n self.NComponent")
                        print(self.NComponent)
                        print("\n Le node 1" )
                        print(self.Node[Genreration[i]])
                        """
                        
                        R2.append([self.IndFiabVal[j][k] for k in range(len(self.Time))])   # The reliability is the probability of the component   
                    else:
                        """
                        print("\n self.NComponent")
                        print(self.NComponent)
                        print("\n Le node 2" )
                        print(self.Node[Genreration[i]])
                        """
                        #print("\ Reliability steps")
                        #print([len(self.IndFiabFunc),j])
                        R2.append([self.IndFiabFunc[j](self.Time[k]) for k in range(len(self.Time))])
            self.Reliability[Generation[i]]={}  # Creates a new dictionary for the reliability of the node  in the generation Generation    
            #self.Reliability[Genreration[i]][0]=sympy.Symbol("R"+str(Genreration[i]))
            self.Reliability[Generation[i]][0]=R    # The reliability is the probability of the component   
            #self.Reliability[Genreration[i]][1]=[self.IndFiabVal[i][j] for j in range(len(self.Time))]
            self.Reliability[Generation[i]][1]=R2   # The reliability is the probability of the component   
            #self.Reliability[Genreration[i]][1]=[self.IndFiabFunc[i](self.Time[j]) for j in range(len(self.Time))]
            self.Reliability[Generation[i]][1]=R2   # The reliability is the probability of the component   
            #print(self.Reliability[Genreration[i]][0])
            #print(self.Reliability[Genreration[i]][1])
            #print(R)
            #print(R2)
        
        def BranchReliability(Generations,i,Option):    # Recursive reliability of the branch i in the generations Generations  (not used)  
            #print("\n BranchReliability called in DefautTreeR")
            for k in range(len(Generations[i])):    # For each generation in the branch i   
                j=Generations[i][k]                # j is the index of the generation   
                if (self.SubTree[j]==None):     # If the generation is a leaf   
                    LeafReliability(Generations[i],k,Option)    # Recursive reliability of the leaf k in the generation j   
                    #print("Here")  # If the generation is a leaf   
                    #print(j)
                    #print(self.Reliability[j])
                    #print("Ok")

                else:   # If the generation is a branch 
                    Temp1=self.SubTree[j]   # Temp1 is the subtree of the branch j  
                    #print("\n The subTree "+str([i,j]))
                    #print(Temp1.RelMat)
                    #print(Temp1.Node)
                    #print([Temp1.NNode,len(Temp1.Node)])
                    Temp2=[]
                    Temp3=[]
                    Temp4=[]
                    #print("\n Temp1.NNode 1")
                    #print(Temp1.NNode)
                    
                    for kk in range(Temp1.NNode):       # For each node in the subtree of the branch j  
                        if (Temp1.Node[kk]!=self.Node[j]):  # If the node is not the same as the branch j   
                            Temp2=[]                       # Temp2 is the list of the nodes of the subtree of the branch j  
                            Temp3=[]                   # Temp3 is the list of the reliability of the nodes of the subtree of the branch j   
                            Temp4=[]               # Temp4 is the list of the reliability of the nodes of the subtree of the branch j   
                            """
                            print("\n Les fiabilités connues :")
                            print(self.Reliability)
                            
                            print("\n Le node 3")
                            print(Temp1.Node[kk])
                            """
                            
                            for l in range(len(Temp1.Node[kk])):#range(self.NComponent):  
                                if (Temp1.Node[kk][l]==1):  # If the component is active in the node
                                    Temp2.append(l)       # The component is added to the list of the nodes of the subtree of the branch j  
                                    if (l<self.NComponent): # If the component is active in the node    
                                        Temp3.append(sympy.Symbol("R"+str(l)))  # The reliability is the probability of the component       
                                        if (Option==1): 
                                            #print("\n Here 1 !")
                                            #print(self.IndFiabVal[l])
                                            Temp4.append([self.IndFiabVal[l][kkk] for kkk in range(len(self.Time))])
                                        else:
                                            #print("\n Here 2 !")
                                            #print(self.IndFiabFunc[l])
                                            Temp4.append([self.IndFiabFunc[l](self.Time[kkk]) for kkk in range(len(self.Time))])
                                    else:       
                                        Node=[0 for kkk in range(len(Temp1.Node[kk]))]
                                        Node[l]=1
                                        ll=self.IdxNode(Node)
                                        #print("\n Les fiabilités connues :")
                                        #print(self.Reliability)
                                        #print("\n Here 30 !")
                                        #print(ll)
                                        #print(self.Reliability[ll])
                                        #print("Ok")
                                        
                                        Temp3.append(self.Reliability[ll][0][0])
                                        Temp4.append(self.Reliability[ll][1][0])
                            
                            #print(Temp3)
                            #print("\n Index 1")
                            #print(Temp2)
                            #print(Temp4)
                            #print(k)
                            #print(Temp2)
                            Temp5=self.Time
                            #print("\n Here 3 !")
                            #print(Temp2)
                            #print(Temp4)
                            #print(len(Temp4))
                            #print((Temp1,Temp2,Temp3,Temp4,None,Temp5,1))
                            print("Here")
                            print(j)
                            MyUpHasseDiagram=UpHasseDiagram(Temp1,Temp2,Temp3,Temp4,None,Temp5,1)   # The UpHasseDiagram of the subtree of the branch j is created  
                            ##(Tree=DefaultTree(2),IndivIndex=[0],IndivLabel=[0],IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1)
                            
                            MyPolyFiab=MyUpHasseDiagram.GetPolyFiab()   # The polynomial of the reliability of the subtree of the branch j is computed  
                            
                            self.Reliability[j]={}  # The reliability of the branch j is initialized 
                            self.Reliability[j][0]=[MyPolyFiab[0]]  # The reliability of the branch j is initialized 
                            self.Reliability[j][1]=[MyPolyFiab[1]]  
                            #print("\n Current Reliability :")
                            #print(self.Reliability[j][1])
                    #print("Here")
                    #print(j)
                    #print(self.Reliability[j])
                    #print("Ok")
      
        for i in range(len(Temp[0])):   # For each branch in the tree   
            LeafReliability(Temp[0],i,self.Option)   # Recursive reliability of the branch i in the tree 
            #print(i)
        
        if (len(Temp)>1):  # If the tree is not a leaf 
            for i in range(1,len(Temp)):  # For each branch in the tree 
                #print("In")
                #print(i)
                BranchReliability(Temp,i,self.Option)  # Recursive reliability of the branch i in the tree 
                #print("Out")
                #print(i)
            
        res=[]   # The list of the reliability of the tree is initialized 
        for j in Temp[-1]:
            res.append(self.Reliability[j])
        
        #print("\n In BranchReliability ")
        #print("\n Reliability polynomial R= ")
        #print(res)
        return [self.Time,res]

    def ViewGraph(self,Dir=None):  # View the tree in a graph 
        self.AutoCompletion() # The tree is automatically completed
        G=nx.DiGraph() # The graph is initialized 
        GNode={} # The graph is initialized
        nn=len(self.Node) # The number of branches is computed
        for i in self.AdjMat.keys():    # For each branch in the tree
            for j in range(len(self.AdjMat[i])):    # For each node in the branch
                if (self.AdjMat[i][j]==1):  # If the node is active
                    GNode[nn-1-self.IdxNode(self.Node[i])]=str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i]
                    GNode[nn-1-self.IdxNode(self.Node[j])]=str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j]
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
                    #G.add_edge(str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i],str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j])
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))
        #CompleteNode=self.Node.copy()
        
        mm=nn # The number of nodes is computed
        for i in range(nn): # For each node in the tree
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn): # For each node in the tree
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
            for j in range(self.NNode): # For each node in the tree
                Temp=[0 for k in range(self.NNode)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]):
                    #print(Temp)
                    if not(Temp in self.Node):
                        GNode[mm]=str(mm)+':'+ID_P(1)
                        G.add_edge(GNode[mm],GNode[nn-1-self.IdxNode(self.Node[i])])
                        mm+=1
                        #G.add_edge(str(self.Node[i]),str(Temp))
                    #CompleteNode.append(Temp)
        
        #print(G.adj)
        #fig=plt.figure(figsize=(5,5))
        plt.subplots(figsize=(10, 10)) # The graph is displayed
        plt.clf()   # The graph is cleared
        nx.draw_networkx(G,pos=nx.circular_layout(G),node_size=(10**4)/2) # The graph is displayed
        #nx.draw(G)
        #nx.draw(G,pos=nx.circular_layout(G),node_color='r',edge_color='b')
        plt.axis('off') # The graph is not displayed
        #plt.grid(False)
        if (Dir!=None): # If a directory is given
            plt.savefig(Dir+"AD.png")   # The graph is saved
            plt.savefig(Dir+"AD.pdf",format="pdf")  # The graph is saved
        plt.show()  # The graph is displayed
        
"""
Dir="E:/Pedagogie/Encadrement/EncadrementEnsai/MasterRThese/20192020/TadieBenjaulys/"

MyTree=DefaultTreeR(3,[[1],[1]],[One,One],[0],1)
MyTree.NewRelation(3,[1,1,0],[0,0,1])
print(MyTree.RecursiveReliability())
#MyTree.ViewGraph(Dir)

#MyUpHasseDiagram=UpHasseDiagram(MyTree,[0,1],[[1],[1]],[One,One],[0],1)

"""