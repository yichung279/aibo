#!/usr/bin/env python3

import  uvicorn
from fastapi import FastAPI
import config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.host, port=config.port, ssl_keyfile=config.key, ssl_certfile=config.cert)
