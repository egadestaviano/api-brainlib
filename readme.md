## LMS Backend (Quick Start)

### Setup
- Python 3.13 (virtualenv recommended)
- MySQL server running locally (Laragon/XAMPP) with a user that can create DBs

### Install
```bash
python -m venv venv
. venv\Scripts\activate or source venv/Scripts/activate
pip install -r requirements.txt
```

# Migrate your database
```bash
python run.py migrate
```

# Clear All Cache
```bash
python run.py cache:clear
```

# Running Your App
```bash
python run.py serve
```