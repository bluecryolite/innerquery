from flask import Blueprint,render_template,flash,redirect,url_for
from flask_login import login_required,current_user
from innerquery.models import User
from innerquery.extensions import db
from innerquery.forms.user import UserForm,PasswordForm
from innerquery.utils import admin_required

user_bp = Blueprint('user',__name__)

@user_bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('user/index.html',users=users)

@user_bp.route('/deluser/<int:user_id>',methods=['POST'])
@login_required
@admin_required
def del_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.loginname=='admin':
        flash('admin不能被删除','warning')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('用户已删除','success')
    return redirect(url_for('.index'))

@user_bp.route('/add',methods=['GET','POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        loginname = form.loginname.data
        isadmin = form.isadmin.data
        user = User(username=username,loginname=loginname,isadmin=isadmin)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('user/adduser.html',form=form)


@user_bp.route('/setpassword',methods=['GET','POST'])
@login_required
def setpassword():
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        if not user.check_password(form.oldpassword.data):
            flash('密码错误','warning')
        elif form.newpassword.data!=form.renewpassword.data:
            flash('重复密码错误','warning')
        else:
            user.set_password(form.newpassword.data)
            db.session.commit()
            flash('修改密码成功','success')
    return render_template('user/setpassword.html',form=form)
