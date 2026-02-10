# 📚 Modelisation des Donnees - Methode MERISE

## Formation Data Engineer / Dev IA

---

## 🎯 Objectifs Pedagogiques

A l'issue de ce module, vous serez capable de :

- ✅ Comprendre les 3 niveaux de modelisation (Conceptuel, Logique, Physique)
- ✅ Rediger un dictionnaire de donnees complet a partir de besoins metier
- ✅ Concevoir un Modele Conceptuel de Donnees (MCD) en notation MERISE
- ✅ Transformer un MCD en Modele Logique de Donnees (MLD) en appliquant les regles de passage
- ✅ Maitriser la normalisation (1NF, 2NF, 3NF, BCNF) et savoir quand denormaliser
- ✅ Generer un Modele Physique de Donnees (MPD) avec les scripts SQL DDL complets
- ✅ Utiliser les outils professionnels de modelisation (Looping, MySQL Workbench, dbdiagram.io)
- ✅ Appliquer ces competences dans un contexte Data Engineering (pipelines, monitoring, IoT)

---

## 📚 Programme

### 📖 Lecons

| # | Lecon | Description |
|---|-------|-------------|
| 01 | [Introduction a la Modelisation](01-introduction-modelisation.md) | Pourquoi modeliser ? Les 3 niveaux, histoire de MERISE, workflow complet |
| 02 | [Dictionnaire de Donnees](02-dictionnaire-donnees.md) | Recueil des besoins, identification entites/attributs/associations, regles de gestion |
| 03 | [Modele Conceptuel (MCD)](03-modele-conceptuel-mcd.md) | Entites, associations, cardinalites MERISE, heritage, diagrammes |
| 04 | [Modele Logique (MLD)](04-modele-logique-mld.md) | Regles de transformation MCD→MLD, normalisation 1NF a BCNF, denormalisation |
| 05 | [Modele Physique (MPD)](05-modele-physique-mpd.md) | SQL DDL, types de donnees, contraintes, index, partitionnement |
| 06 | [Outils Pratiques](06-outils-pratiques.md) | Looping, MySQL Workbench, dbdiagram.io, draw.io |

### 📝 Exercices

| # | Exercice | Niveau |
|---|----------|--------|
| N1 | [Lecture et Analyse de MCD](07-exercices.md#niveau-1---lecture-et-analyse) | Debutant |
| N2 | [Conception Bibliotheque](07-exercices.md#niveau-2---conception-complete) | Intermediaire |
| N3 | [Projet Data Pipeline Monitoring](07-exercices.md#niveau-3---projet-complet-data-engineering) | Avance |

---

## 🗺️ Parcours Recommande

```
Lecon 01 ──→ Lecon 02 ──→ Lecon 03 ──→ Lecon 04 ──→ Lecon 05 ──→ Lecon 06
  │              │              │              │              │           │
  │   Comprendre │  Dictionnaire│     MCD      │     MLD      │    MPD    │  Outils
  │   les bases  │  de donnees  │  Conceptuel  │   Logique    │  Physique │  pratiques
  │              │              │              │              │           │
  └──────────────┴──────────────┴──────────────┴──────────────┴───────────┘
                                       │
                                       ▼
                               Exercices (N1→N2→N3)
```

## 🛠️ Prerequis

- Connaissances de base en SQL (SELECT, INSERT, CREATE TABLE)
- Notions de bases de donnees relationnelles
- Un editeur de texte ou IDE

## ⏱️ Duree Estimee

- **Lecons** : 12 heures (2h par lecon)
- **Exercices** : 8 heures (N1: 1h, N2: 3h, N3: 4h)
- **Total** : ~20 heures

---

## 💡 Conseils

1. **Suivez l'ordre** : chaque lecon s'appuie sur la precedente
2. **Pratiquez** : la modelisation s'apprend en faisant, pas en lisant
3. **Dessinez** : prenez un papier et un crayon pour les MCD avant de passer a l'outil
4. **Pensez metier** : la modelisation commence toujours par comprendre le besoin, jamais par la technique

---

**Academy** - Formation Data Engineer
