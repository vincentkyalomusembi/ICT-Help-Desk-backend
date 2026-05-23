## Development Workflow

### Getting Started (First Time)
1. Clone the repo
```bash
   git clone https://github.com/vincentkyalomusembi/ICT-Help-Desk-backend.git
   cd ICT-Help-Desk-backend
```

2. Create and activate virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Create your `.env` file — ask the backend lead for the credentials

5. Run migrations
```bash
   alembic upgrade head
```

6. Start the server
```bash
   fastapi dev app/main.py
```

---

### Daily Workflow
1. Switch to main and pull latest changes
```bash
   git checkout main
   git pull
```

2. Activate your virtual environment
```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
```

3. Install any new dependencies
```bash
   pip install -r requirements.txt
```

4. Run migrations — only applies if someone added a new table or column. Safe to always run, it skips if nothing is new.
```bash
   alembic upgrade head
```

5. Switch to your branch and do your work
```bash
   git checkout your-branch-name
```

6. Once done, push and raise a PR for review
```bash
   git add .
   git commit -m "your message"
   git push
```

---

> Never push directly to main. Always work on your own branch and raise a PR.