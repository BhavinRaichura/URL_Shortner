from flask import Flask,render_template,redirect, request, session, url_for
from application import app, db
#from application.models import User, ShortUrls
from hashids import Hashids
from application.forms import LoginForm, RegisterForm
from flask_mail import Mail, Message

app.config['SECRET_KEY'] = 'as$$Gnz5H1H2bWvBbMnZ5A^XCcDsakjd54641254645449$^*efkjlksdmn&K$xz#@3205V@4#98yt4q23wqo!ADei'

hashids = Hashids(
    salt="as$$Gnz5H1H2bWvBbMnZ5A^XCcD&K$xz#@3205V@4#98yt4q23wqo!ADei",
    min_length=7,
    alphabet="1234567890zxcvbnmASDFGHJKLPOIUYqwterQWERMZX"
    )



@app.route('/encoding/<int:num>')
def encoding(num):
    url_id = hashids.encode(num)
    return url_id

def decoding(code):
    return list(hashids.decode(code))[0]


@app.route('/home/<string:msg>')
@app.route('/home')
@app.route('/index')
@app.route('/')
def home(msg=""):
    
    return render_template('index.html',msg=msg)


@app.route('/signup',methods=['POST','GET'])
def signup():
    reg_form = RegisterForm()
    login_form = LoginForm()
    if session['username']!=False:
        return redirect(url_for('home',msg='already login'))
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        print(username)
        check_user_excitance = db.user.find_one({'email':email})
        if check_user_excitance == None:
            count_user=int(db.command("collstats", "user")['count'])+1
            print(count_user)
            db.user.insert_one({'username':username,'email':email,'password':password,'id':count_user,'total_urls':0})
            session['user_id']=count_user
            session['username']=username
            #return redirect(url_for('user_portal',username=username))
            return redirect(url_for('home',msg='account successfully created'))
        return redirect(url_for('home',msg='already have account'))
    return render_template('login.html',reg_form=reg_form,login_form =login_form)


@app.route('/user/<string:username>')
def user_portal(username=None):
    if session['username'] != False:
        obj_urls=db.shorturls.find({'user_id':session['user_id']})
        list_urls =[]
        for i in obj_urls:
            list_urls.append(i)
        return render_template('user.html',list_urls=list_urls,username =username,shortedurl=None)
    return redirect(url_for('home'))



@app.route('/create',methods=['POST','GET'])
def create():
    if session['username'] != False:
        print(session)
        print(request.method)
        if request.method=='POST':
            original_url = request.form['original_url']
            print(original_url)
            count_urls =9900000+int(db.command("collstats", "shortedurl")['count']) +1
            user_id = session['user_id']
            db.shortedurl.insert_one({'user_id':user_id,'url_id':count_urls,'original_url':original_url})
            username=session.get('username')
            new_short_url = 'http://127.0.0.2:50002/u/' + encoding(count_urls)
            print(new_short_url)
            return render_template('index.html',msg=new_short_url)
            #return redirect(url_for('user_portal',username=username))
    return redirect(url_for('home',msg="Please login first"))



@app.route('/login',methods=['POST','GET'])
def login():
    print("r")
    login_form = LoginForm()
    reg_form = RegisterForm()
    print(session)
    if session['username']!=False:
        return redirect(url_for('home',msg='already login'))
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        print("h")
        print(email)
        db_user_info = db.user.find_one({'email':email})
        print(db_user_info)
        if db_user_info is not None and email == db_user_info['email'] and password == db_user_info['password']:
            session['user_id']=db_user_info['id']
            session['username']=db_user_info['username']
            print("session")
            return redirect(url_for('home',msg='successfully login'))
            #return redirect(url_for('user_portal',username=session.get('username')))
    return render_template('login.html',reg_form=reg_form,login_form =login_form)



@app.route('/logout')
def logout():
    session['username']=False
    session.pop('user_id',None)
    return redirect(url_for('home',msg='logout'))


@app.route('/u/<string:encoded_id>')
def decoder(encoded_id):
    id_list = list(hashids.decode(encoded_id))
    print(id_list)
    if id_list ==[]:
        return "<h1>Invailid url</h1>"
    url_id= int(id_list[0])
    url_data = db.shortedurl.find_one({'url_id':url_id})
    print(url_id)
    print(url_data)
    return redirect(url_data['original_url'])


# flask run --host=127.0.0.2  --port=50002