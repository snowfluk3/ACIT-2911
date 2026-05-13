from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

def start_server():
    app.run(debug=True)

# Run the file - uv run run.py
if __name__ == "__main__":
    start_server()
