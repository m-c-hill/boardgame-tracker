from app import create_app

app = create_app()
print(app.root_path)

if __name__ == "__main__":
    app.run()
