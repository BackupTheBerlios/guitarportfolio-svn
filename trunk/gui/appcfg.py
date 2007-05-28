import os.path
import wx

APP_TITLE           = "Guitar Portfolio"
APP_VERSION         = "1.0"
DBNAME              = 'guitarportfolio.db'

CFG_APPNAME         = 'GuitarPortfolio'
CFG_VENDORNAME      = 'ImpossibleSoft'
CFG_DBPATH          = 'DbPath'                      # path to database + filename
CFG_PROGRESS        = 'filter/status'               # progress filter index
CFG_DIFFICULTY      = 'filter/difficulty'           # difficulty index
CFG_CATEGORIESAND   = 'filter/categoriesand'        # checkbox AND all categories
CFG_LOWERDIFFICULTY = 'filter/matchlowerdiff'       # checkbox also match lower difficulties
CFG_LASTRELPATH     = 'songs/last_relative_path'    # last path that was used for relative directory
CFG_ABSWORKPATH     = 'songs/absworkpath'           # absolute work path for relative paths
CFG_LAYOUT_DEFAULT  = 'window/default_layout'       # default layout upon saving (saved one time only)
CFG_LAYOUT_LAST     = 'window/last_layout'          # last layout when closing window
CFG_LAYOUT_LAST_H   = 'window/last_height'          # last height when closing window
CFG_LAYOUT_LAST_W   = 'window/last_width'           # last width when closing window

# defaults
DEF_RELPATH         = '{artist}\{title}'            # default path mask to take when no relpath exists

# replace some illegal char sequences in a file with more
# friendly characters (it can happen in a title name)
_file_illegal_chars = [ ('?',  '' ),
                        ('*',  '_'),
                        ('|',  '_'),
                        (',',  ' '),
                        (':',  '' ),
                        ('\t', '' ),
                        ('\n', '' ),
                        ('\r', '' ),
                        ('<',  '('),
                        ('>',  ')'),
                        ("'",  '' ),
                        ('"',  '' ) ]

# app CFG
__cfg = None

def Get():
    global __cfg
    if not __cfg:
        if 'wxGTK' in wx.PlatformInfo:
            # force a file config, because our local config dir is similar to the 
            # app name and the default is not the registry like Windows
            __cfg = wx.FileConfig(CFG_APPNAME, CFG_VENDORNAME, localFilename = '.guitarportfolio_cfg')
        else:
            __cfg = wx.Config()
            __cfg.AppName = CFG_APPNAME
            __cfg.VendorName = CFG_VENDORNAME
        
    return __cfg

# helper functions

# ------------------------------------------------------------------------------
def GetWorkSubDir(workdir, artist, title):
    """ Substitutes the given tags to create a dir that can be part of the
        work dir for a link. """
    result = workdir.replace('{artist}', artist)
    result = result.replace('{title}', title)    
    # replace odd characters
    for odd_char, rep_char in _file_illegal_chars:
        result = result.replace(odd_char, rep_char)
    return result

# ------------------------------------------------------------------------------
def GetAbsWorkPath(workmask = None, artist = None, title = None):
    """ Gets the work path from the settings, prepares it and if needed
        appends the workmask as a path to it """
    path = Get().Read(CFG_ABSWORKPATH, '')
    if artist and workmask and title:
        relpath = GetWorkSubDir(workmask, artist, title)
        if relpath:
            if not os.path.isabs(relpath):
                path = os.path.join(path, relpath)
            else:
                path = relpath
    return path
         
# ------------------------------------------------------------------------------
def GetAbsWorkPathFromSong(song):
    """ Convenience method to get work path from song """
    return GetAbsWorkPath(song.getRelativePath(), song.getArtist(), song.getTitle())
