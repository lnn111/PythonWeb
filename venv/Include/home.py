from flask import Flask, redirect, url_for, request, render_template, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
import sqlite3 as sql
from flask_admin import BaseView, expose
from flask_babelex import Babel

# 导入tf扩展的表单类
from flask_wtf import FlaskForm

# 导 入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField

# 导入wtf扩展提供的表单验证
from wtforms.validators import DataRequired, EqualTo, Length

import Spider

app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        lists = Article.query.all()
        for item in lists:
            db.session.delete(item)
        db.session.commit()
        Spider.getHyArtical()
        Spider.getKyleduo()
        Spider.getWeishu()
        lists = Article.query.all()
        size = len(lists)
        return self.render('admin/index.html', lists=lists, size=size)

admin = Admin(app
              , name='SkyBlog'
              , index_view=MyAdminIndexView(name='首页')
              , template_mode='bootstrap3')
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstweb.sqlite3'
db = SQLAlchemy(app)
app.secret_key = 'random string'





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    user = db.Column(db.String(100), unique=True, nullable=False)
    psw = db.Column(db.String(16))

    def __init__(self, user, psw, username):
        self.username = username
        self.user = user
        self.psw = psw


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    link = db.Column(db.String(5000))
    time = db.Column(db.String(5000))
    read_num = db.Column(db.String(100))
    comm_num = db.Column(db.String(100))

    def __init__(self,title,content,link,time,read_num,comm_num):
        self.title=title
        self.content=content
        self.link=link
        self.time=time
        self.read_num=read_num
        self.comm_num=comm_num



class MyView(ModelView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',lists=lists)


class UserModelView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    page_size = 50
    column_labels = {
        'id': u'序号',
        'user': u'账号',
        'psw': u'密码',
        'username': u'昵称'
    }


admin.add_view(UserModelView(User, db.session, name=u'用户表'))

class MicroBlogModelView(ModelView):
    @expose('/')
    def __index__(self):
        lists=Article.query.all()
        for item in lists:
            db.session.delete(item)
        db.session.commit()
        Spider.getHyArtical()
        lists = Article.query.all()
        size=len(lists)
        return self.render('admin/article.html',lists=lists ,size=size)

# admin.add_view(MicroBlogModelView(Article,db.session,name=u'文章'))

class RegisterView(BaseView):
    @expose('/')
    def index(self):
        form = LoginForm()
        return self.render('admin/register.html', form=form)


admin.add_view(RegisterView(name=u'注册', endpoint='register'))


class LoginForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    psw = PasswordField('密码', validators=[Length(6, 12)])
    username = StringField('昵称', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = LoginForm()
    msg = None
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            psw = request.form['psw']
            username = request.form['username']
            user = User(name, psw, username)
            db.session.add(user)
            try:
                db.session.commit()
            except BaseException:
                msg = '操作数据库出错！'
            else:
                msg = 'You were successfully registered'
        else:
            msg = '表单验证出错！'
    else:
        msg = 'You were registered failed'
    flash(msg)
    url = url_for('register.index')
    return redirect(url)


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
