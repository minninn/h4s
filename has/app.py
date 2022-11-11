from flask import session, render_template, request, redirect, url_for, flash, send_file
from flask import Flask
from flask_wtf.csrf import CSRFProtect
import config
from final import *
from functools import wraps
from pdf import *
import db
import time
import path
import smtplib
from email import policy
from email.mime.text import MIMEText
from email.header import Header
import base64
import dsalt



# _init__.py

headers = {
    #"User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15, 'Allow':'POST', 'GET'"  # Mac OS, Safari
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"      # Windows OS, Chrome
    }

path_dir = path.user_path()

def decrypt( data ):
    return base64.b64decode( data ).decode( 'utf-8' ).replace( dsalt.dsalt(), "" )

def login_required(f):
    @ wraps(f)
    def deco_func(*args, **kwargs):
        if session.get("userid") is None:
            return redirect(url_for("login", next_url=request.url))
        return f(*args, **kwargs)
    return deco_func


def return_filename():
    finish = datetime.datetime.now()
    today = finish.strftime("%Y%m%d")
    filename = str(today) + ".pdf"

    return filename

def decorater(f):
    def wrapper():
        start = time.time()
        f()
        end   = time.time()
        print( "수행시간 {0:f}초".format( end - start ) )
    return wrapper()

def bdecode( data ):
    return base64.b64decode( data ).decode( 'utf-8' )


connect_database = db.connect_database()

app = Flask(__name__, template_folder='templates', static_folder='./static')

app.config.from_object(config)
app.config['SECRET_KEY'] = "SECRET"
app.config["WTF_CSRF_ENABLED"] = False

csrf = CSRFProtect()
csrf.init_app(app)

# main.py


@ app.route('/', methods=['GET', 'POST'])
def index():
    tags = [ tag[:-4] for tag in path_dir.get_files() ]
    ToFrontData = { "tags":tags }

    print( ToFrontData[ "tags" ] )
    return render_template( 'index.html' )

@ app.route( '/loading' )
def load_page():
    return render_template( 'test.html' )


@ app.route('/register', methods=['GET', 'POST'])
def register():
    time.sleep(0.5)
    if request.method == 'GET':
        return render_template('register.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        userId = connect_database.db_userid()

        if not (userid and password and re_password):
            return redirect('/register')
        elif password != re_password:
            return redirect('/register')
        else:
            for i in userId:
                if userid == decrypt( i ):
                    return redirect('/register')

            connect_database.db_input_users( userid, password )
            return redirect('/login') # 회의 필요 ( 회원가입 후 돌아갈 화면 )


@ app.route('/login', methods=['GET', 'POST'])
def login():
    time.sleep(0.5)
    if request.method == 'GET':
        return render_template('login.html')

    else:
        userid = request.form['userid']  # post : get userid
        password = request.form['password']  # post : get userpw
        userId = connect_database.db_userid()
        userPw = connect_database.db_userpw()

        chk_id = 0
        chk_pw = 0

        for i in userId:
            if userid == decrypt( i ):  # check userid == userId(list)
                chk_id = 1

        for i in userPw:  # check userpw == userPw(list)
            if password == decrypt( i ):
                chk_pw = 1

        if chk_id == 1 and chk_pw == 1:  # login OK
            session['userid'] = userid
            return redirect('/')
        else:  # login FAILURE
            flash('Try Again')
            return redirect('/login')


@ app.route('/logout', methods=['GET', 'POST'])
def logout():
    time.sleep(0.5)
    session.pop('userid', None)
    return redirect('/')


#@ decorater
@ login_required
@ app.route('/result', methods=['GET', 'POST'])
def result():
    time.sleep(0.5)
    if request.method == 'GET':
        return render_template('index.html')

    else:
        if session.get("userid"):
            urlink = request.form.get('urlink')
            start = time.time()
            try:
                scan_data = scan_xss(urlink)
            except:
                flash('Please enter a valid URL')
                return render_template('index.html')
            end = time.time()
            print( "수행시간 {0:f}초".format( end - start ) )

            link = scan_data[0]
            con = scan_data[1:]
            print( "con: {0}".format( con ) )
            connect_database.db_input_contents( con, urlink )
            return render_template('result.html', data=link)
        else:
            flash("Please LOGIN !")
            return render_template('login.html')


@ app.route('/result_pdf', methods=['GET', 'POST'])
def pdf():
    
    time.sleep(0.5)
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body()
    pdf.output(pdf.filename, 'F')
    filename = return_filename()

    path = path_dir.get_path() + "/" + filename
    return send_file( path, as_attachment=True )
    #return send_file(path, attachment_filename=filename, as_attachment=True)  # 수정필요
    #return send_file( path )

    '''except:
        print('close ERROR')
        #connect_database.db_close()   # drop
        return redirect('/result_pdf')'''

'''
@ app.route('/faq', methods=['GET', 'POST'])
def faq():
    time.sleep(0.5)
    return render_template('faq.html')'''

@ app.route('/team', methods=['GET', 'POST'])
def team():
    time.sleep(0.5)
    return render_template('team.html')

@ app.route( '/faq', methods = [ 'GET', 'POST' ] )                 # email send 구현
def faq():
    if request.method == 'GET':
        print( "get method, return faq.html" )
        return render_template( 'faq.html' )
    
    else:
        userName  = request.POST.get( 'name' )
        userEmail = request.POST.get( 'email' )
        subject   = request.POST.get( 'subject' )
        message   = request.POST.get( 'message' )                     # get post data
        print( userName, userEmail, subject, message )
'''
        sMail = smtplib.SMTP( 'smtp.gmail.com', 587 )              # use gmail.com
        sMail.starttls()                                           # use tls
        sMail.login( 'h4semail@gmail.com', 'ykbrkvpkzflueejm' )    # h4s mail, 앱 인증 비밀번호

        msg = MIMEText( message )                                  # 본문
        msg[ 'Subject' ] = userName + subject                      # 메일 제목 ( 사용자이름 + 제목 )

        sMail.sendmail( userEmail, "rn2685rn@gmail.com",  msg.as_string() )    # 이메일 전송 ( 김근택 계정에서 수신 )
        sMail.quit()
        print( "done" )'''

@ app.route( '/faq2', methods = [ 'GET', 'POST' ] )                 # email send 구현
def faq2():
    if request.method == 'GET':  
        return render_template( 'faq2.html' )
    
    else:
        userName  = request.form.get( 'name' )
        userEmail = request.form.get( 'email' )
        subject   = request.form.get( 'subject' )
        message   = request.form.get( 'message' )                     # get post data

        smtpInfo = config.smtp_info()

        sMail = smtplib.SMTP( 'smtp.gmail.com', 587 )              # use gmail.com
        sMail.starttls()                                           # use tls
        sMail.login( bdecode( smtpInfo['id'] ), bdecode( smtpInfo['pw'] ) )    # h4s email

        # -*- coding: utf-8 -*-
        msg = MIMEText( "username: {0}, useremail: {1}\n\n{2}".format( userName, userEmail, message ).encode( 'utf-8' ), _charset = 'UTF-8' )                                 # 본문
        msg[ 'Subject' ] = subject         # 메일 제목 ( 사용자이름 + 제목 )

        sMail.sendmail( userEmail, smtpInfo['email'] ,  msg.as_string() )    # 이메일 전송 ( 김근택 계정에서 수신 )
        sMail.quit()

        return redirect( '/faq2' )


if __name__ == '__main__':

    app.run(debug=False, host='192.168.0.2', port='8088')
