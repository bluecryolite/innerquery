from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import CSRFProtect

login_manager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from innerquery.models import User
    user = User.query.get(int(user_id))
    return user
    
login_manager.login_view = 'auth.login'
#不显示需要登录的信息
login_manager.login_message = None
