📊 Prédiction de la consommation d’énergie et des émissions de CO₂ des bâtiments non résidentiels à Seattle
📌 Contexte
Seattle vise la neutralité carbone en 2050. Les bâtiments représentent une part importante des émissions de gaz à effet de serre. Cependant, les relevés de consommation sont coûteux et incomplets.
👉 Objectif : prédire la consommation énergétique et les émissions de CO₂ à partir des données structurelles des bâtiments.
-----
🎯 Objectifs du projet
- Analyse exploratoire approfondie (EDA)
- Nettoyage complet des données
- Feature engineering
- Entraînement et optimisation de modèles
- Choix du meilleur modèle (Random Forest)
- Création d'une API BentoML
- Conteneurisation en Docker
- Déploiement sur Google Cloud Run
- Test final de l’API en production

🗂️ Données
Source : dataset énergétique des bâtiments de Seattle.
Taille après nettoyage : 3119 lignes, 50 colonnes.
Variable cible : SiteEUIWN (kBtu/sf) → intensité énergétique normalisée par la météo.
--------
🔧 Prétraitement
Suppression des colonnes non pertinentes (administratives, énergétiques à risque de fuite, trop vides).
Détection et suppression des incohérences et outliers (méthode IQR).
Encodage des variables catégorielles (One-Hot Encoding → 128 colonnes).
Feature engineering :BuildingAge , FloorsPerBuilding , ParkingRatio , EnergyUsePerArea , GHGPerArea , etc.
-------
📈 Analyse exploratoire
- Distribution asymétrique des variables énergétiques → transformation log recommandée.
- Outliers détectés sur les émissions et surfaces.
- Corrélations modérées avec les surfaces (PropertyGFATotal, PropertyGFABuilding(s)).
- Impact du type de bâtiment visible via boxplots.

🤖 Modélisation
Modèles testés :
- Dummy Regressor
- Régression Linéaire
- SVR
- Random Forest

⚡ Résultats :
Modèle	CV R²	Test R²	MAE	RMSE	Interprétation
Dummy Regressor	~0	~0	32.5	65.4	Non pertinent
Linear Regression	0.10	~0.42	27.9	78.3	Fiabilité limitée
SVR	0.11	~0.08	25.3	62.4	Faible généralisation
Random Forest	0.89	~0.83	6.9	26.6	✅ Modèle fiable
👉 Random Forest retenu pour sa capacité de généralisation et ses performances élevées.

 ⚙️ Optimisation
- Hyperparamètres optimisés :  
  - `max_depth = 20`  
  - `min_samples_split = 2`  
  - `n_estimators = 200`  
- Score CV R² : **0.887**

🔍 Interprétation des features
Top 3 des variables les plus influentes :
  -  SiteEnergyUseWN (kBtu) → 51.6%
  -  PropertyGFABuilding(s) → 16.6%
  -  argestPropertyUseTypeGFA → 16.5%

✅ Bilan
- Pipeline complet : nettoyage, encodage, scaling, validation croisée, tuning hyperparamètres.
- Random Forest = modèle final avec R² test = 0.83 et MAE ~ 6.9.
- Visualisations et analyses claires pour appuyer les choix.

🚀 Perspectives
- Intégration du modèle dans une application métier pour prédire la consommation énergétique.
- Extension à d’autres villes ou années pour tester la robustesse.
- Recommandations ciblées pour améliorer l’efficacité énergétique des bâtiments.

📂 Structure du projet

projet-seattle-energy
│
├── notebooks/
│ └── EDA_Modelling.ipynb
│
├── api/
│ ├── service.py # API BentoML
│ ├── bentofile.yaml
│ ├── Dockerfile
│ ├── requirements.txt
│ └── model.joblib # Modèle exporté
│
├── data/
│ └── seattle_energy.csv # Jeu de données nettoyé
│
├── slides/
│ └── projet6.pdf # Présentation finale
│
└── README.md
- Docker :
docker build -t energy-service .
docker run -p 8080:8080 energy-service

- Test API :
import requests
r = requests.post("https://energy-model-146194267768.europe-west1.run.app", json=payload)
print(r.json())

- Résultat attendu :
Réponse JSON : {'prediction': 56.85652750516837}

* Auteur

Projet réalisé par Cheikh