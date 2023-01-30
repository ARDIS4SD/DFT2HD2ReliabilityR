# It's a class that creates a directed graph
"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go
import networkx as nx
import  matplotlib.pyplot  as  plt

from LogicDoorLib import *

"""
Fault tree construction
"""

FaultTrees={}
class FaultTree:
    NFaultTree=0       
    def __init__(self,n):
        """
        It creates a new object of class Tree, and adds it to the dictionary FaultTreeRs
        
        :param n: number of nodes
        """
        self.id=id(self)
        FaultTrees[str(self.id)]=self
        self.__class__.NFaultTree+=1
        self.NNode=n # Le système a moins de composant que n
        self.Node=[]
        self.Label=[]
        self.AdjMat={}#matlib.zeros((n, n))
        self.RelMat=[[],[],[],[],[],[]] 
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        self.IdxTable=[[],[],[]] 
        #[[NumRel],[Node i],[Node j]]
    
    def __del__(self):
        """
        The __del__ method is called when the instance is about to be destroyed
        """
        self.__class__.NFaultTree-=1
    
    def IdxNode(self,Indices=None):
        """
        It returns the index of the node in the list of nodes
        
        :param Indices: The index of the node you want to find
        :return: The index of the node in the list of nodes.
        """
        res=None
     
        if (Indices in self.Node):
            res=0
            while (self.Node[res]!=Indices):
                res=res+1
        return res

    def Root(self):
        """
        It returns the roots of the graph.
        :return: The roots of the graph.
        """
        res=[]
        for i in self.AdjMat.keys():
            if (sum(self.AdjMat[i])<=self.AdjMat[i][i]):
                res.append(i)
        return res
    
    def Leaves(self):
        """
        The function `Leaves` returns a list of all the leaf nodes in the graph
        :return: The function `Leaves` returns a list of all the leaf nodes in the graph.
        """
        res=[]
     # Checking if the node is a leaf node.
        for j in range(len(self.AdjMat)):
            Temp=0
            # Iterating over the keys of the dictionary `self.AdjMat`.
            for i in range(len(self.AdjMat)):
               # Checking if the node is a leaf node.
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(j)
        return res
    
    def Update(self,ID_P ):
        """
        If the number of nodes is less than the maximum number of nodes, then add the new node to the
        list of nodes
        """
        n=len(self.RelMat[0])
        if (n>0):
            Test=(len(self.Node)<=self.NNode-2)
            Test=Test or ((self.RelMat[1][-1] in self.Node) and (self.RelMat[2][-1] in self.Node))
            Test=Test or ((not(self.RelMat[1][-1] in self.Node) or not(self.RelMat[2][-1] in self.Node)) and (len(self.Node)<=self.NNode-1))
            if not(Test):
                del(self.RelMat[0][-1])
                del(self.RelMat[1][-1])
                del(self.RelMat[2][-1])
                del(self.RelMat[3][-1])
                del(self.RelMat[4][-1])
                del(self.RelMat[5][-1])
            else:
                if not(self.RelMat[1][-1] in self.Node):
                    self.Node.append(self.RelMat[1][-1])
                    # Appending the label of the node to the list of labels.
                    self.Label.append(ID_P(1))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if not(self.RelMat[2][-1] in self.Node):
                    self.Node.append(self.RelMat[2][-1])
                    # Appending the label of the node to the list of labels.
                    self.Label.append(ID_P(self.RelMat[0][-1]))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if (self.RelMat[0][-1]>=0):
                    self.IdxTable[0].append(n-1)
                    self.IdxTable[1].append(self.IdxNode(self.RelMat[1][-1]))
                    self.IdxTable[2].append(self.IdxNode(self.RelMat[2][-1]))
                    self.AdjMat[self.IdxTable[1][-1]][self.IdxTable[2][-1]]=1
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):
        """
        The function `InOrder2` takes two lists of numbers as input and returns `True` if the first list
        is in ascending order and the second list is in descending order
        
        :param xx: the list of x-coordinates of the points in the first polygon
        :param yy: the list of the values of the nodes in the tree
        :return: True or False


        Examples:
        ---------

        >>> self=(1),xx=[1,3,2],yy=[1,2,30]
        False
        """
        res=True
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))):
            res=(res and (xx[i]<=yy[i]))
            i=i+1
        return res
   
    def Sort(self):   
        """
        It sorts the relations in the order of the nodes in the graph
        """  
        Temp1=[]
        Temp2=[]
        for i in range(len(self.IdxTable[0])):
            j=0
            for k in range(len(self.IdxTable[0])):           
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
        
    def NewRelation(self,Port=1,IndicesIn=None,IndicesOut=None,Orders=None,Times=None,IndicesPrincipal=None):
        """
        It takes in a list of lists, and appends a list to the end of the list of lists
        
        :param Port: The port number of the relation, defaults to 1 (optional)
        :param IndicesIn: The indices of the nodes that are input to the relation
        :param IndicesOut: The indices of the output nodes
        :param Orders: a list of the orders of the relations
        :param Times: The time at which the relation is applied
        :param IndicesPrincipal: This is a list of indices that are the principal indices of the relation
        """
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
    
    def ViewGraph(self,ID_P,Dir=None):
        """
        It takes a graph and returns a graph with the same nodes and edges, but with the nodes labeled
        with their index in the original graph.
        
        :param Dir: the directory where the graph will be saved
        """
        G=nx.DiGraph()
        GNode={}
        nn=len(self.Node)
        for i in self.AdjMat.keys():
            for j in range(len(self.AdjMat[i])):
                if (self.AdjMat[i][j]==1):
                    GNode[nn-1-self.IdxNode(self.Node[i])]=str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i]
                    GNode[nn-1-self.IdxNode(self.Node[j])]=str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j]
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
                    #G.add_edge(str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i],str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j])
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))
        #CompleteNode=self.Node.copy()
        
        mm=nn
        for i in range(nn):
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn):
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
            for j in range(self.NNode):
                Temp=[0 for k in range(self.NNode)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]):
                    #print(Temp)
                    if not(Temp in self.Node):
                        # Adding a node to the graph.
                        GNode[mm]=str(mm)+':'+ID_P(1)
                        G.add_edge(GNode[mm],GNode[nn-1-self.IdxNode(self.Node[i])])
                        mm+=1
                        #G.add_edge(str(self.Node[i]),str(Temp))
                    #CompleteNode.append(Temp)
        
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
            plt.savefig(Dir+"AD.png")
            plt.savefig(Dir+"AD.pdf",format="pdf")
        plt.show()
        
"""
Dir="E:/Pedagogie/Encadrement/EncadrementEnsai/MasterRThese/20192020/TadieBenjaulys/"
MyTree=FaultTree(2)
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