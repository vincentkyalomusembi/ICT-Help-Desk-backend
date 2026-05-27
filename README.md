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

4. Create your `.env` file and ask the team lead / backend lead for the credentials

5. Start the server
```bash
   fastapi dev app/main.py
```

---

### Daily Workflow
1. Activate your virtual environment
```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
```

2. Switch to your branch and pull latest changes from dev
```bash
   git checkout your-branch-name
   git pull origin dev
```

3. Do your work, then push and raise a PR for review
```bash
   git add .
   git commit -m "your message"
   git push
```

---

> Never push directly to main or dev. Always work on your own branch and raise a PR into dev.