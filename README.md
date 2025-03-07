# JànguXayma AI

### 📌 Plateforme intelligente d'évaluation automatisée des exercices de bases de données

## 🚀 Présentation
JànguXayma AI est une plateforme intelligente permettant aux étudiants d'uploader leurs exercices en bases de données. Une IA analyse et corrige automatiquement leurs travaux, fournissant des feedbacks détaillés et des statistiques pour améliorer l’apprentissage.

## 🛠 Technologies utilisées

### Backend :
- **Django** (Python) - Framework web
- **PostgreSQL** - Base de données relationnelle
- **DeepSeek AI (via Ollama)** - Moteur d’évaluation intelligente
- **Django REST Framework (DRF)** - API REST

### Frontend :
- **React** - Interface utilisateur dynamique
- **TailwindCSS & DaisyUI** - UI moderne et responsive

### DevOps & Déploiement :
- **Docker & Docker Compose** - Conteneurisation et orchestration
- **Amazon EC2** - Hébergement
- **NGINX** - Serveur proxy

---

## 🏰 Installation et Configuration

### 1️⃣ Cloner le projet
```sh
git clone https://github.com/janguXayma/backend.git
cd backend
```

### 2️⃣ Backend - Django
#### 📌 Configuration
- **Créer et activer un environnement virtuel**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

- **Installer les dépendances**
```sh
pip install -r requirements.txt
```

- **Créer un fichier `.env` et copier celui de `.env.example`**
```sh
cp .env.example .env
```

- **Appliquer les migrations et lancer le serveur**
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 3️⃣ Frontend - React
```sh
cd frontend
npm install
npm start
```

---

## 🔥 Fonctionnalités principales
✅ Upload des fichiers SQL par les étudiants  
✅ Correction automatique via IA  
✅ Explication détaillée des erreurs  
✅ Génération de statistiques sur les performances  
✅ Interface moderne et intuitive  
✅ Possibilité pour les professeurs d'affiner la correction  

---

## 🛠 Déploiement avec Docker Compose
### Prérequis
- Avoir **Docker** et **Docker Compose** installés sur votre machine.

### Lancer l'application avec Docker Compose
```sh
docker-compose up -d --build
```
Cela va créer et démarrer les conteneurs pour le backend, le frontend et la base de données PostgreSQL.

### Arrêter les conteneurs
```sh
docker-compose down
```

### Exécuter les migrations avec Docker
```sh
docker-compose exec backend python manage.py migrate
```

### Accéder aux logs
```sh
docker-compose logs -f
```

---

## 🌟 Améliorations futures
- Intégration d’un système de feedback personnalisé
- Ajout d’un mode examen avec notation automatique
- Dashboard avancé pour les enseignants

---

## 🐝 Contribuer
Les contributions sont les bienvenues ! Merci de suivre ces étapes :
1. **Forker** le projet
2. **Créer** une branche feature (`git checkout -b feature-ma-feature`)
3. **Commit** vos modifications (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. **Pousser** vers votre repo (`git push origin feature-ma-feature`)
5. **Créer** une Pull Request

---

## 🌇 Licence
Ce projet est sous licence **ESP**.

👥 **Contributeurs**
- Omar DIOP  
- Mouhamed THIAM  
- Nafissatou M SOW  
- Mouhamed DIAHATE  
- Ndeye Mareme GUEYE  

📩 **Contact :** [email@example.com](mailto:email@example.com)

