from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
import smtplib
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date, datetime
import bleach
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import AddForm, RegisterForm, LoginForm
from dotenv import load_dotenv
import os
from flask_migrate import Migrate


load_dotenv() 

# Define allowed tags and attributes
allowed_tags = ['b', 'i', 'u', 'em', 'strong']
allowed_attributes = {}

# Example of sanitizing user input
user_input = '<script>alert("XSS")</script><b>Bold text</b>'
clean_input = bleach.clean(user_input, tags=allowed_tags, attributes=allowed_attributes)


print(clean_input)


email = "pywork69@gmail.com"
key = "iuuwhrajukmcezdi"


print(os.environ.get('POSTGRES'))

app = Flask(__name__)

end_pt = "https://api.npoint.io/c790b4d5cab58020d391"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:eZCj1c5NduwY@ep-flat-lab-a4qrz9nf-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

ckeditor = CKEditor()
ckeditor.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Blog(db.Model):
    __tablename__='blog'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(250), unique=True, nullable=False)
    date = db.Column(String(500), nullable=False)
    body = db.Column(String(250), nullable=False)
    author = db.Column(String(250), nullable=False)
    img_url = db.Column(String(500), nullable=False)
    subtitle = db.Column(String(500), nullable=False)

    def __init__(self,title,date,body, author, img_url, subtitle):
        self.title=title
        self.date=date
        self.body=body
        self.author=author
        self.img_url=img_url
        self.subtitle=subtitle

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "body": self.body,
            "author": self.author,
            "img_url": self.img_url,
            "subtitle": self.subtitle,
        }   
    


class User(db.Model, UserMixin):
    __tablename__='register'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.VARCHAR(69))
    password=db.Column(db.VARCHAR(69))
    name=db.Column(db.VARCHAR(69))

    def __init__(self, email, password, name):
        self.email=email
        self.password=password
        self.name=name


    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "name": self.name
        }    
    
class AddForm(FlaskForm):
    blog_title = StringField(label='Blog Title', validators=[DataRequired()])
    blog_subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    blog_author = StringField(label='Author', validators=[DataRequired()])
    blog_img = StringField(label='Image URL', validators=[DataRequired()])
    blog_body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit")    


bootstrap = Bootstrap5(app)

app.secret_key = "panda"

@app.route("/")
def home():
    result = db.session.execute(db.select(Blog).order_by(Blog.title))
    all_cafes = result.scalars().all()
    cafes=[blog.to_dict() for blog in all_cafes]
    return render_template("index.html", blog_posts=cafes)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()

        if user:
            flash("You've already signed up with that email, Log in exist!!")
            return redirect(url_for('login'))
        
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('password incorrect, please try again')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form, current_user=current_user)

@app.route("/blog/<int:num>")
def blog_post(num):
    
    result = db.session.execute(db.select(Blog).order_by(Blog.title))
    all_cafes = result.scalars().all()
    cafes=[blog.to_dict() for blog in all_cafes]
    # return render_template("index.html", blog_posts=cafes)
    return render_template("blogs.html", blog_posts = cafes, number = num)


@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/contact",  methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form["username"]
        passw = request.form["password"]
        message = request.form["message"]
        print(name)
        print(passw)
        print(message)
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=email, password=key)

        connection.sendmail(from_addr=email, to_addrs="parthibanpavendhan@gmail.com", msg=f"Subject:Contact Form \n\n Name:{name} \n Password:{passw} \n Message:{message}")
        connection.close()
        return render_template("contact.html")


    else:
       return render_template("contact.html")     


@app.route("/add_post", methods=['GET', 'POST'])
def make_post():
    data_form = AddForm()
    if data_form.validate_on_submit(): 

        now = datetime.now()

        current_date = now.date()
        title = data_form.blog_title.data
        subtitle = data_form.blog_subtitle.data  
        author = data_form.blog_author.data
        body = data_form.blog_body.data
        img = data_form.blog_img.data
        date = current_date

        std = Blog(title, date, body, author,  img, subtitle)
            # self,title,date,body, author, img_url, subtitle
        db.session.add(std)
        db.session.commit()

    return render_template("make-post.html", form=data_form)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Blog, post_id)
    print(post.id)

    edit_form = AddForm(
        blog_title=post.title,
        blog_subtitle=post.subtitle,
        blog_img=post.img_url,
        blog_author=post.author,
        blog_body=post.body,

        )
    
    # print(edit_form.title)
    

    if edit_form.validate_on_submit():
       post.title = edit_form.blog_title.data
       post.subtitle = edit_form.blog_subtitle.data
       post.img_url = edit_form.blog_img.data
       post.author = edit_form.blog_author.data
       post.body = edit_form.blog_body.data    
       db.session.commit()
       return redirect(url_for("blog_post", num=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(Blog, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True) 