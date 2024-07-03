from app import create_app

app = create_app()  # factory function for initialisation of the flask app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
