from API.main import app as app
import uvicorn
import os
import joblib

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


