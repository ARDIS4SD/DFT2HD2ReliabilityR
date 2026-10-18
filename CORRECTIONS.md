# CORRECTIONS.md — journal complet des modifications

> Chaque modification est numérotée, localisée (fichier + anciens numéros de ligne),
> justifiée (bug observé **par exécution**, pas par lecture) et verrouillée par un test
> de `tests/test_dft2hd2reliabilityr.py`. Rien n'est modifié "en creux".
>
> Règle d'emplacement (depuis CORRECTION-11) : le **package `src/dft2hd2reliabilityr`**
> est l'unique source de vérité — les copies de la racine et l'ancien dossier `source/`
> ont été supprimés. `pyproject.toml` (PEP 621) décrit le packaging.

## Sommaire
1. [Modifications de code (tableaux par fichier)](#1-modifications-de-code)
2. [Corrections détaillées (une section par ID)](#2-corrections-détaillées)
3. [LIMITATION-09 (historique — corrigée par CORRECTION-09)](#3-limitation-09)
4. [À traiter avant publication PyPI (P0 restant)](#4-p0-restant)

---

## 1. Modifications de code

### `FaultTreeLib.py`
| ID | Ancien | Nouveau | Test |
|---|---|---|---|
| 04 | `import networkx as nx` + `import matplotlib.pyplot as plt` en tête de module | supprimés ; import paresseux dans `ViewGraph` avec message `pip install matplotlib networkx` | (indirect : import du module sans matplotlib) |
| 11 | module déplacé racine → `src/dft2hd2reliabilityr/` ; `from LogicDoorLib import *` absolu → `from .LogicDoorLib import *` | import package via `pip install -e .` |
| 12 | pseudo-exemple `InOrder2` (`>>> self=(1),xx=…`) | doctest réel `FaultTree.InOrder2(None,[1,3,2],[1,2,30])` → `False` | `pytest --doctest-modules src -q` |
| 01 | `def Update(self,ID_P ):` | `def Update(self,ID_P=None):` + `if ID_P is None: ID_P = ID_G` ; docstring annotée | `test_new_relation_fonctionne_nativement` |
| 04 | `ViewGraph` : `G=nx.DiGraph()` en tête | `try: import networkx… / matplotlib… except ImportError → ImportError explicite` | (indirect) |

### `FaultTreeRLib.py`
| ID | Ancien | Nouveau | Test |
|---|---|---|---|
| 01b | `def Update(self,ID_P):` | `def Update(self,ID_P=None):` + défaut `ID_G` + docstring | `test_faultree_r_reliabilite_recursive` |
| 11 | module déplacé racine → `src/dft2hd2reliabilityr/` ; 3 imports absolus → relatifs | import package via `pip install -e .` |
| 12 | pseudo-exemple `InOrder2` (`>>> self=(1),xx=…` / « Output: True ») | doctest réel `FaultTreeR.InOrder2(None,[1,3,2],[1,2,30])` → `True` | `pytest --doctest-modules src -q` |
| 04 | imports `networkx`/`matplotlib.pyplot` au top | supprimés ; import paresseux dans `ViewGraph` | (indirect) |
| 03 | `print("Here")` + `print(j)` dans `BranchReliability` | `logger.debug("BranchReliability: computing node %s", j)` | `test_faultree_r_reliabilite_recursive` (sortie stdout vide) |
| — | imports `logging`/`logger` ajoutés en tête | — | — |

### `HasseDiagramLib.py`
| ID | Ancien | Nouveau | Test |
|---|---|---|---|
| 03 | imports `logging`/`logger` ajoutés en tête ; `matplotlib`/`networkx` retirés du top | — | — |
| 02 | `MyCut.CollectCut()` (dans `DownHasseDiagram.__init__`) | `MyCut.CollectCut(G_Gen)` | `test_or_gate_down_hasse` |
| 02 | `self.Cut.CollectCut()` (dans `Link.__init__`) | `self.Cut.CollectCut(G_Gen)` | `test_and_gate_up_hasse` |
| 02b | `MyLink=Link(self.Tree,self.IndIndex)` | `MyLink=Link(G_NOT,self.Tree,self.IndIndex)` | `test_and_gate_up_hasse`, `test_up_hasse_12_composants_se_termine` |
| 08 | boucle de complétion du treillis **descendant** sans garde | garde `_sweep` + levée `RuntimeError("…did not converge…")` quand la génération devient vide ou dépasse `2**NComponent+10` boucles | garanti a posteriori par `test_down_hasse_12_composants_poly_ferme` (CORRECTION-09 : le treillis 12-comp converge désormais au lieu de figer) ; l'ancien test de levée a été remplacé |
| 08 | boucle de complétion du treillis **ascendant** (`xx==0`) sans garde | même garde | `test_up_hasse_12_composants_se_termine` |
| 03 | `print("\n Minimal Links")` + `print(self.MinLink)` (init `Up`) | `logger.debug("Minimal links: %s", …)` | `test_and_gate_up_hasse` (stdout vide) |
| 03 | `print(R2)` (fin de `UpHasseDiagram.GetPolyFiab`) | `logger.debug("GetPolyFiab: individual reliabilities %s", R2)` | `test_and_gate_up_hasse` (stdout vide) |
| 10 | `Down.GetPolyFiab` / `Up.GetPolyFiab` renvoyaient `[poly, [val]]` brut, sémantique implicite hétérogène (`1-P` sans doc, `1-P` seulement en commentaire pour Up) | les deux renvoient une **dataclasse `ReliabilityResult`** (contrat : fiabilité système, champs nommés) ; Up simplifie/développe l'expression comme Down ; compat `[0]`/`[1]` construite | `test_getpolyfiab_unifie_down_up_reliability_result` |
| 11 | `from FaultTreeLib import *` (absolu, racine) | `from .FaultTreeLib import *` (package relatif) | import package via `pip install -e .` |
| 12 | 27 pseudo-exemples `>>>` morts dont `Cut.InOrder2` / `Link.InOrder2` | doctest réel `Cut.InOrder2(None,[1,3,2],[1,2,30])` → `False`, idem `Link.InOrder2` ; 2 exemples imbriqués faux corrigés en prose | `pytest --doctest-modules src -q` (17 doctests) |
| 04 | `ViewGraph` Down + Up : `G=nx.DiGraph()` en tête | import paresseux `networkx`/`matplotlib` + `ImportError` explicite (2 occurrences) | (indirect) |

### `HasseDiagramLib.py` (section CORRECTION-09 — voir détail au §2)
| ID | Ancien | Nouveau | Test |
|---|---|---|---|
| 09a | `Leaves()` : chaque feuille recevait les singletons de **tous** les composants | singletons des **bits propres** de chaque feuille | `test_collect_cut_12_composant_coupes_correctes` |
| 09 | `CollectCut` : fusion par dominance univers + décalage d'index porte/Orders après Sort + P_Gen sur liste plate + coupe = dernier résultat | moteur **topologique porte-par-porte** (`_CarrierNodes`, `_PackInputs`, `_FlatOf`, Kahn + garde-boucle), livre de bord aligné `rowNum`, coupe = **sortie du nœud racine** | 3 tests 12-composants + non-régression complète |

### `LogicDoorLib.py`
| ID | Ancien | Nouveau | Test |
|---|---|---|---|
| — | imports `logging`/`logger` ajoutés en tête | — | — |
| 05 | `Reductible` : `sum(abs(x[i]-y[i]))` sans contrôle | garde `len(x)!=len(y)` → `ValueError("same length…")` | `test_reductible_longueur_incoherente_leve_erreur` |
| 03 | `G_AND` : `print("Bad")` quand littéraux incompatibles (1×(−1)) | `logger.debug("G_AND: incompatible literals…")` | `test_gportes_de_base` (comportement inchangé) |
| 06 | `G_PAND` : `InOrder(Orders,Times)` en 1-based alors que des appelants passaient du 0-based → résultat faux silencieux (`[[0,0]]`) | normalisation : si `min(Orders)==0` → décalage +1 + log; si négatif → `ValueError` ; `print("Porte PAND appellee 1/2")` → `logger.debug` | `test_g_pand_orders_0_based_normalise`, `test_g_pand_orders_1_based_convention` |
| 07 | `G_SPARE` : `Orders=Order(Times)[1]` (liste triée) puis `Temp5[int(Temp3[i])]` → le **temps** sert d'index → `IndexError` (ex. `Temp5[20]`) | `Ranks=Order(Times)[0]` puis tri des primaires/veilles par `(rang, index)` → indices d'entrée valides | `test_g_spare_ne_plante_plus` |
| 12 | 13 pseudo-exemples `>>>` morts (fragments Python invalides, sorties fausses, « Porte PAND appellee 1 » hérité d'un print supprimé) | 13 doctests réels exécutés, sorties recopiées de l'exécution (dont aliasing détecté : entrées fraîches) | `pytest --doctest-modules src -q` |

### Fichiers créés (hors code préexistant)
| Fichier | Rôle |
|---|---|
| `tests/conftest.py` | expose `src/` au `sys.path` pour pytest (CORRECTION-11) |
| `tests/test_dft2hd2reliabilityr.py` | 14 tests verrouillant chaque correction |
| `ANALYSE.md` | rapport d'analyse complet |
| `CORRECTIONS.md` | ce journal |
| `src/dft2hd2reliabilityr/__init__.py` | package (version, `__all__`, CORRECTION-11) |
| `pyproject.toml` | packaging PEP 621 (setuptools, extra `[viz]`, ruff, pytest) |
| `.github/workflows/ci.yml` | CI : lint ruff + pytest + doctests + build/twine (CORRECTION-12) |

> Rappels **non modifiés volontairement** (comportements préservés en P0) :
> registres globaux (`FaultTrees`, `Cuts`, …), convention d'accumulation interne
> Down (1−P) vs Up (P) — le contrat public est unifié par CORRECTION-10,
> suppression silencieuse des relations invalides dans `Update`, `Sort` en O(k²),
> aliasing d'entrée des portes (constat CORRECTION-12 §4). Tout est listé au §3 / §4.

---

## 2. Corrections détaillées

### CORRECTION-01 / 01b — signature `Update`
- **Où** : `FaultTreeLib.py` (`class FaultTree.Update`) ; `FaultTreeRLib.py` (`class FaultTreeR.Update`).
- **Bug observé** : `NewRelation` appelle `self.Update()` sans le 2ᵉ argument requis. La
  première commande de la bibliothèque — créer un arbre — levait donc `TypeError:
  Update() missing 1 required positional argument: 'ID_P'` sur **tout** usage.
  Cela reste invisible dans le dépôt car tous les exemples vivent dans des chaînes
  `"""…"""` jamais exécutées.
- **Correction** : paramètre par défaut `ID_P=None` résolu en `ID_G` (lien : `from
  LogicDoorLib import *` en tête). Les docstrings mentionnent la correction.
- **Alternatives écartées** : passer `ID_G` explicitement à cada call-site — plus
  restrictif (bloque les étiquettes personnalisées).
- **Vérification** : `test_new_relation_fonctionne_nativement`,
  `test_faultree_r_reliabilite_recursive`, plus les 4 tests Hasse qui créent des arbres.

### CORRECTION-02 / 02b — appels `CollectCut` / `Link` mal fichus
- **Où** : `DownHasseDiagram.__init__`, `Link.__init__`, `UpHasseDiagram.__init__` (HasseDiagramLib).
- **Bug observé** :
  1. `MyCut.CollectCut()` sans `P_Gen` → `TypeError` (le paramètre `P_Gen` est la porte
     générique `G_Gen` requise pour évaluer chaque relation).
  2. `Link(P_NOT, Tree=…)` mais `UpHasseDiagram` appelle `Link(self.Tree, …)` en position 1 :
     l'arbre remplace le `NOT` → plus tard `temp=P_NOT([self.Cut.Cut])` exécute l'arbre
     comme une fonction → `AttributeError: 'FaultTree' object is not callable` (observé
     sous la forme `'list' object has no attribute 'Leaves'`).
- **Correction** : `CollectCut(G_Gen)` ×2 ; `Link(G_NOT, self.Tree, self.IndIndex)`.
- **Vérification** : `test_or_gate_down_hasse` (OR→`R1·R2`), `test_and_gate_up_hasse`
  (AND→`R1+R2−R1·R2`), `test_up_hasse_12_composants_se_termine`.

### CORRECTION-03 — propreté de sortie (logging)
- **Où** : 4 modules ; 8 points d'affichage remplacés.
- **Bug observé** : le calcul émet du texte sur la sortie standard
  (`Porte PAND appellee 1/2`, `Bad`, `Here`, `Minimal Links`, `print(R2)`) — une librairie
  doit rester silencieuse (notebooks, pipelines, CI).
- **Correction** : `logger = logging.getLogger(__name__)` par module ; tous les `print`
  vivants deviennent `logger.debug(...)`. **Niveau API inchangé** ; les traces restent
  activables via `logging.basicConfig(level=logging.DEBUG)`.
- **Vérification** : `capsys.readouterr().out == ""` dans
  `test_or_gate_down_hasse`, `test_and_gate_up_hasse`, `test_faultree_r_reliabilite_recursive`.

### CORRECTION-04 — dépendances visuelles optionnelles
- **Où** : en-têtes des 4 modules + les 4 méthodes `ViewGraph*`.
- **Motif** : `matplotlib`/`networkx` ne servent qu'à `ViewGraph` ; en tête de module ils
  pédent l'import du **moteur de calcul** pour les environnements sans affichage (CI,
  serveurs, docker slim). Candidate dédiée à l'extra `[viz]` (§ANALYSE 4.2).
- **Correction** : imports retirés du top ; `try/except ImportError` paresseux dans
  chaque `ViewGraph` avec message d'aide explicite.
- **Vérification** : la suite teste le moteur ; aucun graphique requis pour la lancer.

### CORRECTION-05 — validation `Reductible`
- **Bug observé** : `Reductible([1,0,1],[1,0])` → `IndexError` (somme `abs` sans garde).
- **Correction** : `ValueError` claire quand les longueurs diffèrent.
- **Alternatives écartées** : `zip()` tronqué — masquerait l'erreur.
- **Vérification** : `test_reductible_longueur_incoherente_leve_erreur`.

### CORRECTION-06 — convention d'ordre de `G_PAND`
- **Bug observé** : `InOrder` (LogicDoorLib) décode les ordres **1-based**
  (`Times[int(Orders[i])-1]`, cf. exemples `Orders=[1,3,2]`), tandis que les appelants
  (ex. tests, paramètres 0-based de `NewRelation`) utilisent du **0-based** → la porte
  PAND interprète l'ordre inversé et renvoie **silencieusement** une coupe nulle
  `[[0,0]]` au lieu du résultat ordonné — reproduction expérimentée.
- **Correction** : normalisation en tête de `G_PAND` :
  * `min(Orders)==0` → décalage `o+1` + `logger.debug` (le 0-based continue de marcher) ;
  * valeur négative → `ValueError` claire ;
  * entrée déjà 1-based → inchangée.
- **Alternatives écartées** : changer la convention d'`InOrder` globalement → rupture
  d'API sur les autres appelants ( hors périmètre P0 ).
- **Vérification** : `test_g_pand_orders_0_based_normalise` (0-based donne désormais le
  résultat de la branche ordonnée), `test_g_pand_orders_1_based_convention` (non-régression).

### CORRECTION-07 — crash `G_SPARE`
- **Bug observé** : `Orders=Order(Times)[1]` prend la liste des **temps triés**
  (ex. `[10,20]`), ensuite utilisée comme *index d'entrée* dans `Temp5[int(Temp3[i])]` →
  `IndexError: list index out of range` dès qu'un temps dépasse la taille de la liste
  (cas reproduit avec `Times=[20,10]`).
- **Correction** : récupérer les **rangs** `Order(Times)[0]` (1-based sur la liste
  saisie), puis trier les primaires (`Temp1`) et les veilles (`Temp2`) par
  `(rang, indice)` → `Temp3/Temp4` contiennent les **indices de `ValuesIn`** attendus
  par la suite du code. La sémantique "pare le k-ième primaire avec le k-ième
  spare, dans l'ordre de failure" est conservée.
- **Alternatives écartées** : patch limité au `try/except` — la mauvaise valeur resterait
  fausse en silence.
- **Vérification** : `test_g_spare_ne_plante_plus` (aucune exception, retour exploitable).

### CORRECTION-08 — garde-fous de convergence du treillis
- **Bug observé** : sur l'arbre canonique 12 composants du dépôt
  (bloc 1161-1175 de `HasseDiagramLib`), `DownHasseDiagram(...)` **ne rend jamais la main**
  (tué par `timeout 40` ; le fingerprint du processus montre la construction bloquée
  après `FaultTree` construit = 9 nœuds). Mécanique identifiée : si la coupe "tout-à-1"
  est déjà présente dans la liste des coupes (fausses — cf. LIMITATION-09), la
  condition d'arrêt `self.NodeGeneration[-1]!=[[1]*NComponent]` ne peut **jamais**
  redevenir vraie (elle ne s'y ajoute pas deux fois) et la génération éponge en liste
  vide → boucle infinie.
- **Correction** : garde `_sweep` dans les deux complétions (Down et Up). Si la
  génération courante devient vide **ou** que le nombre de boucles dépasse
  `2**NComponent + 10`, levée de `RuntimeError("… did not converge …")` avec renvoi vers
  ce document. Le programme se termine toujours, avec une erreur explicite et rapide.
- **Alternatives écartées** : `assert` désactivable en `-O` → non ; `timeout` interne →
  non-déterministe.
- **Vérification** : la levée explicite a d'abord été testée par
  `test_down_hasse_12_composants_leve_erreur_au_lieu_de_figervr` (levée, < 1,05 s), puis
  `test_up_hasse_12_composants_se_termine` (terminaison rapide). Après CORRECTION-09 le
  treillis 12-composants converge normalement : la garantie de marche d'arrêt est
  désormais couverte par `test_down_hasse_12_composants_poly_ferme` / `test_up_hasse_12_composants_poly_ferme`
  (terminaison + forme fermée exacte), et la levée reste un filet de sécurité non atteint.

---

### CORRECTION-09 — moteur de collecte des coupes porte-par-porte (`HasseDiagramLib.py`, classe `Cut`)

C'est la correction de **LIMITATION-09** : le lot suivant du plan P0. Elle réécrit
`Leaves()` et `CollectCut()` et introduit 4 helpers (`_CarrierNodes`, `_IsCutVector`,
`_IsCutList`, `_FlatOf`, `_PackInputs`).

**Répercussions observées avant la correction** (cf. §3, LIMITATION-09) :
- `Cut.Leaves` associait à **chaque** feuille les singletons de **tous** les composants ;
- `CollectCut` fusionnait par dominance composante-composante **sur tout l'arbre** :
  les feuilles des branches voisines fuitent dans le même accumulateur ;
- résultat sur l'arbre canonique 12/7 : singletons `c1..c6` + coupe pleine
  `[1,1,1,1,1,1,1]` au lieu de `{c0} ∪ 9 paires`, et boucle infinie (CORRECTION-08) ;
- defect de **décalage d'index** caché : porte/Orders/Times/IndicesPrincipal été
  lus sur la ligne `Temp3[k][i]` alors que la relation triée i correspond à la ligne
  `IdxTable[0][i]` (mismatch dès que `Sort` réordonne).

**Nouveau moteur** — 4 mécanismes :
1. `Leaves()` : chaque feuille → singletons de **ses propres** bits réels.
2. `_PackInputs` : pour une relation, **un groupe d'entrées par bit actif** du
   vecteur de `IndicesIn` : composant réel k → `[[singleton k]]`, composant virtuel k
   → le groupe de coupes déjà évalué de la porte-fille (via `_CarrierNodes` : le
   vecteur mono-bit qui porte k). La sémantique OR/AND des portes `G_*` (conçues pour
   *une liste de groupes*) est enfin respectée.
3. Boucle **topologique (Kahn)** : on évalue une porte quand toutes ses sorties-filles
   existent ; aucune progression → `RuntimeError("cyclic or malformed tree…")` avec
   garde anti-boucle (`maxGuard`). Plus d'exécution silencieusement fausse ni de blocage.
4. La **coupe système** est celle du *nœud racine* via `Tree.Root()` (et non plus
   "dernière relation accumulée") + livre de bord `RelMat` aligné sur `rowNum`.

**Alignement avec le résultat théorique** (arbre 12/7 : `g11=ID(g10); g10=OR(c0,g9);
g9=AND(g7,g8); g7=OR(c1,c2,c3); g8=OR(c4,c5,c6)`) :
- coupes : `{c0} ∪ {c1,c2,c3}×{c4,c5,c6}` = **10 coupes** exactes ✔
- polynôme Down & Up : `R0·(R1R2R3 + R4R5R6 − R1R2R3R4R5R6)` (forme fermée exacte) ✔
- valeur numérique à `R_k=0.9 ∀k` : **0,8339031** exacte ✔
- non-régression : OR2 → `R1·R2`, AND2 → `R1+R2−R1·R2` inchangés ✔

**Alternatives écartées** :
- patcher uniquement le test de dominance de l'ancienne fusion → le décalage
  d'index et la structure plate restaient ; la composition des portes serait
  demeurée fausse sur les arbres imbriqués ;
- réimplémenter en module séparé → casse l'API existante (`DownHasseDiagram`,
  `Link` consomment `Cut`).

**Vérifications** : `test_collect_cut_12_composant_coupes_correctes`,
`test_down_hasse_12_composants_poly_ferme`, `test_up_hasse_12_composants_poly_ferme`,
plus toute la suite de non-régression antérieure. **13/13 verts en 1,45 s.**

---

### CORRECTION-10 — unification `GetPolyFiab` Down/Up : dataclasse `ReliabilityResult` (`HasseDiagramLib.py`)

**Hétérogénéité observée** (ANALYSE.md §3.3) : `DownHasseDiagram.GetPolyFiab`
renvoyait `[simplify(expand(1-P)), [1-P2[k]]]` (sémantique implicite « fiabilité = 1 -
defaut ») tandis que `UpHasseDiagram.GetPolyFiab` renvoyait le `[P, P2]` brut, sans
`simplify`/`expand`, la variante `1-P` étant seulement en commentaire — le sous-module
`FaultTreeRLib.BranchReliability` consommait d'ailleurs l indexing aveugle `MyPolyFiab[0]`,
`MyPolyFiab[1]`.

**Correctif** :
1. Nouvelle dataclasse `ReliabilityResult` (en tête de `HasseDiagramLib`) : champs
   nommés `poly_symbolic`, `reliability_numeric` (par point de temps), `method`
   (traçage du treillis de coupes ou de liens), `n_min_items` (nombre de coupes /
   liens minimaux) ; contrat documenté : **l'objet représente TOUJOURS la fiabilité
   système R_sys**.
2. Down : `R_sys = 1 - somme des poids de défaillance` → `ReliabilityResult`
   (expression `simplify(expand(1-P))`, valeurs `[1-P2[k]]`).
3. Up : `R_sys = somme des poids de réussite` → `ReliabilityResult` ; l'expression
   symbolique est désormais `simplify(expand(P))` comme Down (`[P, P2]` brut et le
   vieux commentaire `#return [...,1-P...]` supprimés).
4. Compatibilité ascendante : la dataclasse implémente `__getitem__` (0 → expression
   symbolique, 1 → valeurs), `__len__`, `__iter__`, `to_list()` — l'ancien usage
   `myPolyFiab[0]` / `myPolyFiab[1]` continue de marcher (vérifié dans
   `FaultTreeRLib` par `test_faultree_r_reliabilite_recursive`).

**Verrouillé** par `test_getpolyfiab_unifie_down_up_reliability_result` : Down et Up
donnent la même fiabilité système sur l'arbre 12 composants (égalité symbolique
`sympy.simplify(d - u) == 0`, égalité numérique, compatibilité indexation).

---

### CORRECTION-11 — packaging PEP 621 + layout `src/` + suppression des doublons

**Avant** : les 4 modules existaient 2 fois (racine + `source/`) sans `pyproject.toml`,
avec des imports absolus mutuellement entrecroisés (`from FaultTreeLib import *`), sous
PYPI cette librairie ne pouvait pas s'installer proprement ; `tests/conftest.py` pointait
sur la racine.

**Correctif** :
1. **Layout `src/` unique** : `src/dft2hd2reliabilityr/` reçoit les 4 modules déplacés
   (pas copiés) + `__init__.py` (version `0.2.0`, exports principaux
   `FaultTree`, `FaultTreeR`, `DownHasseDiagram`, `UpHasseDiagram`, `ReliabilityResult`,
   `Cut`, `Link`, `G_*`, `Reductible`, `One`, `__all__`).
2. **Imports relatifs** au package (`from .LogicDoorLib import *`, `from .FaultTreeLib
   import *`, `from .HasseDiagramLib import *`) — annotés `# CORRECTION-11`.
3. **Suppression** de l'ancien dossier `source/` (leurs copies exigeaient une
   synchronisation manuelle par `cmp`/`cp`, cf. §5) et des 4 copies de racine.
4. `pyproject.toml` (PEP 621) : setuptools ; nom `dft2hd2reliabilityr` ; version
   `0.2.0` ; `requires-python >= 3.9` ; dépendance dure `sympy>=1.9` uniquement
   (CORRECTION-04) ; extras `[viz]` (matplotlib/networkx, paresseux) et `[test]`
   (pytest) ; extra `[ml]` réservé (commenté) pour la future couche IA ; licence
   MIT du `LICENSE` (copyright 2022 ARDIS4SD) ; `[tool.pytest.ini_options]` et
   `[tool.ruff]`.
5. `tests/conftest.py` : expose `src` au `sys.path` ; les tests importent désormais
   via `dft2hd2reliabilityr.*`.

**Vérifications concrètes** : `pip install -e .` OK (venv Ø network autonome) ;
import + usage complet depuis une arborescence extérieure au dépôt (`cd /tmp &&
python -c "import dft2hd2reliabilityr ..."`) ; build wheel OK
(`dft2hd2reliabilityr-0.2.0-py3-none-any.whl` avec les 5 modules + `LICENSE`) ;
**14/14 tests verts** via pytest après migration.

---

### CORRECTION-12 — CI GitHub Actions, lint minimal, doctests réels

**Avant** : aucun CI, aucun linter, 27 pseudo-exemples `>>>` « morts » (fragments
Python invalides : `>>> Orders=[1,3,2],Times=[10,20,30]`, `>>> x=[1,0,1],y=[1,1,0])`,
sorties attendues FAUSSES — ex. `G_OR` affichait `[[[1,0,1],[1,1,0]],[[1,0,0]]]` pour
un vrai résultat `[[[1, 0, 1], [0, 1, 0]]]`, `G_PAND` embarquait encore le texte d'un
`print` supprimé « Porte PAND appellee 1 »).

**Correctif** :
1. `.github/workflows/ci.yml` : matrix Python 3.9→3.12 ; `pip install -e ".[test,viz]"` ;
   `ruff check src tests` ; `pytest -q` ; `pytest --doctest-modules src -q` ;
   job séparé `package`= build sdist/wheel + `twine check` + smoke-test de la wheel.
2. `pyproject.toml` `[tool.ruff]` : baseline minimale honnête pour un legs
   (~E9/F7/F63/F82) — 0 erreur à la création, sans réécrire 2 500 lignes de style.
3. **17 docstrings converties en doctests réels exécutés** (toutes sorties
   recopiées depuis l'exécution réelle, jamais inventées) : `Order`, `InOrder`,
   `RemoveEmpty`, `Reductible`, `G_ID`, `G_OR`, `G_AND`, `G_NOT`, `G_PAND`,
   `G_FDEP`, `G_SPARE`, `G_Gen`, `ID_G`, `Cut.InOrder2`, `Link.InOrder2`,
   `FaultTree.InOrder2`, `FaultTreeR.InOrder2` ; les 2 exemples imbriqués faux
   (InOrder3 « false », InOrder2 Up « False ») corrigés en prose.
4. **Découverte opportuniste documentée** : certains murs d'aliasing mutent les
   vecteurs partagés en entrée (les portes NOT/PAND réutilisent les objets
   reçues) — c'est pour ça que les attendus ont été fixés depuis des appels à
   entrée fraîche (ce que le doctest fait naturellement). Le non-mutation des
   entrées est renvoyé à une future passe API (v2).

---

## 3. LIMITATION-09 (historique — CORRIGÉE par CORRECTION-09)

**Coupes minimales fausses dès qu'une feuille est un "bundle" multi-composants.**

- **Symptôme** (arbre canonique 12/7 — reproduction `CollectCut` réussie en 0,0 s) :
  coupes obtenues `{[1,0,0,0,0,0,0], [1,1,1,1,1,1,1], [0,0,0,0,0,0,1], …}` — soit
  **singletons c1..c6 + la coupe pleine `[1,1,1,1,1,1,1]`** au lieu de
  `{c0} ∪ ({c1∨c2∨c3} ∧ {c4∨c5∨c6})` = `{c0}` + 9 paires `{ci,cj}`.
- **Causes mécaniques (deux sur-fusions)** :
  1. `Cut.Leaves` (`HasseDiagramLib` ~l.86-108) : chaque feuille d'arbre reçoit les
     singletons de **tous** les composants (`for k in range(NComponent)`), pas celui(s)
     qu'elle contient.
  2. `CollectCut` (~l.141-151) : la fusion `self.Node[inIdx] += self.Node[IdxNode(x)]`
     retient tout nœud `x` **dominant par composants** (test `InOrder2`), sans vérifier
     qu'il appartient à la **sous-arborescence de la porte en cours** ; les feuilles des
     branches voisines fuitent alors dans le même accumulateur.
- **Conséquences** : faux polynômes dès que les entrées de porte sont des bundles
  (motif standard des arbres réels), cf. B4/B5. Le
  test antérieur `test_down_hasse_12_composants_leve_erreur_au_lieu_de_figervr` avait
  transformé le plantage muet en erreur explicite via CORRECTION-08.
- **Correctif proposé (P1)** : réécrire la collecte en moteur « structure-aware » :
  pour chaque relation `porte(entrées→sortie)`, grouper les coupes **directement** à
  partir des relations d'entrées d'attente (inscriptions `IdxTable`), puis appliquer
  la sémantique de la porte ; ajouter un test de référence sur l'arbre 12 composants
  démontrant `{c0} ∪ 9 paires`.

- **FAIT — CORRECTION-09** (section 2, moteur topologique porte-par-porte) :
  `{c0} ∪ 9 paires` exactes + forme fermée vérifiée symboliquement et numériquement.
  Les tests associés sont désormais `test_collect_cut_12_composant_coupes_correctes`,
  `test_down_hasse_12_composants_poly_ferme`, `test_up_hasse_12_composants_poly_ferme`.

---

## 4. P0 restant (avant publication PyPI)

| Priorité | Tâche |
|---|---|
| ~~1~~ ✅ | ~~**LIMITATION-09** : réécriture structure-aware de `CollectCut`~~ → corrigée par **CORRECTION-09** |
| ~~2~~ ✅ | ~~Unifier `GetPolyFiab` Down/Up~~ → **CORRECTION-10** (`ReliabilityResult`, compatibilité construite) |
| ~~3~~ ✅ | ~~Packaging~~ → **CORRECTION-11** (`pyproject.toml` PEP 621, layout `src/`, doublons supprimés ; extra `[viz]` + `[test]`, `[ml]` réservé) |
| ~~4~~ ✅~~5~~ | ~~CI + lint + doctests~~ → **CORRECTION-12** (GitHub Actions `pytest`/doctest/ruff/build/twine ; ruff baseline minimale verte ; 17 doctests réels) |
| 6 | P1..P3 IA de décision (importances, sampling, ml) — cf. `ANALYSE.md` §5. |

---

## 5. Emplacement des fichiers (ancienne règle de sync — OBSOLÈTE depuis CORRECTION-11)

L'ancienne duplication racine ⇄ `source/` (interdite au sens de l'audit : deux
sources de vérité) a été **supprimée** par CORRECTION-11 :

- les 4 modules vivent uniquement dans `src/dft2hd2reliabilityr/` ;
- `source/` n'existe plus ; les copies de racine ont été déplacées (pas copiées) ;
- les imports inter-modules sont **relatifs** (`from .FaultTreeLib import *`) ;
- `pyproject.toml` décrit le package (PEP 621) — `pip install -e .` fonctionne.

---

## 6. Publication PyPI (version 0.2.0)

Événement tracé (pas un correctif de code, mais s'inscrit dans le journal) :

| Élément | Valeur |
|---|---|
| Package / version | `dft2hd2reliabilityr` **0.2.0** |
| URL | https://pypi.org/project/dft2hd2reliabilityr/ |
| Artefacts | wheel `py3-none-any` + sdist `.tar.gz` (upload 2026-10-18) |
| Contrôle avant upload | `python -m build` + `twine check` → **PASSED** sdist & wheel |
| Contrôle après upload | JSON PyPI inspecté (métadonnées : `sympy>=1.9`, extras `[viz]`/`[test]`, MIT, Python ≥3.9, owner `fopoussi`) |
| Vérification d'acceptation | venv **vierge** (`/tmp/opencode/pypi_smoke`) : `pip install dft2hd2reliabilityr` depuis PyPI → import + calcul complet (`R_sys = R1*R2` sur OR 2 composants) ✅ |

Ajustements de métadonnées faits pour l'upload (sans effet sur le comportement
de la bibliothèque, donc non numérotés comme correctifs de code) :

1. `pyproject.toml` : `authors`/`maintainers` avec email + `[project.urls]`
   (Homepage/Repository → dépôt GitHub ARDIS4SD).
2. `README.rst` : soulignage du titre « Pourquoi ce projet est-il utile ? »
   allongé d'un caractère — `twine check` refusait le rendu avec
   « Title underline too short » (RST, ligne 20).

> Hygiène du jeton : l'upload a consommé un jeton d'API PyPI transmis en session ;
> il n'a été ni écrit dans le dépôt ni dans un fichier projet (fichier temporaire
> `/tmp/opencode/pypi_token`, permissions 0600, supprimé par `trap EXIT`
> immédiatement après usage). **Recommandation : révoquer ce jeton sur
> https://pypi.org/manage/account/token/ et préférer un jeton à portée de projet
> (ou le Trusted Publishing GitHub) pour les publications suivantes.**

---

### CORRECTION-13 — hygiène de la description publique PyPI (version 0.2.1)

**Constat** (après publication `0.2.0`, signalé par l'utilisateur) : deux blocs
« livre de recettes développeurs » figuraient sur la **page PyPI publique** parce que
`README.rst` sert de `long_description` :

1. *Vérification* (commandes pytest/doctest ciblant le dépôt de développement,
   inopérantes après un simple `pip install` depuis PyPI) ;
2. *Documentation de projet* (renvois internes `ANALYSE.md` / `CORRECTIONS.md`,
   pertinents uniquement dans le dépôt GitHub).

**Correctif** (sans effet sur le comportement de la bibliothèque) :

1. `README.rst` : les deux blocs **retirés** de la description publique.
2. `contributing.md` (placeholder vide d'origine, 1 octet) : les mêmes contenus
   **déplacés** ici — guide de développement : installation `-e".[test]"`,
   commandes de vérification, tableau de la documentation projet, procédure de
   publication (double bump de version, `twine check`, jeton à portée projet).
3. **Version bump 0.2.0 → 0.2.1** dans `pyproject.toml` ET
   `src/dft2hd2reliabilityr/__init__.py` : la description d'une version déjà
   publiée est **immuable** sur PyPI (ré-upload interdit), seule une
   version croissante devient la version « latest » dont la description
   s'affiche sur la page d'accueil du projet — d'où le rappel dans
   `contributing.md`: la double synchronisation pyproject/__init__ est le
   point de contrôle n°1 avant tout upload.

**Vérifications** : parmi les contenus après rebuild, la description PyPI de 0.2.1
ne contient ni « Vérification », ni « Documentation de projet », ni « CORRECTIONS.md »
(inspectée via le JSON `https://pypi.org/pypi/dft2hd2reliabilityr/json`) ;
`twine check` **PASSED** ; suite 14/14 + 17/17 doctests inchangée.

**Retour de publication** (vérifié en ligne) : `0.2.1` = version latest de
https://pypi.org/project/dft2hd2reliabilityr/ ; description publique confirmée
propre ; installation depuis PyPI dans un venv neuf OK. Leçon appliquée au
dépôt : la ligne d'installation du README ne doit pas épingler un numéro de
version (devient obsolète à chaque release) → rewording agnostique ; le point
de contrôle « double bump pyproject/__init__ » fait partie de la procédure de
publication documentée dans `contributing.md`.

---

*Journal mis à jour lors de la passe de correction 2026-10 ; 14/14 tests verts
(`pytest -q`, 1,73 s) + 17/17 doctests réels (`pytest --doctest-modules src -q `,
0,50 s) + `ruff check src tests` 0 erreur ; **version 0.2.0 hébergée sur PyPI**.*
