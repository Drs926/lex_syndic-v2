# MIGRATION_POLICY

Règles applicables à toute migration de code, de données ou de configuration
depuis V1 (`C:\Users\Harib\CascadeProjects\lex-syndic`) vers V2.

## Principe fondateur

V2 est canonique. V1 est une **source de migration contrôlée**, pas une base
de copie. Référence : `DECISIONS.md` DEC-001.

## Interdictions

1. **Copie massive interdite.** Aucune copie de répertoire entier de V1 vers
   V2. Aucune importation en bloc de modules V1.
2. **Pas d'import implicite.** Pas de `git merge`, `git cherry-pick` ou de
   patch global depuis V1.
3. **Pas de dépendance V1.** V2 ne dépend d'aucun chemin, package ou artefact
   V1 à l'exécution.
4. **Pas de code non couvert.** Aucun code migré ne peut entrer dans `src/`
   sans test correspondant dans `tests/`.

## Procédure de migration par lots

Chaque migration est exécutée comme un lot `MIG-XXX` listé dans `PLAN.md`.

Étapes obligatoires d'un lot :

1. **Cadrage** : périmètre limité à un seul module canonique de
   `software_architecture_v2.md` §3.
2. **Sélection** : identifier précisément les fichiers V1 servant de source.
3. **Réécriture ou adaptation** : le code est repris en respectant les modèles
   canoniques de V2 (`software_architecture_v2.md` §6). La copie aveugle est
   interdite.
4. **Tests** : ajout de tests dans `tests/` avant fusion. Le lot ne peut être
   fusionné si les tests sont absents ou échouent.
5. **Décision** : entrée correspondante dans `DECISIONS.md`.
6. **Sortie** : production du bloc défini par `OUTPUT_CONTRACT.md`.

## Critères de rejet d'un lot

Un lot est rejeté si l'une des conditions suivantes est vraie :

- Il introduit une dépendance hors `software_architecture_v2.md`.
- Il franchit une dépendance interdite (`software_architecture_v2.md` §8).
- Il modifie plus d'un module canonique.
- Il livre du code sans tests.
- Il ne fournit pas le bloc de sortie contractuel.

## Cas limites

- **Configuration** : la configuration ne se migre que si elle est utilisée
  par du code déjà migré.
- **Données de test** : les jeux de données de V1 peuvent être réutilisés à
  condition qu'ils soient explicitement référencés dans le lot.
- **Documentation** : les documents V1 peuvent être cités, jamais copiés
  sans relecture et adaptation.

## Suivi

Chaque lot validé met à jour `STATUS.md` pour refléter l'état réel.
Chaque mission de migration s'inscrit dans `PROMPTS_INDEX.md`.
