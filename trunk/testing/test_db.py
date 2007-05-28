from db import engine, category_peer, tuning_peer, songs_peer, tabs_peer
from objs import category, tuning, songs, tabs, tuning_mgr, category_mgr
import db
import sqlite3
import datetime

class TestDb:
    def setup_class(self):
        self._conn = sqlite3.connect(':memory:')
        r = self._conn.executescript(engine.create_sql)

    def teardown_class(self):
        pass

    def setup_method(self, method):
        pass

###===========================================================================    
    def test_category(self):

# -- test -- Create a new category --

        c = category.Category(id = -1) 
        c._name = 'Some Name'

        p = category_peer.CategoryPeer(self._conn)
        p.Update(c)

# -- test -- Restore category --

        l = category.Category(id = c._id)
        p.Restore(l)
        
        assert l._name == c._name 

# -- test -- Delete category --

        p.Delete(c)
        try:
            p.Restore(c)
            assert False
        except db.base.DbException:
            pass
        
###===========================================================================    
    def test_category_mgr(self):

# -- test -- Restore categories --

        category_mgr.RestoreFromDb(self._conn)

        mgr = category_mgr.Get()

        assert len(mgr._list) == 20
        assert mgr._list[0]._name == 'Travis Picking'

# -- test -- GetCategoryByName --

        cat = mgr.GetCategoryByName('Travis Picking')
        assert cat == mgr._list[0]
        
        cat = mgr.GetCategoryByName('jfgdjhddkjhgfskjhfgsd')
        assert cat == None
        
# -- test -- GetCategoryById --

        id = mgr._list[10]._id
        cat = mgr.GetCategoryById(id)
        assert cat == mgr._list[10]

###===========================================================================    
    def test_tuning_mgr(self):
        tuning_mgr.RestoreFromDb(self._conn)

# -- test -- retrieve all tunings from db --

        mgr = tuning_mgr.Get()
        assert len(mgr._list) == 28
        assert mgr._list[0]._tuningName == 'Standard'
        assert mgr._list[0]._tuningText == 'E  A  D  G  B  E '
        assert mgr._list[1]._tuningName == 'Drop D'
        assert mgr._list[1]._tuningText == 'D  A  D  G  B  E '
        
# -- test -- GetDefaultTuning --

        t = mgr.GetDefaultTuning()
        assert t <> None
        assert t._tuningName == 'Standard'
        
# -- test -- GetTuningById --

        t_id = mgr._list[27]._id
        assert t_id <> -1
        
        t = mgr.GetTuningById(t_id)
        assert mgr._list[27] == t
        
        t = mgr.GetTuningById(-1)
        assert t == None
        
        
###===========================================================================    
    def test_song_partial(self):

# -- test -- Insert in DB --

        s = songs.Song(id = -1)
        s._title = 'Spike Driver Blues'
        s._artist = 'Mississippi John Hurt'
        s._status = songs.SS_POSTPONED
        s._difficulty = songs.SD_INTERMEDIATE
        s._barCount = 14
        s._time = datetime.datetime.now()
        tst_time = s._time
        s._lyrics = 'John Henry Was a Steel Drivin Man ....'
        s._information = 'One of the best songs ever'
        s._altTuning = 'E  A  D  G  B  E '
        s._dateUnknown = False
        s._yearOnly = True
        s._percCompleted = 85
        s._percAccuracy = 60
        s._capoOnFret = 2
        s._relativePath = '{artist}\\{title}'

        p = songs_peer.SongPeer(self._conn)
        p.Update(s)
        
        assert s._id <> -1
        
# -- test -- Restore from DB --

        ss = songs.Song(s._id)
        p.Restore(ss)
        
# -- test -- Restore from DB -- Verify Values --

        assert ss._id == s._id
        assert ss._title == 'Spike Driver Blues'
        assert ss._artist == 'Mississippi John Hurt'
        assert ss._status == songs.SS_POSTPONED
        assert ss._difficulty == songs.SD_INTERMEDIATE
        assert ss._barCount == 14
        assert ss._lyrics == 'John Henry Was a Steel Drivin Man ....'
        assert ss._information == 'One of the best songs ever'
        assert ss._altTuning == 'E  A  D  G  B  E '
        assert ss._dateUnknown == False
        assert ss._yearOnly == True
        assert ss._percCompleted == 85
        assert ss._percAccuracy == 60
        assert ss._capoOnFret == 2
        assert ss._relativePath == '{artist}\\{title}'
        
# -- test -- Update in DB -- Single Field --

        ss._title = 'Coffee Blues'
        p = songs_peer.SongPeer(self._conn)
        p.Update(ss)
        
        ss = songs.Song(s._id)
        p.Restore(ss)  
                
        assert ss._id == s._id
        assert ss._title == 'Coffee Blues'
        assert ss._artist == 'Mississippi John Hurt'
        assert ss._status == songs.SS_POSTPONED
        assert ss._difficulty == songs.SD_INTERMEDIATE
        assert ss._barCount == 14
        assert ss._lyrics == 'John Henry Was a Steel Drivin Man ....'
        assert ss._information == 'One of the best songs ever'
        assert ss._altTuning == 'E  A  D  G  B  E '
        assert ss._dateUnknown == False
        assert ss._yearOnly == True
        assert ss._percCompleted == 85
        assert ss._percAccuracy == 60
        assert ss._capoOnFret == 2
        assert ss._relativePath == '{artist}\\{title}'

# -- test -- Update in DB -- All Fields --
        
        ss._title = 'Shake That Thing'
        ss._artist = 'M.J.H'
        ss._status = songs.SS_COMPLETED
        ss._difficulty = songs.SD_HARD
        ss._barCount = 16
        ss._time = datetime.datetime.now()
        ss._lyrics = 'I bought my girl, a diamond ring ...'
        ss._information = 'Blues in G'
        ss._altTuning = 'E  A  D  G  B  D '
        ss._dateUnknown = True
        ss._yearOnly = False
        ss._percCompleted = 40
        ss._percAccuracy = 50
        ss._capoOnFret = 0
        ss._relativePath = '{title}'        

        p.Update(ss)
        
        ss = songs.Song(s._id)
        p.Restore(ss)
        
        assert ss._title == 'Shake That Thing'
        assert ss._artist == 'M.J.H'
        assert ss._status == songs.SS_COMPLETED
        assert ss._difficulty == songs.SD_HARD
        assert ss._barCount == 16
        assert ss._lyrics == 'I bought my girl, a diamond ring ...'
        assert ss._information == 'Blues in G'
        assert ss._altTuning == 'E  A  D  G  B  D '
        assert ss._dateUnknown == True
        assert ss._yearOnly == False
        assert ss._percCompleted == 40
        assert ss._percAccuracy == 50
        assert ss._capoOnFret == 0
        assert ss._relativePath == '{title}'        
        
# -- test -- Delete from DB -- 

        p.Delete(ss)
        try:
            p.Restore(ss)
            assert True == False
        except db.base.DbException:
            pass

###===========================================================================    
    def test_tabs(self):                

# -- test -- Insert Tab in DB --

        t = tabs.Tab(id = -1)
        t._name = 'Original tab'
        t._text = 'Some tab info'
        
        tp = tabs_peer.TabPeer(self._conn)
        tp.Update(t)
        
        assert t._id <> -1
        
# -- test -- Restore Tab from DB --

        tt = tabs.Tab(t._id)
        tp.Restore(tt)
        assert tt._name == 'Original tab'
        assert tt._text == 'Some tab info'        
                
        tt._name = 'Not so original tab'
        tt._text = '--A----------------'
        tp.Update(tt)
        
        tt = tabs.Tab(t._id)
        tp.Restore(tt)
        assert tt._name == 'Not so original tab'
        assert tt._text == '--A----------------'
                
# -- test -- Delete Tab from DB --

        tp.Delete(tt)
        try:
            tp.Restore(tt)
            assert True == False
        except db.base.DbException:
            pass

###===========================================================================    
    def test_tab_song(self):

# -- test -- Appending Tab to Song --
        
        s = songs.Song(id = -1)
        sp = songs_peer.SongPeer(self._conn)
        sp.Update(s)
        
        t = tabs.Tab(-1)
        t._name = 'Song tab'
        t._text = 'tab text'
        tp = tabs_peer.TabPeer(self._conn)
        tp.Update(t)
        
        s.tabs.append(t)
        
# -- test -- Store Tab Relations in DB --

        tsp = songs_peer.SongTabListPeer(self._conn)
        tsp.Update(s)
        
# -- test -- Restore tabs and song from DB --

        sr = songs.Song(s._id)
        sp.Restore(sr, all = True)
        
        assert sr.tabs.count() == 1
        tab = sr.tabs[0]
        assert tab._name == 'Song tab'
        assert tab._text == 'tab text'
        
# -- test -- Append Two tabs to song --

        t = tabs.Tab(-1)
        t._name = 'Song tab 2'
        t._text = 'tab text 2'
        tp = tabs_peer.TabPeer(self._conn)
        tp.Update(t)
        
        sr.tabs.append(t)
        
        tsp = songs_peer.SongTabListPeer(self._conn)
        tsp.Update(sr)
        
# -- test -- Restore Tab Relations --

        sr = songs.Song(s._id)
        sp.Restore(sr, all = True)
        
        assert len(sr.tabs) == 2
        tab = sr.tabs[0]
        assert tab._name == 'Song tab'
        assert tab._text == 'tab text'

        tab = sr.tabs[1]
        assert tab._name == 'Song tab 2'
        assert tab._text == 'tab text 2'

# -- test -- Remove a tab + relation from song --

        sr.tabs.remove(tab)
        tp = tabs_peer.TabPeer(self._conn)
        tp.Delete(tab)
        
# -- test -- Check for deletion of tab from DB --

        try:
            tp.Restore(tab)
            assert False == True
        except db.base.DbException:
            pass                

# -- test -- Restore only one tab after deleting one --
        
        sp.Update(sr, all = True)
        
        sr = songs.Song(s._id)
        sp.Restore(sr, all = True)
        
        assert len(sr.tabs) == 1
        tab = sr.tabs[0]
        assert tab._name == 'Song tab'
        assert tab._text == 'tab text'
        
# -- test -- Remove all tabs from the song --

        sr.tabs.remove(tab)
        assert len(sr.tabs) == 0
        
        tp = tabs_peer.TabPeer(self._conn)
        tp.Delete(tab)
        
# -- test -- Attempt Restore No tabs --

        try:
            tp.Restore(tab)
            assert False == True
        except db.base.DbException:
            pass                
        
# -- test -- No tabs should be present all are deleted --

        sp.Update(sr, all = True)

        sr = songs.Song(s._id)
        sp.Restore(sr, all = True)

        assert len(sr.tabs) == 0
                
# -- test -- Append another tab after deleting all --

        t = tabs.Tab(-1)
        t._name = 'Song tab'
        t._text = 'Tab text'
        tp = tabs_peer.TabPeer(self._conn)
        tp.Update(t)
        
        sr.tabs.append(t)

        sp.Update(sr, all = True)
        
        sr = songs.Song(s._id)
        sp.Restore(sr, all = True)

        assert len(sr.tabs) == 1

# -- test -- Test propagate deletion of tabs together with song --

        tab_id = sr.tabs[0]._id
        sp.Delete(sr)
        
        try:
            tab = tabs.Tab(tab_id)
            tp.Restore(tab)
            assert False == True
        except db.base.DbException:
            pass                

###===========================================================================    
    def test_song_tuning(self):

        s = songs.Song(id = -1)
        sp = songs_peer.SongPeer(self._conn)
        sp.Update(s)

        mgr = tuning_mgr.Get()
        assert len(mgr._list) > 0

# -- test -- Assign Tuning -- Assign a tuning
            
        s._tuning = mgr._list[1]
        sp.Update(s)
        
        ss = songs.Song(s._id)
        sp.Restore(ss)
        
        assert ss._tuning == s._tuning
        
# -- test -- Assign Tuning -- Assign empty
    
        s._tuning = None
        sp.Update(s)
        
        ss = songs.Song(s._id)
        sp.Restore(ss)

        assert ss._tuning == None
                
###===========================================================================    
    def test_song_categories(self):

        s = songs.Song(id = -1)
        sp = songs_peer.SongPeer(self._conn)
        sp.Update(s)
        
        mgr = category_mgr.Get()
        assert len(mgr._list) > 3
 
# -- test -- Song Categories -- Add One Category --

        s.categories.append(mgr._list[0])
        
        assert s.categories.has_item(mgr._list[0]) == True 
        assert s.categories.has_item(mgr._list[1]) == False 
        
# -- test -- Song Categories -- Add One Category -- Restore from DB

        sp.Update(s, all = True)
        
        ss = songs.Song(s._id)
        sp.Restore(ss, all = True)
        
        assert ss.categories.has_item(mgr._list[0]) == True 
        assert ss.categories.has_item(mgr._list[1]) == False 
                
# -- test -- Song Categories -- Set Two Categories --

        s.categories.append(mgr._list[1])
        assert s.categories.has_item(mgr._list[0]) == True 
        assert s.categories.has_item(mgr._list[1]) == True 
        sp.Update(s, all = True)

        ss = songs.Song(s._id)
        assert ss.categories.has_item(mgr._list[0]) == False 
        assert ss.categories.has_item(mgr._list[1]) == False 

        sp.Restore(ss, all = True)
        assert ss.categories.has_item(mgr._list[0]) == True 
        assert ss.categories.has_item(mgr._list[1]) == True 
        
# -- test -- Song Categories -- Remove One Set Another --

        s.categories.remove(mgr._list[0])
        sp.Update(s)
        
        ss = songs.Song(s._id)
        assert ss.categories.has_item(mgr._list[0]) == False 
        assert ss.categories.has_item(mgr._list[1]) == False 

        sp.Restore(ss, all = True)
        assert ss.categories.has_item(mgr._list[0]) == False 
        assert ss.categories.has_item(mgr._list[1]) == True 
        
        
