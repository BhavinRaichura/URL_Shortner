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



@app.route('/user')
def user_portal():
    if session:
        list_urls=db.shorturls.find({'user_id':session[user_id]})
        return render_template('user.html',list_urls=list_urls,name =name)
    return redirect(url_for(home))


@app.route('/<string:encoded_id>')
def view(encoded_id):
    id_list = list(hashids.decode(encoded_id))
    if id_list ==():
        return "<h1>Invailid url</h1>"
    url_id= id_list[0]
    url_data = db.shorturls.find_one({'url_id':url_id})
    return redirect(url_data['original_url'])

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for(home))