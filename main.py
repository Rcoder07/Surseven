from datetime import date, datetime
from enum import unique
import os
from os import name
from types import FrameType
from flask import Flask, render_template,request,session,flash,redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import json
import urllib.request


app = Flask(__name__)
app.secret_key='super secret-key'

UPLOAD_FOLDER='C:\\Users\Rudra\\OneDrive\\Desktop\\SONG PROJECTS\\static\\videos'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


with open('config.json', 'r') as c:
    params= json.load(c) ["params"]
   
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/surseven website'   
db = SQLAlchemy(app)

class Videoscompany(db.Model):
    Slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12))
    video_file = db.Column(db.String(20), nullable=False)

class Videosuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    video_file = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12))
    

class Registerusers(db.Model):
    Slno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(2),nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12))

class Contacts(db.Model):
    Slno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    msg = db.Column(db.String(50),nullable=False)
    date = db.Column(db.String(12))

@app.route('/')
def homedahbord():
    return render_template('home.html',params=params)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
     posts=Videosuser.query.filter_by().all()
    return render_template('dashboard.html',params=params)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
     video=request.files['inputFile']
     title=request.form['title']
     filename=secure_filename(video.filename)

     video.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
     vid=Videosuser( video_file=filename,title=title,date=datetime.now()) 
     db.session.add(vid)
     db.session.commit()
     
     flash('File Uploaded Successfully. ' + title)
     return redirect('/create')


     
    return render_template('create_upload.html')    

    

@app.route('/videos',methods=['GET', 'POST'])
def videos():
    if request.method == 'GET':
     posts=Videosuser.query.filter_by().all()
      
    return render_template('videos.html',params=params,posts=posts)

@app.route('/videoplayer/<string:post_slug>', methods=['GET'])
def videos_route(post_slug):
    
    post=Videosuser.query.filter_by(title=post_slug).first()

    return render_template('videoplayer.html',params=params,post=post)



@app.route('/audios')
def audios():
    
    return render_template('audios.html',params=params)

@app.route('/audioplayer')
def audio_route():
    
    return render_template('audioplayer.html',params=params)    

@app.route('/profile')
def profile():
     
      return render_template('profile.html')

      


@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        user = Registerusers.query.filter_by(email = email).first()
        if user is not None and user.password:
            (user)
            return render_template('dashboard.html',params=params)
     
     return render_template('login.html')       

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
      return render_template('register.html')

    else:
        #get name,email,phone,password from html video_file
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        age=request.form.get('age')
        password=request.form.get('password')
        #entry with database
        register_entry = Registerusers(name=name,email=email,phone_num=phone,age=age,password=password,date=datetime.now())

        db.session.add(register_entry)
        db.session.commit()

        #create a session object
        session['name']=request.form.get('name')
        session['email']=request.form.get('email')
        session['phone']=request.form.get('phone')
        session['age']=request.form.get('age')
        session['password']=request.form.get('password')
       

        return render_template('profile.html')




@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if(request.method=="POST"):

      name = request.form.get('name')
      email = request.form.get('email')
      subject = request.form.get('subject')
      message  = request.form.get('message')

      entry = Contacts(name=name, email=email, subject=subject, msg=message, date=datetime.now())

      db.session.add(entry)
      db.session.commit()

    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('dashboard.html')




if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')    
