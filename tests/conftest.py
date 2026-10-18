"""
Configuration pytest : expose le package `src/dft2hd2reliabilityr` au sys.path.

CORRECTION-11 : le package est désormais la seule source de vérité (layout src/,
doublons racine et `source/` supprimés). Les tests importent via
`dft2hd2reliabilityr.*` ; cette insertion permet de les lancer depuis un checkout
sans installation. Variante "comme PyPI" : `pip install -e .[test]` puis pytest.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
for path in (SRC, ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)
