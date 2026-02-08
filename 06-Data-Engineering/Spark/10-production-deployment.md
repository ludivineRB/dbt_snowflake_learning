# 10 - Déploiement en production

[← 09 - Sujets avancés](09-advanced-topics.md) | [🏠 Accueil](README.md)

---

## 1. Modes de déploiement

- **Standalone** : Géré par Spark.
- **YARN** : Cluster Hadoop.
- **Kubernetes** : Orchestration native.
- **Managed** : Databricks, AWS EMR, GCP Dataproc.

## 2. Soumission de Job (spark-submit)

```bash
spark-submit 
  --master yarn 
  --deploy-mode cluster 
  --num-executors 10 
  --executor-memory 8G 
  my_app.py
```

## 3. Monitoring

- **Spark UI** : http://localhost:4040.
- **History Server** : Analyse post-mortem.

## 4. Best Practices
- Validation de schéma.
- Gestion d'erreurs (Try/Except).
- Idempotence des écritures.

---

[← 09 - Sujets avancés](09-advanced-topics.md) | [🏠 Accueil](README.md)
