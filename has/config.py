import os

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
    filename     = 'payload.txt'    # payloads filename ( in has directory )
    filepath     = ''               # payloads path ( Default: '' )

    payloadsInfo = { 'filename':filename, 'filepath':filepath}
    return payloadsInfo[ userInput ]