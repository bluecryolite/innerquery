import os
import click
from flask import Flask,render_template
from innerquery.extensions import db,bootstrap,csrf,login_manager
from innerquery.settings import config
from innerquery.blueprints.main import main_bp
from innerquery.blueprints.auth import auth_bp
from innerquery.blueprints.user import user_bp
from innerquery.models import User,QueryCondition
from innerquery.forms.main import QueryForm


def create_app(config_name=None):
    app = Flask('innerquery')
    if config_name == None:
        config_name = os.getenv('FLASK_CONFIG','development')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context(app)
    register_template_context(app)
    register_errorhandles(app)
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp,url_prefix='/user')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, QueryCondition=QueryCondition)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        queryconditions = QueryCondition.query.order_by(QueryCondition.id).all()
        return dict(queryconditions=queryconditions)

def register_commands(app):
    @app.cli.command()
    def test():
        click.echo('This is a test')

    @app.cli.command()
    @click.option('--drop',is_flag=True,help='Create after drop')
    def initdb(drop):
        if drop:
            click.confirm('确认是否删掉原来的表',abort=True)
            db.drop_all()
            click.echo('成功删除表')
        db.create_all()
        click.echo('创建所有表')
        admin = User(
                    loginname='admin',
                    username='管理员',
                    isadmin=True
                    )
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        click.echo('添加管理员成功')

    
def register_errorhandles(app):
    # @app.errorhandler(400)
    # def bad_request(e):
    #     return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # @app.errorhandler(CSRFError)
    # def handle_csrf_error(e):
    #     return render_template('errors/400.html', description=e.description), 500


