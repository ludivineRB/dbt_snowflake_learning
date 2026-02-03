## Objectifs du module

- Comprendre Embedded vs Referenced
- Connaitre les patterns de modelisation
- Appliquer les regles d'or de la modelisation
- Choisir la bonne strategie selon le cas d'usage

## Embedded vs Referenced : Deux approches

MongoDB offre deux principales strategies pour modeliser les relations entre documents :

### 1. Embedded Documents (Documents imbriques)

Les donnees liees sont stockees dans le meme document :

```bash
{
  "_id": ObjectId("..."),
  "name": "Alice Dupont",
  "email": "alice@example.com",
  "address": {
    "street": "123 Rue de la Paix",
    "city": "Paris",
    "zipcode": "75001",
    "country": "France"
  },
  "orders": [
    {
      "order_id": "ORD001",
      "date": ISODate("2024-01-15"),
      "total": 150.50,
      "items": [
        { "product": "Laptop", "price": 150.50, "quantity": 1 }
      ]
    },
    {
      "order_id": "ORD002",
      "date": ISODate("2024-01-20"),
      "total": 45.00,
      "items": [
        { "product": "Mouse", "price": 25.00, "quantity": 1 },
        { "product": "Keyboard", "price": 20.00, "quantity": 1 }
      ]
    }
  ]
}
```

#### Avantages

- Une seule requete pour tout
- Meilleures performances en lecture
- Transactions atomiques automatiques
- Pas de joins necessaires

#### Inconvenients

- Limite de 16 MB par document
- Duplication de donnees possible
- Difficile de requeter uniquement les sous-documents

### 2. Referenced Documents (Documents references)

Les donnees sont stockees dans des collections separees avec des references :

```bash
// Collection users
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "Alice Dupont",
  "email": "alice@example.com"
}

// Collection orders
{
  "_id": ObjectId("507f191e810c19729de860ea"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),  // Reference
  "order_number": "ORD001",
  "date": ISODate("2024-01-15"),
  "total": 150.50
}

// Collection order_items
{
  "_id": ObjectId("..."),
  "order_id": ObjectId("507f191e810c19729de860ea"),  // Reference
  "product": "Laptop",
  "price": 150.50,
  "quantity": 1
}
```

**Recuperer avec $lookup :**

```bash
db.users.aggregate([
  {
    $lookup: {
      from: "orders",
      localField: "_id",
      foreignField: "user_id",
      as: "orders"
    }
  }
])
```

#### Avantages

- Pas de limite de taille
- Reutilisation des donnees (pas de duplication)
- Flexibilite pour requeter chaque collection
- Mise a jour plus facile (un seul endroit)

#### Inconvenients

- Plusieurs requetes ou utilisation de $lookup
- Performances legerement inferieures
- Joins necessaires

### Quand utiliser chaque approche ?

| Critere | Embedded | Referenced |
| --- | --- | --- |
| **Relation** | One-to-few (1 a quelques) | One-to-many (1 a beaucoup), Many-to-many |
| **Frequence d'acces** | Toujours ensemble | Acces separe possible |
| **Taille des donnees** | Petite a moyenne | Grande (> 16 MB) |
| **Frequence de mise a jour** | Rarement mis a jour | Souvent mis a jour |
| **Duplication acceptable ?** | Oui | Non |

## Patterns de modelisation courants

### Pattern 1 : One-to-Few (Embedded)

Exemple : Un utilisateur avec quelques adresses

```bash
{
  "name": "Alice",
  "addresses": [
    { "type": "home", "city": "Paris" },
    { "type": "work", "city": "Lyon" }
  ]
}
```

### Pattern 2 : One-to-Many (Referenced)

Exemple : Un auteur avec beaucoup de livres

```bash
// Collection authors
{ "_id": ObjectId("..."), "name": "Victor Hugo" }

// Collection books
{ "title": "Les Miserables", "author_id": ObjectId("...") }
{ "title": "Notre-Dame de Paris", "author_id": ObjectId("...") }
```

### Pattern 3 : Many-to-Many (Array of References)

Exemple : Etudiants et cours

```bash
// Collection students
{
  "name": "Alice",
  "course_ids": [ObjectId("course1"), ObjectId("course2")]
}

// Collection courses
{
  "name": "Data Engineering",
  "student_ids": [ObjectId("student1"), ObjectId("student2")]
}
```

### Pattern 4 : Bucket Pattern (pour time-series)

Regrouper les donnees temporelles par buckets :

```bash
{
  "sensor_id": "temp_sensor_01",
  "date": ISODate("2024-01-15"),
  "hour": 10,
  "measurements": [
    { "minute": 0, "temperature": 22.5 },
    { "minute": 1, "temperature": 22.6 },
    { "minute": 2, "temperature": 22.4 },
    // ... 60 mesures dans un document
  ],
  "count": 60,
  "avg_temperature": 22.5
}
```

**Avantages :** Reduit le nombre de documents, ameliore les performances

### Regles d'or pour la modelisation MongoDB

- Modelisez vos donnees en fonction de vos patterns d'acces
- Embed quand vous lisez ensemble, reference quand independant
- Privilegiez la denormalisation si cela ameliore les performances
- Utilisez embedded pour one-to-few, referenced pour one-to-many
- Attention a la limite de 16 MB par document
- Testez et mesurez avec vos vraies donnees

[Module 5: Index](05-index-performance.md)
[Module 7: Data Engineering](07-data-engineering.md)