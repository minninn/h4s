import os
import db

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = "SECRET"


# db
def db_info( userInput ):
    host     = 'localhost'          # db address
    user     = 'has'                # db username
    password = 'elwlxjfqhdks!!'     # db password
    db       = 'h4s_db'             # db name
    charset  = 'utf8mb4'            # db character set

    dbInfo   = { 'host':host, 'user':user, 'password':password, 'db':db, 'charset':charset }
    return dbInfo[ userInput ]

# payloads
def payloads_info( userInput ):
    filename     = 'payload.txt'    # payloads filename ( in has directory ), non-used
    filepath     = []       # payloads path ( Default: '' ): tags
    ospath       = os.getcwd() + r"/payload/"
    FileList     = os.listdir( os.getcwd() + r"/payload/" )
    for file in FileList:
        filepath.append( ospath + file )
    
    filepath = [ ospath + "a.txt" ]

    payloadsInfo = { 'filename':filename, 'filepath':sorted( filepath ), 'files':sorted( FileList ) }
    return payloadsInfo[ userInput ]

# SMTP
def smtp_info():
    connect_database = db.connect_database()
    adminEmail = 'rn2685rn@gmail.com' # get faq message
    account    = connect_database.smtp_account()[0]
    password   = connect_database.smtp_password()[0]

    return { 'email':adminEmail, 'id':account, 'pw':password }