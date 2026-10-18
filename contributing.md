# Contribuer / Vérifier le projet (guide développeurs)

> Ce guide est volontairement **hors description PyPI** : il s'adresse aux
> contributeurs du dépôt. La page PyPI ne porte que la description publique
> (`README.rst`).

## Installation de développement

```bash
pip install -e ".[test]"     # pytest inclus
pip install -e ".[test,viz]" # + matplotlib/networkx pour ViewGraph
```

## Vérification (corrections, cf. CORRECTIONS.md)

```bash
python -m pytest -q                       # 14 tests unitaires (< 2 s)
python -m pytest --doctest-modules src -q # 17 doctests réels (< 1 s)
ruff check src tests                      # lint baseline (cf. pyproject.toml)
```

## Documentation de projet

| Fichier | Rôle |
|---|---|
| `ANALYSE.md` | analyse technique complète + feuille de route publication PyPI + plan IA de décision de maintenance (importance → sampling → ML) |
| `CORRECTIONS.md` | journal complet et tracé de TOUTES les modifications de code (identifiants CORRECTION-01..13 — CORRECTION-09 : coupes minimales exactes, CORRECTION-10 : sortie unifiée `ReliabilityResult`, CORRECTION-11 : packaging `src/` + PyPI-ready, CORRECTION-12 : CI/lint/doctests, CORRECTION-13 : hygiène de la description PyPI —, tests associés) |

## Publier une nouvelle version

1. Bumper la version DEUX FOIS :
   - `pyproject.toml` → `version = "x.y.z"` (PEP 440, strictement croissante ;
     une version déjà publiée sur PyPI ne peut jamais être ré-uploadée) ;
   - `src/dft2hd2reliabilityr/__init__.py` → `__version__ = "x.y.z"` (doit coller).
2. `python -m build` puis `twine check dist/*` (le README est rendu comme
   description PyPI : tout titre RST doit être souligné sur TOUTE sa longueur).
3. `twine upload dist/*` avec un **jeton à portée de projet**
   (`pypi.org/manage/account/token/` → « Add a token for this project ») ;
   ne jamais committer le jeton, le passer à twine en variable d'environnement.
4. Vérifier : nouveau venv → `pip install dft2hd2reliabilityr` → import + calcul.
