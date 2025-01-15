"""
Run the backend server from the command line.

python -m app.web
"""

import uvicorn

from .main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
