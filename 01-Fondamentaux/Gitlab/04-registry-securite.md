# 04 - Registry et Sécurité

[← 03 - GitLab CI/CD](03-gitlab-ci-cd.md) | [🏠 Accueil](README.md) | [05 - Exercices →](05-exercices.md)

---

## 🎯 Objectifs de cette partie

- Utiliser le Container Registry intégré
- Découvrir les outils de sécurité (SAST, Secret Detection)
- Maîtriser les environnements et déploiements

---

## 1. Container Registry

GitLab inclut nativement un registre d'images Docker. C'est extrêmement pratique pour vos pipelines de Data Engineering.

### Pusher une image depuis la CI :
```yaml
build_image:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
```

---

## 2. Sécurité (DevSecOps)

GitLab est réputé pour ses outils de sécurité intégrés (souvent en un clic) :
- **SAST (Static Application Security Testing)** : Analyse votre code à la recherche de failles.
- **Secret Detection** : Empêche de pusher des mots de passe ou des clés API.
- **Dependency Scanning** : Analyse vos bibliothèques Python (via `requirements.txt`) pour trouver des vulnérabilités.

### Activer les scans simplement :
```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml
```

---

## 3. Environnements et Déploiements

GitLab permet de suivre où votre code est déployé (Staging, Production).
- **Environments** : Historique des déploiements.
- **Protected Environments** : Seuls certains utilisateurs peuvent déployer en production.

---

## 💡 Points clés à retenir

- Le **Container Registry** évite d'utiliser des outils externes comme Docker Hub.
- Utilisez les templates de sécurité (`include`) pour protéger vos projets sans effort.
- Surveillez vos environnements dans le menu `Operate > Environments`.

---

[← 03 - GitLab CI/CD](03-gitlab-ci-cd.md) | [🏠 Accueil](README.md) | [05 - Exercices →](05-exercices.md)
