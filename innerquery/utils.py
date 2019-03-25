import os
from functools import wraps
import xlwt 
from flask import current_app, abort
from flask_wtf.csrf import generate_csrf
from flask_login import current_user
from pyecharts import Bar, Line, Pie


def buildsql(sql, params):
    ret = sql
    if params:
        for i in range(len(params)):
            ret = ret.replace('{'+str(i)+'}', params[i])
    return ret


def buildform(id, inparam=None):
    formlist = []
    formlist.append('<form action="/query/'+str(id)+'" method="post" class="form">')
    formlist.append('<input type="hidden" name="csrf_token" value="'+generate_csrf()+'">')
    paracount = 0
    if inparam:
        params = inparam.splitlines()
        paracount = len(params)
        for i in range(paracount):
            param = params[i]
            eles = param.split('|')
            formlist.append('<div class="form-group required">')
            elename = "q_"+str(i)
            formlist.append('<label class="form-control-label" for="'+elename+'">'+eles[1]+'</label>')
            if eles[0] in ['text', 'date']:
                formlist.append('<input class="form-control" type="text" id="'+elename+'" name="'+elename+'" value="">')
            #  select 格式  select|name|elename:elevalue,elename:elevalue
            if eles[0] in ['select']:
                formlist.append('<select class="form-control" id="'+elename+'" name="'+elename+'" >')
                sels = eles[2].split(',')
                for sel in sels:
                    nv = sel.split(':')
                    formlist.append('<option value="'+nv[1]+'">'+nv[0]+'</option>')
                formlist.append('</select>')
            formlist.append('</div>')
    formlist.append('<input class="btn btn-primary" id="subquery" name="subquery" type="submit" value="查询">')
    if current_user.isadmin:
        formlist.append('<button type="button" id="btnedt" class="btn btn-primary" data-toggle="modal" data-target="#edtQueryModal">修改查询</button>')
        formlist.append('<input class="btn btn-danger" id="subdel" name="subdel" type="submit" onclick="return confirm(\'确认删除此查询?\');" value="删除此查询">')
    formlist.append('<input class="btn btn-success" id="toexcel" name="toexcel" type="submit"  value="生成EXCEL">')
    formlist.append('</form>')
    return paracount, ''.join(formlist)


def buildresult(resulttype, data):
    coldesc, outdata = data[0], data[1]
    buildmap = {0: buildtable,
                1: buildbar,
                2: buildline,
                3: buildpie}
    func = buildmap[resulttype]
    return func(coldesc, outdata)


def buildtable(coldesc, outdata):
    tablelist = []
    tablelist.append('<table class="table table-striped">')
    
    tablelist.append('<thead><tr>')
    tablelist.extend(['<th>'+col+'</th>' for col in coldesc])
    tablelist.append('</tr></thead>')

    tablelist.append('<tbody>')
    for row in outdata:
        tablelist.append('<tr>')
        tablelist.extend(['<td>'+str(ele)+'</td>' for ele in row])
        tablelist.append('</tr>')
    tablelist.append('</tbody>')

    tablelist.append('</table>')
    return [], ''.join(tablelist)


def buildbar(coldesc, outdata):
    return __build_shape(Bar(''), coldesc, outdata)


def buildline(coldesc, outdata):
    return __build_shape(Line(''), coldesc, outdata)


def buildpie(coldesc, outdata):
    return __build_shape(Pie(''), coldesc, outdata)


def buildexcel(name, coldesc, outdata):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(name, cell_overwrite_ok=True)
    for i in range(len(coldesc)):
        sheet.write(0, i, coldesc[i])
        print(coldesc[i])
    for i in range(len(outdata)):
        for j in range(len(outdata[i])):
            sheet.write(i+1, j, u'%s' % str(outdata[i][j]))
    filename = 'toexcel.xls'
    workbook.save(os.path.join(current_app.config['EXCEL_DOWNLOAD_PATH'], filename))
    return filename


# @admin_required decorator,create query,user manage is need
def admin_required(func):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.isadmin:
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator(func)


def __build_shape(shape, coldesc, outdata):
    count = 2
    if not isinstance(shape, Pie):
        count = len(coldesc)

    for i in range(1, count):
        if isinstance(shape, Bar):
            shape.add(coldesc[i], [ele[0] for ele in outdata], [ele[i] for ele in outdata], is_label_show=True)
        else:
            shape.add(coldesc[i], [ele[0] for ele in outdata], [ele[i] for ele in outdata])
    print(outdata)
    print(coldesc)

    return shape.get_js_dependencies(), shape.render_embed()
