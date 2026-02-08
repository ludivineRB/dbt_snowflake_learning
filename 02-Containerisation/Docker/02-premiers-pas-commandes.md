# 02 - Premiers Pas avec Docker

[← 01 - Fondamentaux](01-fondamentaux-docker.md) | [🏠 Accueil](README.md) | [03 - Images et Conteneurs →](03-images-et-conteneurs.md)

---

## Objectifs de cette partie

- Installer Docker sur votre système d'exploitation
- Vérifier l'installation et lancer un premier conteneur
- Maîtriser les commandes Docker essentielles
- Comprendre les options de docker run
- Gérer les images et conteneurs localement

---

## 2.1 Installation de Docker

### Windows & Mac

```bash
# Télécharger Docker Desktop depuis :
https://www.docker.com/products/docker-desktop/

# Vérifier l'installation
docker --version
docker version
```

### Linux (Ubuntu/Debian)

```bash
# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Vérifier l'installation
docker run hello-world
```

---

## 2.2 Votre Premier Conteneur

### 📝 Exemple : Lancer un serveur web Nginx

```bash
# Lancer Nginx en mode détaché
docker run -d -p 8080:80 --name mon-nginx nginx

# Explication des options :
# -d          : Mode détaché (background)
# -p 8080:80  : Mapper le port 8080 de l'hôte vers le port 80 du conteneur
# --name      : Donner un nom au conteneur
# nginx       : Nom de l'image à utiliser

# Vérifier que le conteneur est actif
docker ps

# Tester dans le navigateur
# Ouvrir http://localhost:8080
```

---

## 2.3 Commandes Docker Essentielles

### Gestion des Images

```bash
# Rechercher une image sur Docker Hub
docker search python

# Télécharger une image
docker pull python:3.11

# Lister toutes les images locales
docker images

# Afficher les détails d'une image
docker inspect python:3.11

# Supprimer une image
docker rmi python:3.11

# Supprimer toutes les images non utilisées
docker image prune -a
```

### Gestion des Conteneurs

```bash
# Lancer un conteneur
docker run -d --name mon-app -p 8000:8000 python:3.11

# Lister les conteneurs actifs
docker ps

# Lister TOUS les conteneurs (actifs et arrêtés)
docker ps -a

# Arrêter un conteneur
docker stop mon-app

# Démarrer un conteneur arrêté
docker start mon-app

# Redémarrer un conteneur
docker restart mon-app

# Voir les logs d'un conteneur
docker logs mon-app
docker logs -f mon-app  # Suivre les logs en temps réel

# Exécuter une commande dans un conteneur
docker exec -it mon-app bash
docker exec mon-app ls /app

# Copier des fichiers
docker cp fichier.txt mon-app:/app/
docker cp mon-app:/app/resultat.txt ./

# Voir les statistiques
docker stats

# Supprimer un conteneur
docker rm mon-app

# Supprimer tous les conteneurs arrêtés
docker container prune
```

---

## 2.4 Options de docker run

| Option | Description | Exemple |
|--------|-------------|---------|
| `-d, --detach` | Exécuter en arrière-plan | `docker run -d nginx` |
| `-p, --publish` | Publier un port | `docker run -p 8080:80 nginx` |
| `--name` | Nommer le conteneur | `docker run --name web nginx` |
| `-v, --volume` | Monter un volume | `docker run -v /host:/container nginx` |
| `-e, --env` | Variable d'environnement | `docker run -e DB_HOST=localhost app` |
| `--rm` | Supprimer après arrêt | `docker run --rm python:3.11 python --version` |
| `-it` | Mode interactif | `docker run -it python:3.11 bash` |
| `--network` | Connecter à un réseau | `docker run --network mon-reseau app` |
| `--restart` | Politique de redémarrage | `docker run --restart always nginx` |

---

## 💡 Points clés à retenir

- Docker Desktop est la méthode d'installation recommandée pour Windows et Mac
- `docker pull` télécharge des images, `docker run` lance des conteneurs
- `docker ps` liste les conteneurs actifs, `docker ps -a` liste tous les conteneurs
- `docker exec -it` permet d'accéder à l'intérieur d'un conteneur
- Les options de `docker run` se combinent pour configurer le conteneur

---

[← 01 - Fondamentaux](01-fondamentaux-docker.md) | [🏠 Accueil](README.md) | [03 - Images et Conteneurs →](03-images-et-conteneurs.md)