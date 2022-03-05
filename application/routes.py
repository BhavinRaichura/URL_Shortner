from flask import Flask,render_template,redirect, request, session, url_for
from application import app, db
from hashids import Hashids
from application.models import User, ShortUrls
from application.forms import LoginForm, RegisterForm


hashids = Hashids(
    salt="as$$Gnz5H1H2bWvBbMnZ5A^XCcD&K$xz#@3205V@4#98yt4q23wqo!ADei",
    min_length=7,
    alphabet="1234567890zxcvbnmASDFGHJKLPOIUYqwterQWERMZX"
    )



def encoding(num):
    url_id = hashids.encode(num)
    return url_id


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    if session:
        if request.method == "post":
            original_url = request.form['original_url']
    
    return "hello world"

@app.route('/signup')
def signup():
    return "signup"


@app.route('/user/<string:username>')
def user_portal(username=None):
    if session:
        list_urls=db.shorturls.find({'user_id':session[user_id]})
        return render_template('user.html',list_urls=list_urls,username =username,shortedurl=None)
    return redirect(url_for('home'))

@app.route('/create',methods=['POST','GET'])
def create():
    if session:
        if request.method=='post':
            original_url = request.form['original_url']
            # need count of id_num
            id_num+=1
            url_id =encoding(id_num)
            user_id = session['user_id']
            db.shorturls.insert_one({'user_id':user_id,'url_id':url_id,'original_url':original_url})
            return redirect(url_for('user_portal'))
    return redirect(url_for('home'))


@app.route('/<string:encoded_id>')
def decoder(encoded_id):
    id_list = list(hashids.decode(encoded_id))
    if id_list ==():
        return "<h1>Invailid url</h1>"
    url_id= id_list[0]
    url_data = db.shorturls.find_one({'url_id':url_id})
    return redirect(url_data['original_url'])


@app.route('/Login',methods=['POST','GET'])
def login():
    if request.method == 'post':
        email = request.form['email']
        password = request.form['password']
        db_user_info = db.user.find_one({'email':email})
        if db_user_info != None and email == db_user_info['email'] and password == db_user_info['password']:
            session['user_id']=db_user_info['user_id']
            return redirect(url_for('user_portal',username=db_user_info['name']))
    form = LoginForm()
    return render_template('login.html',form = form)


@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('home'))