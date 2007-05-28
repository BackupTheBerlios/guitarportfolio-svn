from db import category_peer, tuning_peer, songs_peer, tabs_peer
from objs import category, tuning, songs, tabs, tuning_mgr, category_mgr, songfilter, signals
import db
import sqlite3
import datetime

from wx.lib.pubsub import Publisher

song_info = [ ('What Its Like', 'Everlast', songs.SS_STARTED), 
              ('Coffee Blues', 'Mississippi John Hurt', songs.SS_COMPLETED),
              ('Railroad Bill', 'Stephan Grossman', songs.SS_STARTED),
              ('Got the blues and cant be satisfied', 'Mississippi John Hurt', songs.SS_STARTED),
              ('Cocaine Blues', 'Rev Gary Davis', songs.SS_POSTPONED) ]


_signal = None
_data = None
_received = False
_count = 0

class TestSongFilter:
    def setup_class(self):
        self._conn = sqlite3.connect(':memory:')
        r = self._conn.executescript(db.engine.create_sql)
        
        # restore categories
        category_mgr.RestoreFromDb(self._conn)
        
    def teardown_class(self):
        pass

    def setup_method(self, method):
        self._filter = songfilter.SongFilter()
        self._songs = []

        Publisher.subscribe(self.signal_received, signals.SONG_VIEW_ADDED)
        self.ResetSignal()        
        
        # fill songs
        for si in song_info:
            s = songs.Song(id = -1)
            s._title = si[0]
            s._artist = si[1]
            s._status = si[2]
            self._songs.append(s)
            
    def ResetSignal(self):
        global _signal, _data, _received, _count
        _signal = None
        _data = None
        _received = False
        _count = 0               

    def CheckNoSignal(self):
        global _signal, _data, _received, _count
        assert _signal == None
        assert _data == None
        assert _received == False
        assert _count == 0    

    def SignalCount(self):
        global _count
        return _count
        
    def SignalReceived(self, signal):
        global _received, _signal, _count
        assert _received
        assert _signal == signal
     
    def SignalDataReceived(self, signal, data):
        global _received, _signal, _count
        assert _received
        assert _signal == signal
        assert _data == data

###===========================================================================    
    def test_adding(self):
        self._filter.AddSong(self._songs[0])
        self.SignalDataReceived(signals.SONG_VIEW_ADDED, self._songs[0])

# -- Test -- Add Songs with ignored status

        self._filter.ChangeStatusCriteria(songs.SS_STARTED)
        assert self._songs[1]._status == songs.SS_COMPLETED
        assert self._songs[4]._status == songs.SS_POSTPONED
        
        self.ResetSignal()
        self._filter.AddSong(self._songs[1])
        self.CheckNoSignal()

        self._filter.AddSong(self._songs[4])
        self.CheckNoSignal()

# -- Test -- Change status to ALL again

        self.ResetSignal()
        self._filter.ChangeStatusCriteria(songfilter._CRIT_STATUS_ALL)
        assert len(self._filter._critList) == 3
        assert self.SignalCount() == 2

###===========================================================================    
    def test_categories(self):
        mgr = category_mgr.Get()
        self._songs[0].categories.append(mgr._list[0])
        self._songs[0].categories.append(mgr._list[1])
        
# -- Test -- Add Songs with a category, later put these in visibility

        self._filter.ChangeCategoriesCriteria([mgr._list[2]])
        
        self.ResetSignal()
        self._filter.AddSong(self._songs[0])

        self.CheckNoSignal()
        
        
                
###===========================================================================    
    def test_removing(self):
        pass

###===========================================================================    
    def test_updating(self):
        pass

###===========================================================================    
    def test_change_difficulty(self):
        pass
        
###===========================================================================    
    def test_change_status(self):
        pass
        
###===========================================================================    
    def test_signal_db_add(self):
        pass

###===========================================================================    
    def test_signal_db_remove(self):
        pass

###===========================================================================    
    def test_signal_db_update(self):
        pass

    def signal_received(self, message):
        global _signal, _data, _received, _count
                
        _received = True
        _signal = message.topic
        _data = message.data
        _count += 1
        
