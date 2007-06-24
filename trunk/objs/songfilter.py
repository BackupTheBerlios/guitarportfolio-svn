from wx.lib.pubsub import Publisher
from objs import songs, objlist, linkmgt
from gui import appcfg

# definitions
ADD    = 0
DELETE = 1
UPDATE = 2

# internal do not use as status
_CRIT_STATUS_ALL = -1 

SHOW_ALL       = 0
SHOW_TUTORIALS = 1
SHOW_SONGS     = 2

SONG_VIEW_ADDED        = ('song', 'view', 'added')          # song added to view
SONG_VIEW_UPDATED      = ('song', 'view', 'updated')        # selected song updated in view 
SONG_VIEW_DELETED      = ('song', 'view', 'deleted')        # song deleted from view

class SongFilter:
    def __init__(self):
        self._list = objlist.ObjList(class_name = songs.Song)
        self.Reset()

        # subscribe to the viewmanager to keep our list
        # up to date!

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
    
    # --------------------------------------------------------------------------
    def AddSong(self, song):
        """ Adds a song to the list of songs to be played """
        self._list.append(song)
        self.__SyncWithCriteriaList(song, action = ADD)
        pass 
        
    # --------------------------------------------------------------------------
    def RemoveSong(self, song):
        """ Removes the song from the list """
        if self._list.has_item(song):
            self._list.remove(song)
            self.__SyncWithCriteriaList(song, action = DELETE)

    # --------------------------------------------------------------------------
    def UpdateSong(self, song):
        """ Updates the song in the database and issues an update signal to update
            all views """
        if self._list.has_item(song):
            self.__SyncWithCriteriaList(song, action = UPDATE)
            # if we are still the selected song, repopulate links
            if song == self._selectedSong:
                # refresh the links
                linkmgt.Get().Load(appcfg.GetAbsWorkPathFromSong(song))                

        
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
        for s in self._list:
            self.__SyncWithCriteriaList(s, action = ADD)

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
        
        # always if not visible, but present, remove
        if not visible and present:
            self._critList.remove(song)
            Publisher().sendMessage(SONG_VIEW_DELETED, song)
            if song == self._selectedSong:
                viewmgr.signalSetSong(self.GetNextVisibleSong())  
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
                    viewmgr.signalSetSong(self.GetNextVisibleSong())  

    # --------------------------------------------------------------------------
    def GetNextVisibleSong(self):
        """ Looks at the criteria list and tries to get the next song that is still valid 
            to be shown. If there isn't any, we return None """
        try:
            idx = self._critList.index(self._selectedSong)
        except ValueError:
            idx = -1 # force taking the first item in the list
        
        # retrieve the next value, if that does not exist retrieve 
        # the first value, if all fails, return None (empty criteria)
        if idx + 1 < len(self._critlist):
            return self._critlist[idx + 1]
        else:
            if len(self._critlist) > 0:
                return self._critlist[0]
        return None # I give up

    # --------------------------------------------------------------------------
    def GetPreviousVisibleSong(self):
        """ Looks at the criteria list and tries to get the previous song that is still valid 
            to be shown. If there isn't any, we return None """
        try:
            idx = self._critList.index(self._selectedSong)
        except ValueError:
            idx = 1 # force taking the first item in the list
        
        # retrieve the next value, if that does not exist retrieve 
        # the first value, if all fails, return None (empty criteria)
        if idx - 1 > 0 and len(self._critlist) > 0:
            return self._critlist[idx - 1]
        else:
            if len(self._critlist) > 0:
                return self._critlist[len(self._critlist - 1)]
        return None # I give up

#===============================================================================

__obj = None

def Get():
    global __obj
    if not __obj:
        __obj = SongFilter()
    return __obj
