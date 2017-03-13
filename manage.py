from app import create_app

config = 'debug'
app = create_app(config)

if __name__ == "__main__":
    if config == 'debug':
        app.run(debug=True)
    else:
        app.run(debug=False)
