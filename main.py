import os
import requests
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def relay(request: Request, path: str):
    # Extract headers and body from incoming request from Google Script
    headers = dict(request.headers)
    body = await request.body()
    
    # Clean up host header to avoid conflicts
    headers.pop("host", None)
    
    # We expect the real destination URL to be sent via a custom header from Google Apps Script
    # Usually passed as 'x-target-url' or encoded in the request.
    target_url = request.headers.get("x-target-url")
    
    if not target_url:
        return {"status": "Exit Node is running successfully!"}
        
    try:
        # Forward request to the actual website
        res = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=body,
            timeout=30,
            allow_redirects=False
        )
        
        # Return response back to Google Script
        return Response(
            content=res.content,
            status_code=res.status_code,
            headers=dict(res.headers)
        )
    except Exception as e:
        return Response(content=str(e), status_code=500)
