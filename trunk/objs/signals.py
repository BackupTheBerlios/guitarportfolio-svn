"""
    This module contains all signal constants for communicating
    with pydispatcher.
"""

APP_READY              = ('app', 'ready')                   # app is ready
APP_CLEAR              = ('app', 'clear')                   # request a clear

SONG_DB_ADDED          = ('song', 'db', 'added')
SONG_DB_INSERTED       = ('song', 'db', 'added', 'inserted')
SONG_DB_RESTORED       = ('song', 'db', 'added', 'restored')
SONG_DB_UPDATED        = ('song', 'db', 'updated')
SONG_DB_DELETED        = ('song', 'db', 'deleted')
SONG_DB_CAT_UPDATED    = ('song', 'db', 'categories', 'updated')

# emitted when the relation table is synced in the DB
SONG_DB_TAB_ADDED      = ('song', 'db', 'tab', 'added')
SONG_DB_TAB_DELETED    = ('song', 'db', 'tab', 'deleted')

TAB_DB_ADDED           = ('tab', 'db', 'added')             # tab added 
TAB_DB_INSERTED        = ('tab', 'db', 'added', 'insert')   # tab inserted in db
TAB_DB_RESTORED        = ('tab', 'db', 'added', 'restore')  # tab restored from DB
TAB_DB_UPDATED         = ('tab', 'db', 'updated')           # tab updated in db
TAB_DB_DELETED         = ('tab', 'db', 'deleted')           # tab deleted from db

CATEGORY_ADDED         = ('category', 'added')


SONG_VIEW_SELECTED     = ('song', 'view', 'selected')       # song selected 
SONG_VIEW_TAB_ADDED    = ('song', 'tab', 'added')           # tab added to selected song
SONG_VIEW_AFTER_SELECT = ('song', 'view', 'after', 'select')
SONG_VIEW_PRESELECT    = ('song', 'view', 'pre', 'select')

LINKMGR_CLEAR          = ('linkmgr', 'clear')               # links cleared
LINKMGR_POPULATED      = ('linkmgr', 'links', 'populated')  # populated the links
LINKMGR_QUERY_EDIT     = ('linkmgr', 'edit')

# TODO: Not certain if this will work, if a query is sent after a remove from
# the view, and that song is also removed after the re-evaluating, it will come
# in some kind of select after select query. Maybe the select query needs to be
# sent AFTER all songs in the list are evaluated, and if the selected song is 
# no longer there, then re-issue a select or send a select = none when the 
# view list is empty 
SONG_VIEW_QUERY        = ('song', 'view', 'query')          # query for select a song

SONG_QUERY_ADD         = ('song', 'query', 'add')           # query to add a song
SONG_QUERY_DELETE      = ('song', 'query', 'delete')        # query to delete selected song
SONG_QUERY_MODIFY      = ('song', 'query', 'modify')        # query to modify selected song

CFG_UPDATED            = ('config', 'updated')              # configuration changed
