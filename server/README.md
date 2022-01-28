TODO:
* Add hidden field to song
* Lead singer as an array
* Add description metadata
* Buttons should be object



# Installation
python3 -m venv LiveTools-env
source LiveTools-env/bin/activate

pip3 install fastapi
pip3 install uvicorn
pip3 install websockets
pip3 install python-osc

pip3 install -r requirements.txt

# Start development server
uvicorn main:app --reload


# Ngrok

./ngrok 8000