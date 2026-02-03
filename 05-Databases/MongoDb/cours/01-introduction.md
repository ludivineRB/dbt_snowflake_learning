## Objectifs du module

- Comprendre ce qu'est MongoDB
- Connaitre les differences SQL vs NoSQL
- Maitriser les concepts cles (documents, collections, BSON)
- Identifier les cas d'usage de MongoDB

## Qu'est-ce que MongoDB ?

**MongoDB** est une base de donnees NoSQL orientee documents, open-source, qui stocke les donnees
au format JSON/BSON (Binary JSON). Creee en 2009, elle est devenue l'une des bases NoSQL les plus populaires
pour sa flexibilite et sa scalabilite.

#### Open Source

Code source ouvert et communaute active

#### Orientee Documents

Stockage en format JSON/BSON flexible

#### Scalable

Scalabilite horizontale native (sharding)

#### Haute Performance

Optimisee pour les lectures et ecritures rapides

### SQL vs NoSQL : Les differences

| Aspect | SQL (ex: PostgreSQL) | NoSQL (MongoDB) |
| --- | --- | --- |
| **Structure** | Tables avec schema rigide | Documents flexibles (JSON) |
| **Schema** | Defini a l'avance, fixe | Dynamique, flexible |
| **Relations** | Joins entre tables | Documents imbriques ou references |
| **Scalabilite** | Verticale (scale-up) | Horizontale (scale-out) |
| **Cas d'usage** | Transactions complexes, donnees structurees | Big Data, donnees semi-structurees, flexibilite |

#### Quand utiliser MongoDB ?

- Donnees semi-structurees ou non structurees
- Schema changeant frequemment
- Besoin de scalabilite horizontale
- Donnees hierarchiques ou imbriquees
- Prototypage rapide

### Concepts cles de MongoDB

| Concept SQL | Equivalent MongoDB | Description |
| --- | --- | --- |
| **Database** | Database | Conteneur de collections |
| **Table** | Collection | Groupe de documents |
| **Row** | Document | Enregistrement JSON/BSON |
| **Column** | Field | Paire cle-valeur |
| **Index** | Index | Optimisation des recherches |
| **Join** | $lookup | Agregation entre collections |

### Exemple de document MongoDB

```bash
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "Alice Dupont",
  "email": "alice.dupont@example.com",
  "age": 28,
  "skills": ["Python", "SQL", "MongoDB"],
  "address": {
    "city": "Paris",
    "country": "France",
    "zipcode": "75001"
  },
  "projects": [
    {
      "name": "Data Pipeline",
      "status": "completed",
      "technologies": ["Python", "Airflow", "MongoDB"]
    },
    {
      "name": "ML Model",
      "status": "in_progress",
      "technologies": ["Python", "TensorFlow"]
    }
  ],
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-20T14:45:00Z")
}
```

#### Avantages du format document

- Structure flexible et evolutive
- Donnees imbriquees sans joins
- Modele proche du code applicatif (objets)
- Pas besoin de migrations de schema complexes

### BSON : Le format interne de MongoDB

MongoDB stocke les documents au format **BSON** (Binary JSON), une extension binaire de JSON
qui supporte plus de types de donnees et est plus efficace pour le stockage et le parcours.

#### Types supplementaires

Date, ObjectId, Binary, Decimal128, etc.

#### Plus rapide

Encodage/decodage binaire optimise

#### Plus compact

Stockage binaire efficace

### Points cles a retenir

- MongoDB est une base NoSQL orientee documents (JSON/BSON)
- Schema flexible vs schema rigide en SQL
- Concepts: Database > Collection > Document > Field
- Ideal pour donnees semi-structurees et scalabilite horizontale
- Documents imbriques eliminent le besoin de nombreux joins

[Retour a l'accueil](index.md)
[Module 2: Installation](02-installation.md)