from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()

# https://kevalnagda.github.io/flask-app-with-wsgi-and-nginx