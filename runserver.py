import os

from app import create_app
from config import config

app_config = config[os.getenv("FLASK_CONFIG") or "default"]
app = create_app(app_config)

if __name__ == "__main__":
    app.run()
