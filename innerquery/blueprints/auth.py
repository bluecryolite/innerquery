from flask import render_template,Blueprint,flash,redirect,url_for
from flask_login import login_user,logout_user,login_required
from innerquery.forms.auth import LoginForm
from innerquery.models import User

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        loginname = form.loginname.data
        password = form.password.data
        user = User.query.filter_by(loginname=loginname).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('登录失败','warning')

    return render_template('auth/login.html',form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

