## Objectifs de cette partie

- Créer un compte GitHub professionnel
- Configurer votre profil de manière optimale
- Mettre en place l'authentification SSH
- Créer votre premier repository
- Cloner un repository et pousser du code

## Créer un compte GitHub

1. Rendez-vous sur [github.com](https://github.com)
2. Cliquez sur "Sign up"
3. Choisissez votre nom d'utilisateur (visible publiquement)
4. Vérifiez votre email
5. Choisissez un plan (Free est suffisant pour commencer)

#### Conseils pour votre nom d'utilisateur

- Choisissez un nom professionnel (il apparaîtra sur vos contributions)
- Évitez les caractères spéciaux
- Il peut servir de portfolio pour votre carrière

### Configurer votre profil

Un profil complet améliore votre crédibilité professionnelle :

##### Éléments essentiels

- **Photo de profil** : Photo professionnelle ou avatar
- **Nom complet** : Votre véritable nom
- **Bio** : Courte description (ex: "Data Engineer @ Company | Python, SQL,
  Airflow")
- **Localisation** : Ville, Pays
- **Site web / LinkedIn** : Liens professionnels
- **Entreprise** : Votre employeur actuel

### Authentification avec SSH

Pour éviter de saisir votre mot de passe à chaque push, configurez une clé SSH :

#### Générer une clé SSH

```bash
# Générer une nouvelle clé SSH
ssh-keygen -t ed25519 -C "votre.email@example.com"

# Appuyez sur Entrée pour accepter l'emplacement par défaut
# Entrez une passphrase (optionnel mais recommandé)

# Démarrer l'agent SSH
eval "$(ssh-agent -s)"

# Ajouter votre clé à l'agent
ssh-add ~/.ssh/id_ed25519

# Copier la clé publique
cat ~/.ssh/id_ed25519.pub
# ou sur macOS :
pbcopy < ~/.ssh/id_ed25519.pub
```

#### Ajouter la clé à GitHub

1. Sur GitHub, allez dans **Settings** → **SSH and GPG keys**
2. Cliquez sur **New SSH key**
3. Donnez un titre (ex: "MacBook Pro")
4. Collez votre clé publique
5. Cliquez sur **Add SSH key**

#### Tester la connexion

```bash
# Tester la connexion SSH
ssh -T git@github.com

# Résultat attendu :
# Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

#### C'est configuré !

Vous pouvez maintenant cloner des dépôts et push sans mot de passe avec les URLs SSH
(git@github.com:...).

### Créer votre premier repository

#### Via l'interface web

1. Cliquez sur le bouton **+** en haut à droite
2. Sélectionnez **New repository**
3. Configurez votre repository :
   - **Repository name** : `data-pipeline-demo`
   - **Description** : "Demo ETL pipeline for learning"
   - **Public/Private** : Choisissez selon vos besoins
   - ✅ Cochez "Add a README file"
   - Choisissez un **.gitignore** (Python)
   - Choisissez une **License** (MIT pour l'open source)
4. Cliquez sur **Create repository**

À ce stade, votre premier repository est créé sur GitHub !

#### Cloner le repository localement

```bash
# Cloner avec SSH (recommandé)
git clone git@github.com:votre-username/data-pipeline-demo.git

# Ou avec HTTPS
git clone https://github.com/votre-username/data-pipeline-demo.git

# Entrer dans le dossier
cd data-pipeline-demo

# Vérifier le remote
git remote -v
```

### Pousser un projet existant vers GitHub

Si vous avez déjà un projet Git local, voici comment le pousser sur GitHub :

```bash
# 1. Créer un repository vide sur GitHub (sans README, .gitignore, license)

# 2. Dans votre projet local existant
cd mon-projet-existant

# 3. Ajouter le remote GitHub
git remote add origin git@github.com:votre-username/mon-projet.git

# 4. Vérifier
git remote -v

# 5. Pousser votre code
git branch -M main
git push -u origin main
```

#### Attention aux secrets !

Avant de pousser, vérifiez que votre `.gitignore` exclut bien tous les fichiers
sensibles
(.env, credentials, API keys, etc.). Une fois pushé sur GitHub, même supprimé, le secret reste
dans l'historique !

### 💡 Points clés à retenir

- Configurez SSH pour éviter de saisir votre mot de passe à chaque push
- Un profil GitHub complet améliore votre crédibilité professionnelle
- Utilisez des noms de repository clairs et descriptifs
- Ajoutez toujours un README, .gitignore et une license
- Ne committez JAMAIS de secrets ou credentials

#### Prochaine étape

Votre environnement GitHub est prêt ! Passons à la **Partie 3** pour apprendre à
collaborer avec les Pull Requests.

[← Partie 1 : Introduction](partie1.md)
[Partie 3 : Pull Requests →](partie3.md)