import os
import requests
import base64
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

AUTH_KEY = "Mohammad#4512"

@app.post("/")
async def handle_relay(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"e": "Invalid JSON"})

    client_key = data.get("k") or request.headers.get("x-exit-psk")
    if client_key != AUTH_KEY:
        return JSONResponse(status_code=401, content={"e": "unauthorized"})

    if "q" in data and isinstance(data["q"], list):
        results = []
        for q_item in data["q"]:
            results.append(execute_request(q_item))
        return {"q": results}
    
    return execute_request(data)

def execute_request(item):
    url = item.get("u")
    if not url:
        return {"e": "bad url"}
    try:
        method = item.get("m", "GET").upper()
        headers = {k: v for k, v in item.get("h", {}).items() if k.lower() not in ["host", "content-length", "accept-encoding"]}
        
        payload = None
        if item.get("b"):
            payload = base64.b64decode(item["b"])
            
        res = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=payload,
            timeout=15,
            allow_redirects=False
        )
        
        return {
            "s": res.status_code,
            "h": dict(res.headers),
            "b": base64.b64encode(res.content).decode('utf-8')
        }
    except Exception as e:
        return {"e": str(e)}

@app.get("/")
def health():
    return {"status": "ready"}
