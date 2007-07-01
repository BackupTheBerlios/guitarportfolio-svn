import os.path
import wx

APP_TITLE           = "Guitar Portfolio"
APP_VERSION         = "1.0"
DBNAME              = 'guitarportfolio.db'

CFG_APPNAME         = 'GuitarPortfolio'
CFG_VENDORNAME      = 'ImpossibleSoft'
CFG_XRCFILE         = 'gui/guitarportfolio.xrc'

CFG_DBPATH          = 'DbPath'                      # path to database + filename
CFG_PROGRESS        = 'filter/status'               # progress filter index
CFG_DIFFICULTY      = 'filter/difficulty'           # difficulty index
CFG_CATEGORIESAND   = 'filter/categoriesand'        # checkbox AND all categories
CFG_LOWERDIFFICULTY = 'filter/matchlowerdiff'       # checkbox also match lower difficulties
CFG_SHOWONLYTUTS    = 'filter/onlyshowtuts'         # show only tutorials, songs or all
CFG_HIDE_CONCEPTS   = 'filter/hideconcepts'         # show concept songs or not (empty info, lyrics, tabs)
CFG_LASTRELPATH     = 'songs/last_relative_path'    # last path that was used for relative directory
CFG_ABSWORKPATH     = 'songs/absworkpath'           # absolute work path for relative paths
CFG_LAYOUT_DEFAULT  = 'window/default_layout'       # default layout upon saving (saved one time only)
CFG_LAYOUT_LAST     = 'window/last_layout'          # last layout when closing window
CFG_LAYOUT_LAST_H   = 'window/last_height'          # last height when closing window
CFG_LAYOUT_LAST_W   = 'window/last_width'           # last width when closing window
CFG_LINUX_EXEC_CMD  = 'os/linux/shellexec'          # exec command 
CFG_LOG_SELECTTIME  = 'log/selecttime'              # what time period was last selected
CFG_LOG_PROGRESS    = 'log/progress'                # should progress logs be displayed
CFG_LOG_STUDY       = 'log/studytime'               # should study time logs be displayed
CFG_LOG_STATUS      = 'log/status'                  # should status logs be displayed
CFG_LOG_COMMENT     = 'log/comment'                 # should comment logs be displayed
CFG_LOG_SORT        = 'log/sortorder'               # ascending / descending log order

# TODO: Needs better description!
description = "Guitar Portfolio is an application that manages the songs you are playing on the guitar. " + \
              "It will help you to keep track of the progress, times practiced and attachments belonging to the song.\n" 

site_url = ("http://guitarportfolio.berlios.de/", "Guitar Portfolio Project Page")

licensetext = """
Based upon GNU GENERAL PUBLIC LICENSE, Version 2, June 1991
For full text, please visit http://www.gnu.org/licenses/gpl.txt
"""

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


# placeholder to set images directory. Will be set by the application instance
imagesdir = ''

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
    # make proper path
    if "wxGTK" in wx.PlatformInfo:
        result = result.replace('\\', '/')
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
    return GetAbsWorkPath(song._relativePath, song._artist, song._title)
