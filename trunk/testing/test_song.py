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

class TestSong:
    def setup_class(self):
        self._conn = sqlite3.connect(':memory:')
        r = self._conn.executescript(db.engine.create_sql)
        
        # restore categories
        category_mgr.RestoreFromDb(self._conn)
        
    def teardown_class(self):
        pass

    def setup_method(self, method):
        self._songs = []

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
    def test_song_perc(self):
        song = self._songs[0]
        song._percCompleted = 10
        song._percAccuracy = 10
        assert song.GetProgressPerc() == 100
        
        song._percCompleted = 5
        song._percAccuracy = 5
        assert song.GetProgressPerc() == 50
        
        song._percCompleted = 1
        song._percAccuracy = 8
        assert song.GetProgressPerc() == 45
        
        song._percCompleted = 0
        song._percAccuracy = 8
        assert song.GetProgressPerc() == 40

        song._percCompleted = 0
        song._percAccuracy = 0
        assert song.GetProgressPerc() == 0

    def test_tuning(self):
        song = self._songs[0]
        
        song._altTuning = 'Bla'
        assert song.GetTuningText() == 'Bla'
        assert song.GetTuningName() == 'Custom'
        
        song._tuning = tuning_mgr.Get()._list[1]
        assert song.GetTuningText() == 'D  A  D  G  B  E '
        assert song.GetTuningName() == 'Drop D'

        song._tuning = tuning_mgr.Get().GetDefaultTuning()
        assert song.GetTuningText() == 'E  A  D  G  B  E '
        assert song.GetTuningName() == 'Standard'
    
    def signal_received(self, message):
        global _signal, _data, _received, _count
                
        _received = True
        _signal = message.topic
        _data = message.data
        _count += 1
        
