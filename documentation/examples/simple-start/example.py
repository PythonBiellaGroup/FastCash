from typing import Optional
import fastapi
import uvicorn

api = fastapi.FastAPI()

@api.get("/")
def index():
    body = "<html>" \
           "<body style='padding: 10px;'>" \
           "<h1>Benvenuti su FastAPI</h1>" \
           "<div>" \
           "Try it: <a href='/api/calcola?x=7&y=11'>/api/calcola?x=7&y=11</a>" \
           "</div>" \
           "</body>" \
           "</html>"

    return fastapi.responses.HTMLResponse(content=body)

api.get('/default')
def default():
    '''
    Che tipo di informazioni restituisce di default?
    '''
    return {
        "messaggio":"PythonBiellaGroup!" 
    }

api.get('/api/test')
def calcola(x: int, y: int, z: Optional[int] = None):
    if z == 0:
        # per gestire meglio gli errori! E non tornare per forza 500 internal server error!
        return fastapi.responses.JSONResponse(content={"Errore":"Il terzo parametro non esiste!"}, status_code = 400)
    
    value = x + y
    
    if z is not None:
        value *= z
    
    return {
        'x': x,
        'y': y,
        'z': z,
        'value': value
    }
    
    
if __name__ == "__main__":
    uvicorn.run(api, port=8000, host="127.0.0.1")