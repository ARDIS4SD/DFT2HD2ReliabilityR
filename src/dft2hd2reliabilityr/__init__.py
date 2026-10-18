"""
DFT2HD2ReliabilityR — Dynamic Fault Tree -> Hasse diagram -> Reliability.

Bibliothèque d'analyse de sûreté de fonctionnement :
arbres de défaillance (statiques et dynamiques) -> diagrammes de Hasse ->
coupes / liens minimaux, polynômes de fiabilité système.

CORRECTION-11 (cf. CORRECTIONS.md) : ce package remplace l'ancienne disposition
(Racine + doublons `source/`). Import principal :

    from dft2hd2reliabilityr import FaultTree, DownHasseDiagram, UpHasseDiagram

Les dépendances visuelles (matplotlib, networkx) restent optionnelles
(PYPI extra `viz`, cf. pyproject.toml) : elles ne sont chargées que par `ViewGraph`.
"""

__version__ = "0.2.1"  # CORRECTION-11 : version de packaging (PEP 621)

# Imports ordonnancés pour éviter les cycles (LogicDoor -> FaultTree -> Hasse -> FaultTreeR)
from .LogicDoorLib import G_Gen, G_AND, G_FDEP, G_ID, G_NOT, G_OR, G_PAND, G_SPARE, Reductible
from .FaultTreeLib import FaultTree
from .HasseDiagramLib import Cut, Link, DownHasseDiagram, UpHasseDiagram, ReliabilityResult  # noqa: F401
from .FaultTreeRLib import FaultTreeR, One

__all__ = [
    "__version__",
    # Portes logiques + utilitaires
    "G_Gen", "G_ID", "G_OR", "G_AND", "G_NOT", "G_FDEP", "G_PAND", "G_SPARE",
    "Reductible", "One",
    # Arbres
    "FaultTree", "FaultTreeR",
    # Diagrammes de Hasse / coupes / résultats
    "Cut", "Link", "DownHasseDiagram", "UpHasseDiagram", "ReliabilityResult",
]
