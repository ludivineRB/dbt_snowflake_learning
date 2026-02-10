[🏠 Accueil](README.md)

# 🔐 RGPD & Gouvernance des Donnees

## Formation Data Engineer / Dev IA

---

## 🎯 Objectifs Pedagogiques

A l'issue de ce module, vous serez capable de :

1. **Comprendre le cadre legal** du RGPD et ses implications pour les metiers de la data et de l'IA
2. **Identifier les donnees personnelles** dans vos pipelines de donnees et modeles d'apprentissage
3. **Appliquer les 6 principes fondamentaux** du RGPD dans vos developpements quotidiens
4. **Implementer les droits des personnes** (acces, effacement, portabilite) dans vos systemes
5. **Rediger et maintenir un registre des traitements** conforme a l'article 30
6. **Maitriser les techniques d'anonymisation et de pseudonymisation** adaptees au Data Engineering
7. **Conduire une analyse d'impact** (DPIA/AIPD) pour vos projets data et IA
8. **Mettre en place une gouvernance des donnees** securisee (RBAC, chiffrement, audit, lineage)
9. **Integrer la conformite RGPD** dans vos workflows CI/CD et pipelines de donnees

---

## 📚 Programme

### Module 1 - Fondamentaux du RGPD

| # | Cours | Description | Duree estimee |
|---|-------|-------------|---------------|
| 1 | [Introduction et Enjeux](01-introduction-enjeux.md) | Pourquoi le RGPD concerne les Data Engineers et Dev IA, historique, sanctions, acteurs | 1h30 |
| 2 | [Principes Fondamentaux](02-principes-fondamentaux.md) | Les 6 principes, les 6 bases legales, donnees sensibles, Privacy by Design | 2h |
| 3 | [Droits des Personnes](03-droits-des-personnes.md) | Les 8 droits, DSAR, impact sur les BDD et pipelines ML | 2h |

### Module 2 - Mise en Conformite

| # | Cours | Description | Duree estimee |
|---|-------|-------------|---------------|
| 4 | [Registre des Traitements](04-registre-des-traitements.md) | Article 30, template, exemples concrets ETL et ML | 1h30 |
| 5 | [Anonymisation & Pseudonymisation](05-anonymisation-pseudonymisation.md) | Techniques, implementation Python/pandas, arbre de decision | 2h30 |
| 6 | [Analyse d'Impact (DPIA)](06-analyse-impact.md) | Methodologie, matrice de risques, exemple complet | 2h |

### Module 3 - Securite & Gouvernance

| # | Cours | Description | Duree estimee |
|---|-------|-------------|---------------|
| 7 | [Securite & Gouvernance des Donnees](07-securite-gouvernance.md) | Chiffrement, RBAC, audit logs, data lifecycle, lineage, catalogue | 2h30 |

### Mise en Pratique

| # | Activite | Description | Duree estimee |
|---|----------|-------------|---------------|
| 8 | [Exercices](08-exercices.md) | Quiz, cas pratiques, scripts Python/SQL, mini-DPIA | 3h |

---

## 🗺️ Parcours Recommande

```
┌─────────────────────────────────────────────────────────────────┐
│                    RGPD & Gouvernance des Donnees               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📖 Module 1 - Fondamentaux                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │ 01-Intro │──│02-Princip│──│03-Droits │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
│       │                            │                            │
│  📖 Module 2 - Mise en Conformite  │                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │04-Registr│──│05-Anonymi│──│06-DPIA   │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
│       │                            │                            │
│  📖 Module 3 - Securite           │                            │
│  ┌──────────┐                ┌──────────┐                      │
│  │07-Securit│────────────────│08-Exercic│                      │
│  └──────────┘                └──────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💡 Prerequis

- Connaissances de base en **Python** et **SQL**
- Familiarite avec les concepts de **bases de donnees** relationnelles
- Notions de **pipelines de donnees** (ETL/ELT) appreciees
- Aucune connaissance juridique prealable requise

---

## 🔧 Outils Utilises

| Outil | Usage |
|-------|-------|
| Python 3.x + pandas | Anonymisation, automatisation DSAR |
| PostgreSQL / SQL | RBAC, soft delete, retention policies |
| Apache Airflow | Exemples de DAGs pour la purge automatique |
| Git | Versionnement du registre des traitements |

---

## 📖 Ressources Complementaires

- [Site officiel de la CNIL](https://www.cnil.fr/)
- [Texte officiel du RGPD](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32016R0679)
- [Guide du DPO - CNIL](https://www.cnil.fr/fr/le-guide-du-delegue-la-protection-des-donnees)
- [Outil PIA de la CNIL](https://www.cnil.fr/fr/outil-pia-telechargez-et-installez-le-logiciel-de-la-cnil)

---

**Academy** - Formation Data Engineer
