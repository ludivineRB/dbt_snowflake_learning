# 07 - Concepts Avancés et Bonnes Pratiques

[← 06 - Docker Compose](06-docker-compose-orchestration.md) | [🏠 Accueil](README.md)

---

## Objectifs de cette partie

- Optimiser la taille et les performances des images
- Appliquer les règles de sécurité essentielles
- Maintenir et nettoyer votre environnement Docker
- Découvrir les ressources pour aller plus loin

---

## 7.1 Optimisation des Images

### ❌ Mauvaise Pratique

```dockerfile
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt
# Taille : ~900 MB
```

### ✅ Bonne Pratique

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
# Taille : ~200 MB
```

### Techniques d'Optimisation

- **Utilisez des images de base slim ou alpine** : Réduisez la taille de base
- **Multi-stage builds** : Séparez la compilation de l'exécution
- **Ordonnez vos instructions** : Placez ce qui change rarement en premier
- **Combinez les commandes RUN** : Minimisez le nombre de couches
- **Nettoyez dans le même RUN** : `rm -rf /var/lib/apt/lists/*`
- **Utilisez .dockerignore** : Ne copiez que ce qui est nécessaire

---

## 7.2 Sécurité

### 🔒 Règles de Sécurité Essentielles

1. **N'exécutez jamais en root** - Créez un utilisateur non-root
2. **Ne stockez jamais de secrets** - Utilisez des variables d'environnement
3. **Scannez les vulnérabilités** - Utilisez Trivy : `trivy image mon-app:v1`
4. **Limitez les ressources** - Utilisez `--memory` et `--cpus`
5. **Mettez à jour régulièrement** - Reconstruisez vos images fréquemment

### 🔒 Exemple : Dockerfile Sécurisé

```dockerfile
FROM python:3.11-slim

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Installer les dépendances en root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY --chown=appuser:appuser src/ ./src/

# Changer vers l'utilisateur non-root
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import sys; sys.exit(0)"

CMD ["python", "src/main.py"]
```

### Scanner les Vulnérabilités

```bash
# Scanner une image (exemple avec Trivy)
trivy image python:3.11-slim

# Afficher seulement les vulnérabilités critiques
trivy image --severity HIGH,CRITICAL mon-app:latest
```

---

## 7.3 Nettoyage et Maintenance

```bash
# Nettoyer tous les éléments non utilisés
docker system prune -a

# Voir l'espace disque utilisé
docker system df

# Supprimer les images non taguées (dangling)
docker image prune

# Supprimer les conteneurs arrêtés
docker container prune

# Supprimer les volumes non utilisés
docker volume prune

# Tout nettoyer d'un coup (avec confirmation)
docker system prune -a --volumes
```

---

## 7.4 Limiter les Ressources

```bash
# Limiter la mémoire
docker run -m 512m mon-app

# Limiter le CPU
docker run --cpus=".5" mon-app

# Avec Docker Compose
services:
  app:
    image: mon-app
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 1G
```

---

## 🎯 Points Clés à Retenir

1. **Docker résout "ça marche sur ma machine"** en garantissant la reproductibilité
2. **Images = Templates, Conteneurs = Instances**
3. **Les conteneurs sont légers** vs les VMs qui sont lourdes
4. **Dockerfile** décrit comment construire une image
5. **Volumes** persistent les données au-delà du conteneur
6. **Réseaux** permettent la communication inter-conteneurs
7. **Docker Compose** orchestre des applications multi-conteneurs
8. **Sécurité** : jamais en root, pas de secrets dans les images
9. **Optimisation** : images slim, cache, multi-stage builds
10. **Data Engineering** : essentiel pour les pipelines modernes

---

## 📚 Ressources et Prochaines Étapes

### Documentation Officielle
- [Documentation Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

---

[← 06 - Docker Compose](06-docker-compose-orchestration.md) | [🏠 Accueil](README.md)