from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    loginname = StringField('登录名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    submit = SubmitField('登录',render_kw={'class':'btn btn-primary'})