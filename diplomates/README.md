# 🎓 Complexe Scolaire Les Diplomates — Système de Gestion Scolaire

Plateforme Django complète pour la gestion d'un établissement scolaire en Guinée.

---

## 🚀 Installation & Démarrage

### 1. Prérequis
```bash
Python 3.11+
pip
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditez .env avec vos valeurs
```

### 5. Créer le fichier `.env`
```
SECRET_KEY=votre-cle-secrete-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Appliquer les migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations eleves
python manage.py makemigrations finance
python manage.py makemigrations notes
python manage.py makemigrations badges
python manage.py makemigrations actualites
python manage.py migrate
```

### 7. Créer les données de démonstration
```bash
python setup_initial_data.py
```

### 8. Collecter les fichiers statiques (production)
```bash
python manage.py collectstatic
```

### 9. Lancer le serveur
```bash
python manage.py runserver
```

Accédez à : **http://127.0.0.1:8000**

---

## 🔑 Comptes de Connexion (Démo)

| Rôle | Identifiant | Mot de passe |
|------|-------------|--------------|
| **Administrateur** | `admin` | `Admin@2024!` |
| **Parent** | `parent1` | `Parent@2024!` |
| **Professeur** | `prof1` | `Prof@2024!` |

---

## 📱 Pages & Fonctionnalités

### 🌐 Public
| Page | URL |
|------|-----|
| Accueil | `/` |
| Actualités | `/actualites/` |
| Contact | `/contact/` |
| Programmes | `/programmes/` |

### 🔐 Authentification
| Page | URL |
|------|-----|
| Splash screen | `/compte/` |
| Connexion | `/compte/connexion/` |
| Déconnexion | `/compte/deconnexion/` |

### 👨💼 Admin / Finance
| Page | URL |
|------|-----|
| Dashboard Financier | `/finance/` |
| Transactions | `/finance/transactions/` |
| Validation paiement | `/finance/transactions/<id>/valider/` |
| Paiement manuel | `/finance/paiement/manuel/` |

### 👨🏫 Professeurs
| Page | URL |
|------|-----|
| Liste classes | `/notes/` |
| Saisie notes | `/notes/classe/<id>/saisie/` |
| Bulletin élève | `/notes/eleve/<id>/bulletin/` |

### 🎫 Badges
| Page | URL |
|------|-----|
| Gestion badges | `/badges/` |
| Détail badge | `/badges/<id>/` |
| Vérification QR | `/badges/verifier/<uuid>/` |

### 👨👧 Parent / Élève
| Page | URL |
|------|-----|
| Portail parent | `/eleves/portail/` |
| Paiement mobile | `/finance/paiement/<eleve_id>/` |
| Succès paiement | `/finance/paiement/succes/<id>/` |

---

## 🏗️ Architecture

```
diplomates/                   ← Config Django (settings, urls)
apps/
├── accounts/                 ← Utilisateurs (Admin, Parent, Prof, Élève)
├── eleves/                   ← Gestion des élèves & classes
├── finance/                  ← Paiements, transactions, frais
├── notes/                    ← Notes, bulletins, matières
├── badges/                   ← Badges numériques + QR codes
└── actualites/               ← News, événements, contact
templates/
├── base.html                 ← Layout principal
├── includes/
│   ├── navbar.html
│   ├── footer.html
│   ├── sidebar_admin.html
│   └── topbar_admin.html
├── pages/
│   ├── home.html
│   ├── actualites.html
│   ├── contact.html
│   ├── dashboard.html
│   ├── portail_parent.html
│   ├── paiement.html
│   ├── paiement_succes.html
│   ├── badge_etudiant.html
│   ├── splash.html
│   ├── finance/
│   │   ├── transactions.html
│   │   ├── validation_paiement.html
│   └── paiement_manuel.html
│   ├── notes/
│   │   ├── saisie.html
│   │   ├── classes.html
│   │   └── bulletin.html
│   ├── badges/
│   │   ├── liste.html
│   │   └── verification.html
│   └── eleves/
│       ├── liste.html
│       ├── detail.html
│       └── form.html
├── registration/
│   └── login.html
static/
├── css/
│   ├── style.css             ← CSS principal
│   └── admin-extra.css       ← CSS admin étendu
├── js/
│   └── main.js
└── images/
```

---

## 🛡️ Sécurité & Permissions

| Rôle | Accès |
|------|-------|
| `admin` / `directeur` | Tout le système |
| `finance` | Dashboard + transactions + validation |
| `professeur` | Saisie notes + classes |
| `parent` | Portail + paiements + badges enfant |
| `eleve` | Espace élève + notes + badge |

---

## 🔧 Administration Django

Accédez au panel admin : **http://127.0.0.1:8000/admin/**

---

## 📦 Stack Technique

- **Backend** : Django 5.0
- **Base de données** : SQLite (dev) → PostgreSQL (prod)
- **Auth** : Custom User Model avec rôles
- **CSS** : CSS3 pur + variables (pas de Bootstrap)
- **Fonts** : Sora + Plus Jakarta Sans (Google Fonts)
- **QR Codes** : qrcode library
- **Static files** : WhiteNoise

---

*© 2024 Complexe Scolaire Les Diplomates — Conakry, République de Guinée*
