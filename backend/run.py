import os
# from dotenv import load_dotenv
from .app import create_app

# load_dotenv()

config_name = os.getenv("CONFIG_MODE") or 'development'
app = create_app(config_name)

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT") or 5000)
