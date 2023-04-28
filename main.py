from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime  ## date.strftime('%B %d,%Y')
from flask_session import Session
from email.message import EmailMessage
import ssl
import smtplib
import json


app = Flask(__name__)
app.secret_key = "somthing"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
DB_NAME = 'database.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)

#--------------------------DATABASE----------------------------------------#

class Article(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100))
    numberviews = db.Column(db.Integer)
    numberlikes = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    category = db.Column(db.String(15))
    description = db.Column(db.Text)
    content = db.Column(db.Text)

class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    message = db.Column(db.Text)


#-----------------------INDEX------------------------------------#
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form.get("email")
        message =request.form.get("message")
        mail = Mail(email=email, message=message)
        db.session.add(mail)
        db.session.commit()
        email_sender = 'oussamabouzalim942@gmail.com'
        email_password = 'itpkgsubxjihedpx'
        email_receiver = email
        subject = 'test email.'
        body = """ this is a test email."""
        em = EmailMessage()
        em['From'], em['To'], em['Subject'] = email_sender, email_receiver, subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
    if not "LIKED_ARTICLES" in session:
        session["LIKED_ARTICLES"] = []    
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('index.html',articles=articles, LIKED_ARTICLES = session['LIKED_ARTICLES'])

@app.route('/likes/<string:data>', methods=['POST'])
def likes(data):
    data = json.loads(data)
    id =int(data['id'])
    like = data['liked']
    article = db.get_or_404(Article, id )
    if like : 
        article.numberlikes += 1 
        session["LIKED_ARTICLES"].append(id)
    else:
        article.numberlikes -= 1
        if id in session["LIKED_ARTICLES"]:
            session["LIKED_ARTICLES"].remove(id)
    db.session.commit()
    return f"{article.date.strftime('%B %d %Y')} . {article.numberviews} views . {article.numberlikes} likes"

@app.route('/views/<string:data>', methods=['POST'])
def views(data):
    data = json.loads(data)
    id =int(data['id'])
    article = db.get_or_404(Article, id )
    article.numberviews += 1 
    db.session.commit()
    return f"{article.date.strftime('%B %d %Y')} . {article.numberviews} views . {article.numberlikes} likes"
     

#-----------------------ARTICLE------------------------------------------#

@app.route('/article/<article_id>')
def article(article_id):
    article = Article.query.filter_by(id=article_id).one()
    return render_template('article.html',article=article)


#----------------------ADMIN---------------------------------------#


@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'oussama' and password == '123':
            return redirect(url_for('addpost', logged='44576345451167'))           
    return render_template('admin.html')

@app.route('/addpost/<string:logged>', methods=['GET','POST'])
def addpost(logged):
    if logged == '44576345451167' :
        if request.method == 'POST':
            title = request.form['title']
            category = request.form['category']
            description = request.form['description']
            content = request.form['content']
            article = Article(title=title, numberviews=0, numberlikes=0, date= datetime.datetime.now(), category=category, description=description, content=content)
            db.session.add(article)
            db.session.commit()
        articles = Article.query.order_by(Article.date.desc()).all()
        messages = Mail.query.order_by(Mail.id.desc()).all()
        return render_template('addpost.html',articles=articles, messages=messages)
    return redirect(url_for('admin'))  

@app.route('/delete/<string:data>', methods=['POST'])
def delete(data):
    data = json.loads(data)
    id =int(data['id'])
    type = data['type']
    if type == "article" : 
        article = db.get_or_404(Article, id )
        db.session.delete(article)
    else:
        message = db.get_or_404(Mail, id)
        db.session.delete(message)
    db.session.commit()
    return 

#---------------------------RUN_APP-----------------------------------------------------#

if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   app.run(debug = True)