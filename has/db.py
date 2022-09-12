import pymysql

# db

class connect_database:
    def __init__( self ):
        self.connect   = pymysql.connect( 
            host     = 'localhost', 
            user     = 'has', 
            password = 'elwlxjfqhdks!!', 
            db       = 'h4s_db',
            charset  = 'utf8mb4' )
        
        self.cur       = self.connect.cursor()
        self.query     = ""


    def db_inputdata( self ):
        self.cur.execute( self.query )
        self.connect.commit()


    def db_close( self ):
        self.cur.close()
        self.connect.close()


    def get_data( self, argv ):
        dataTuple = argv
        dataList  = []
        
        for data in dataTuple:
            dataList.append( str( data )[ 2:-3 ] )   # ex) tuple: ('test',), ('test2',)

        return dataList


    def db_userid( self ):
        self.__init__()

        # ----- GET users_id query -----
        self.query = "SELECT tblusers.users_id FROM tblusers"
        # ------------------------------

        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------

        return self.get_data( self.cur.fetchall() )


    def db_userpw( self ):
        self.__init__()

        # ----- GET users_pw query -----
        self.query = "SELECT tblusers.users_pw FROM tblusers"
        # ------------------------------

        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------

        return self.get_data( self.cur.fetchall() )


    def db_input_users( self, id, pw ):
        self.__init__()

        # ----- users query 1 -----
        self.query = "INSERT INTO tblusers( users_id, users_pw ) VALUES ( '" + str( id ) + "', '" + str( pw ) + "' )"
        # -------------------------

        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------

    
    def db_input_contents( self, con, urlink ):
        self.__init__()

        # ----- contents query 1 -----
        self.query = "INSERT INTO tblcontents( payloads ) VALUES ( '" + str( con )[ 2:-3 ] + "' )"
        # ----------------------------

        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------


        self.__init__()

        # ----- contents query 2 -----
        self.query = "INSERT INTO tblcontents( urlink ) VALUES( '" + str( urlink )+"' )"
        # ----------------------------

        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------


    def db_get_payloads( self ):
        self.__init__()

        # ----- GET payloads query -----
        self.query = "SELECT tblcontents.payloads FROM tblcontents"
        # ------------------------------

        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------

        return self.get_data( self.cur.fetchall() )


    def db_get_urls( self ):
        self.__init__()

        # ----- GET url query -----
        self.query = "SELECT tblcontents.urlink FROM tblcontents"
        # -------------------------
        
        # ----- DB  -----
        self.db_inputdata()
        self.db_close()
        # ---------------

        return self.get_data( self.cur.fetchall() )


