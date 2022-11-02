#MY_LOCAL_IP=$(ipconfig getifaddr en0)
#uvicorn src.main:app --host "$MY_LOCAL_IP" --port 8000 --reload
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
