import os

class user_path:
    def __init__( self ):
        self.dirPath  = ''
        self.fileName = ''
        self.fname    = ''     # payloads path. (Default = '')

    def get_path( self ):
        self.dirPath = os.getcwd()
        return self.dirPath

    def get_filename( self ):
        self.fileName = os.listdir( os.getcwd() )
        return self.fileName

    def payload_path( self ):
        self.fname = "{0}/payload.txt".format( self.get_path() ) if self.fname == "" else self.fname
        return self.fname