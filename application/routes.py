from flask import Flask,render_template,redirect, request, session, url_for
from application import app, db
#from application.models import User, ShortUrls
from hashids import Hashids
from application.forms import LoginForm, RegisterForm

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
    list(hashids.decode(code))
    return 


@app.route('/home/<string:msg>')
@app.route('/home')
@app.route('/index')
@app.route('/')
def home(msg=""):
    s ="<h1>home</h1>" +msg
    return s


@app.route('/Signup',methods=['POST','GET'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        check_user_excitance = db.user.find_one({'email':email})
        if check_user_excitance == None:
            count_user+=1
            db.user.insert_one({'username':username,'email':email,'password':password,'id':count_user,'total_urls':0})
            session['user_id']=count_user
            session['username']=username
            return redirect(url_for('user_portal',username=username))
    return render_template('signup.html',form=form)




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
        if request.method=='post':
            original_url = request.form['original_url']
            count_urls +=1
            user_id = session['user_id']
            db.shorturls.insert_one({'user_id':user_id,'url_id':count_url,'original_url':original_url})
            username=session.get('username')
            return redirect(url_for('user_portal',username=username))
    return redirect(url_for('home'))




@app.route('/<string:encoded_id>')
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




@app.route('/login',methods=['POST','GET'])
def login():
    print("r")
    form = LoginForm()
    print(session)
    if session['username'] != False:
        return redirect(url_for('home',msg='already login'))
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
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
    return render_template('login.html',form = form)




@app.route('/logout')
def logout():
    session['username']=False
    session.pop('user_id',None)
    return redirect(url_for('home',msg='logout'))



# flask run --host=127.0.0.2  --port=50002