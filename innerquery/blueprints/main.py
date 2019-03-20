
from flask import Blueprint,render_template,request,redirect,url_for,abort,flash,send_from_directory,current_app
from flask_login import login_required,current_user
from pyecharts import Bar
from innerquery.extensions import db
from innerquery.forms.main import QueryForm,EdtQueryForm
from innerquery.models import  QueryCondition,queryfromtarget
from innerquery.utils import buildform,buildsql,buildresult,buildexcel

main_bp = Blueprint('main',__name__)

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

@main_bp.route('/',methods=['GET','POST'])
@login_required
def index():
    form = QueryForm()
    if form.validate_on_submit():
        submitqueryform(form)
    return render_template('main/index.html',form=form,edtform=None)

@main_bp.route('/query/<int:query_id>',methods=['GET','POST'])
@login_required
def query(query_id):
    condition = QueryCondition.query.get_or_404(query_id)
    sqlstr = condition.description
    paracount,formstr = buildform(query_id,condition.inparam)
    form = QueryForm()
    edtform = EdtQueryForm()
    edtform.qid.data = condition.id
    edtform.name.data = condition.qname
    edtform.description.data = condition.description
    edtform.inparam.data = condition.inparam
    edtform.resulttype.data = condition.resulttype
    result = ""
    data=''
    jsdependencies=[]
    if request.method == 'POST':
        if request.form.get('submit',None)=='保存查询':
            if form.validate_on_submit():
                submitqueryform(form)
                return redirect(url_for('.index'))
        else: 
            if request.form.get('subquery',None)=='查询':
                iscanquery = True
                if paracount:
                    params = []
                    for i in range(paracount):
                        if request.form.get('q_'+str(i)).strip() == '':
                            iscanquery = False
                            break
                        params.append(request.form.get('q_'+str(i)))
                    sqlstr = buildsql(sqlstr,params)
                if iscanquery:
                    data = queryfromtarget(sqlstr)
                    jsdependencies,result = buildresult(condition.resulttype,data)
                else:
                    flash('请输入正确的查询条件','danger')
            if request.form.get('subdel',None)=='删除此查询':
                db.session.delete(condition)
                db.session.commit()
                return redirect(url_for('.index'))
            if request.form.get('toexcel',None)=='生成EXCEL':
                iscanquery = True
                if paracount:
                    params = []
                    for i in range(paracount):
                        if request.form.get('q_'+str(i)).strip() == '':
                            iscanquery = False
                            break
                        params.append(request.form.get('q_'+str(i)))
                    sqlstr = buildsql(sqlstr,params)
                if iscanquery:
                    data = queryfromtarget(sqlstr)
                    filename = buildexcel(condition.qname,data[0],data[1])
                    return redirect(url_for('.get_excel',filename=filename))
                else:
                    flash('请输入正确的查询条件','danger')
    return render_template('main/query.html',form=form,condition=condition,formstr=formstr,result=result,\
        host=REMOTE_HOST,script_list=jsdependencies,conditionname=condition.qname,edtform=edtform)


@main_bp.route('/downloads/<path:filename>')
def get_excel(filename):
    #return send_from_directory(current_app.config['EXCEL_DOWNLOAD_PATH'], filename,as_attachment=True)
    return current_app.send_static_file(filename)

@main_bp.route('/edtquery',methods=['POST'])
@login_required
def edtquery():
    if not current_user.isadmin:
        abort(403)
    form = EdtQueryForm()
    condition = QueryCondition.query.get_or_404(int(form.qid.data))
    condition.qname = form.name.data
    condition.description = form.description.data
    condition.inparam =  form.inparam.data
    condition.resulttype = form.resulttype.data
    print(condition.qname)
    if not condition.check_description():
        abort(500)
    db.session.commit()
    return redirect(url_for('.query',query_id=condition.id))

def submitqueryform(form):
    if not current_user.isadmin:
        abort(403)
    qname = form.name.data
    description = form.description.data
    inparam =  form.inparam.data
    resulttype = form.resulttype.data
    querycondition = QueryCondition(qname=qname,description=description,inparam=inparam,resulttype=resulttype)
    if not querycondition.check_description():
        abort(500)
    db.session.add(querycondition)
    db.session.commit()

