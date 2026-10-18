# ANALYSE — DFT2HD2ReliabilityR

> Analyse technique complète du dépôt : structure, état réel du code, blocage publication
> PyPI, et plan pour en faire le socle d'un **modèle IA d'aide à la décision de maintenance**.
> Chaque action corrective renvoie au journal `CORRECTIONS.md`.

*Date d'analyse : 2026-10 — Analyse réalisée par exécution réelle du code (venv +
pytest : `networkx`, `sympy`, `matplotlib`), pas par simple lecture.*

---

## 1. Périmètre analysé

| Fichier | Contenu | Taille |
|---|---|---|
| `LogicDoorLib.py` | Portes logiques symboliques : `G_ID, G_NOT, G_OR, G_AND, G_PAND, G_FDEP, G_SPARE, G_Gen` (encodage binomial ±1 des implicants) | 477 l. |
| `FaultTreeLib.py` | `FaultTree` : graphe d'arbre de défaillance (matrice d'adjacence, `NewRelation`, `Sort`, `ViewGraph`) | 276 l. |
| `FaultTreeRLib.py` | `FaultTreeR` : fiabilité récursive de l'arbre (valeurs OU fonctions de fiabilité par composant) | 601 l. |
| `HasseDiagramLib.py` | `Cut` (coupes minimales), `Link` (liens minimaux), `DownHasseDiagram` / `UpHasseDiagram` (treillis + `GetPolyFiab`) | 1180 l. |
| `docs/` + `conf.py` | Sphinx (`autodoc`, `viewcode`, …), compilé depuis la racine | — |
| Racine **et** `source/` | **4 modules dupliqués à l'identique** (vérifié par `cmp`) | 5 111 l. |

**Outillage "paquet" inexistant** : pas de `setup.py`, pas de `pyproject.toml`, pas de
`tests/`, pas de CI. → la publication PyPI est *impossible en l'état*, indépendamment
des bugs (voir §3).

---

## 2. Ce que le projet veut faire (et fait en principe)

Socle méthodologique de fiabilité pour maintenanciers :

1. Modéliser un système en **arbre de défaillance** statique avec portes
   `OR / AND / NOT / PAND / FDEP / SPARE` (`LogicDoorLib`, `FaultTreeLib`).
2. En déduire **coupes minimales** et **liens minimaux** (`Cut`, `Link`).
3. Poser le **treillis de Hasse descendant / ascendant** et en extraire le
   **polynôme de fiabilité symbolique** (`R_sys` avec `sympy`) ou ses valeurs numériques
   à des instants donnés (`DownHasseDiagram.GetPolyFiab`, `UpHasseDiagram.GetPolyFiab`,
   `FaultTreeR.RecursiveReliability`).
4. Visualiser (`ViewGraph` via networkx/matplotlib).

C'est exactement la matière dont a besoin unequette de **décision de maintenance**
(§4) : cause de panne structurelle (coupes), chemins de survie (liens),
probabilisation (polynômes), importance des composants (dérivée du polynôme).

---

## 3. Constats vérifiés par exécution

### 3.1 Ce qui fonctionne après correctifs (CORRECTIONS.md)
- Polynômes corrects sur arbres simples : OR 2 comp. → `R1·R2` ✔ ;
  AND 2 comp. → `R1 + R2 − R1·R2` ✔ ; valeur numérique 0,9/0,9 → 0,81 ✔.
- Sémantique des portes `G_OR / G_AND / G_NOT / G_FDEP` correcte ✔.
- `FaultTreeR.RecursiveReliability` aboutit (format `{0: [symbole], 1: [[valeur]]}`) ✔.

### 3.2 Bugs bloquants (tous reproduction negative→positive tracée dans CORRECTIONS.md)
| # | Bug | Preuve d'exécution |
|---|---|---|
| B1 | `FaultTree.Update()` / `FaultTreeR.Update()` exigeaient `ID_P` non fourni par `NewRelation` | `TypeError` sur toute création d'arbre |
| B2 | `DownHasseDiagram` et `Link` appelaient `Cut.CollectCut()` sans `P_Gen` | `TypeError` |
| B2b | `UpHasseDiagram` passait l'arbre à `Link(P_NOT, …)` à la place du `NOT` | `AttributeError` |
| B3 | `G_SPARE` : temps triés utilisés comme index → `IndexError` | `Temp5[20]` sur liste de 2 |
| B4 | Boucle infinie ; l'exemple officiel 12 composants (bloc `1161-1175` de `HasseDiagramLib`) figeait > 40 s | tué par `timeout` |
| B5 | `CollectCut` générait des coupes mathématiquement fausses sur le même arbre : singletons `c1..c6` + la coupe "tout-à-1" au lieu de `{c0} ∪ ({c1∨c2∨c3} ∧ {c4∨c5∨c6})` | **corrigé — CORRECTION-09** : `test_collect_cut_12_composant_coupes_correctes` verrouille les 10 coupes exactes |
| B6 | Convention d'ordre 0-based vs 1-based mal fixée (`InOrder` 1-based, appelants 0-based) → PAND fausse *silencieusement* | result `[0,0]` au lieu de la réduction correcte |
| B7 | `Reductible` plantait (`IndexError`) sur longueurs inégales — aucune validation d'entrée dans la librairie | crash reproduit |
| B8 | `print()` de debug dans le calcul (stdout pollue notebooks/pipelines) | "Porte PAND appellee 2", "Bad", "Here", `print(R2)` |

### 3.3 Limites structurelles (documentées, non corrigées dans cette passe)
- `LIMITATION-09` — la fusion des coupes dans `Cut.CollectCut` ne respectait pas la
  structure d'arbre : domination testée **composante par composante sur tout l'arbre**
  (`HasseDiagramLib` lignes ~141-151) et `Cut.Leaves` associait à chaque feuille *tous* les
  singletons de composants. Conséquence : dès qu'une feuille-bundle (ex. OR à 3 inputs)
  apparaît, l'union des coupes déborde. C'était la cause racine de B4 et de B5.
  → **RÉSOLUE par CORRECTION-09** (moteur topologique porte-par-porte ; coupes exactes
  `{c0} ∪ 9 paires`, forme fermée Down/Up vérifiées — cf. `CORRECTIONS.md` §2, CORRECTION-09).
- Registres globaux (`FaultTrees`, `Cuts`, `Links`, …) jamais nettoyés → fuite mémoire
  en usage long.
- API inconsistante : `DownHasse.GetPolyFiab()` renvoyait `1−P` (fiabilité) alors que
  `UpHasse.GetPolyFiab()` renvoyait `P` (commenté `1-P` désactivé) ; `Label` sert tantôt
  de nom de porte, tantôt de symbole `sympy`.
  → **RÉSOLU par CORRECTION-10** : dataclasse `ReliabilityResult` avec une sémantique
  explicite — la fiabilité système est garantie identique Down et Up ; la compatibilité
  d'indexation `[0]`/`[1]` est conservée. La polysémie de `Label` reste pour la v2 (§4.3).
- Perf : treillis complet en `O(2^n)` (```DownHasse``` boucle `while` sur tous les
  nœuds du treillis), `Sort` en `O(k²)`. Plafond pratique ~**12 composants utiles** ;
  au-delà, prévoir BDD / troncature de treillis (feuille de route §4).
- Exemples `"""…" au milieu des fichiers` = code **jamais exécuté** (c'est pour ça que
  les bugs B1-B4 ont survécu) → à convertir en *doctest* réels.
  → **FAIT (CORRECTION-12)** : 17 doctests réels exécutés en CI
  (`pytest --doctest-modules src`), sorties recopiées de l'exécution réelle.
- Dépendances dures `matplotlib`+`networkx` juste pour `ViewGraph` → désormais
  importées **paresseusement** (`CORRECTION-04`), candidate à l'extra `[viz]` sur PyPI.

---

## 4. Publication PyPI — feuille de route

### 4.1 État actuel vs exigence PyPI
| Exigence | État |
|---|---|
| `pyproject.toml` (PEP 621) | ✅ **CORRECTION-11** (setuptools, version 0.2.0, deps `sympy` + extras `[viz]`/`[test]`) |
| Structure `src/paquet/` | ✅ **CORRECTION-11** (`src/dft2hd2reliabilityr/`, imports relatifs, doublons racine/`source/` supprimés — renommages en `gates.py`/`hasse.py`… pour la v2) |
| Suite de tests | ✅ 14 tests unitaires + 17 doctests (`pytest -q` 1,7 s ; `pytest --doctest-modules src -q` 0,5 s) |
| Doc `Sphinx` | ✅ (à rebrancher sur `src/dft2hd2reliabilityr/` — `conf.py` actuel pointe sur la vieille racine) |
| CI (tests + build + publication) | ✅ **CORRECTION-12** (`.github/workflows/ci.yml` : ruff + pytest + doctests + build + `twine check` + smoke wheel) |
| Publication PyPI réelle | ✅ **0.2.0 publiée le 2026-10-18** — https://pypi.org/project/dft2hd2reliabilityr/ (twine check PASSED, install venv neuf vérifiée ; cf. CORRECTIONS.md §6) |
| Licence compatible | ✅ `MIT` (`LICENSE`, repris dans `pyproject.toml`) — build wheel vérifié en venv |

### 4.2 Layout cible proposé
```
DFT2HD2RELIABILITYR/
├── pyproject.toml
├── src/dft2hd2reliabilityr/
│   ├── __init__.py          # exports propres (pas de import * chaîné)
│   ├── gates.py             # LogicDoorLib
│   ├── fault_tree.py        # FaultTreeLib + FaultTreeR réunis
│   ├── hasse.py             # Cut / Link / Down / Up
│   ├── viz.py               # ViewGraph* (extra [viz])
│   ├── importance.py        # P1 : Birnbaum, Fussell-Vesely (socle décision IA)
│   ├── sampling.py          # P2 : Monte-Carlo DFT -> dataset
│   └── ml.py                # P3 : pipeline décision maintenancier (extra [ml])
├── tests/
├── docs/
└── ANALYSE.md, CORRECTIONS.md
```
`pyproject.toml` minimal : `dependencies = ["sympy"]` ; `[project.optional-dependencies]`
`viz = ["matplotlib", "networkx"]`, `ml = ["scikit-learn", "pandas"]`.

### 4.3 Références d'API à figer avant publication (v2)
- Convention **0-based homogène** pour `Orders` (la normalisation auto n'est que
  transition : `CORRECTION-06`) ; signature PAND explicite.
- `GetPolyFiab` → retourne un dataclasse unique `ReliabilityResult(symbol, values,
  times)` avec la même sémantique Down/Up (fiabilité), et `unreliability()` explicite.
- `NewRelation` lève `InvalidRelationError` au lieu de *supprimer silencieusement*
  la relation invalide (comportement `Update` actuel). Registres globaux supprimés.
- Nommage en anglais, docstrings EN standard Google; README FR préservé.

---

## 5. IA de décision de maintenance — le cas d'usage

C'est le cœur de ta demande. La bibliothèque est déjà **~60 % du socle d'un moteur de
décision expliquable** parce qu'elle produit les objets à valeur décisionnelle :

- **Coupes minimales** = *tous les scénarios de panne système* — candidats directs à la
  priorisation d'intervention.
- **Liens minimaux** = toutes les "chaînes de survie" — utiles pour la redondance.
- **Polynôme R(t)** = couche probabiliste différentiable.

### 5.1 Trois couches IA possibles
```
   ┌────────────────────────────────────────────────────┐
   │ Option A — ANALYTIQUE (sans apprentissage)  [P1]   │
   │  Birnbaum / Fussell-Vesely / criticité             │
   │  → "quel composant intervenir en premier?"         │
   ├────────────────────────────────────────────────────┤
   │ Option B — PRÉDICTIF (hybride)              [P2/P3]│
   │  R_i(t+Δt) prédite par capteurs (GBM/LSTM)         │
   │  → injectée dans le DFT → R_sys(t)                 │
   │  → seuil d'alerte sur R_sys                        │
   ├────────────────────────────────────────────────────┤
   │ Option C — PRESCRIPTIF (MDP / RL)           [P3]   │
   │  états = niveaux de dégradation                    │
   │  actions = {rien, inspecter, réparer}              │
   │  récompense = disponibilité − coût                 │
   │  simulateur d'entraînement = DFT (digital twin)    │
   └────────────────────────────────────────────────────┘
```
La **force structurale** de cette approche : une coupes d'explication (le "pourquoi")
est déjà calculée par la bibliothèque — ce que l'IA apprend habituellement à coûteux
apr coup (type SHAP). La décision devient **traçable au niveau structure**.

Le point dangereux : avec les coupes fausses (ex-LIMITATION-09) l'IA apprend le bruit →
**l'ordre des couches doit être : corriger → puis IA** (correction faite : CORRECTION-09).

### 5.2 Plan par lots
- **P0 (fait)** — endurcissement : correctifs `CORRECTION-01…12` + 14 tests verts +
  17 doctests (09 = LIMITATION-09 ; 10 = `ReliabilityResult` Down/Up unifiés ;
  11 = packaging `src/` + `pyproject.toml` ; 12 = CI/lint/doctests).
- **P1 — `importance.py`** : Birnbaum (dérivée ∂R/∂R_i du polynôme `sympy`),
  Fussell-Vesely via coupes, ranking libre → décision "qui en premier" sans data.
- **P2 — `sampling.py`** : Monte-Carlo sur l'arbre → dataset (état, panne système)
  pour entraîner la couche B là où les données réelles sont rares.
- **P3 — `ml.py`** : (a) priorisation C&F indisponibilité+coût ; (b) `GBM/LSTM` sur la
  dégradation des composants → `R_i(t)` ; (c) RL si le P&G récompense est saisi.
- **Lise note (§3.3)** : limites de performance (~12 comp. utiles) définissent le
  périmètre voulu de la P1/P2 ; la couche ML ne réclame pas le treillis complet.

---

## 6. Propos final
1. **Publiable techniquement** : les verrous honnêtes levés (`CORRECTION-01…12`) —
   coupes exactes, contrat `ReliabilityResult` unifié, package installable, CI verte.
   Le *seuil* reste la décision de l'auteur (version, nom final du package).
2. **Un seul chemin physique** : **FAIT (CORRECTION-11)** — layout `src/` unique,
   doublons supprimés (`pyproject.toml` + wheel vérifiée).
3. **Réparer `LIMITATION-09`** — **FAIT (CORRECTION-09)** : réécriture de `CollectCut`
   structurée par porte, coupes exactes + forme fermée vérifiées. C'était le verrou
   scientifique principal ; il est levé.
4. **Ensuite** : monter la couche décision IA (importance → sampling → ML/RL) telle
   que §5 ; préparer v2 (renommage modules, erreurs typées, 0-based homogène).

---

*Auteur de l'analyse : audit technique OpenCode (GLM) — documents frères : `CORRECTIONS.md`
(journal bilingue de toutes les modifications), `README.rst` (quickstart mis à jour),
`tests/test_dft2hd2reliabilityr.py` (preuves d'exécution).*
