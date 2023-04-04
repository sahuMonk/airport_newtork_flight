from flask import Flask
from models import db, UserModel
from flask_login import LoginManager

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'BadSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///votrbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ""
app.config['MAIL_PASSWORD'] = ""
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


from auth import auth
import views

app.register_blueprint(auth, url_prefix="/auth")


if __name__ == '__main__':
    app.run()

