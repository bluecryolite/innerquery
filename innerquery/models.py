from datetime import datetime
from flask import current_app
from innerquery.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

result_type = [ (0,'普通数据集'),
                (1,'柱状图'),
                (2,'曲线图'),
                (3,'饼图')]

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(db.String(100),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(100))
    isadmin = db.Column(db.Boolean,default=False)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def rolename(self):
        if self.isadmin:
            return '管理员'
        else:
            return '操作员'

class QueryCondition(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    qname = db.Column(db.String(100),unique=True)
    tag = db.Column(db.String(100))
    description = db.Column(db.Text)
    inparam = db.Column(db.String(500))
    outstyle = db.Column(db.String(500))
    resulttype = db.Column(db.Integer(),default=0)
    ctime = db.Column(db.DateTime, default=datetime.utcnow)

    #before_models_committed信号不会用，先用对象方法代替
    def check_description(self):
        black_sheet = {'delete','drop','dump','update'}
        return len(set(self.description.split(' '))&black_sheet)==0

#从目标数据库中查询数据
def queryfromtarget(sql):
    #return db.session.execute(sql,bind='target').fetchall()
    #如果目标是MSSQL，单独处理
    if 'MSSQL_TARGET' in current_app.config.keys():
        msdict = current_app.config['MSSQL_TARGET']
        if msdict:
            return getmssqldata(msdict,sql)    
    cur = db.session.execute(sql, bind=db.get_engine(current_app,bind='target'))

    return cur.keys(),cur.fetchall()

#next two function is for mssql
def getmssqlconnect(msdict):
    import pymssql
    return pymssql.connect(host=msdict['host'],port=msdict['port'],user=msdict['user'],
                           password=msdict['password'],database=msdict['database'])

def getmssqldata(msdict,sql):
    conn=getmssqlconnect(msdict)
    cur = conn.cursor()
    cur.execute(sql)
    desc = [c[0] for c in cur.description]
    retdata = cur.fetchall()
    conn.close()
    return desc,retdata