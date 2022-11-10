import os
import config

class user_path:
    def __init__( self ):
        self.dirPath  = ''
        self.fileName = ''
        self.fname    = config.payloads_info( 'filepath' )
        self.tagfiles    = config.payloads_info( 'files' )

    def get_path( self ):
        self.dirPath = os.getcwd()
        return self.dirPath

    def get_filename( self ):
        self.fileName = os.listdir( os.getcwd() )
        return self.fileName

    def get_files( self ):
        return self.tagfiles

    def payload_path( self ):
        self.fname = "{0}/{1}".format( self.get_path(), config.payloads_info( 'filename' ) ) if self.fname == "" else self.fname
        return self.fname