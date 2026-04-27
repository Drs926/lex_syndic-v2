# OUTPUT_CONTRACT

Contrat de sortie applicable à toute mission exécutée sur V2.

## Objectif

Garantir que chaque mission produit une sortie auditable, comparable et
réversible.

## Format de sortie obligatoire

Toute mission se termine par un bloc structuré exactement comme suit :

```
VERDICT:
RAISON UNIQUE:
FILES READ:
FILES CHANGED:
PROOFS:
RISKS:
NEXT ACTION:
```

## Définition des champs

| Champ | Contenu attendu |
|-------|-----------------|
| `VERDICT` | `OK`, `PARTIAL` ou `BLOCKED`. Un seul mot. |
| `RAISON UNIQUE` | Une phrase décrivant la cause racine du verdict. |
| `FILES READ` | Liste exhaustive des fichiers lus pendant la mission. |
| `FILES CHANGED` | Liste exhaustive des fichiers créés ou modifiés. |
| `PROOFS` | Commandes vérifiables (`git status --short`, diff résumé, sortie de tests). |
| `RISKS` | Risques résiduels après l'exécution. |
| `NEXT ACTION` | Action concrète à exécuter ensuite. |

## Règles transverses

1. Aucun champ ne doit être omis.
2. Aucun champ ne doit contenir de promesse non prouvée.
3. Toute capacité revendiquée doit être référencée dans `FILES CHANGED` ou
   `PROOFS`.
4. En cas d'écart par rapport à `MIGRATION_POLICY.md` ou `AGENTS.md`, le
   verdict est `BLOCKED`.

## Refus explicite

Si une mission demande une action interdite par `AGENTS.md`, la mission doit :

- ne pas exécuter l'action ;
- retourner `VERDICT: BLOCKED` ;
- indiquer la règle violée dans `RAISON UNIQUE`.
