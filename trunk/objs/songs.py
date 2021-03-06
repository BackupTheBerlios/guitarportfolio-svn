"""
    Songs manager. Module that manages the Song and SongList classes
    The song object contains the song information
"""

import datetime
from wx.lib.pubsub import Publisher

import db
import signals
import tuning, tuning_mgr
import tabs
import category
import objlist

# song state 
SS_STARTED     = 0
SS_POSTPONED   = 1
SS_COMPLETED   = 2
SS_NOT_STARTED = 3

ST_NORMAL      = 0  # normal song
ST_TUTORIAL    = 1  # riff / snippet

# song difficulty
SD_EASY         = 0
SD_NORMAL       = 1
SD_INTERMEDIATE = 2
SD_ADVANCED     = 3
SD_HARD         = 4
SD_IMPOSSIBLE   = 5

# possible selections for the song status
song_status = (SS_STARTED, 
               SS_POSTPONED,
               SS_COMPLETED,
               SS_NOT_STARTED)

# possible selections for the song difficulty
song_difficulty = (SD_EASY, 
                   SD_NORMAL, 
                   SD_INTERMEDIATE, 
                   SD_ADVANCED, 
                   SD_HARD, 
                   SD_IMPOSSIBLE)
  
# ------------------------------------------------------------------------------
def GetCapoString(fret_nr):
    """ Convenience function to return string for the user telling what 
        capo number is used """
    if fret_nr > 0:
        return 'Fret %d' % fret_nr
    return 'No Capo'

# ------------------------------------------------------------------------------
def SongTitleCmpFunction(song1, song2):
    """
    Compares song1 and song2 title and returns 0, -1 or 1 to 
    let the built in sort method do it's work
    """
    if song1._title.upper() > song2._title.upper():
        return 1
    elif song1._title.upper() < song2._title.upper():
        return -1
    return 0

"""
    Song object. 
"""
class Song(db.base.Object):
    def __init__(self, id = -1):
        super(Song, self).__init__(id)
        self._title = ''
        self._artist = ''
        self._status = SS_NOT_STARTED
        self._difficulty = SD_NORMAL
        self.categories = objlist.ObjList(class_name = category.Category)
        self._barCount = 0
        self._time = datetime.datetime.now()
        self._tuning = None
        self._lyrics = ''
        self._information = ''
        self._altTuning = 'E  A  D  G  B  E '
        self._dateUnknown = True
        self._yearOnly = False
        self._percCompleted = 0
        self._percAccuracy = 0
        self._capoOnFret = 0    # capo on none
        self._relativePath = ''
        self.tabs = objlist.ObjList(class_name = tabs.Tab) 
        self._timeStarted = datetime.datetime.now()
        self._timeAdded = datetime.datetime.now()
        self._timeCompleted = datetime.datetime.now()
        self._timePostponed = datetime.datetime.now()
        self._songType = ST_NORMAL
        
    #--------------------------------------------------------------------------
    def GetProgressPerc(self):
        assert self._percAccuracy <= 10 and self._percAccuracy >= 0
        assert self._percCompleted <= 10 and self._percCompleted >= 0
        """ Returns the progress averaged for the song """
        return int((self._percAccuracy * 10 + self._percCompleted * 10) / 2)
        
    #--------------------------------------------------------------------------
    def _GetTuningId(self):
        if self._tuning <> None:
            return self._tuning._id
        return -1    
              
    #--------------------------------------------------------------------------
    def GetTuningText(self):
        """ Get the tuning, based upon the relation or the alternate text """
        if self._tuning:
            return self._tuning._tuningText
        return self._altTuning
        
    #--------------------------------------------------------------------------
    def GetTuningName(self):
        """ Get the tuning name, if no tuning is present, Custom is returned """
        if self._tuning:
            return self._tuning._tuningName
        return "Custom"

    def IsConcept(self):
        """ Returns true when nearly all values are still set to their defaults. """
        
        # unfortunately we cannot check the tabs because we do restore them at
        # the very last moment.
        return (self._status == SS_NOT_STARTED) and \
               (self._lyrics == '') and \
               (self._information == '') and \
               (self._percCompleted == 0) and \
               (self._percAccuracy == 0) and \
               (self._capoOnFret == 0)
        
