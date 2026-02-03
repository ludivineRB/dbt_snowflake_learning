# Formation Data Warehouse

## Objectifs pédagogiques

A l'issue de cette formation, vous serez capable de :

- **Comprendre** les concepts fondamentaux du Data Warehouse
- **Distinguer** les systèmes OLTP des systèmes OLAP
- **Concevoir** une architecture de données décisionnelle
- **Modéliser** des données selon l'approche dimensionnelle (Kimball vs Inmon)
- **Choisir** la technologie adaptée à votre contexte (Snowflake, BigQuery, Redshift, Synapse)
- **Implémenter** l'architecture Medallion (Bronze/Silver/Gold)

## Prérequis

- Connaissances SQL de base (SELECT, JOIN, GROUP BY)
- Notions de modélisation de données
- Compréhension basique du Cloud

## Structure du cours

| Module | Titre | Durée |
|--------|-------|-------|
| 01 | [Introduction au Data Warehouse](./01-introduction.md) | 1h |
| 02 | [OLTP vs OLAP](./02-oltp-vs-olap.md) | 45min |
| 03 | [Architectures et Patterns](./03-architectures.md) | 1h30 |
| 04 | [Modélisation dimensionnelle](./04-modelisation.md) | 1h30 |
| 05 | [Technologies Cloud](./05-technologies-cloud.md) | 1h |
| 06 | [Architecture Medallion](./06-medallion.md) | 1h |

**Durée totale :** ~7 heures

## Parcours recommandé

```
Débutant            Intermédiaire           Avancé
    │                     │                    │
    ▼                     ▼                    ▼
 Module 01 ──────► Module 02 ──────► Module 03
    │                     │                    │
    ▼                     ▼                    ▼
 Module 04 ──────► Module 05 ──────► Module 06
```

## Ressources complémentaires

- [Brief pratique BigQuery Medallion](../../../99-Brief/BigQuery-Medallion/)
- [Cours Snowflake](../../04-Cloud-Platforms/snowflake/)
- [Cours Microsoft Fabric](../../06-Data-Engineering/Fabric/)
