import os
from src.app import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5009))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)