## Objectifs du module

- Comprendre l'importance des index
- Creer differents types d'index
- Analyser les performances avec explain()
- Appliquer les bonnes pratiques d'indexation

## Pourquoi les index ?

Les **index** ameliorent drastiquement les performances des requetes en permettant a MongoDB
de localiser rapidement les documents sans scanner toute la collection. Sans index, MongoDB doit effectuer
un *collection scan* (lire tous les documents).

#### Sans index

Collection scan : O(n)

Temps : lent sur grandes collections

#### Avec index

Index scan : O(log n)

Temps : tres rapide

### Types d'index

#### 1. Single Field Index (Index simple)

```bash
// Creer un index sur le champ email
db.users.createIndex({ email: 1 })  // 1 = croissant, -1 = decroissant

// Index unique (empeche les doublons)
db.users.createIndex({ email: 1 }, { unique: true })

// Voir les index
db.users.getIndexes()

// Supprimer un index
db.users.dropIndex("email_1")
```

#### 2. Compound Index (Index compose)

```bash
// Index sur plusieurs champs
db.users.createIndex({ department: 1, age: -1 })

// Utile pour les requetes :
db.users.find({ department: "Data", age: { $gt: 25 } })
db.users.find({ department: "Data" }).sort({ age: -1 })
```

#### 3. Text Index (Index de texte)

```bash
// Creer un index de texte
db.articles.createIndex({ title: "text", content: "text" })

// Recherche plein texte
db.articles.find({ $text: { $search: "mongodb data engineering" } })

// Recherche avec score de pertinence
db.articles.find(
  { $text: { $search: "mongodb" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })
```

#### 4. Geospatial Index (Index geospatial)

```bash
// Index 2dsphere pour coordonnees GPS
db.places.createIndex({ location: "2dsphere" })

// Document avec localisation
{
  name: "Paris Office",
  location: {
    type: "Point",
    coordinates: [2.3522, 48.8566]  // [longitude, latitude]
  }
}

// Recherche a proximite
db.places.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [2.35, 48.85]
      },
      $maxDistance: 5000  // 5 km
    }
  }
})
```

### Analyser les performances : explain()

```bash
// Analyser une requete
db.users.find({ email: "alice@example.com" }).explain("executionStats")

// Resultat (sans index)
{
  "executionStats": {
    "executionTimeMillis": 45,
    "totalDocsExamined": 10000,    // Tous les documents scannés
    "nReturned": 1
  }
}

// Creer un index
db.users.createIndex({ email: 1 })

// Analyser a nouveau
{
  "executionStats": {
    "executionTimeMillis": 2,       // Beaucoup plus rapide
    "totalDocsExamined": 1,         // Un seul document scanne
    "nReturned": 1
  }
}
```

#### Modes d'explain()

- `"queryPlanner"` : Plan d'execution (par defaut)
- `"executionStats"` : Statistiques d'execution detaillees
- `"allPlansExecution"` : Tous les plans possibles

### Bonnes pratiques d'indexation

#### A faire

- Indexer les champs frequemment requetes
- Utiliser explain() pour valider
- Index composes pour queries multiples
- Index unique sur emails, usernames

#### A eviter

- Trop d'index (ralentit les ecritures)
- Indexer des champs peu utilises
- Oublier de monitorer les performances
- Index sur champs avec peu de variete

### Avec Python (PyMongo)

```bash
from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# Creer un index simple
collection.create_index([("email", ASCENDING)], unique=True)

# Index compose
collection.create_index([
    ("department", ASCENDING),
    ("age", DESCENDING)
])

# Lister les index
indexes = collection.list_indexes()
for index in indexes:
    print(index)

# Analyser une requete
explain_result = collection.find({"email": "alice@example.com"}).explain()
print(f"Temps d'execution: {explain_result['executionStats']['executionTimeMillis']}ms")
print(f"Documents examines: {explain_result['executionStats']['totalDocsExamined']}")
```

#### Index par defaut

MongoDB cree automatiquement un index unique sur le champ `_id` de chaque collection.
Vous n'avez pas besoin de creer cet index manuellement.

### Points cles a retenir

- Les index accelerent drastiquement les requetes (O(n) → O(log n))
- Types : simples, composes, texte, geospatiaux
- explain() permet d'analyser les performances des requetes
- Index unique pour garantir l'unicite (emails, usernames)
- Trop d'index ralentit les ecritures : trouver le bon equilibre

[Module 4: Agregation](04-aggregation.md)
[Module 6: Modelisation](06-modelisation.md)