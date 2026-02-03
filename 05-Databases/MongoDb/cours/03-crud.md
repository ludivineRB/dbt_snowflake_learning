## Objectifs du module

- Inserer des documents (insertOne, insertMany)
- Lire des documents (find, findOne)
- Mettre a jour des documents (updateOne, updateMany)
- Supprimer des documents (deleteOne, deleteMany)

## Create - Inserer des documents

### insertOne() - Inserer un document

```bash
// MongoDB Shell
db.users.insertOne({
  name: "Alice Dupont",
  email: "alice@example.com",
  age: 28,
  skills: ["Python", "MongoDB"],
  created_at: new Date()
})

// Resultat
{
  acknowledged: true,
  insertedId: ObjectId("507f1f77bcf86cd799439011")
}
```

### insertMany() - Inserer plusieurs documents

```bash
db.users.insertMany([
  {
    name: "Bob Martin",
    email: "bob@example.com",
    age: 32,
    skills: ["JavaScript", "React"],
    department: "Frontend"
  },
  {
    name: "Charlie Brown",
    email: "charlie@example.com",
    age: 25,
    skills: ["Python", "Django", "PostgreSQL"],
    department: "Backend"
  },
  {
    name: "Diana Prince",
    email: "diana@example.com",
    age: 30,
    skills: ["Data Science", "Python", "ML"],
    department: "Data"
  }
])

// Resultat
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("..."),
    '1': ObjectId("..."),
    '2': ObjectId("...")
  }
}
```

### Avec Python (PyMongo)

```bash
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# Insert one
user = {
    "name": "Alice Dupont",
    "email": "alice@example.com",
    "age": 28,
    "skills": ["Python", "MongoDB"],
    "created_at": datetime.utcnow()
}

result = collection.insert_one(user)
print(f"Inserted ID: {result.inserted_id}")

# Insert many
users = [
    {"name": "Bob", "age": 32, "department": "Frontend"},
    {"name": "Charlie", "age": 25, "department": "Backend"},
    {"name": "Diana", "age": 30, "department": "Data"}
]

result = collection.insert_many(users)
print(f"Inserted {len(result.inserted_ids)} documents")
```

## Read - Lire des documents

### find() - Trouver plusieurs documents

```bash
// Tous les documents
db.users.find()

// Avec filtre
db.users.find({ age: { $gt: 25 } })

// Projection (selectionner des champs)
db.users.find(
  { age: { $gt: 25 } },
  { name: 1, email: 1, _id: 0 }
)

// Limiter les resultats
db.users.find().limit(5)

// Trier les resultats
db.users.find().sort({ age: -1 })  // -1 = decroissant, 1 = croissant

// Skip (pagination)
db.users.find().skip(10).limit(5)

// Compter les documents
db.users.countDocuments({ age: { $gt: 25 } })
```

### findOne() - Trouver un document

```bash
// Premier document correspondant
db.users.findOne({ email: "alice@example.com" })

// Par ID
db.users.findOne({ _id: ObjectId("507f1f77bcf86cd799439011") })
```

### Operateurs de requete

| Operateur | Description | Exemple |
| --- | --- | --- |
| `$eq` | Egal a | `{ age: { $eq: 25 } }` |
| `$ne` | Different de | `{ age: { $ne: 25 } }` |
| `$gt` | Plus grand que | `{ age: { $gt: 25 } }` |
| `$gte` | Plus grand ou egal | `{ age: { $gte: 25 } }` |
| `$lt` | Plus petit que | `{ age: { $lt: 30 } }` |
| `$lte` | Plus petit ou egal | `{ age: { $lte: 30 } }` |
| `$in` | Dans un tableau | `{ age: { $in: [25, 30, 35] } }` |
| `$nin` | Pas dans un tableau | `{ age: { $nin: [25, 30] } }` |
| `$and` | ET logique | `{ $and: [{ age: {$gt: 25} }, { age: {$lt: 35} }] }` |
| `$or` | OU logique | `{ $or: [{ age: 25 }, { age: 30 }] }` |
| `$exists` | Champ existe | `{ email: { $exists: true } }` |
| `$regex` | Expression reguliere | `{ name: { $regex: /^A/ } }` |

### Avec Python (PyMongo)

```bash
# Find all
users = collection.find()
for user in users:
    print(user)

# Find with filter
users = collection.find({"age": {"$gt": 25}})

# Find one
user = collection.find_one({"email": "alice@example.com"})

# Projection
users = collection.find(
    {"age": {"$gt": 25}},
    {"name": 1, "email": 1, "_id": 0}
)

# Sort, limit, skip
users = collection.find().sort("age", -1).limit(5).skip(10)

# Count
count = collection.count_documents({"age": {"$gt": 25}})
print(f"Nombre d'utilisateurs > 25 ans: {count}")
```

## Update - Mettre a jour des documents

### updateOne() - Mettre a jour un document

```bash
// Modifier un champ
db.users.updateOne(
  { email: "alice@example.com" },
  { $set: { age: 29, updated_at: new Date() } }
)

// Ajouter un element a un tableau
db.users.updateOne(
  { email: "alice@example.com" },
  { $push: { skills: "Docker" } }
)

// Incrementer une valeur
db.users.updateOne(
  { email: "alice@example.com" },
  { $inc: { age: 1 } }
)

// Supprimer un champ
db.users.updateOne(
  { email: "alice@example.com" },
  { $unset: { temporary_field: "" } }
)
```

### updateMany() - Mettre a jour plusieurs documents

```bash
// Mettre a jour tous les utilisateurs > 25 ans
db.users.updateMany(
  { age: { $gt: 25 } },
  { $set: { status: "senior", updated_at: new Date() } }
)
```

### Operateurs de mise a jour

| Operateur | Description | Exemple |
| --- | --- | --- |
| `$set` | Definir la valeur d'un champ | `{ $set: { age: 30 } }` |
| `$unset` | Supprimer un champ | `{ $unset: { age: "" } }` |
| `$inc` | Incrementer une valeur | `{ $inc: { age: 1 } }` |
| `$mul` | Multiplier une valeur | `{ $mul: { price: 1.1 } }` |
| `$rename` | Renommer un champ | `{ $rename: { "name": "fullName" } }` |
| `$push` | Ajouter a un tableau | `{ $push: { skills: "Python" } }` |
| `$pull` | Retirer d'un tableau | `{ $pull: { skills: "Python" } }` |
| `$addToSet` | Ajouter si n'existe pas | `{ $addToSet: { skills: "Python" } }` |

### Avec Python (PyMongo)

```bash
# Update one
result = collection.update_one(
    {"email": "alice@example.com"},
    {"$set": {"age": 29, "updated_at": datetime.utcnow()}}
)
print(f"Modified {result.modified_count} document")

# Update many
result = collection.update_many(
    {"age": {"$gt": 25}},
    {"$set": {"status": "senior"}}
)
print(f"Modified {result.modified_count} documents")

# Upsert (update or insert)
result = collection.update_one(
    {"email": "new@example.com"},
    {"$set": {"name": "New User", "age": 25}},
    upsert=True
)
```

## Delete - Supprimer des documents

### deleteOne() et deleteMany()

```bash
// Supprimer un document
db.users.deleteOne({ email: "alice@example.com" })

// Supprimer plusieurs documents
db.users.deleteMany({ age: { $lt: 18 } })

// Supprimer tous les documents d'une collection
db.users.deleteMany({})

// Supprimer une collection entiere
db.users.drop()
```

### Avec Python (PyMongo)

```bash
# Delete one
result = collection.delete_one({"email": "alice@example.com"})
print(f"Deleted {result.deleted_count} document")

# Delete many
result = collection.delete_many({"age": {"$lt": 18}})
print(f"Deleted {result.deleted_count} documents")

# Drop collection
collection.drop()
```

#### Attention aux suppressions !

`deleteMany({})` et `drop()` suppriment definitivement les donnees.
Assurez-vous d'avoir des sauvegardes avant d'executer ces commandes en production.

### Points cles a retenir

- insertOne/insertMany pour creer des documents
- find/findOne avec operateurs de requete ($gt, $in, $regex, etc.)
- updateOne/updateMany avec operateurs ($set, $inc, $push, etc.)
- deleteOne/deleteMany pour supprimer des documents
- PyMongo offre une API Python similaire au shell MongoDB

[Module 2: Installation](02-installation.md)
[Module 4: Agregation](04-aggregation.md)