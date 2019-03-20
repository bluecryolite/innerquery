from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField
from wtforms.validators import DataRequired,Length

class UserForm(FlaskForm):
    username = StringField('用户姓名',validators=[DataRequired()])
    loginname = StringField('登录名',validators=[DataRequired()])
    password = StringField('登录密码',validators=[DataRequired()])
    isadmin = BooleanField('是否管理员')
    submit = SubmitField('保存')

class PasswordForm(FlaskForm):
    oldpassword = PasswordField('旧密码',validators=[DataRequired()])
    newpassword = PasswordField('新密码',validators=[DataRequired()])
    renewpassword = PasswordField('重复新密码',validators=[DataRequired()])
    submit = SubmitField('确认修改')