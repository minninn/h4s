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
    filepath     = 'payload/{0}.txt'.format( "a" )        # payloads path ( Default: '' ): tags

    payloadsInfo = { 'filename':filename, 'filepath':filepath }
    return payloadsInfo[ userInput ]

# SMTP
def smtp_info():
    connect_database = db.connect_database()
    adminEmail = 'rn2685rn@gmail.com' # get faq message
    account    = connect_database.smtp_account()[0]
    password   = connect_database.smtp_password()[0]

    return { 'email':adminEmail, 'id':account, 'pw':password }