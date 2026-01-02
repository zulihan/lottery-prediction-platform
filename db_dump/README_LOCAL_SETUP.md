# Lottery Prediction Platform - Guide d'Installation Locale

## Prérequis

- Python 3.11+
- PostgreSQL 14+ (ou 16)
- pip ou uv pour la gestion des packages

## 1. Installation des Dépendances Python

```bash
pip install streamlit pandas numpy plotly matplotlib scipy sqlalchemy psycopg2-binary requests beautifulsoup4 trafilatura python-dateutil xlsxwriter
```

Ou avec un fichier requirements.txt :
```bash
pip install -r requirements.txt
```

## 2. Configuration de la Base de Données PostgreSQL

### Créer la base de données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE lottery_prediction;

# Se connecter à la nouvelle base
\c lottery_prediction
```

### Importer les données

```bash
# Importer les tirages Euromillions
psql -U postgres -d lottery_prediction -f db_dump/euromillions_drawings.sql

# Importer les tirages French Loto
psql -U postgres -d lottery_prediction -f db_dump/french_loto_drawings.sql
```

## 3. Configuration des Variables d'Environnement

Créer un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql://postgres:votre_mot_de_passe@localhost:5432/lottery_prediction
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=votre_mot_de_passe
PGDATABASE=lottery_prediction
```

Ou exporter directement :

```bash
export DATABASE_URL="postgresql://postgres:votre_mot_de_passe@localhost:5432/lottery_prediction"
```

## 4. Lancer l'Application

```bash
streamlit run app.py --server.port 5000
```

L'application sera accessible sur : http://localhost:5000

## Structure des Fichiers Importants

```
.
├── app.py                  # Application principale Streamlit
├── database.py             # Configuration et modèles de base de données
├── prediction_strategies.py # Stratégies de prédiction Euromillions
├── french_loto_strategy.py  # Stratégies de prédiction French Loto
├── fibonacci_strategy.py    # Stratégie basée sur Fibonacci
├── combination_analysis.py  # Analyse des combinaisons
└── db_dump/
    ├── euromillions_drawings.sql  # Dump SQL Euromillions
    ├── euromillions_drawings.csv  # Export CSV Euromillions
    ├── french_loto_drawings.sql   # Dump SQL French Loto
    └── french_loto_drawings.csv   # Export CSV French Loto
```

## Schéma de Base de Données

### Table `euromillions_drawings`
| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL | Clé primaire |
| date | DATE | Date du tirage |
| day_of_week | VARCHAR(20) | Jour de la semaine |
| n1-n5 | INTEGER | Les 5 numéros (1-50) |
| s1, s2 | INTEGER | Les 2 étoiles (1-12) |

### Table `french_loto_drawings`
| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL | Clé primaire |
| date | DATE | Date du tirage |
| draw_num | INTEGER | Numéro du tirage (1 ou 2 si double) |
| n1-n5 | INTEGER | Les 5 numéros (1-49) |
| lucky | INTEGER | Le numéro chance (1-10) |
| winners_rank1-7 | INTEGER | Nombre de gagnants par rang |
| prize_rank1-7 | FLOAT | Montant des gains par rang |
| currency | VARCHAR(10) | EUR ou FRF |

### Table `generated_combinations`
| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL | Clé primaire |
| created_at | DATE | Date de création |
| target_draw_date | DATE | Date du tirage ciblé |
| numbers | VARCHAR(50) | Numéros (JSON) |
| stars | VARCHAR(20) | Étoiles (JSON) |
| strategy | VARCHAR(100) | Stratégie utilisée |
| score | FLOAT | Score de la combinaison |

## Connexion à la Base de Données

Le fichier `database.py` gère automatiquement la connexion avec :
- Connection pooling (2-5 connexions)
- Retry logic avec exponential backoff
- Fallback vers SQLite en mémoire si PostgreSQL n'est pas disponible

### Exemple de code pour se connecter :

```python
from database import get_session, EuromillionsDrawing

# Obtenir une session
session = get_session()

# Récupérer les derniers tirages
recent_draws = session.query(EuromillionsDrawing)\
    .order_by(EuromillionsDrawing.date.desc())\
    .limit(10).all()

for draw in recent_draws:
    print(f"{draw.date}: {draw.n1}, {draw.n2}, {draw.n3}, {draw.n4}, {draw.n5} | {draw.s1}, {draw.s2}")

session.close()
```

## Données Historiques

- **Euromillions** : 1864 tirages (2004 - Août 2025)
- **French Loto** : 3522 tirages (1976 - Août 2025)

## Stratégies de Prédiction Disponibles

1. **Risk/Reward Balance** - Optimisation basée sur les probabilités
2. **Frequency Analysis** - Analyse des numéros chauds/froids
3. **Fibonacci Enhanced** - Séquences mathématiques de Fibonacci
4. **Markov Chain** - Prédiction basée sur les transitions de numéros
5. **Time Series Analysis** - Identification des patterns temporels
6. **Bayesian Inference** - Modélisation probabiliste

## Support

Pour toute question, consulter le fichier `replit.md` pour plus de détails sur l'architecture du projet.
