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



# _init__.py

headers = {
    #"User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"  # Mac OS, Safari
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"        # Windows OS, Chrome
    }

path_dir = path.user_path()


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
    time.sleep(0.5)
    def decorator():
        print( "done" )
        return render_template( 'test.html' )
    #return decorator()
    print( path_dir.get_path() )
    print( path_dir.get_filename() )

    return render_template( 'index.html' )


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
            flash("Please check the blank")
            return redirect('/register')
        elif password != re_password:
            flash("Check Password")
            return redirect('/register')
        else:
            for i in userId:
                if userid == i:
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
            if userid == i:  # check userid == userId(list)
                chk_id = 1

        for i in userPw:  # check userpw == userPw(list)
            if password == i:
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


@ login_required
@ app.route('/result', methods=['GET', 'POST'])
def result():
    time.sleep(0.5)
    if request.method == 'GET':
        return render_template('index.html')

    else:
        if session.get("userid"):
            urlink = request.form.get('urlink')
            try:
                scan_data = scan_xss(urlink)
            except:
                flash('Please enter a valid URL')
                return render_template('index.html')

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


@ app.route('/faq', methods=['GET', 'POST'])
def faq():
    time.sleep(0.5)
    return render_template('faq.html')

@ app.route('/team', methods=['GET', 'POST'])
def team():
    time.sleep(0.5)
    return render_template('team.html')
'''
@ app.route( '/faq', methods = [ 'GET', 'POST' ] )                 # email send 구현
def send_mail():
    if request.method == 'GET':
        print( "get method, return faq.html" )
        return render_template( 'faq.html' )
    
    else:
        userName  = request.form[ 'name' ]
        userEmail = request.form[ 'email' ]
        subject   = request.form[ 'subject' ]
        message   = request.form[ 'message' ]                      # get post data
        print( userName, userEmail, subject, message )

        sMail = smtplib.SMTP( 'smtp.gmail.com', 587 )              # use gmail.com
        sMail.starttls()                                           # use tls
        sMail.login( 'h4semail@gmail.com', 'ykbrkvpkzflueejm' )    # h4s mail, 앱 인증 비밀번호

        msg = MIMEText( message )                                  # 본문
        msg[ 'Subject' ] = userName + subject                      # 메일 제목 ( 사용자이름 + 제목 )

        sMail.sendmail( userEmail, "rn2685rn@gmail.com",  msg.as_string() )    # 이메일 전송 ( 김근택 계정에서 수신 )
        sMail.quit()
        print( "done" )'''



if __name__ == '__main__':

    app.run(debug=False, host='192.168.0.2', port='8088')
