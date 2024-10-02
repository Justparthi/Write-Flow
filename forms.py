from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for
import bleach
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

bootstrap = Bootstrap5(app)

allowed_tags = ['b', 'i', 'u', 'em', 'strong']
allowed_attributes = {}


login_manager = LoginManager()
login_manager.init_app(app)

user_input = '<script>alert("XSS")</script><b>Bold text</b>'
clean_input = bleach.clean(user_input, tags=allowed_tags, attributes=allowed_attributes)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:parthi@localhost:5432/postgres"
db = SQLAlchemy(app)




class Blog(db.Model):
    __tablename__='blog'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(250), unique=True, nullable=False)
    password = db.Column(String(500), nullable=False)
    name = db.Column(String(250), nullable=False)
    # author = db.Column(String(250), nullable=False)
    # img_url = db.Column(String(500), nullable=False)
    # subtitle = db.Column(String(500), nullable=False)

    def __init__(self,email,password,name):
        self.email=email
        self.password=password
        self.name=name
        # self.author=author
        # self.img_url=img_url
        # self.subtitle=subtitle

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            # "author": self.author,
            # "img_url": self.img_url,
            # "subtitle": self.subtitle,
        }   
# WTForm for creating a blog post
app.secret_key = "panda"

class AddForm(FlaskForm):
    blog_title = StringField(label='Blog Title', validators=[DataRequired()])
    blog_subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    blog_author = StringField(label='Author', validators=[DataRequired()])
    blog_img = StringField(label='Image URL', validators=[DataRequired()])
    blog_body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit") 



class RegisterForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    name = StringField(label='name', validators=[DataRequired()])
    # blog_img = StringField(label='Image URL', validators=[DataRequired()])
    # blog_body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")




class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

