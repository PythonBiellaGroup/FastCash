export PYTHONPATH=$(pwd)
export API_ENDPOINT_PORT=8080
export VERBOSITY=DEBUG
export DEBUG_MODE=True
#python3 live/main.py
uvicorn live.main:app --reload --port 8042