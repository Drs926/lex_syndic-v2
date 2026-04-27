LEX\_SYNDIC\_V2

Software Architecture v2



Version : 1.0

Status : architecture baseline

Scope : analyse juridique des accords d’entreprise (droit du travail français)



1\. Objectif de l’architecture



Cette architecture définit la structure logicielle du système LEX\_SYNDIC\_V2.



Le système doit permettre :



l’analyse structurée d’accords d’entreprise



la comparaison juridique de textes



l’identification d’impacts sur les droits des salariés



la génération de dossiers juridiques exploitables par les représentants du personnel



Le système assiste l’analyse juridique, il ne remplace pas le raisonnement humain.



2\. Principes architecturaux



Les principes suivants sont non négociables.



2.1 Pipeline déterministe



Le système repose sur une chaîne d’analyse structurée.



document

→ ingestion

→ structuration

→ analyse des clauses

→ comparaison juridique

→ règles calculables

→ synthèse

→ dossier juridique



Le LLM n’intervient qu’en fin de pipeline.



2.2 Séparation stricte des responsabilités



Chaque module a une responsabilité unique.



Un module ne doit jamais :



implémenter la logique d’un autre module



manipuler directement les données internes d’un autre module



introduire des dépendances implicites.



2.3 Traçabilité juridique



Toute conclusion doit être reliée à :



une clause



une norme juridique



une règle explicite.



Aucune conclusion ne doit être produite sans référence.



2.4 Modèle canonique unique



Les objets juridiques doivent avoir une seule représentation canonique.



Exemples :



LegalDocument



Clause



LegalReference



ComparisonResult



Il est interdit d’avoir plusieurs représentations concurrentes.



2.5 LLM comme composant secondaire



Le LLM est utilisé uniquement pour :



reformuler



structurer



synthétiser



Le LLM ne doit jamais :



déterminer la structure du document



inventer des règles juridiques



remplacer l’analyse déterministe.



3\. Architecture des modules



Le système est organisé en modules Python.



src/lex\_syndic/



Modules principaux :



core

ingestion

legal

analysis

comparison

rules

retrieval

storage

report

interface

4\. Description des modules

4.1 core



Responsabilité :



fondations techniques du système.



Contient :



configuration



exceptions



types communs



logging



utilitaires



Le module core ne contient aucune logique juridique.



4.2 ingestion



Responsabilité :



faire entrer les documents dans le système.



Fonctions :



lecture des fichiers



extraction du texte



normalisation documentaire



structuration initiale



Technologies possibles :



Docling



extracteurs PDF



extracteurs DOCX



Sortie :



LegalDocument

4.3 legal



Responsabilité :



représentation de la matière juridique.



Contient :



modèles juridiques



hiérarchie des normes



taxonomie des clauses



références juridiques



Exemples d’objets :



LegalDocument

Clause

LegalReference

Norm

4.4 analysis



Responsabilité :



analyse interne d’un document.



Fonctions :



segmentation de clauses



classification des thèmes



extraction des références



enrichissement sémantique



Sortie :



AnalyzedClause

4.5 comparison



Responsabilité :



confronter des objets juridiques.



Fonctions :



comparaison clause ↔ clause



comparaison clause ↔ norme



détection des écarts



scoring de divergence



Sortie :



ComparisonResult

4.6 rules



Responsabilité :



règles calculables.



Fonctions :



application de règles juridiques



calcul de seuils



validation de conformité



Technologie possible :



OpenFisca.



Sortie :



RuleCheckResult

4.7 retrieval



Responsabilité :



recherche documentaire.



Fonctions :



indexation



recherche lexicale



recherche sémantique



récupération de textes juridiques



Technologie possible :



OpenSearch.



4.8 storage



Responsabilité :



persistance des données.



Fonctions :



stockage documents



stockage métadonnées



stockage résultats d’analyse



Technologies possibles :



PostgreSQL



OpenSearch



stockage objet.



4.9 report



Responsabilité :



génération des dossiers juridiques.



Fonctions :



génération de synthèses



génération d’arguments juridiques



structuration du dossier



Sorties :



Markdown



JSON



interface.



4.10 interface



Responsabilité :



point d’entrée utilisateur.



Fonctions :



upload documents



lancement analyses



visualisation résultats.



5\. Pipeline fonctionnel



Pipeline complet :



Document

→ ingestion

→ legal structuring

→ clause analysis

→ retrieval

→ comparison

→ rules

→ report

→ LLM synthesis



Chaque étape produit des objets structurés.



6\. Modèle de données principal



Entités principales :



LegalDocument

DocumentVersion

Clause

LegalReference

MetadataTag

AnalyzedClause

ComparisonResult

RuleCheckResult

CaseFile

GeneratedMemo

AuditEvent

7\. Dépendances entre modules



Dépendances autorisées :



core

↓

ingestion

↓

legal

↓

analysis

↓

comparison

↓

rules

↓

report



retrieval et storage peuvent être utilisés par plusieurs modules.



8\. Dépendances interdites



Les dépendances suivantes sont interdites :



report → analysis

analysis → report

core → legal

rules → ingestion



Ces dépendances créent des cycles dangereux.



9\. Gestion des évolutions



Toute évolution d’architecture doit :



être documentée



être justifiée



être validée avant implémentation.



10\. Objectif de la V2



La V2 vise à améliorer :



robustesse de l’analyse



précision des comparaisons



traçabilité juridique



qualité des dossiers générés.



Fin du document



software\_architecture\_v2.md

est le document de référence pour toute implémentation du système LEX\_SYNDIC\_V2.

