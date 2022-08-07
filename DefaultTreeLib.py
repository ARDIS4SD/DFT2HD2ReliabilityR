"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go
import networkx as nx
import  matplotlib.pyplot  as  plt

from DFT2HD2ReliabilityR.LogicDoorLib import *

"""
Construction de l'arbre de défaillance
"""

DefaultTrees={} # fault tree dictionary
class DefaultTree: # fault tree class
    NDefaultTree=0          # Number of failures
    def __init__(self,n): # fault tree class
        self.id=id(self) # id of the fault tree
        DefaultTrees[str(self.id)]=self # add the fault tree to the dictionary
        self.__class__.NDefaultTree+=1  # increase the number of fault trees
        self.NNode=n # number of nodes; The system has fewer components than n
        self.Node=[]    # list of nodes
        self.Label=[]   # list of labels
        self.AdjMat={}#matlib.zeros((n, n))
        self.RelMat=[[],[],[],[],[],[]] # list of relations
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        self.IdxTable=[[],[],[]] 
        #[[NumRel],[Node i],[Node j]]
    
    def __del__(self):
        self.__class__.NDefaultTree-=1 
    
    def IdxNode(self,Indices=None):     # return the index of the node
        res=None
        if (Indices in self.Node):
            res=0
            while (self.Node[res]!=Indices):
                res=res+1
        return res

    def Root(self): # return the root of the tree
        res=[]
        for i in self.AdjMat.keys():
            if (sum(self.AdjMat[i])<=self.AdjMat[i][i]):
                res.append(i)
        return res
    
    def Leaves(self):   # return the leaves of the tree
        res=[]
        for j in range(len(self.AdjMat)):   # for each node
            Temp=0
            for i in range(len(self.AdjMat)):   # for each node
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(j)
        return res
    
    def Update(self):   # update the adjacency matrix
        n=len(self.RelMat[0])
        if (n>0): # if there are relations
            Test=(len(self.Node)<=self.NNode-2)
            Test=Test or ((self.RelMat[1][-1] in self.Node) and (self.RelMat[2][-1] in self.Node))
            Test=Test or ((not(self.RelMat[1][-1] in self.Node) or not(self.RelMat[2][-1] in self.Node)) and (len(self.Node)<=self.NNode-1))
            if not(Test):   # if the last relation is not valid
                del(self.RelMat[0][-1])
                del(self.RelMat[1][-1])
                del(self.RelMat[2][-1])
                del(self.RelMat[3][-1])
                del(self.RelMat[4][-1])
                del(self.RelMat[5][-1])
            else:   # if the last relation is valid
                if not(self.RelMat[1][-1] in self.Node):
                    self.Node.append(self.RelMat[1][-1])
                    self.Label.append(ID_P(1))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if not(self.RelMat[2][-1] in self.Node): # if the last node is not in the list of nodes
                    self.Node.append(self.RelMat[2][-1])
                    self.Label.append(ID_P(self.RelMat[0][-1]))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if (self.RelMat[0][-1]>=0): # if the last relation is a door
                    self.IdxTable[0].append(n-1)
                    self.IdxTable[1].append(self.IdxNode(self.RelMat[1][-1]))
                    self.IdxTable[2].append(self.IdxNode(self.RelMat[2][-1]))
                    self.AdjMat[self.IdxTable[1][-1]][self.IdxTable[2][-1]]=1
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]): # return the inorder of the tree
        res=True
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))): # for each node
            res=(res and (xx[i]<=yy[i]))
            i=i+1
        return res
   
    def Sort(self):         # sort the relations
        Temp1=[]
        Temp2=[]
        for i in range(len(self.IdxTable[0])): # for each relation
            j=0
            for k in range(len(self.IdxTable[0])): # for each relation
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
        for i in range(len(self.IdxTable[0])): # for each relation
            Temp2[int(Temp1[i])]=i
        Temp3=[[],[],[]]
        Temp4=[[],[],[],[],[],[]]
        for i in range(len(self.IdxTable[0])): # for each relation
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
        
    def NewRelation(self,Port=1,IndicesIn=None,IndicesOut=None,Orders=None,Times=None,IndicesPrincipal=None):   # add a new relation
        if (IndicesIn!=None) and (IndicesOut!=None):
            if True:#(len(IndicesIn)==self.NNode) and (len(IndicesOut)==self.NNode):
                self.RelMat[0].append(Port)
                self.RelMat[1].append(IndicesIn)
                self.RelMat[2].append(IndicesOut)
                self.RelMat[3].append(Orders)
                self.RelMat[4].append(Times)
                self.RelMat[5].append(IndicesPrincipal)
                self.Update()
                self.Sort()
        #print(self.RelMat)
    
    def ViewGraph(self,Dir=None):   # view the graph
        G=nx.DiGraph()
        GNode={}
        nn=len(self.Node)
        for i in self.AdjMat.keys():    # for each node
            for j in range(len(self.AdjMat[i])):    # for each neighbor
                if (self.AdjMat[i][j]==1):
                    GNode[nn-1-self.IdxNode(self.Node[i])]=str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i]
                    GNode[nn-1-self.IdxNode(self.Node[j])]=str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j]
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
                    #G.add_edge(str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i],str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j])
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))
        #CompleteNode=self.Node.copy()
        
        mm=nn             # number of nodes
        for i in range(nn): # for each node
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn):     # for each node
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
            for j in range(self.NNode): # for each node
                Temp=[0 for k in range(self.NNode)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]): # if the node is in the order of the node
                    #print(Temp)
                    if not(Temp in self.Node):
                        GNode[mm]=str(mm)+':'+ID_P(1)
                        G.add_edge(GNode[mm],GNode[nn-1-self.IdxNode(self.Node[i])])
                        mm+=1
                        #G.add_edge(str(self.Node[i]),str(Temp))
                    #CompleteNode.append(Temp)
        
        #print(G.adj)
        #fig=plt.figure(figsize=(5,5))
        plt.subplots(figsize=(10, 10))  # create a figure with size 10x10
        plt.clf() # Efface le contenu de la figure courante
        nx.draw_networkx(G,pos=nx.circular_layout(G),node_size=(10**4)/2)   # draw the graph
        #nx.draw(G)
        #nx.draw(G,pos=nx.circular_layout(G),node_color='r',edge_color='b')
        plt.axis('off') # turn off the axis
        #plt.grid(False)
        if (Dir!=None): # if a directory is given
            plt.savefig(Dir+"AD.png")
            plt.savefig(Dir+"AD.pdf",format="pdf")
        plt.show()  # display the graph
        
"""
Dir="E:/Pedagogie/Encadrement/EncadrementEnsai/MasterRThese/20192020/TadieBenjaulys/"
MyTree=DefaultTree(2)
#MyTree.NewRelation(1,[1,0],[1,0])
#MyTree.NewRelation(1,[0,1],[0,1])
MyTree.NewRelation(4,[0,1],[1,1])
MyTree.NewRelation(3,[1,1],[1,1])

print(MyTree.NNode)
print(MyTree.Leaves())
print(MyTree.Node)
print(MyTree.IdxTable)
print(MyTree.RelMat)
print(MyTree.AdjMat)
print(MyTree.Root())
MyTree.ViewGraph(Dir)
"""