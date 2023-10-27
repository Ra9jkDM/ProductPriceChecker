!/bin/bash
source .venv/bin/activate
export $(cat .env)
python3 app.py
