from flask import Flask, render_template, request, redirect, url_for
import pyrebase
from datetime import datetime

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyDqbOPqc7dCn57_--KYI_Jl96iFpXn5Ix4",
    "authDomain": "codeakc-9cd9c.firebaseapp.com",
    "databaseURL": "https://codeakc-9cd9c.firebaseio.com",
    "projectId": "codeakc-9cd9c",
    "storageBucket": "codeakc-9cd9c.appspot.com",
    "messagingSenderId": "169742393497",
    "appId": "1:169742393497:web:8bbde1e4fcb3e6b6625808",
    "measurementId": "G-1GS5YZZ3ZJ"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/w5.html', methods=['GET', 'POST'])
def Main():
    return render_template('w5.html')


@app.route('/', methods=['GET', 'POST'])
def Main1():
    return render_template('w5.html')


@app.route('/signup.html', methods=['GET', 'POST'])
def datavalidation():
    btn1 = ""
    btn2 = ""
    btn3 = ""
    btn4 = ""
    signup = ""
    txt = ""
    if request.method == 'POST' or 'GET' and 'sign' in request.form:
        btn1 = request.form.get('nam')
        btn2 = request.form.get('em')
        btn3 = request.form.get('pass1')
        btn4 = request.form.get('pass2')
        signup = request.form.get('sign')
        if btn3 == btn4:
            try:
                auth.create_user_with_email_and_password(btn2, btn3)
                txt = "Your id is successfully created"
            except:
                txt = "either password is weak or email already exists"
        else:
            txt = "password didnt match"

    return render_template('signup.html', nam=btn1, em=btn2, pass1=btn3, pass2=btn4, txt=txt, sign=signup)


@app.route('/write.html', methods=['GET', 'POST'])
def write():
    namea = ""
    title = ""
    article = ""
    publish = ""
    if request.method == 'POST' or 'GET' and 'pub' in request.form:
        namea = request.form.get('aurthor')
        title = request.form.get('title')
        article = request.form.get('article')
        publish = request.form.get('pub')
        date = date = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
        data = {"name": namea, "title": title, "article": article, "date": date}
        db.child('codefreaks').push(data)
    return render_template('write.html', aurthor=namea, title=title, article=article, pub=publish)


@app.route('/login.html', methods=['GET', 'POST'])
def log():
    lbtn1 = ""
    lbtn2 = ""
    lbtn3 = ""
    lbtn4 = ""
    txt2 = ""
    if request.method == 'POST' or 'GET' and 'llogin' in request.form:
        lbtn1 = request.form.get('lem')
        lbtn2 = request.form.get('lpass')
        lbtn3 = request.form.get('llogin')
        lbtn4 = request.form.get('lforget')
        try:
            login = auth.sign_in_with_email_and_password(lbtn1, lbtn2)
            txt2 = "login successfull"
            return redirect(url_for('write'))
        except:
            txt2 = "invalid email or password"
    return render_template('login.html', llogin=lbtn3, lem=lbtn1, txt2=txt2, lpass=lbtn2, lforget=lbtn4)


@app.route('/forgot.html', methods=['GET', 'POST'])
def forgot():
    lbtn1 = ""
    lbtn2 = ""
    lbtn3 = ""
    lbtn4 = ""
    txt2 = ""
    if request.method == 'POST' or 'GET' and 'lforget' in request.form:
        lbtn1 = request.form.get('lem')
        lbtn2 = request.form.get('lpass')
        lbtn3 = request.form.get('llogin')
        lbtn4 = request.form.get('lforget')
        try:
            forget = auth.send_password_reset_email(lbtn1)
            txt2 = "link has been sent to your email"
            redirect('write.html')
        except:
            txt2 = "email does not exist"
    return render_template('forgot.html', llogin=lbtn3, lem=lbtn1, txt2=txt2, lpass=lbtn2, lforget=lbtn4)


@app.route('/about.html', methods=['GET', 'POST'])
def abt():

    return render_template('about.html')


@app.route('/contact.html', methods=['GET', 'POST'])
def cont():
    return render_template('contact.html')


@app.route('/post.html/<string:id>', methods=['GET', 'POST'])
def post(id):
    u = db.child('codefreaks').child(id).get()

    name = u.val()['name']
    title = u.val()['title']
    article = u.val()['article']
    date = u.val()['date']
    return render_template('post.html', name=name, title=title, article=article, date=date)


@app.route('/blog.html', methods=['GET', 'POST'])
def blog():
    u = db.child('codefreaks').get()
    return render_template('blog.html', u=u)


app.run()
