SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
BASE_DATOS = "./data/crypto.db"