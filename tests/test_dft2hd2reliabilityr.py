"""
Suite de verification (smoke tests) — DFT2HD2ReliabilityR.

Chaque test reference la correction qu'il verrouille (CORRECTIONS.md) :
  - CORRECTION-01 : FaultTree.Update / FaultTreeR.Update (TypeError sur NewRelation)
  - CORRECTION-02 / 02b : Cut.CollectCut(G_Gen) + Link(G_NOT, ...)
  - CORRECTION-05 : Reductible (validation longueur)
  - CORRECTION-06 : G_PAND (normalisation 0-based -> 1-based)
  - CORRECTION-07 : G_SPARE (IndexError)
  - CORRECTION-08 : garde-fous de convergence Down/UpHasse (boucle infinie -> RuntimeError)
  - CORRECTION-09 : moteur de collecte porte-par-porte — LIMITATION-09 corrigee :
    coupes minimales EXACTES + forme fermee sur l'arbre canonique 12 composants.
  - CORRECTION-10 : GetPolyFiab Down/Up unifie via la dataclasse ReliabilityResult
    (fiabilite systeme ; compatibilite d'indexation [0]/[1] conservee).

Lancement :  <venv>/bin/python -m pytest -v
"""
import io
import contextlib
import time as _time

import pytest

import matplotlib
matplotlib.use("Agg")  # pas de fenetre pendant les tests

from dft2hd2reliabilityr.FaultTreeLib import FaultTree
from dft2hd2reliabilityr.FaultTreeRLib import FaultTreeR, One
from dft2hd2reliabilityr.HasseDiagramLib import (
    DownHasseDiagram, ReliabilityResult, UpHasseDiagram)
from dft2hd2reliabilityr.LogicDoorLib import (
    G_AND, G_FDEP, G_NOT, G_OR, G_PAND, G_SPARE, Reductible)


def _silence_logs():
    """Neutralise la sortie standard ET le logger pendant un bloc."""
    import logging
    logging.disable(logging.CRITICAL)
    return contextlib.ExitStack()


def _build_or_tree(ncomps=3):
    """Arbre depanifance : OR2(c0,c1) — GT = defaillance systeme si un composant tombe."""
    tree = FaultTree(ncomps)
    tree.NewRelation(3, [1, 1, 0], [0, 0, 1])
    return tree


def _build_and_tree(ncomps=3):
    """Arbre défaillance : AND2(c0,c1) — GT = defaillance si les deux tombent."""
    tree = FaultTree(ncomps)
    tree.NewRelation(4, [1, 1, 0], [0, 0, 1])
    return tree


# --------------------------------------------------------------------------
# CORRECTION-01 : l'API de base doit fonctionner SANS monkeypatch
# --------------------------------------------------------------------------
def test_new_relation_fonctionne_nativement():
    """CORRECTION-01 : NewRelation ne leve plus TypeError (Update(ID_P=None))."""
    tree = _build_or_tree()
    assert len(tree.Node) == 2
    assert tree.IdxTable[0] == [0]
    assert tree.Label[1] == "G_OR"  # etiquette par defaut ID_G


# --------------------------------------------------------------------------
# CORRECTION-02 / 02b : les moteurs Hasse doivent se construire nativement
# --------------------------------------------------------------------------
@pytest.mark.skipif(True, reason="Voir test_or_gate_down_hasse: construit via DownHasseDiagram")
def _unused_marker():
    pass


def test_or_gate_down_hasse(capsys):
    """CORRECTION-02 : DownHasseDiagram marche sans patch ; poly OR = R1*R2."""
    import sympy
    R1, R2 = sympy.Symbol("R1"), sympy.Symbol("R2")
    tree = _build_or_tree()
    with _silence_logs():
        hasse = DownHasseDiagram(
            tree, [0, 1], [R1, R2], [[1], [1]], [One, One], [0], 1
        )
        poly = hasse.GetPolyFiab()
    assert sympy.simplify(poly[0]) == R1 * R2
    # CORRECTION-03 : aucune trace résiduelle dans la sortie standard
    assert capsys.readouterr().out == ""


def test_and_gate_up_hasse(capsys):
    """CORRECTION-02b : UpHasseDiagram marche sans patch ; poly AND = R1+R2-R1*R2."""
    import sympy
    R1, R2 = sympy.Symbol("R1"), sympy.Symbol("R2")
    tree = _build_and_tree()
    with _silence_logs():
        hasse = UpHasseDiagram(
            tree, [0, 1], [R1, R2], [[1], [1]], [One, One], [0], 1
        )
        poly = hasse.GetPolyFiab()
    assert sympy.simplify(poly[0]) == -(R1 * R2) + R1 + R2
    assert capsys.readouterr().out == ""


def test_or_gate_valeur_numerique():
    """Sanité numerique : OR gate sur reliabilites 0.9/0.9 -> dispo systeme 0.81."""
    tree = _build_or_tree()
    with _silence_logs():
        hasse = DownHasseDiagram(
            tree, [0, 1], [0, 1], [[0.9], [0.9]], [One, One], [0], 1
        )
        _ = hasse.GetPolyFiab()
    # GetPolyFiab -> [poly_symbolique, valeurs par temps]
    vals = hasse.GetPolyFiab()
    assert abs(vals[1][0] - 0.81) < 1e-9


# --------------------------------------------------------------------------
# CORRECTION-05 : Reductible valide
# --------------------------------------------------------------------------
def test_reductible_longueur_incoherente_leve_erreur():
    """CORRECTION-05 : IndexError -> ValueError claire."""
    with pytest.raises(ValueError, match="same length"):
        Reductible([1, 0, 1], [1, 0])


# --------------------------------------------------------------------------
# CORRECTION-06 : G_PAND accepte le 0-based et ne redevient pas silencieusement faux
# --------------------------------------------------------------------------
def test_g_pand_orders_0_based_normalise():
    """CORRECTION-06 : Orders=[0,1] (0-based) est normalise ; resultat = branche ordre."""
    out = G_PAND(
        [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],
        Orders=[0, 1],   # 0-based AVANT la correction -> branche hors-ordre -> [0,0]
        Times=[10, 20],
    )
    got = {tuple(cut) for cut in out[0]}
    assert got == {(1, 1), (1, 0), (0, 1)}


def test_g_pand_orders_1_based_convention():
    """Convention 1-based inchangee (exemples canoniques de la doc)."""
    out = G_PAND(
        [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],
        Orders=[1, 2],
        Times=[10, 20],
    )
    got = {tuple(cut) for cut in out[0]}
    assert got == {(1, 1), (1, 0), (0, 1)}


# --------------------------------------------------------------------------
# CORRECTION-07 : G_SPARE ne plante plus
# --------------------------------------------------------------------------
def test_g_spare_ne_plante_plus():
    """CORRECTION-07 : G_SPARE s'exécutait en IndexError (temps pris pour index)."""
    res = G_SPARE(
        [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],
        Orders=[0, 0],
        Times=[20, 10],
        IndicesPrincipal=[1, 0],
    )
    assert isinstance(res, list)
    assert len(res) >= 1


# --------------------------------------------------------------------------
# LIMITATION-09 (corrigée par CORRECTION-09) : le moteur porte-par-porte
# produit les coupes minimales EXACTES sur l'arbre canonique 12 composants
# --------------------------------------------------------------------------
def _build_12_comp_tree():
    """Arbre canonique du dépôt (bloc d'exemple HasseDiagramLib 1161-1175).

    Structure (GT = defaillance systeme) :
        g11 = ID(g10) ; g10 = OR(c0, g9) ; g9 = AND(g7, g8) ;
        g7 = OR(c1, c2, c3) ; g8 = OR(c4, c5, c6)
    Coupes minimales attendues : {c0} + 9 paires {c1..c3} x {c4..c6}.
    """
    tree = FaultTree(12)
    tree.NewRelation(3, [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
    tree.NewRelation(3, [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
    tree.NewRelation(4, [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    tree.NewRelation(3, [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    tree.NewRelation(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    return tree


def test_collect_cut_12_composant_coupes_correctes():
    """CORRECTION-09 : {c0} + 9 paires exactes au lieu des singletons +
    coupe pleine de l'ancien moteur (LIMITATION-09)."""
    from dft2hd2reliabilityr.LogicDoorLib import G_Gen
    from dft2hd2reliabilityr.HasseDiagramLib import Cut
    tree = _build_12_comp_tree()
    cut_engine = Cut(tree, [k for k in range(7)])
    cut_engine.CollectCut(G_Gen)
    got = {tuple(cut) for cut in cut_engine.Cut}
    expected = {(1, 0, 0, 0, 0, 0, 0)}  # {c0}
    for ci in (1, 2, 3):
        for cj in (4, 5, 6):
            vector = [0] * 7
            vector[ci] = 1
            vector[cj] = 1
            expected.add(tuple(vector))
    assert got == expected
    assert cut_engine.NCut == 10


def test_down_hasse_12_composants_poly_ferme():
    """CORRECTION-09 : forme fermée exacte R0*(R1R2R3 + R4R5R6 - R1R2R3R4R5R6),
    plus la valeur numérique exacte à R=0.9 pour tout k (0.8339031)."""
    import sympy
    tree = _build_12_comp_tree()
    R = [sympy.Symbol(f"R{k}") for k in range(7)]
    with _silence_logs():
        hasse = DownHasseDiagram(tree, [k for k in range(7)], R,
                                 [[1] for _ in range(7)], [One] * 7, [0], 1)
        poly = hasse.GetPolyFiab()
    expected = R[0] * (R[1] * R[2] * R[3] + R[4] * R[5] * R[6]
                       - R[1] * R[2] * R[3] * R[4] * R[5] * R[6])
    assert sympy.simplify(poly[0] - expected) == 0

    R09 = [[0.9] for _ in range(7)]
    with _silence_logs():
        hasse9 = DownHasseDiagram(tree, [k for k in range(7)], [k for k in range(7)],
                                  R09, [One] * 7, [0], 1)
        poly9 = hasse9.GetPolyFiab()
    assert abs(poly9[1][0] - 0.9 * (2 * 0.9 ** 3 - 0.9 ** 6)) < 1e-9


def test_getpolyfiab_unifie_down_up_reliability_result():
    """CORRECTION-10 : GetPolyFiab renvoie une ReliabilityResult unifiée ;
    Down et Up fournissent la même fiabilité système (symbolique et numérique),
    et la compatibilité ascendante (indexation [0]/[1], to_list) est conservée."""
    import sympy
    tree = _build_12_comp_tree()
    R = [sympy.Symbol(f"R{k}") for k in range(7)]
    numeric_check = 0.9 * (2 * 0.9 ** 3 - 0.9 ** 6)
    with _silence_logs():
        down = DownHasseDiagram(tree, [k for k in range(7)], R,
                                [[0.9] for _ in range(7)], [One] * 7, [0], 1)
        up = UpHasseDiagram(tree, [k for k in range(7)], R,
                            [[0.9] for _ in range(7)], [One] * 7, [0], 1)
        res_down = down.GetPolyFiab()
        res_up = up.GetPolyFiab()
    # Attributs nommés du nouveau contrat
    assert "cut-lattice" in res_down.method and "link-lattice" in res_up.method
    assert res_down.n_min_items == 10
    assert res_down.poly_symbolic is not None and res_up.poly_symbolic is not None
    assert sympy.simplify(res_down.poly_symbolic - res_up.poly_symbolic) == 0
    # Numérique : même valeur par point de temps
    assert len(res_down.reliability_numeric) == len(res_up.reliability_numeric)
    assert abs(res_down.reliability_numeric[0] - res_up.reliability_numeric[0]) < 1e-9
    assert abs(res_down.reliability_numeric[0] - numeric_check) < 1e-9
    # Compatibilité ascendante
    assert res_down[0] is res_down.poly_symbolic
    assert res_down[1] is res_down.reliability_numeric
    assert res_down.to_list()[0] is res_down.poly_symbolic
    assert len(res_down) == 2


def test_up_hasse_12_composants_poly_ferme():
    """CORRECTION-02b+09 : UpHasse converge avec les memes liens minimaux ; le
    polynome remonte et coincide avec la forme fermée du test Down."""
    import sympy
    tree = _build_12_comp_tree()
    R = [sympy.Symbol(f"R{k}") for k in range(7)]
    t0 = _time.perf_counter()
    with _silence_logs():
        hasse = UpHasseDiagram(tree, [k for k in range(7)], R,
                               [[1] for _ in range(7)], [One] * 7, [0], 1)
        poly = hasse.GetPolyFiab()
    assert _time.perf_counter() - t0 < 10.0
    expected = R[0] * (R[1] * R[2] * R[3] + R[4] * R[5] * R[6]
                       - R[1] * R[2] * R[3] * R[4] * R[5] * R[6])
    assert sympy.simplify(poly[0] - expected) == 0


# --------------------------------------------------------------------------
# Comportement existant (non-regression) : gate s de base
# --------------------------------------------------------------------------
def test_gportes_de_base():
    assert G_OR([[[1, 1, 0]], [[1, 0, 0], [0, 1, 0]]]) == [[[1, 0, 0], [0, 1, 0]]]
    assert G_AND([[[1, 0], [0, 1]], [[0, 1], [1, 1]]]) == [[[1, 1], [0, 1]]]
    assert G_NOT([[[1, 0]]]) == [[[-1, 0]]]
    assert G_FDEP([[[1, 0]], [[0, 1]]]) == [[[-1, 0], [0, 1]]]


def test_faultree_r_reliabilite_recursive(capsys):
    """FaultTreeR.RecursiveReliability : aboutit sans patch ; format {symbole, valeur}."""
    with _silence_logs():
        tree_r = FaultTreeR(3, [[1], [1]], [One, One], [0], 1)
        tree_r.NewRelation(3, [1, 1, 0], [0, 0, 1])
        out = tree_r.RecursiveReliability()
    assert capsys.readouterr().out == ""
    # out = [temps, [{0: [expr_symbolique], 1: [[valeur]]}]]
    assert out[0] == [0]
    assert len(out[1]) == 1
    entry = out[1][0]
    assert 0 in entry and 1 in entry
