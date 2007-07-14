import os
import os.path

import wx
from wx.lib.pubsub import Publisher

import db, db.engine, db.songs_peer, db.log_peer
from objs import category_mgr, tuning_mgr, linkmgt, songs, objlist, log
from gui import appcfg


SIGNAL_CLEAR_DATA       = ('do', 'clear', 'data')       # transmits a clear data signal, all views must 
                                                        # initialize to their defaults
SIGNAL_DATA_RESTORED    = ('data', 'restored')          # issued when all trivial data in the db is restored
SIGNAL_SONG_SELECTED    = ('song', 'selected')          # transmits when a song is selected, and all 
                                                        # relations and dependencies are restored
SIGNAL_SONG_ADDED       = ('song', 'added')             # transmits a signal when a new song is added to 
                                                        # the database. This does not mean it is selected
SIGNAL_SONG_UPDATED     = ('song', 'updated')           # transmitted when the song is updated
SIGNAL_SONG_DELETED     = ('song', 'deleted')           # transmitted when a song is deleted, can be followed
                                                        # by a SIGNAL_SONG_SELECTED as well
SIGNAL_SHOW_EDIT_INFO   = ('song', 'show', 'edinfo')    # show the edit information of the song
SIGNAL_SHOW_EDIT_LYRICS = ('song', 'show', 'edlyrics')  # show the edit lyrics of the song
SIGNAL_SHOW_EDIT_PROGR  = ('song', 'show', 'progress')  # show the progress panel

SIGNAL_SETTINGS_CHANGED = ('settings', 'changed')       # someone changed the settings, we need to send this out
SIGNAL_LINKS_REFRESHED  = ('links', 'refreshed')        # transmitted when deliberately the attachments list
                                                        # needs to be refreshed.
SIGNAL_TAB_SELECTED     = ('tab', 'selected')           # transmitted when a tab is selected for viewing
SIGNAL_SET_HOMEPAGE     = ('do', 'set', 'homepage')     # transmitted when the homepage needs to be set in 
                                                        # the song browser
SIGNAL_ADD_SONG         = ('do', 'song', 'add')         # transmitted when a song needs to be added
                                                        # a convenience callback function
SIGNAL_EDIT_SONG        = ('do', 'song', 'edit')        # sent when the selected song needs to be edited
SIGNAL_DELETE_SONG      = ('do', 'song', 'delete')      # sent when the selected song needs to be deleted
SIGNAL_EDIT_LINKS       = ('do', 'edit', 'links')       # send a command to edit the links 
SIGNAL_TAB_ADDED        = ('tab', 'added')              # a new tab is added to the database
SIGNAL_TAB_UPDATED      = ('tab', 'updated')            # send a command to update the tab
SIGNAL_TAB_DELETED      = ('tab', 'deleted')            # send around that we lost a tab 

SIGNAL_APP_READY        = ('app', 'ready')              # sent when all stuff is done, app is ready
SIGNAL_APP_QUIT         = ('app', 'quit')               # sent when app quits

SONG_VIEW_ADDED          = ('song', 'view', 'added')     # song added to view
SONG_VIEW_UPDATED        = ('song', 'view', 'updated')   # selected song updated in view 
SONG_VIEW_DELETED        = ('song', 'view', 'deleted')   # song deleted from view
SIGNAL_CRITLIST_CHANGED  = ('song', 'view', 'changed')   # criteria list is changed 

SIGNAL_RESET_SONGFILTER  = ('songfilter', 'reset')       # reset the songfilter

SIGNAL_LINKS_DIR_CREATED = ('songs', 'links', 'create')    # create links directory of song

# definitions
ADD    = 0
DELETE = 1
UPDATE = 2

# internal do not use as status
_CRIT_STATUS_ALL = -1 

SHOW_ALL       = 0
SHOW_TUTORIALS = 1
SHOW_SONGS     = 2

class SongFilter:
    def __init__(self):
        self._list = objlist.ObjList(class_name = songs.Song)
        self.Reset()

        #Publisher().subscribe(self._PopulateSongs, SIGNAL_DATA_RESTORED)
        Publisher().subscribe(self._SignalAddSong, SIGNAL_SONG_ADDED)
        Publisher().subscribe(self._RemoveSong, SIGNAL_SONG_DELETED)
        Publisher().subscribe(self._UpdateSong, SIGNAL_SONG_UPDATED)
        
    # --------------------------------------------------------------------------
    def _PopulateSongs(self, songlist):
        """ Populate the list after all data is restored """
        
        self._critList = []
        self._list.clear()
        
        for s in songlist:
            self._list.append(s)
        self.__ResyncAllSongs()

    # --------------------------------------------------------------------------
    def Reset(self):
        """ Reset all the data """
        self._critList = []
        self._list.clear()
        self._critStatus = _CRIT_STATUS_ALL
        self._critDifficulty = _CRIT_STATUS_ALL
        self._critCategories = []
        self._selectedSong = None    
        self._critCategoryAND = False 
        self._critDifficultyLO = False
        self._showSongType = SHOW_ALL   
        self._hideConcepts = False
    
    # --------------------------------------------------------------------------
    def ResetFilter(self):
        """ Reset all the view settings """
        
        # reset all the values
        self._critStatus = _CRIT_STATUS_ALL
        self._critDifficulty = _CRIT_STATUS_ALL
        self._critCategories = []
        self._critCategoryAND = False 
        self._critDifficultyLO = False
        self._showSongType = SHOW_ALL   
        self._hideConcepts = False    
        self.__ResyncAllSongs()

    # --------------------------------------------------------------------------
    def _SignalAddSong(self, message):
        """ Convenience function to call the actual function _AddSong """
        
        self._AddSong(message.data)
        
    # --------------------------------------------------------------------------
    def _AddSong(self, song):
        """ Adds a song to the list of songs to be played """
        
        self._list.append(song)
        self.__SyncWithCriteriaList(song, action = ADD)
        # send a message always when criteria list is changed
        Publisher().sendMessage(SIGNAL_CRITLIST_CHANGED, self._critList)
        pass 
        
    # --------------------------------------------------------------------------
    def _RemoveSong(self, message):
        """ Removes the song from the list """
        
        song = message.data
        if self._list.has_item(song):
            self._list.remove(song)
            self.__SyncWithCriteriaList(song, action = DELETE)
            # send a message always when criteria list is changed
            Publisher().sendMessage(SIGNAL_CRITLIST_CHANGED, self._critList)

    # --------------------------------------------------------------------------
    def _UpdateSong(self, message):
        """ Updates the song in the database and issues an update signal to update
            all views """
            
        song = message.data
        if self._list.has_item(song):
            self.__SyncWithCriteriaList(song, action = UPDATE)
            # if we are still the selected song, repopulate links
            if song == self._selectedSong:
                # refresh the links
                linkmgt.Get().Load(appcfg.GetAbsWorkPathFromSong(song))   
            # send a message always when criteria list is changed
            Publisher().sendMessage(SIGNAL_CRITLIST_CHANGED, self._critList)
        
    # --------------------------------------------------------------------------
    def ChangeStatusCriteria(self, criteria):
        """ Go by the song list again, and match all with criteria, in the  
            hope we can add new songs to the criteria, else delete commands
            are issued to delete songs that no longer match """
        if (criteria in songs.song_status) or (criteria == _CRIT_STATUS_ALL):
            self._critStatus = criteria
            self.__ResyncAllSongs()
        
    # --------------------------------------------------------------------------
    def ChangeDifficultyCriteria(self, criteria):
        """ Go by the song list again, and match all with criteria, in the  
            hope we can add new songs to the criteria, else delete commands
            are issued to delete songs that no longer match """
        if criteria in songs.song_difficulty or (criteria == _CRIT_STATUS_ALL):
            self._critDifficulty = criteria
            self.__ResyncAllSongs()
            
    # --------------------------------------------------------------------------
    def ChangeCategoriesCriteria(self, categories):
        """ Resyncs the category list """
        # clear list every time to avoid 'stuck' categories
        # which might be not related to songs anymore
        self._critCategories = categories
        self.__ResyncAllSongs()

    # --------------------------------------------------------------------------
    def ChangeCategoriesCriteriaAND(self, value):
        """ Adds AND boolean to criteria, if all set, all categories must
            exist in the song being filtered """
        self._critCategoryAND = value
        self.__ResyncAllSongs()
        
    # --------------------------------------------------------------------------
    def ChangeDifficultyCriteriaLO(self, value):
        self._critDifficultyLO = value
        self.__ResyncAllSongs()

    # --------------------------------------------------------------------------
    def ChangeHideConceptSongs(self, value):
        """ Change the criteria to hide or show concept songs. Concept songs are 
            songs that have no lyrics or information set yet. Typically the songs
            that you quickly add for later, but not want to see yet because they
            are not in your scope of playing """
        
        self._hideConcepts = value
        self.__ResyncAllSongs()
        
    # --------------------------------------------------------------------------
    def OnlySnowType(self, value):
        self._showSongType = value
        self.__ResyncAllSongs()
        
    # --------------------------------------------------------------------------
    def GetUsedCategories(self):
        """ Returns a list of categories that are used by 
            the songs. This is easy for a search filter 
            so unused categories are not displayed """
        result = []
        for s in self._list:
            for c in s.categories:
                if c not in result:
                    result.append(c)
        return result

    # --------------------------------------------------------------------------
    def __ResyncAllSongs(self):
        """ Resync the whole list, remove all the songs not matching
            add new that are matching """
        changed = False
        for s in self._list:
            self.__SyncWithCriteriaList(s, action = ADD)
        
        # send a message always when criteria list is changed
        Publisher().sendMessage(SIGNAL_CRITLIST_CHANGED, self._critList)

    # --------------------------------------------------------------------------
    def __SyncWithCriteriaList(self, song, action = ADD):
        """ Potentially add a song to the criteria list, if the criteria
            matches. 
            - If the object already exists, no signal is emitted. 
            - If the does not exist but matches the criteria, signal is emitted
            - If the song was present, but does not match the criteria anymore
              a delete signal is sent
            - If the song is not present, and also does not match, nothing is 
              done """

        present = (song in self._critList)

        visible = True
        # status of the song
        if self._critStatus <> _CRIT_STATUS_ALL:
            visible = (self._critStatus == song._status)

        # difficulty of the song
        if visible and (self._critDifficulty <> _CRIT_STATUS_ALL):
            if self._critDifficultyLO == False:
                visible = (self._critDifficulty == song._difficulty)
            else:
                visible = (self._critDifficulty >= song._difficulty)
                    
        # test categories
        if visible and len(self._critCategories) > 0:
            if self._critCategoryAND == False:
                # filter any
                visible = False # don't be optimistic
                for c in song.categories:
                    if c in self._critCategories:
                            visible = True
                            break
            else:
                # filter all
                visible = True # be optimistic
                for c in self._critCategories:
                    if c not in song.categories:
                        visible = False
                        break                
        
        # test song type
        if visible and self._showSongType != SHOW_ALL:
            visible = (self._showSongType == SHOW_TUTORIALS and song._songType == songs.ST_TUTORIAL) or \
                      (self._showSongType == SHOW_SONGS and song._songType == songs.ST_NORMAL)
        
        # hide the concept songs from the view
        if visible and self._hideConcepts:
            visible = not song.IsConcept()
        
        # always if not visible, but present, remove
        if not visible and present:
            self._critList.remove(song)
            Publisher().sendMessage(SONG_VIEW_DELETED, song)
            if song == self._selectedSong:
                signalSetSong(self.GetNextVisibleSong())  
            return

        # try adding a song
        if action == ADD:
            if visible and not present:            
                self._critList.append(song)
                Publisher().sendMessage(SONG_VIEW_ADDED, song)
        # try updating a song
        if action == UPDATE:
            if visible and not present:            
                self._critList.append(song)
                Publisher().sendMessage(SONG_VIEW_ADDED, song)
            elif visible and present:
                Publisher().sendMessage(SONG_VIEW_UPDATED, song)
        # try deleting a song
        if action == DELETE:
            if visible and present:
                Publisher().sendMessage(SONG_VIEW_DELETED, song)
                # issue a select query when selected one is deleted
                if song == self._selectedSong:
                    signalSetSong(self.GetNextVisibleSong())  

    # --------------------------------------------------------------------------
    def GetNextVisibleSong(self):
        """ Looks at the criteria list and tries to get the next song that is still valid 
            to be shown. If there isn't any, we return None """
        try:
            idx = Get()._critList.index(self._selectedSong)
        except ValueError:
            idx = -1 # force taking the first item in the list
        
        # retrieve the next value, if that does not exist retrieve 
        # the first value, if all fails, return None (empty criteria)
        if idx + 1 < len(Get()._critList):
            return Get()._critList[idx + 1]
        else:
            if len(Get()._critList) > 0:
                return Get()._critList[0]
        return None # I give up

    # --------------------------------------------------------------------------
    def GetPreviousVisibleSong(self):
        """ Looks at the criteria list and tries to get the previous song that is still valid 
            to be shown. If there isn't any, we return None """
        try:
            idx = Get()._critList.index(self._selectedSong)
        except ValueError:
            idx = 1 # force taking the first item in the list
        
        # retrieve the next value, if that does not exist retrieve 
        # the first value, if all fails, return None (empty criteria)
        if idx - 1 >= 0 and len(Get()._critList) > 0:
            return Get()._critList[idx - 1]
        else:
            if len(Get()._critList) > 0:
                return Get()._critList[len(Get()._critList) - 1]
        return None # I give up

# ==============================================================================

def signalDbChange():
    """ The database is changed, this means all the views must get rid of their referenced
        data, and all views must change to their default. After all data is restored, 
        the views get a go signal to repopulate everything """
        
    # send None as argument, to allow SIGNAL_SONG_SELECTED handlers to be 
    # used to revert to a disabled viewstate
    Publisher().sendMessage(SIGNAL_CLEAR_DATA, None)
    
    # restore all relations that are static to the lifetime of the app
    # like categories, tunings etc.
    
    Get().Reset()
    linkmgt.Get().Clear()

    # load categories and tunings
    dbc = db.engine.GetDb()
    category_mgr.RestoreFromDb(dbc)
    tuning_mgr.RestoreFromDb(dbc)
    
    # restore all songs
    sp = db.songs_peer.SongSetPeer(dbc)
    songlist = sp.Restore()        
    
    # restore all song category relations
    sp = db.songs_peer.SongPeer(dbc)
    for s in songlist:
        sp.RestoreCategories(s)     
    
    # first populate song filter, so others can use that
    # criteria list for the song selection
    Get()._PopulateSongs(songlist)
   
    # now inform others
    Publisher().sendMessage(SIGNAL_DATA_RESTORED, songlist)
    
    # one last message to to post processing, 
    # when all views are initialized
    Publisher().sendMessage(SIGNAL_APP_READY)
        
# ------------------------------------------------------------------------------
def signalSetSong(song):
    """ A new song needs to be set as selected song. Every view is notified of this
        If the song to be set is 'None', all views should reset to their default views """
        
    # prune tab relations from the old song
    # this is to reduce the memory footprint
    old_song = Get()._selectedSong
    if old_song:
        old_song.tabs.prune()
    
    # load the tabs for the new song
    if song:
        tlp = db.songs_peer.SongTabListPeer(db.engine.GetDb())
        tlp.Restore(song)        

    _DoReloadAttachments(song)
    
    Get()._selectedSong = song
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
    song = Get()._selectedSong
    if song:
        Publisher().sendMessage(SIGNAL_EDIT_SONG)

# ------------------------------------------------------------------------------
def signalSongUpdated(song):
    """ The song in question is updated. If the song is the selected song, we will also reload
        some stuff, like the attachments list before emitting the updated signal """
    # reload the attachments when we are in view
    if song == Get()._selectedSong and song != None:
        _DoReloadAttachments(song)

    # song is updated
    Publisher().sendMessage(SIGNAL_SONG_UPDATED, song)
    
# ------------------------------------------------------------------------------
def signalDeleteSong():
    """ A callback we need to delete the song in question """

    #  can we delete?
    song = Get()._selectedSong
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
    if song == Get()._selectedSong:
        signalSetSong(Get().GetNextVisibleSong())
    
    # now update the lists because we have a deleted song
    Publisher().sendMessage(SIGNAL_SONG_DELETED, song)

# ------------------------------------------------------------------------------
def signalSettingsChanged():
    """ The settings are changed, this means we need to reload the attachments list. This 
        also means all views related to attachments need an update """
    
    # reload the attachments list, or clear when we 
    # have no valid attachment directory
    _DoReloadAttachments(Get()._selectedSong)

    Publisher().sendMessage(SIGNAL_SETTINGS_CHANGED)

# ------------------------------------------------------------------------------
def signalRefreshLinks():
    """ The attachment list needs refreshing. We refresh and we need to issue out a signal 
        informing all views to (possibly) update their data """
    
    # reload the attachments list, or clear when we 
    # have no valid attachment directory
    _DoReloadAttachments(song = Get()._selectedSong)
    Publisher().sendMessage(SIGNAL_LINKS_REFRESHED)
        
# ------------------------------------------------------------------------------
def signalFilterChanged():
    """ The song filter contents is changed, e.g. a criteria is changed or a search is issued,
        this means we might have to select a new song """
    
    # first, if we have an old song, we check if it 
    # is still in the criteria view
    old_song = Get()._selectedSong
    if old_song:
        if old_song in Get()._critlist:
            # nothing to be done, we still have this song
            # in view, so let's quit
            return
    
    # basically here, we have no selected song, or it is not in 
    # the criteria so we are going to request a next song and set it
    signalSetSong(Get().GetNextVisibleSong())

# ------------------------------------------------------------------------------
def signalTabSelected(tab):
    """ A tab is selected, we need to transmit this so all views can sync using this 
        tab if needed. """
    
    # let's transmit a signal
    Publisher().sendMessage(SIGNAL_TAB_SELECTED, tab)

# ------------------------------------------------------------------------------
def signalTabUpdated(tab, song):
    """ A tab is updated, we need to transmit so all views can sync using this 
        tab if needed. """
        
    # fire in the hull!
    Publisher().sendMessage(SIGNAL_TAB_UPDATED, tab)
    
    # if our song is the song with the updated tab, we signal an update
    if song == Get()._selectedSong and song != None:
        Publisher().sendMessage(SIGNAL_SONG_UPDATED, song) 

# ------------------------------------------------------------------------------
def signalTabDeleted(tab, song):
    """ A tab is deleted, we need to transmit so all views can remove this 
        tab if needed. """
        
    # fire in the hull! and it's a hit!
    Publisher().sendMessage(SIGNAL_TAB_DELETED, tab)  
   
    # if our song is the song with the deleted tab, we signal an update
    if song == Get()._selectedSong and song != None:
        Publisher().sendMessage(SIGNAL_SONG_UPDATED, song) 

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
    signalSetSong(Get().GetNextVisibleSong())
    
# ------------------------------------------------------------------------------
def signalSelectPreviousSong():
    """ This is called when the previous song in the criteria list needs to be selected. A convenient
        method of browsing through the criteria list """
    
    # get the next song we have in our criteria and view it
    signalSetSong(Get().GetPreviousVisibleSong())
    
# ------------------------------------------------------------------------------
def signalTabAdded(tab, song):
    """ A new tab is added to the list of tabs in the database, send out a signal to all the listeners
        to update the views if needed """
    
    Publisher().sendMessage(SIGNAL_TAB_ADDED ,tab)
    
    # if our song is the song with the added tab, we signal an update
    if song == Get()._selectedSong and song != None:
        Publisher().sendMessage(SIGNAL_SONG_UPDATED, song) 
    
# ------------------------------------------------------------------------------
def signalEditAttachments():
    """ We are going to edit the attachments. This is a callback signal to make sure other parts
        of the GUI can also invoke an edit mechanism in the main form """
    
    Publisher().sendMessage(SIGNAL_EDIT_LINKS)

# ------------------------------------------------------------------------------
def signalSongStatusChange(song, new_status):
    """ We are about to change the status of the song, this will be logged and some intelligent stuff
        is performed. 
        
        Song status TODO -> IN PROGRESS:
            - Set date started to this date
            - Set status of song to IN PROGRESS
            - Create a log entry and save it to DB
            - Update the song in the DB
            - Call signalSongUpdated 
            
        Song status IN PROGRESS -> NOT PRACTICING:
            - Set time postponed to this date
            - Set status of song to POSTPONED
            - Create a log entry and save it to DB
            - Update the song in the DB
            - Call signalSongUpdated
            
        Song status IN PROGRESS -> COMPLETED:
            - Is song been completed earlier? If not
                - Set time completed to this date
            - Set status of song to to completed
            - Create a log entry and save it to DB
            - Update the song in the DB
            - Call signalSongUpdated 
            
        Song status COMPLETED -> IN_PROGRESS:
            - Set status of song to in progress
            - Create a log entry and save it to DB
            - Update the song in the DB
            - Call signalSongUpdated 
    """
    
    # make sure we are not going to log an unchanged or illegal status
    valid_entry = False
    if (song._status == new_status) or (new_status == songs.SS_NOT_STARTED):
        return
        
    # create a new log object, we borrow the date from 
    # this object to set in the song object
    logentry = log.LogItem()
    logentry._type = log.LOG_STATUSCHANGE
    
    # TODO --> STARTED
    if song._status == songs.SS_NOT_STARTED:
        if new_status == songs.SS_STARTED:
            valid_entry = True
            song._timeStarted = logentry._date
    elif song._status == songs.SS_STARTED:
        # IN PROGRESS -> POSTPONED
        if new_status == songs.SS_POSTPONED:
            valid_entry = True
            song._timePostponed = logentry._date
        # IN PROGRESS -> COMPLETED
        elif new_status == songs.SS_COMPLETED:
            valid_entry = True
            song._timeCompleted = logentry._date
    elif song._status == songs.SS_COMPLETED:
        # COMPLETED -> IN PROGRESS
        if new_status == songs.SS_STARTED:
            valid_entry = True
    elif song._status == songs.SS_POSTPONED:
        # POSTPONED-> IN PROGRESS
        if new_status == songs.SS_STARTED:
            valid_entry = True

    # when we have a valid entry we store the log
    # and the song to the database, and change the status
    if valid_entry:
        song._status = new_status
        logentry._value = new_status
        
        # update the song object
        sp = db.songs_peer.SongPeer(db.engine.GetDb())
        sp.Update(song, all = False)
        
        # insert the log object
        sp = db.log_peer.LogPeer(db.engine.GetDb())
        sp.Update(logentry, song._id)
        
        # invoke the update signal
        signalSongUpdated(song)
            
# ------------------------------------------------------------------------------
def signalAccuracyChange(song, accuracy):
    """ Signal an accuracy % change to the log, and update the song and the database """
                
    if song:
        # only change when a change occured
        if song._percAccuracy != accuracy:
            # create a new log object
            logentry = log.LogItem()
            logentry._type = log.LOG_PROGRESS_CHANGE_ACC
            logentry._value = accuracy
            
            # in the text portion set the current % in progress
            logentry._text = '%.02i' % (((song._percCompleted *10) + (accuracy * 10)) / 2)
            
            song._percAccuracy = accuracy
            
            # update the song object
            sp = db.songs_peer.SongPeer(db.engine.GetDb())
            sp.Update(song, all = False)
            
            # insert the log object
            sp = db.log_peer.LogPeer(db.engine.GetDb())
            sp.Update(logentry, song._id)
            
            # invoke the update signal
            signalSongUpdated(song)

# ------------------------------------------------------------------------------
def signalCompletedChange(song, completed):
    """ Signal an completed % change to the log, and update the song and the database """

    if song:                
        # only change when a change occured
        if song._percCompleted != completed:
            # create a new log object
            logentry = log.LogItem()
            logentry._type = log.LOG_PROGRESS_CHANGE_CMP
            logentry._value = completed

            # in the text portion set the current % in progress
            logentry._text = '%.02i' % (((song._percAccuracy *10) + (completed * 10)) / 2)
            
            song._percCompleted = completed
            
            # update the song object
            sp = db.songs_peer.SongPeer(db.engine.GetDb())
            sp.Update(song, all = False)
            
            # insert the log object
            sp = db.log_peer.LogPeer(db.engine.GetDb())
            sp.Update(logentry, song._id)
            
            # invoke the update signal
            signalSongUpdated(song)

# ------------------------------------------------------------------------------
def signalAddComment(song, comment):
    """ Add a comment to the song log """
    
    if song:                
        # only log when we have somthing to say
        if comment != '':
            # create a new log object
            logentry = log.LogItem()
            logentry._type = log.LOG_COMMENT
            logentry._text = comment
                        
            # insert the log object
            sp = db.log_peer.LogPeer(db.engine.GetDb())
            sp.Update(logentry, song._id)

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
        
# ------------------------------------------------------------------------------
def signalAddStudyTime(song, studytime):
    """ Send a study time to the log belonging to the current song """
    
    if song and studytime:
        # create a new log object
        logentry = log.LogItem()
        logentry._type = log.LOG_STUDYTIME
        logentry._value = studytime
                    
        # insert the log object
        sp = db.log_peer.LogPeer(db.engine.GetDb())
        sp.Update(logentry, song._id)
        
# ------------------------------------------------------------------------------
def signalAppQuit():
    """ Send a signal that the application closes """
    
    # update the config, etc
    Publisher().sendMessage(SIGNAL_APP_QUIT)
    
# ------------------------------------------------------------------------------
def signalResetFilter():
    """ Performs a clear on the songfilter object, and sends around that other views
        should update accordingly """
    
    Get().ResetFilter()
    Publisher().sendMessage(SIGNAL_RESET_SONGFILTER)

# ------------------------------------------------------------------------------
def signalSongEditInfo(song):
    """
    A signal is sent that the edit panel needs to be shown and the edit tab for the 
    song info needs to be shown
    """
    if song:
        Publisher().sendMessage(SIGNAL_SHOW_EDIT_INFO)

# ------------------------------------------------------------------------------
def signalSongEditLyrics(song):
    """
    A signal is sent that the edit panel needs to be shown and the edit tab for the 
    song lyrics needs to be shown
    """
    if song:
        Publisher().sendMessage(SIGNAL_SHOW_EDIT_LYRICS)

# ------------------------------------------------------------------------------
def signalSongEditProgress(song):
    """
    A signal is sent that the edit panel needs to be shown and the edit tab for the 
    song progress needs to be shown
    """
    if song:
        Publisher().sendMessage(SIGNAL_SHOW_EDIT_PROGR)

# ------------------------------------------------------------------------------
def signalOnCreateAttachmentsDir(song):
    """
    Signal a request to create the work directory based upon the song that
    is currently sent to us
    """
    if song:
        path = appcfg.GetAbsWorkPathFromSong(song)
        if os.path.isabs(path):        
            result = wx.MessageBox('Would you like to create the work directory for this song?', 'Warning', wx.ICON_QUESTION | wx.YES_NO)
            if result == wx.YES:
                try:
                    # create the images dir, and the attachments dir
                    os.makedirs(path)
                    os.makedirs(os.path.join(path, 'images'))
                    
                    wx.MessageBox('Path creation succesful!\n' + 
                                  'Now copy your gathered song files to this directory', 'Succes', wx.ICON_INFORMATION | wx.OK)                
                    
                    Publisher().sendMessage(SIGNAL_LINKS_DIR_CREATED)
                
                except EnvironmentError:
                    wx.MessageBox('Path creation unsuccesful\n' +
                                  'Please check for a valid base path, file rights and retry', 'Error', wx.ICON_ERROR | wx.OK)
                
        else:
            # warn about relative path
            wx.MessageBox('Cannot create a relative work directory\n'
                          'Please fill in your base directory in the Preferences', 'Error', wx.ICON_ERROR | wx.OK)
        
#===============================================================================

__obj = None

def Get():
    global __obj
    if not __obj:
        __obj = SongFilter()
    return __obj
