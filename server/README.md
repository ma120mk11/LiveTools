# Installation
python3 -m venv LiveTools-env
source LiveTools-env/bin/activate

`pip3 install -r requirements.txt`

# Start development server
uvicorn main:app --reload
Dev:
uvicorn main:app --host 0.0.0.0
Prod:
uvicorn app.main:app --host 192.168.1.40

# Ngrok

./ngrok 8000


# Run DB migrations
`alembic revision --autogenerate -m "Some description"`
`alembic upgrade head`