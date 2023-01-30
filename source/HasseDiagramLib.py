
"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go
#from numpy import matlib # importer le module matlib 

import sympy
import networkx as nx
import  matplotlib.pyplot  as  plt

from FaultTreeLib import *

"""
Construction des coupes minimales
"""

Cuts={} # Dictionary of Cups
class Cut: # Classe de coupes
    NCut=0    
    def __init__(self,Tree=FaultTree(2),IndivIndex=[0]):  # Constructeur
        """
        Décrémentation du nombre de coupes
        

        And here's the full docstring:
        
        Dictionary of Cups 
        :Args:Tree (list, optional): _description_. Defaults to FaultTreeR(2).
        :Args:IndivIndex (list, optional): _description_. Defaults to [0].
        Décrémentation du nombre de coupes
        
        The docstring is a mess. It's not clear what the function does, and it's not clear what the
        arguments are
        
        :param Tree: the tree of failure
        :param IndivIndex: list of indices of individuals
        """
        self.id=id(self)    # Identifiant de la classe
        Cuts[str(self.id)]=self # Ajout de la classe dans le dictionnaire
        self.__class__.NCut+=1 # Incrémentation du nombre de coupes
        self.Tree=Tree  # Arbre de défaillance
        self.IndIndex=IndivIndex    # Indices des individus
        self.NComponent=len(self.IndIndex)  # Nombre de composants
        self.NNode=0    # Nombre de noeuds
        self.Node={}    # Dictionnaire des noeuds
        self.NCut=0    # Nombre de coupes
        self.Cut=[]   # Liste des coupes
        self.RelMat=[[],[],[],[],[],[],[],[]]   # Matrice de relations
        #[[NumRel],[Node i],[Node j],[Door],[Orders],[Times],[IndicesPrincipal],[Result]]
        
    def __del__(self):  # Destructeur
        """
        The __del__ method is called when the instance is about to be destroyed
        """
        self.__class__.NCut-=1  # 
        
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):  # Traitement d'un arbre
        """
        As long as the function is true and the end of the list has not been reached, the function returns
        True if xx is in the order of yy
        
        :param xx: list of integers
        :param yy: the list of the values of the nodes of the tree
        :return: True if xx is in the order of yy
        
        Examples:
        ---------

        >>> self,xx=[1,3,2],yy=[1,2,30]
        false
        """
        res=True    
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))):
            res=(res and (xx[i]<=yy[i])) 
            i=i+1
        return res
    
    def Leaves(self):   
        """
        It takes the leaves of the tree and creates a list of lists 
        :return: A list of lists.
        """
        Temp1=self.Tree.Leaves()
        #print("\n DT leaves")
        #print(Temp1)
        n=len(Temp1)
        res=[]
        for i in range(n):
            Leaf=[]
            #Temp2=self.Tree.Node[Temp1[i]]
            #print("\n Raw leaf :")
            #print(Temp2)
            #print(self.IndIndex)
            #print(self.NComponent)
            for k in range(self.NComponent):    # Pour chaque composant
                Temp3=[0 for l in range(self.NComponent)]
                Temp3[k]=1
                #print("\n Cutomized leaf :")
                #print(Temp3)
                Leaf+=[[Temp3]]
            #if (Leaf!=[]):
            res.append([Temp1[i],Leaf])
            #print("\n Leaf:")
            #print(Leaf)
        return res

    def CollectCut(self,P_Gen): # Collecte des coupes
        """
        It takes a tree and returns a list of cuts
        """
        Temp1=self.Leaves()
        #print("\n Customized DT Leaves")
        #print(Temp1)
        Temp2=self.Tree.IdxTable
        #print("\n Index Table")
        #print(Temp2)
        #[[NumRel],[Node i],[Node j]]
        Temp3=self.Tree.RelMat
        #print("\n Tree.RelMat")
        #print(Temp3)
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        for i in range(len(Temp1)):
            self.NNode+=1
            self.Node[Temp1[i][0]]=Temp1[i][1]
            #self.Cut=P_Gen(3,[self.Cut]+Temp1[i][1])[0]
            #self.NCut=len(self.Cut)
        #print("\n Nodes")
        #print(self.Node)   
        for i in range(len(Temp2[0])):
            #[[NumRel],[Node i],[Node j],[Door],[Orders],[Times],[IndicesPrincipal],[Result]]
            self.RelMat[0].append(Temp2[0][i])
            self.RelMat[1].append(Temp2[1][i])
            self.RelMat[2].append(Temp2[2][i])
            self.RelMat[3].append(Temp3[0][i])
            self.RelMat[4].append(Temp3[3][i])
            self.RelMat[5].append(Temp3[4][i])
            self.RelMat[6].append(Temp3[5][i])
            for x in self.Tree.Node:
                if (self.Tree.IdxNode(x) in self.Node):
                    y=self.Tree.Node[self.RelMat[1][-1]]
                    Test=(x!=y) and (self.InOrder2(x,y))
                    Test=(Test and (self.Tree.AdjMat[self.Tree.IdxNode(y)][self.Tree.IdxNode(x)]==0))
                    Test=(Test and (self.Tree.AdjMat[self.Tree.IdxNode(x)][self.Tree.IdxNode(y)]==0))
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
            if not(self.RelMat[2][-1] in self.Node):
                self.NNode+=1
                # Creating a new node in the graph, and it is a Python node.
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
MyTree=FaultTree(3)
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

Links={} 
"""Dictionary of minimal links

    Returns:
    list: contain the minimal links of order 3
"""
class Link:     # Classe liens minimaux
    NLink=0    
    def __init__(self,P_NOT,Tree=FaultTree(2),IndivIndex=[0]): # 
        """
        This function is used to create a new link
        
        :param Tree: The tree that the link is in
        :param IndivIndex: The index of the individual in the tree
        """
        self.id=id(self) # Identifiant
        Links[str(self.id)]=self # Ajout dans le dictionnaire
        self.__class__.NLink+=1 # Incrémentation du nombre de liens
        self.Tree=Tree # Arbre
        self.IndIndex=IndivIndex    # Indices des individus    
        self.NComponent=len(self.IndIndex)  # Nombre de composants
        
        self.NNode=0 # Nombre de noeuds
        self.Node={} # Dictionnaire des noeuds
        self.NLink=0    # Nombre de liens
        self.Link=[] # Liste des liens
        self.NMinLink=0 # Nombre de liens minimaux
        self.MinLink=[] # Liste des liens minimaux
        
        def InOrder3(xx=[1,0,1],yy=[0,-1,-1]): 
            """
            If the two lists are of equal length, then the function returns True if and only if the first
            list is less than or equal to the second list in the lexicographic order
            
            :param xx: the x-coordinates of the points
            :param yy: the list of y-coordinates of the points in the polygon
            :return: True or False
            
            
            Examples:
            -------
            
            >>> xx=[1,0,1],yy=[0,-1,-1]
            false
            """
            #print([xx,yy])
            res=True
            i=0
            while ((res==True) and (i<min(len(xx),len(yy)))):
                if (xx[i]*yy[i]!=0):
                    res=(res and (xx[i]<=yy[i]))
                i=i+1
            return res
        
        def TrueVal1(xx=[1,0],yy=[0,-1]):   
            """
            If the two input vectors are in order, then the output vector is the same as the first input
            vector, except that if the first input vector has a zero in a position where the second input
            vector has a nonzero, then the output vector has a one in that position
            
            :param xx: the first input vector
            :param yy: the first input vector
            :return: a list of 1's and 0's.
            
            
            Examples:
            -------
            >>> xx=[1,0],yy=[0,-1]
            [1, 1]
            
            """
            res=xx.copy()
            if InOrder3(xx,yy):
                i=0
                while (i<min(len(xx),len(yy))):
                    if (xx[i]*yy[i]==0) and (xx[i]+yy[i]!=0):
                        res[i]=1
                    i=i+1
            return res
        
        def TrueVal2(xx=[1,0],yy=[[0,-1]]):  
            """
            It takes a list of lists of numbers and returns a list of numbers
            
            :param xx: a list of numbers, each number is either 0 or 1
            :param yy: a list of lists of numbers. Each list of numbers is a list of coefficients of a
            polynomial
            :return: the result of the operation.
            
            Examples:
            ---------

            >>> xx=[1,0],yy=[[0,-1]]
            [1, 1]
            """
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
        
        for x in self.Cut.Cut:  # For each vertex of the cut
            for i in range(len(x)):
                x[i]=-x[i]
        
        if (self.Cut.Cut!=[]): # If the cut is not empty
            temp=P_NOT([self.Cut.Cut])
            if (temp!=[]):
                self.Link=temp[0]
        else: # If the cut is empty
            temp=[]
            for i in range(self.NComponent): # For each component
                tempBis=[0 for j in range(self.NComponent)]
                tempBis[i]=1
                temp.append(tempBis)
            self.Link=temp
            #print("Here")
            #print(self.Link)
        
        self.NLink=len(self.Link) # Number of links
        
        #print("\n Minimal Cuts: ")
        #print(self.Cut.Cut)
        
        #print("\n Raw set of Links: ")
        #print(self.Link)
        
    def __del__(self): 
        """
        The function __del__ is a destructor. It is called when the object is about to be destroyed
        """
        self.__class__.NLink-=1
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]): 
        """
        Checking if the first vector is less than or equal to the second vector
        
        :param xx: the first vector
        :param yy: the vector of the current state
        :return: a boolean value.
        
        
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

    def CollectLink(self): # Collecte des liens minimaux
        """
        It takes a list of links and returns a list of minimal links.
        Checking if the link is already in the dictionary. If not, it adds it to the dictionary.

        """
        #Temp=self.Node.copy()
        #nn=len(Temp)     
        def InOrder3(xx=[1,0],yy=[0,-1]): # Fonction d'ordre 3
            """
            summary Function of order 3 
            
            Here's a longer description of the function:
            
            Checking if the cut is feasible
            
            :param xx: the list of the number of vertices in each connected component of the graph
            :param yy: the list of the number of vertices in each part of the cut
            :return: a boolean value.
            
            Examples:
            ---------

            >>> xx=[1,0],yy=[0,-1]
            True
        
            """
            res=True
            i=0
            while ((res==True) and (i<min(len(xx),len(yy)))): # Pour chaque sommet du cut
                if (xx[i]*yy[i]!=0):
                    res=(res and (xx[i]<=yy[i]))
                i=i+1
            return res
        
        def InOrder4(xx=[1,0],yy=[[0,-1],[-1,0]]): # Fonction d'ordre 4
            """
            Checking if the list xx is in the list of lists yy
            
            Here's a longer description of the above function:
            
            Checking if the list xx is in the list of lists yy
            
            :param xx: the list to be checked
            
            :param yy: the list of lists
            
            :return: a boolean value
            
            :param xx: the list to be checked
            :param yy: the list of lists
            :return: The list of orders.
            
            
            Examples:
            ---------

            >>> xx=[1,0],yy=[[0,-1],[-1,0]]
            True
            """
            res=False
            i=0
            while (not(res) and (i<len(yy))):
                res=(res or InOrder3(xx,yy[i]))
                i=i+1
            return res
        
        Order=[] # Liste des ordres
# Creating a list of links that are not in order.
        for y in self.Link: # Pour chaque lien
            if not(y in [self.Node[k] for k in self.Node.keys()]): # Si le lien n'est pas déjà dans le dictionnaire
                self.Node[self.NNode]=y
                self.NNode+=1
                Order.append(0)
                for x in self.Link:     # Pour chaque lien
                    if ((x!=y)and(self.InOrder2(x,y))): # Si le lien est dans l'ordre
                        Order[-1]+=1
                if (Order[-1]==0):  # Si le lien n'est pas dans l'ordre
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
MyTree=FaultTree(3)
MyTree.NewRelation(3,[1,1,0],[0,0,1])

MyLink=Link(MyTree,2)

MyLink.CollectLink()

print(MyLink.NLink)
print(MyLink.Link)

print(MyLink.NMinLink)
print(MyLink.MinLink)
"""

"""
 
"""

def One(x):
    """
    Function that returns 1 if x is a positive integer    
    :param x: int
    :return: 1
    """
    return 1
            
DownHasseDiagrams={}    # Dictionnaire des diagrammes de Hasse
class DownHasseDiagram: # Classe des diagrammes de Hasse
    NDownHasseDiagram=0   # Nombre de diagrammes de Hasse
    
    def __init__(self,Tree=FaultTree(2),IndivIndex=[0],IndivLabel=[0],IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1): # Constructeur
        """
        The function is used to create a Hasse diagram of the system. 
        
        Here's a more detailed explanation of the function: 
        
        The function is used to create a Hasse diagram of the system. The function takes in the following
        parameters: 
        
        Tree: This is the tree of the system. 
        
        IndivIndex: This is the index of the individual. 
        
        IndivLabel: This is the label of the individual. 
        
        IndivReliabilityVal: This is the reliability value of the individual. 
        
        IndivReliabilityFunc: This is the reliability function of the individual. 
        
        t: This is the time. 
        
        Option: This is the option. 
        
        The function returns the following: 
        
        The function returns the Hasse diagram of the
        
        :param Tree: The tree that is used to generate the Hasse diagram
        :param IndivIndex: The index of the individual
        :param IndivLabel: The labels of the components
        :param IndivReliabilityVal: The reliability of each component
        :param IndivReliabilityFunc: A list of functions that will be used to calculate the reliability
        of the individual
        :param t: time
        :param Option: 1, defaults to 1 (optional)
        """
        self.id=id(self)
        DownHasseDiagrams[str(self.id)]=self    # Ajout du diagramme dans le dictionnaire
        self.__class__.NDownHasseDiagram+=1   # Incrémentation du nombre de diagrammes de Hasse
        self.Tree=Tree                     # Arbre
        self.IndIndex=IndivIndex       # Indices des individus
        self.IndLabel=IndivLabel    # Labels des individus
        self.IndFiabVal=IndivReliabilityVal # Valeurs de fiabilité des individus
        self.IndFiabFunc=IndivReliabilityFunc # Fonctions de fiabilité des individus
        self.NComponent=len(self.IndLabel)  # Nombre de composants
        self.Time=t # Temps
        self.Option=Option  # Option
        self.Times=[0 for i in range(self.NComponent)]  # Liste des temps
        self.Order=[0 for i in range(self.NComponent)] # Liste des ordres
        self.IndicesPrincipal=[1 for i in range(self.NComponent)]   # Liste des indices principaux
        self.NNode=0    # Nombre de noeuds
        self.Node={}    # Dictionnaire des noeuds
        self.NCut=0    # Nombre de cuts
        self.Cut=[]   # Liste des cuts
        
        MyCut=Cut(self.Tree,self.IndIndex) # Création du cut
        MyCut.CollectCut()  # Collecte du cut
        self.MinCut=MyCut.Cut   # Minimal cuts
        
        #print("\n Minimal Cuts")
        #print(MyCut.Cut)
        
        
        for i in range(len(self.MinCut)):   # Pour chaque cut
            self.Node[i]=self.MinCut[i].copy()
            self.Cut.append(self.MinCut[i].copy())
            self.NNode+=1
            self.NCut+=1
        
        self.NodeGeneration=[self.MinCut]
        
        while (self.NodeGeneration[-1]!=[[1 for j in range(self.NComponent)]]): # Tant que l'on a pas trouvé tous les noeuds
            Leaves=[]
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
        def InOrder2(x=[0,0,1],y=[0,1]):    
            """
            Checking if x is less than or equal to y
            
            :param x: a list of integers
            :param y: [0,1]
            :return: The function InOrder2 is being returned.
            
            
            Examples:
            -------
            
            >>> x=[0,0,1],y=[0,1]
            True
            """
            res=True
            if (x!=None) and (y!=None):
                for i in range(min(len(x),len(y))):
                    res=res and (x[i]<=y[i])
            return res
        
        self.AdjMat={i:[0 for j in range(len(self.Node))] for i in self.Node.keys()} # Matrice d'adjacence
        for i in self.Node.keys():
            for j in self.Node.keys():
                if ((i!=j) and InOrder2(self.Node[i],self.Node[j])):
                    self.AdjMat[i][j]=1
        
        def UpdateGeneration(): # Fonction qui met à jour la génération
            """
            The function UpdateGeneration() is used to find the minimum cut of the graph
            """
            kk=min([sum(self.MinCut[i]) for i in range(len(self.MinCut))])  # Nombre de noeuds dans la génération
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
            
        self.WeightTable=[[],[],[],[],[]]
        #[[Index],[minimalité], [poids], [coef poly fiab], [code coupe]]
        
        def InitWeight():   
            """summary Function that initializes the weights
            """
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
        
        def UpdatePolyDeFiab(): 
            """Function that updates the weight of reliability polynomials
            """
            UpdateGeneration()  # Generation Update
            for i in range(len(self.NodeGeneration)-1,-1,-1):   # For every generation
                for j in self.NodeGeneration[i]:
                    if ((self.Node[j] in self.MinCut)):# and (self.WeightTable[2][j]==1)):
                        self.WeightTable[3][j]+=1
                        #print("\n Leaf Adding")
                        #print(self.Node[j])
                    while ((self.WeightTable[2][j]>1)): # While the node is not a leaf
                        for k in self.Node.keys():
                            if InOrder2(self.Node[j],self.Node[k]):
                                self.WeightTable[2][k]-=1
                                if (k==j):
                                    self.WeightTable[3][k]-=1
                                    #print("\n Branch removal")
                                    #print(self.WeightTable[2])
                    while ((self.WeightTable[2][j]<1)):     # While the node is not a branch
                        for k in self.Node.keys():
                            if InOrder2(self.Node[j],self.Node[k]):
                                self.WeightTable[2][k]+=1
                                if (k==j):
                                    self.WeightTable[3][k]+=1
                                    #print("\n Branch addition")
                                    #print(self.WeightTable[2])
            #print("\n The sum of weights should be nonegative and less than the number of leaves")
            #print(sum(self.WeightTable[3]))
        
        InitWeight()
        UpdatePolyDeFiab()
        #print("Unreliability polynomial")

    def __del__(self):  # Destructor
        """
        The destructor is called when the object is about to be destroyed
        """
        self.__class__.NDownHasseDiagram-=1     # Decrement the number of down hasse diagrams
        
    def GetPolyFiab(self):  
        """Calculating the reliability polynomial of a system GetPolyFiab.

        creating a list of lists. The outer list is a list of lists, where
        each inner list is a list of the reliability values for each component.
        Calculating the reliability polynomial of a system.
            
        """
        #R=[sympy.Symbol("R"+str(self.IndIndex[i])) for i in range(self.NComponent)]
        R=self.IndLabel
        if (self.Option==1):
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
        return [sympy.simplify(sympy.expand(1-P)),[1-P2[k] for k in range(len(self.Time))]]
    
    def ViewGraph(self,Dir=None):
        """
        It takes a graph and draws it
        
        :param Dir: the directory where the graph will be saved
        """
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
MyTree=FaultTree(3)
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

UpHasseDiagrams={}
class UpHasseDiagram:
    NUpHasseDiagram=0    
    
    def __init__(self,Tree=FaultTree(2),IndivIndex=[0],IndivLabel=[0],IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1): 
        """
        It takes a list of lists, and creates a new list of lists, where each sublist contains the
        indices of the original list that have the same value.
        
        :param Tree: The tree that is used to generate the Hasse diagram
        :param IndivIndex: The index of the individual
        :param IndivLabel: a list of the labels of the individuals
        :param IndivReliabilityVal: a list of lists of length equal to the number of components in the
        system. Each
        :param IndivReliabilityFunc: a list of functions that will be used to calculate the reliability
        of the individual
        :param t: the time at which the reliability of the system is to be calculated
        :param Option: 1 for reliability values, 2 for reliability functions, defaults to 1 (optional),
        defaults to 1 (optional)
        """ 
        self.id=id(self)
        UpHasseDiagrams[str(self.id)]=self
        self.__class__.NUpHasseDiagram+=1
        self.Tree=Tree
        self.IndIndex=IndivIndex
        self.IndLabel=IndivLabel
        self.IndFiabVal=IndivReliabilityVal
        self.IndFiabFunc=IndivReliabilityFunc
        self.NComponent=len(self.IndLabel)
        self.Time=t
        self.Option=Option
        self.Times=[0 for i in range(self.NComponent)]
        self.Order=[0 for i in range(self.NComponent)]
        self.IndicesPrincipal=[1 for i in range(self.NComponent)]
        self.NNode=0
        self.Node={}        
        self.NLink=0
        self.Link=[]
        
        MyLink=Link(self.Tree,self.IndIndex)
        MyLink.CollectLink()
        
        self.MinLink=MyLink.MinLink
        self.NMinLink=MyLink.NMinLink
        
        print("\n Minimal Links")
        print(self.MinLink)
        
        for i in range(len(self.MinLink)):
            self.Node[i]=self.MinLink[i].copy()
            self.Link.append(self.MinLink[i].copy())
            self.NNode+=1
            self.NLink+=1
            
        self.NodeGeneration=[self.MinLink]
        
        #print("\n UpHasseDiagram called line 630")
        #print([self.MinLink,[[1 for j in range(self.NComponent)]]])
        xx=max([len(self.MinLink[ii]) for ii in range(len(self.MinLink))])-self.NComponent
        #print(xx)
        if (xx==0):
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
        
        def InOrder2(x=[0,0,1],y=[0,1]):
            """
            If the two lists are not empty, then the function returns True if the first list is less
            than or equal to the second list
            
            :param x: a list of integers
            :param y: the list of values to be sorted
            :return: True
            
            
            Examples:
            -------

            >>> x=[0,0,1],y=[0,1]
            False
            """
            res=True
            if (x!=None) and (y!=None):
                for i in range(min(len(x),len(y))):
                    res=res and (x[i]<=y[i])
            return res
        
        self.AdjMat={i:[0 for j in range(len(self.Node))] for i in self.Node.keys()}   
        for i in self.Node.keys():
            for j in self.Node.keys():
                if ((i!=j) and InOrder2(self.Node[i],self.Node[j])):
                    self.AdjMat[i][j]=1
        #generate hassediagram
        def UpdateGeneration():
            """
            It takes a list of lists, and creates a new list of lists, where each sublist contains the
            indices of the original list that have the same value.
            """
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
        
        
        
        def InitWeight(): 
            """
            For each node, if it is in the minimum spanning tree, then its weight is 1, and the number
            of nodes that are in the minimum spanning tree and are in the order of the node is 1.
            Otherwise, the weight is 0, and the number of nodes that are in the minimum spanning tree
            and are in the order of the node is 0
            """
            for i in self.Node.keys():
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
        
        def UpdatePolyFiab(): 
            """
            The function takes a graph and updates the reliability polynomial of the graph.
            """
            UpdateGeneration() #update generation
            #print("Generations")
            #print(self.NodeGeneration)
            for i in range(len(self.NodeGeneration)-1,-1,-1):
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
        """
        The function __del__ is a special function in Python that is called when an object is about to
        be destroyed
        """
        self.__class__.NUpHasseDiagram-=1
        
    def GetPolyFiab(self):
        """
        The function GetPolyFiab() returns the reliability polynomial and the reliability function for a
        given system
        :return: The reliability polynomial and the reliability polynomial evaluated at the time points.
        """
        #R=[sympy.Symbol("R"+str(self.IndIndex[i])) for i in range(self.NComponent)]
        R=self.IndLabel
        if (self.Option==1):
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
    
    def ViewGraph(self,Dir=None):
        """
        It takes a graph and draws it
        
        :param Dir: the directory where the graph will be saved
        """
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
MyTree=FaultTree(3)
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
MyTree=FaultTree(12)
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