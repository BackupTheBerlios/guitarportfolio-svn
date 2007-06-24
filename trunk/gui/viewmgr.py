
from wx.lib.pubsub import Publisher

import db, db.engine, db.songs_peer
from objs import category_mgr, tuning_mgr, songfilter, linkmgt

SIGNAL_CLEAR_DATA       = ('do', 'clear', 'data')   # transmits a clear data signal, all views must 
                                                    # initialize to their defaults
SIGNAL_DATA_RESTORED    = ('data', 'restored')      # issued when all trivial data in the db is restored
SIGNAL_SONG_SELECTED    = ('song', 'selected')      # transmits when a song is selected, and all 
                                                    # relations and dependencies are restored
SIGNAL_SONG_ADDED       = ('song', 'added')         # transmits a signal when a new song is added to 
                                                    # the database. This does not mean it is selected
SIGNAL_SONG_UPDATED     = ('song', 'updated')       # transmitted when the song is updated
SIGNAL_SONG_DELETED     = ('song', 'deleted')       # transmitted when a song is deleted, can be followed
                                                    # by a SIGNAL_SONG_SELECTED as well
SIGNAL_SETTINGS_CHANGED = ('settings', 'changed')   # someone changed the settings, we need to send this out
SIGNAL_LINKS_REFRESHED  = ('links', 'refreshed')    # transmitted when deliberately the attachments list
                                                    # needs to be refreshed.
SIGNAL_TAB_SELECTED     = ('tab', 'selected')       # transmitted when a tab is selected for viewing
SIGNAL_SET_HOMEPAGE     = ('do', 'set', 'homepage') # transmitted when the homepage needs to be set in 
                                                    # the song browser
SIGNAL_ADD_SONG         = ('do', 'song', 'add')     # transmitted when a song needs to be added
                                                    # a convenience callback function
SIGNAL_EDIT_SONG        = ('do', 'song', 'edit')    # sent when the selected song needs to be edited
SIGNAL_DELETE_SONG      = ('do', 'song', 'delete')  # sent when the selected song needs to be deleted
SIGNAL_EDIT_LINKS       = ('do', 'edit', 'links')   # send a command to edit the links 
SIGNAL_TAB_ADDED        = ('tab', 'added')          # a new tab is added to the database
SIGNAL_TAB_UPDATED      = ('tab', 'updated')        # send a command to update the tab
SIGNAL_TAB_DELETED      = ('tab', 'deleted')        # send around that we lost a tab 

songs = []

# ------------------------------------------------------------------------------
def signalDbChange():
    """ The database is changed, this means all the views must get rid of their referenced
        data, and all views must change to their default. After all data is restored, 
        the views get a go signal to repopulate everything """
    
    global songs
    
    # send None as argument, to allow SIGNAL_SONG_SELECTED handlers to be 
    # used to revert to a disabled viewstate
    Publisher().sendMessage(SIGNAL_CLEAR_DATA, None)
    
    # restore all relations that are static to the lifetime of the app
    # like categories, tunings etc.
    
    songfilter.Get().Reset()
    linkmgt.Get().Clear()

    # load categories and tunings
    dbc = db.engine.GetDb()
    category_mgr.RestoreFromDb(dbc)
    tuning_mgr.RestoreFromDb(dbc)
    
    # restore all songs
    songs = []
    sp = db.songs_peer.SongSetPeer(dbc)
    songs = sp.Restore()        
    
    # restore all song category relations
    sp = db.songs_peer.SongPeer(dbc)
    for s in songs:
        sp.RestoreCategories(s)     
     
    Publisher().sendMessage(SIGNAL_DATA_RESTORED)
        
# ------------------------------------------------------------------------------
def signalSetSong(song):
    """ A new song needs to be set as selected song. Every view is notified of this
        If the song to be set is 'None', all views should reset to their default views """
        
    # prune tab relations from the old song
    # this is to reduce the memory footprint
    old_song = songgilter.Get()._selectedSong
    if old_song:
        old_song.tabs.prune()
    
    # load the tabs for the new song
    if song:
        tlp = db.songs_peer.SongTabListPeer(db.engine.GetDb())
        tlp.Restore(song)        

    _DoReloadAttachments(song)
    
    songfilter.Get()._selectedSong = song
    Publisher().sendMessage(SIGNAL_SONG_SELECTED, song)
        
# ------------------------------------------------------------------------------
def signalSongAdded(song):
    """ A new song is added to the database. All views are informed to update their lists
        if this is needed """
    
    Publisher().sendMessage(SIGNAL_SONG_ADDED, song)

# ------------------------------------------------------------------------------
def signalAddSong():
    """ Send a signal when a new song needs to be added. This is a convenience function so 
        that the other GUI elements can callback to this, to get a song added """
    
    Publisher().sendMessage(SIGNAL_ADD_SONG)

# ------------------------------------------------------------------------------
def signalEditSong():
    """ Send a signal when our selected song needs to be edited. We also verify if this is 
        possible to edit """
    
    #  can we edit?
    song = songfilter.Get()._selectedSong
    if song:
        Publisher().sendMessage(SIGNAL_EDIT_SONG)

# ------------------------------------------------------------------------------
def signalSongUpdated(song):
    """ The song in question is updated. If the song is the selected song, we will also reload
        some stuff, like the attachments list before emitting the updated signal """
    
    # reload the attachments when we are in view
    if song == songfilter.Get()._selectedSong and song != None:
        _DoReloadAttachments(song)

    # song is updated
    Publisher().sendMessage(SIGNAL_SONG_UPDATED, song)
    
# ------------------------------------------------------------------------------
def signalDeleteSong():
    """ A callback we need to delete the song in question """

    #  can we delete?
    song = songfilter.Get()._selectedSong
    if song:
        Publisher().sendMessage(SIGNAL_DELETE_SONG)
        
# ------------------------------------------------------------------------------
def signalSongDeleted(song):
    """ The song in question is deleted. We inform all views that this song is deleted, and 
        when the song was actually the song we were looking at, we select a new song """

    # the db delete action already took place, so now we
    # set a new song first, and then issue a signal delete
    # this is done to avoid that the current selection is
    # invalidated somehow
    if song == songfilter.Get()._selectedSong:
        signalSetSong(songfilter.Get().GetNextVisibleSong())
    
    # now update the lists because we have a deleted song
    Publisher().sendMessage(SIGNAL_SONG_DELETED, song)

# ------------------------------------------------------------------------------
def signalSettingsChanged():
    """ The settings are changed, this means we need to reload the attachments list. This 
        also means all views related to attachments need an update """
    
    # reload the attachments list, or clear when we 
    # have no valid attachment directory
    _DoReloadAttachments(songfilter.Get()._selectedSong)

    Publisher().sendMessage(SIGNAL_SETTINGS_CHANGED)

# ------------------------------------------------------------------------------
def signalRefreshLinks():
    """ The attachment list needs refreshing. We refresh and we need to issue out a signal 
        informing all views to (possibly) update their data """
    
    # reload the attachments list, or clear when we 
    # have no valid attachment directory
    _DoReloadAttachments(song = songfilter.Get()._selectedSong)

    Publisher().sendMessage(SIGNAL_LINKS_REFRESHED)
        
# ------------------------------------------------------------------------------
def signalFilterChanged():
    """ The song filter contents is changed, e.g. a criteria is changed or a search is issued,
        this means we might have to select a new song """
    
    # first, if we have an old song, we check if it 
    # is still in the criteria view
    old_song = songfilter.Get()._selectedSong
    if old_song:
        if old_song in songfilter.Get()._critlist:
            # nothing to be done, we still have this song
            # in view, so let's quit
            return
    
    # basically here, we have no selected song, or it is not in 
    # the criteria so we are going to request a next song and set it
    signalSetSong(songfilter.Get().GetNextVisibleSong())

# ------------------------------------------------------------------------------
def signalTabSelected(tab):
    """ A tab is selected, we need to transmit this so all views can sync using this 
        tab if needed. """
    
    # let's transmit a signal
    Publisher().sendMessage(SIGNAL_TAB_SELECTED, tab)

# ------------------------------------------------------------------------------
def signalTabUpdated(tab):
    """ A tab is updated, we need to transmit so all views can sync using this 
        tab if needed. """
        
    # fire in the hull!
    Publisher().sendMessage(SIGNAL_TAB_UPDATED, tab)   

# ------------------------------------------------------------------------------
def signalTabDeleted(tab):
    """ A tab is deleted, we need to transmit so all views can remove this 
        tab if needed. """
        
    # fire in the hull! and it's a hit!
    Publisher().sendMessage(SIGNAL_TAB_DELETED, tab)   

# ------------------------------------------------------------------------------
def signalSetHomepage():
    """ The browser window is set to the homepage (overview of songs) so we force that 
        no song is selected, by issuing a signalSetSong with None as song argument """
    
    # first deselect all song data
    signalSetSong(None)

    # send the signal
    Publisher().sendMessage(SIGNAL_SET_HOMEPAGE)
    
# ------------------------------------------------------------------------------
def signalSelectNextSong():
    """ This is called when the next song in the criteria list needs to be selected. A convenient
        method of browsing through the criteria list """
    
    # get the next song we have in our criteria and view it
    signalSetSong(songfilter.Get().GetNextVisibleSong())
    
# ------------------------------------------------------------------------------
def signalSelectPreviousSong():
    """ This is called when the previous song in the criteria list needs to be selected. A convenient
        method of browsing through the criteria list """
    
    # get the next song we have in our criteria and view it
    signalSetSong(songfilter.Get().GetPreviousVisibleSong())
    
# ------------------------------------------------------------------------------
def signalTabAdded(tab):
    """ A new tab is added to the list of tabs in the database, send out a signal to all the listeners
        to update the views if needed """
    
    Publisher().sendMessage(SIGNAL_TAB_ADDED ,tab)
    
# ------------------------------------------------------------------------------
def signalEditAttachments():
    """ We are going to edit the attachments. This is a callback signal to make sure other parts
        of the GUI can also invoke an edit mechanism in the main form """
    
    Publisher().sendMessage(SIGNAL_EDIT_LINKS)

# ------------------------------------------------------------------------------
def _DoReloadAttachments(song):
    """ Internal function that reloads the attachments list as it is a very common used 
        piece of code """
    
    # if we have a song, attempt a load in the attachments, if 
    # there is no song or valid path, it will be empty
    if song:
        linkmgt.Get().Load(appcfg.GetAbsWorkPathFromSong(song))
    else:
        linkmgt.Get().Clear()
        
