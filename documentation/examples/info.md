# Modern Python in FastAPI

## Type Hints

Usati non per documentare il codice (come solitamente si fa), ma hanno un impatto concreto nel codice e servono per fare "conversioni" automatiche.

Rendono il codice "tipizzato"

## Async/Await

ASGI = Asynchrous Server Gateway Interface servers.

Consentono di rendere il server asincrono favorendo la scalabilità (e la risposta).

Sfrutta la **potenza** della programmazione concorrente
-  creazione di task
-  funzioni async (con blocchi di async, await)
   -  Ovvero: mentre aspetti, vai avanti e gestisci nuovi comandi (ovvero nuove richieste)
-  Efficienza!!

- WSGI = web service gateway interface (gunicorn, MicroWSGI)
```python
def request(environ, start_response):
    # ...
    return r
```

- ASGI (Asynchrous Server Gateway Interface servers.)
Uvicorn è un server ASGI.
```python
async def app(scope, receive, send):
    r = await receive(scope):
    # ...
    return await send(r, scope)    
```

In pratica: ASGI è il successore spirituale di WSGI (anche se è comunque attivo) ed è a tutti gli effetti entrato a far parte dello standard python per la compatibilità tra web servers, frameworks e applications.

** References ** 
- https://asgi.readthedocs.io/en/latest/introduction.html
- https://medium.com/analytics-vidhya/difference-between-wsgi-and-asgi-807158ed1d4c
- https://morioh.com/p/e544d71b9af2

## Classi Pydantic

dataclasses + validazione dei dati.

- https://pydantic-docs.helpmanual.io/usage/dataclasses/

Servono per fare controlli e conversioni automatiche usando le type annotations.


