[← Precedent](01-introduction-modelisation.md) | [🏠 Accueil](README.md) | [Suivant →](03-modele-conceptuel-mcd.md)

---

# 02 - Le Dictionnaire de Donnees

## 🎯 Objectifs de cette lecon

- Savoir mener des interviews de recueil de besoins
- Identifier les entites, attributs et associations a partir de regles metier
- Rediger des regles de gestion claires et non ambigues
- Construire un dictionnaire de donnees complet et structure
- Appliquer ces techniques sur deux cas concrets : e-commerce et IoT

---

## 1. Le recueil des besoins metier

### 1.1 Pourquoi cette etape est cruciale

Le dictionnaire de donnees est le **pont entre le monde metier et le monde technique**. C'est le document qui traduit les besoins exprimes par les utilisateurs en specifications exploitables pour la modelisation.

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  Monde Metier   │         │  Dictionnaire   │         │  Monde Technique│
│                 │         │  de Donnees     │         │                 │
│ "Le client      │ ──────→ │ Entite: Client  │ ──────→ │ CREATE TABLE    │
│  passe une      │         │ Attr: nom, email│         │ client (...)    │
│  commande"      │         │ RG: email unique│         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

❌ **Sans dictionnaire** : le developpeur interprete les besoins a sa facon → malentendus, refontes

✅ **Avec dictionnaire** : les besoins sont formalises, valides par le metier, et exploitables par la technique

### 1.2 Les techniques d'interview

#### Questions ouvertes pour comprendre le domaine

| Type de question | Exemples |
|-----------------|----------|
| **Exploration** | "Pouvez-vous me decrire votre activite au quotidien ?" |
| **Processus** | "Que se passe-t-il quand un client passe une commande ?" |
| **Donnees** | "Quelles informations enregistrez-vous sur un client ?" |
| **Contraintes** | "Un client peut-il passer une commande sans etre inscrit ?" |
| **Volumes** | "Combien de commandes traitez-vous par jour ?" |
| **Exceptions** | "Que se passe-t-il quand une commande est annulee ?" |
| **Historique** | "Gardez-vous l'historique des prix des produits ?" |

#### Questions specifiques pour le Data Engineer

| Question | Pourquoi |
|----------|----------|
| "A quelle frequence ces donnees changent-elles ?" | Dimensionner les pipelines ETL |
| "Quelle est la retention souhaitee ?" | Prevoir le partitionnement et l'archivage |
| "Qui consomme ces donnees ?" | Adapter le modele (OLTP vs OLAP) |
| "Quelle latence est acceptable ?" | Batch vs streaming |
| "Y a-t-il des sources de donnees externes ?" | Prevoir les tables de staging |

### 1.3 Les pieges a eviter lors des interviews

❌ **Ne pas poser de questions fermees uniquement** : "Est-ce que le client a un email ?" → "Oui" (vous passez a cote du fait qu'il peut en avoir plusieurs)

❌ **Ne pas utiliser du jargon technique** : "Est-ce une relation many-to-many ?" → Incomprehensible pour le metier

❌ **Ne pas oublier les cas limites** : "Et si le produit n'a plus de stock ? Et si le client a deux adresses ?"

✅ **Reformuler** : "Si je comprends bien, un client peut avoir plusieurs adresses de livraison, c'est bien ca ?"

✅ **Prendre des notes structurees** : entites en majuscules, attributs soulignes, regles numerotees

---

## 2. Identifier les composants du modele

### 2.1 Les entites (les noms)

Une **entite** est un objet ou concept du monde reel que l'on souhaite gerer dans le systeme d'information.

**Technique** : dans les phrases du cahier des charges, les entites sont les **noms communs** qui representent des concepts importants.

> "Un **client** passe une **commande** qui contient des **produits** appartenant a des **categories**."

Les entites identifiees sont : **CLIENT**, **COMMANDE**, **PRODUIT**, **CATEGORIE**

💡 **Conseil** : ne confondez pas une entite avec un attribut. "adresse" n'est generalement pas une entite si elle n'a pas de vie propre. Mais si vous devez gerer plusieurs adresses par client avec un historique, elle devient une entite.

### 2.2 Les attributs (les proprietes)

Un **attribut** est une propriete qui decrit une entite.

> "Le **client** est identifie par un **numero unique**. On enregistre son **nom**, son **prenom**, son **email** et sa **date d'inscription**."

Les attributs de CLIENT sont : numero (identifiant), nom, prenom, email, date_inscription

**Caracteristiques d'un attribut :**

| Propriete | Description | Exemple |
|-----------|-------------|---------|
| **Nom** | Nom explicite en snake_case | `date_inscription` |
| **Type** | Type de donnee | VARCHAR, INT, DATE, DECIMAL |
| **Taille** | Longueur maximale | VARCHAR(100), DECIMAL(10,2) |
| **Obligatoire** | NULL autorise ou non | Oui / Non |
| **Identifiant** | Fait partie de la cle primaire ? | Oui / Non |
| **Description** | Explication metier | "Date a laquelle le client s'est inscrit" |

### 2.3 Les associations (les verbes)

Une **association** est un lien entre deux (ou plus) entites, exprime par un **verbe**.

> "Un **client** _passe_ une **commande**."
> "Une **commande** _contient_ des **produits**."
> "Un **produit** _appartient_ a une **categorie**."

Les associations sont : PASSE, CONTIENT, APPARTIENT

### 2.4 Les regles de gestion (RG)

Les **regles de gestion** sont les contraintes metier qui regissent les donnees. Elles determinent les **cardinalites** du MCD.

**Comment les ecrire** :

- Numerotees (RG1, RG2, RG3...)
- Une phrase claire et non ambigue
- Doivent etre validees par le metier

**Exemples** :

| # | Regle de gestion |
|---|-----------------|
| RG1 | Un client est identifie de maniere unique par un numero auto-incremente |
| RG2 | Un client est caracterise par un nom, un prenom, un email (unique) et une date d'inscription |
| RG3 | Un client peut passer zero ou plusieurs commandes |
| RG4 | Une commande est passee par un et un seul client |
| RG5 | Une commande est identifiee par un numero unique et possede une date, un statut et un montant total |
| RG6 | Une commande contient au moins un produit (avec une quantite et un prix unitaire) |
| RG7 | Un produit peut apparaitre dans zero ou plusieurs commandes |
| RG8 | Un produit appartient a une et une seule categorie |
| RG9 | Une categorie peut contenir zero ou plusieurs produits |

💡 **Astuce pour les cardinalites** : chaque regle de gestion impliquant deux entites donne deux cardinalites (une de chaque cote de l'association).

---

## 3. Le template du dictionnaire de donnees

### 3.1 Structure standard

Le dictionnaire de donnees est un tableau qui recense **toutes** les informations sur les donnees du systeme :

| Entite | Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|--------|----------|------|------|--------|-------------|-------------|-------------|
| *Nom de l'entite* | *Nom de l'attribut* | *Nom technique* | *Type SQL* | *Taille max* | *Oui/Non* | *Oui/Non* | *Description metier* |

### 3.2 Conventions de nommage

| Element | Convention | Exemple |
|---------|-----------|---------|
| Entite | MAJUSCULES | CLIENT, COMMANDE |
| Attribut | snake_case | date_inscription |
| Identifiant | Prefixe `id_` | id_client |
| Cle etrangere | Prefixe `id_` + nom entite | id_client (dans commande) |
| Booleen | Prefixe `est_` ou `a_` | est_actif, a_paye |
| Date | Prefixe `date_` | date_creation |

---

## 4. Exemple complet 1 : Plateforme E-commerce

### 4.1 Enonce du besoin

> Une entreprise de e-commerce souhaite informatiser la gestion de ses ventes en ligne. Les clients s'inscrivent avec leurs informations personnelles et peuvent passer des commandes. Chaque commande contient un ou plusieurs produits avec une quantite. Les produits sont organises en categories. On souhaite suivre le statut des commandes et l'historique des achats.

### 4.2 Regles de gestion

| # | Regle de gestion |
|---|-----------------|
| RG1 | Un client est identifie par un numero unique auto-incremente |
| RG2 | Un client possede un nom (obligatoire), un prenom (obligatoire), un email (obligatoire, unique), un telephone (facultatif) et une date d'inscription |
| RG3 | Un client peut passer 0 ou N commandes |
| RG4 | Une commande est passee par 1 et 1 seul client |
| RG5 | Une commande est identifiee par un numero unique et possede une date, un statut (en_attente, validee, expediee, livree, annulee) et un montant total |
| RG6 | Une commande contient 1 ou N produits, avec pour chaque produit une quantite commandee et un prix unitaire au moment de la commande |
| RG7 | Un produit peut apparaitre dans 0 ou N commandes |
| RG8 | Un produit est identifie par une reference unique et possede un nom, une description, un prix unitaire courant et un stock disponible |
| RG9 | Un produit appartient a 1 et 1 seule categorie |
| RG10 | Une categorie peut contenir 0 ou N produits |
| RG11 | Une categorie est identifiee par un code unique et possede un nom et une description |

### 4.3 Dictionnaire de donnees

#### Entite : CLIENT

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| Numero client | id_client | INT | - | Oui | ✅ Oui | Identifiant unique auto-incremente |
| Nom | nom | VARCHAR | 100 | Oui | Non | Nom de famille du client |
| Prenom | prenom | VARCHAR | 100 | Oui | Non | Prenom du client |
| Email | email | VARCHAR | 255 | Oui | Non | Adresse email (unique) |
| Telephone | telephone | VARCHAR | 20 | Non | Non | Numero de telephone |
| Date inscription | date_inscription | TIMESTAMP | - | Oui | Non | Date et heure de creation du compte |

#### Entite : COMMANDE

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| Numero commande | id_commande | INT | - | Oui | ✅ Oui | Identifiant unique auto-incremente |
| Date commande | date_commande | TIMESTAMP | - | Oui | Non | Date et heure de la commande |
| Statut | statut | VARCHAR | 20 | Oui | Non | Etat de la commande (en_attente, validee, expediee, livree, annulee) |
| Montant total | montant_total | DECIMAL | 10,2 | Oui | Non | Montant total TTC de la commande |

#### Entite : PRODUIT

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| Reference produit | id_produit | INT | - | Oui | ✅ Oui | Identifiant unique auto-incremente |
| Nom | nom_produit | VARCHAR | 200 | Oui | Non | Nom commercial du produit |
| Description | description | TEXT | - | Non | Non | Description detaillee du produit |
| Prix unitaire | prix_unitaire | DECIMAL | 10,2 | Oui | Non | Prix unitaire courant HT |
| Stock | stock_disponible | INT | - | Oui | Non | Quantite disponible en stock |

#### Entite : CATEGORIE

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| Code categorie | id_categorie | INT | - | Oui | ✅ Oui | Identifiant unique auto-incremente |
| Nom | nom_categorie | VARCHAR | 100 | Oui | Non | Nom de la categorie |
| Description | description_categorie | TEXT | - | Non | Non | Description de la categorie |

#### Association : CONTIENT (Commande - Produit)

| Attribut | Code | Type | Taille | Obligatoire | Description |
|----------|------|------|--------|-------------|-------------|
| Quantite | quantite | INT | - | Oui | Nombre d'unites commandees |
| Prix unitaire commande | prix_unitaire_commande | DECIMAL | 10,2 | Oui | Prix unitaire au moment de la commande |

---

## 5. Exemple complet 2 : Plateforme IoT (Capteurs)

### 5.1 Enonce du besoin

> Une entreprise industrielle deploie des capteurs IoT dans ses usines. Chaque capteur est installe dans une zone specifique et envoie des mesures periodiques (temperature, humidite, pression). Le systeme doit detecter les anomalies et generer des alertes quand les valeurs depassent des seuils configures.

### 5.2 Regles de gestion

| # | Regle de gestion |
|---|-----------------|
| RG1 | Un capteur est identifie par un numero de serie unique |
| RG2 | Un capteur possede un type (temperature, humidite, pression), un modele, une date d'installation et un statut (actif, inactif, maintenance) |
| RG3 | Un capteur est installe dans 1 et 1 seule zone |
| RG4 | Une zone peut contenir 0 ou N capteurs |
| RG5 | Une zone est identifiee par un code unique et possede un nom, un batiment et un etage |
| RG6 | Un capteur produit 0 ou N mesures |
| RG7 | Une mesure est associee a 1 et 1 seul capteur |
| RG8 | Une mesure possede une valeur numerique, une unite, un horodatage et un indicateur de validite |
| RG9 | Une alerte est declenchee par 1 et 1 seule mesure |
| RG10 | Une mesure peut declencher 0 ou 1 alerte |
| RG11 | Une alerte possede un niveau de severite (info, warning, critical), un message et un statut (ouverte, acquittee, resolue) |

### 5.3 Dictionnaire de donnees

#### Entite : CAPTEUR

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| Numero serie | numero_serie | VARCHAR | 50 | Oui | ✅ Oui | Numero de serie unique du capteur |
| Type capteur | type_capteur | VARCHAR | 30 | Oui | Non | Type de mesure (temperature, humidite, pression) |
| Modele | modele | VARCHAR | 100 | Oui | Non | Reference du modele constructeur |
| Date installation | date_installation | DATE | - | Oui | Non | Date de mise en service |
| Statut | statut_capteur | VARCHAR | 20 | Oui | Non | Etat du capteur (actif, inactif, maintenance) |

#### Entite : ZONE

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| Code zone | id_zone | INT | - | Oui | ✅ Oui | Identifiant unique de la zone |
| Nom | nom_zone | VARCHAR | 100 | Oui | Non | Nom de la zone |
| Batiment | batiment | VARCHAR | 50 | Oui | Non | Nom ou code du batiment |
| Etage | etage | INT | - | Non | Non | Numero d'etage |

#### Entite : MESURE

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| ID mesure | id_mesure | BIGINT | - | Oui | ✅ Oui | Identifiant unique (BIGINT car volume eleve) |
| Valeur | valeur_mesuree | DECIMAL | 10,4 | Oui | Non | Valeur numerique de la mesure |
| Unite | unite_mesure | VARCHAR | 10 | Oui | Non | Unite de mesure (°C, %HR, hPa) |
| Horodatage | date_mesure | TIMESTAMP | - | Oui | Non | Date et heure de la mesure |
| Validite | est_valide | BOOLEAN | - | Oui | Non | Indique si la mesure est fiable |

#### Entite : ALERTE

| Attribut | Code | Type | Taille | Obligatoire | Identifiant | Description |
|----------|------|------|--------|-------------|-------------|-------------|
| ID alerte | id_alerte | INT | - | Oui | ✅ Oui | Identifiant unique de l'alerte |
| Severite | severite | VARCHAR | 20 | Oui | Non | Niveau (info, warning, critical) |
| Message | message_alerte | TEXT | - | Oui | Non | Description de l'alerte |
| Statut | statut_alerte | VARCHAR | 20 | Oui | Non | Etat (ouverte, acquittee, resolue) |
| Date creation | date_creation_alerte | TIMESTAMP | - | Oui | Non | Date et heure de creation |

💡 **Note Data Engineering** : pour la table MESURE, on a choisi BIGINT comme identifiant car un systeme IoT peut generer des millions de mesures par jour. Prevoir le volume des la conception est essentiel.

---

## 6. Conseils pratiques pour les interviews

### 6.1 Preparation

- ✅ Lisez le cahier des charges AVANT l'interview
- ✅ Preparez une liste de questions ouvertes
- ✅ Identifiez les acteurs a interviewer (utilisateurs, managers, experts metier)
- ✅ Prevoyez 45 min a 1h par interview

### 6.2 Pendant l'interview

- ✅ Prenez des notes structurees (entites en MAJUSCULES)
- ✅ Reformulez pour valider votre comprehension
- ✅ Posez la question "Et si...?" pour les cas limites
- ✅ Dessinez des schemas au tableau
- ❌ Ne proposez PAS de solutions techniques pendant l'interview
- ❌ Ne corrigez PAS le vocabulaire du metier ("ce n'est pas une entite, c'est un attribut")

### 6.3 Apres l'interview

- ✅ Redigez le dictionnaire de donnees dans les 24h
- ✅ Envoyez-le pour validation au metier
- ✅ Numerotez les regles de gestion (RG1, RG2...)
- ✅ Identifiez les zones d'ombre et planifiez un complement d'interview si necessaire

### 6.4 Template de compte-rendu d'interview

```
INTERVIEW - [Date] - [Interlocuteur] - [Role]

CONTEXTE :
- [Description du domaine metier]

ENTITES IDENTIFIEES :
- [ENTITE1] : [description breve]
- [ENTITE2] : [description breve]

REGLES DE GESTION :
- RG1 : [regle]
- RG2 : [regle]

QUESTIONS EN SUSPENS :
- [Question non resolue 1]
- [Question non resolue 2]

PROCHAINE ETAPE :
- [Action a mener]
```

---

## 7. Resume

| Concept | A retenir |
|---------|-----------|
| Dictionnaire de donnees | Document pont entre le metier et la technique |
| Entite | Nom commun important dans les regles metier |
| Attribut | Propriete qui decrit une entite (nom, type, taille, obligatoire) |
| Association | Verbe qui relie deux entites |
| Regle de gestion (RG) | Contrainte metier, numerotee, claire, validee |
| Interview | Questions ouvertes, reformulation, cas limites |

---

## 📝 Auto-evaluation

1. A partir de l'enonce suivant, identifiez les entites, attributs et associations :
   > "Un etudiant s'inscrit a des cours. Chaque cours est enseigne par un professeur. Un professeur peut enseigner plusieurs cours."

2. Redigez les regles de gestion correspondantes (RG1 a RG6 minimum).

3. Construisez le dictionnaire de donnees pour l'entite ETUDIANT.

4. Quelle question poseriez-vous au metier pour clarifier si "adresse" doit etre une entite ou un attribut ?

---

[← Precedent](01-introduction-modelisation.md) | [🏠 Accueil](README.md) | [Suivant →](03-modele-conceptuel-mcd.md)

---

**Academy** - Formation Data Engineer
