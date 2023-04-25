from flask import Flask,render_template,flash,redirect,url_for,session, logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from flask_session import Session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import date



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/eray2/Desktop/iusmetaBlog/iusmeta.db"
db = SQLAlchemy(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    author_username = db.Column(db.String(80))
    content = db.Column(db.String(10000000))
    imageUrl = db.Column(db.String(80))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    author_username = db.Column(db.String(80))
    cv = db.Column(db.String(10000000))
    imageUrl = db.Column(db.String(80))
    
    

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    time = date.today()
    articles = Articles.query.all()
    articles.reverse()
    #articles = Articles.query.order_by(Articles.id.desc()).first()
    db.session.commit()
    return render_template("articles.html",articles = articles,time = time)

@app.route("/article/<string:id>")
def article(id):

    article = Articles.query.filter_by(id=id).first()
    
    return render_template("article.html",article = article)

@app.route("/author-page/<string:author_username>")
def author_page(author_username):
    author_page = User.query.filter_by(author_username=author_username).first() # Yazarı veritabanından sorgula
    if author_page:
        return render_template('author-page.html', author_page=author_page) # Yazarın sayfasını render_template ile döndür
    else:
        return "Yazar bulunamadı", 404 # Eğer yazar bulunamazsa 404 hatası döndür




with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


