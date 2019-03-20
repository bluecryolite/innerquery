from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,HiddenField
from wtforms.validators import DataRequired,Length
from innerquery.models import result_type

class QueryForm(FlaskForm):
    name = StringField('查询名称',validators=[DataRequired(),Length(1,100)])
    description = TextAreaField('SQL内容',validators=[DataRequired()],render_kw={'rows':5})
    inparam = TextAreaField('输入条件')
    resulttype = SelectField('结果类型', coerce=int)
    submit = SubmitField('保存查询')
    def __init__(self, *args, **kwargs):
        super(QueryForm,self).__init__(*args, **kwargs)
        self.resulttype.choices = result_type


class EdtQueryForm(FlaskForm):
    qid = HiddenField('id')
    name = StringField('查询名称',validators=[DataRequired(),Length(1,100)])
    description = TextAreaField('SQL内容',validators=[DataRequired()],render_kw={'rows':5})
    inparam = TextAreaField('输入条件')
    resulttype = SelectField('结果类型', coerce=int)
    submit = SubmitField('修改查询',id='edtsubmit',_name='edtsubmit')
    def __init__(self, *args, **kwargs):
        super(EdtQueryForm,self).__init__(*args, **kwargs)
        self.resulttype.choices = result_type