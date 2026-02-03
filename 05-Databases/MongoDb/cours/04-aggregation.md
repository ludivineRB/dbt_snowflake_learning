## Objectifs du module

- Comprendre le framework d'agregation
- Utiliser $match, $group, $project, $sort
- Maitriser $lookup (JOIN) et $unwind
- Creer des pipelines complexes

## Qu'est-ce que l'agregation ?

Le **framework d'agregation** de MongoDB est un pipeline de traitement de donnees puissant
qui permet de transformer et combiner des documents. C'est l'equivalent des GROUP BY, JOIN et sous-requetes SQL.

```bash
Documents     Pipeline Stage 1     Pipeline Stage 2     Pipeline Stage 3     Resultat
   ↓               ↓                    ↓                    ↓                  ↓
[{...}]  →    $match (filter)  →  $group (aggregate)  →  $sort (order)  →  [{result}]
[{...}]            ↓                    ↓                    ↓
[{...}]      Keep only matching    Group and calculate   Sort by field
                documents               statistics
```

### Stages d'agregation courants

| Stage | Description | Equivalent SQL |
| --- | --- | --- |
| `$match` | Filtrer les documents | WHERE |
| `$group` | Grouper et agreger | GROUP BY |
| `$sort` | Trier les resultats | ORDER BY |
| `$project` | Selectionner/transformer les champs | SELECT |
| `$limit` | Limiter le nombre de resultats | LIMIT |
| `$skip` | Sauter des documents | OFFSET |
| `$lookup` | Jointure avec une autre collection | JOIN |
| `$unwind` | Derouler un tableau | UNNEST |

## Exemples d'agregation

### Exemple 1 : Compter les utilisateurs par departement

```bash
db.users.aggregate([
  {
    $group: {
      _id: "$department",
      count: { $sum: 1 },
      avgAge: { $avg: "$age" }
    }
  },
  {
    $sort: { count: -1 }
  }
])

// Resultat
[
  { _id: "Data", count: 15, avgAge: 29.5 },
  { _id: "Backend", count: 12, avgAge: 27.8 },
  { _id: "Frontend", count: 10, avgAge: 26.3 }
]
```

**Equivalent SQL :**

```bash
SELECT
  department AS _id,
  COUNT(*) AS count,
  AVG(age) AS avgAge
FROM users
GROUP BY department
ORDER BY count DESC;
```

### Exemple 2 : Pipeline complexe avec filtres

```bash
db.users.aggregate([
  // Stage 1: Filtrer les utilisateurs > 25 ans
  {
    $match: {
      age: { $gt: 25 }
    }
  },
  // Stage 2: Projeter certains champs et creer des champs calcules
  {
    $project: {
      name: 1,
      age: 1,
      department: 1,
      yearsOfExperience: { $subtract: [{ $year: new Date() }, { $year: "$created_at" }] }
    }
  },
  // Stage 3: Grouper par departement
  {
    $group: {
      _id: "$department",
      avgAge: { $avg: "$age" },
      avgExperience: { $avg: "$yearsOfExperience" },
      employees: { $push: "$name" }
    }
  },
  // Stage 4: Trier par experience moyenne
  {
    $sort: { avgExperience: -1 }
  },
  // Stage 5: Limiter aux 3 premiers
  {
    $limit: 3
  }
])
```

### Exemple 3 : $lookup (JOIN)

```bash
// Collection users et collection orders
db.users.aggregate([
  {
    $lookup: {
      from: "orders",              // Collection a joindre
      localField: "_id",           // Champ dans users
      foreignField: "user_id",     // Champ dans orders
      as: "user_orders"            // Nom du tableau resultant
    }
  },
  {
    $project: {
      name: 1,
      email: 1,
      totalOrders: { $size: "$user_orders" },
      orders: "$user_orders"
    }
  }
])
```

### Exemple 4 : $unwind (Derouler un tableau)

```bash
// Utilisateur avec competences
{
  name: "Alice",
  skills: ["Python", "MongoDB", "Docker"]
}

// Derouler les competences
db.users.aggregate([
  { $unwind: "$skills" },
  {
    $group: {
      _id: "$skills",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])

// Resultat : competences les plus repandues
[
  { _id: "Python", count: 25 },
  { _id: "MongoDB", count: 18 },
  { _id: "Docker", count: 15 }
]
```

### Avec Python (PyMongo)

```bash
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# Pipeline d'agregation
pipeline = [
    {
        "$match": {
            "age": {"$gt": 25}
        }
    },
    {
        "$group": {
            "_id": "$department",
            "count": {"$sum": 1},
            "avgAge": {"$avg": "$age"},
            "employees": {"$push": "$name"}
        }
    },
    {
        "$sort": {"count": -1}
    }
]

# Executer l'agregation
results = collection.aggregate(pipeline)

for result in results:
    print(result)
```

### Operateurs d'agregation courants

- **$sum** : Somme des valeurs
- **$avg** : Moyenne des valeurs
- **$min** / **$max** : Minimum / Maximum
- **$first** / **$last** : Premier / Dernier element
- **$push** : Ajouter a un tableau
- **$addToSet** : Ajouter sans doublons
- **$count** : Compter les documents

[Module 3: CRUD](03-crud.md)
[Module 5: Index et Performance](05-index-performance.md)