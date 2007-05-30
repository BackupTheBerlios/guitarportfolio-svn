import datetime
from wx.lib.pubsub import Publisher

import db
from db import tabs_peer
from objs import songs, signals, tabs, tuning_mgr, category_mgr

#===============================================================================
             
class SongSetPeer(db.base.Peer):
    def __init__(self, conn):
        super(SongSetPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self):
        sql = 'select id from song'
        r = self._ExecuteRestore(None, sql, all = True)
        lst = []
        for c in r:
            sp = SongPeer(self._conn)
            song = songs.Song(id = c[0])
            sp.Restore(song)
            lst.append(song)
        return lst

#===============================================================================
             
class SongArtistSetPeer(db.base.Peer):
    def __init__(self, conn):
        super(SongArtistSetPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, unique = False):
        sql = 'select artist from song'
        r = self._ExecuteRestore(None, sql, all = True)
        lst = []
        for c in r:
            # only add when allowed
            if not (unique and c[0] in lst):
                lst.append(c[0])
        lst.sort()
        return lst

#===============================================================================
             
class SongCategoryListPeer(db.base.Peer):
    def __init__(self, conn):
        super(SongCategoryListPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, obj):
        sql = 'select category_id from songcats where song_id = ?'
        r = self._ExecuteRestore(obj, sql, all = True)
        lst = []
        for c in r:
            lst.append(c[0])
        return lst
        
    # --------------------------------------------------------------------------
    def Delete(self, obj):
        sql = 'delete from songcats where song_id = ?'
        r = self._ExecuteDelete(obj, sql)

    # --------------------------------------------------------------------------
    def Update(self, obj):
        if obj.categories.is_changed():
            self.Delete(obj)
            sql = 'insert into songcats (song_id, category_id) values (?, ?)'
            for c in obj.categories:
                data = (obj._id, c._id)
                self._ExecuteUpdate(None, sql, data)
            
            obj.categories.set_clean()
            Publisher().sendMessage(signals.SONG_DB_CAT_UPDATED, obj)        
    
# ==============================================================================

class SongTabListPeer(db.base.Peer):
    def __init__(self, conn):
        super(SongTabListPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, obj):
        sql = 'select tab_id from songtabs where song_id = ?'
        
        obj.tabs.prune()
        r = self._ExecuteRestore(obj, sql, all = True)
        p = tabs_peer.TabPeer(self._conn)        
        for t in r:
            tab = tabs.Tab(id = t[0])
            p.Restore(tab)
            obj.tabs.append(tab)        
        obj.tabs.set_restored()
            
    # --------------------------------------------------------------------------
    def Delete(self, obj):
        sql = 'delete from songtabs where song_id = ?'
        r = self._ExecuteDelete(obj, sql)

    # --------------------------------------------------------------------------
    def Update(self, obj):
        if obj.tabs.is_changed():
            # old tabs        
            sql = 'select tab_id from songtabs where song_id = ?'
            rows = self._conn.execute(sql, (obj._id,))
            old_tabs = []
            for r in rows:
                old_tabs.append(r[0])
                
            # does the song hold a tab that is not in the relation table?
            for tab in obj.tabs:
                if tab._id not in old_tabs:
                    # we have a new tab added
                    Publisher().sendMessage(signals.SONG_DB_TAB_ADDED, (obj, tab))
            
            # does the relation table hold a tab that is not in the song?
            for tab_id in old_tabs:
                tab = obj.tabs.find_id(tab_id)
                if tab:
                    Publisher().sendMessage(signals.SONG_DB_TAB_DELETED, (obj, tab))
            
            # now update the relations table
            self.Delete(obj)
            sql = 'insert into songtabs (song_id, tab_id) values (?, ?)'
            for c in obj.tabs:
                data = (obj._id, c._id)
                self._ExecuteUpdate(None, sql, data)   
            
#===============================================================================
           
class SongPeer(db.base.Peer):
    def __init__(self, conn):
        super(SongPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, obj, all = False):
        sql = 'select name, artist, barcount, difficulty, ' + \
               'songdate, status, lyrics, information, ' + \
               'tuning_alt, date_unknown, year_only, completed_perc, ' + \
               'accuracy_perc, capo_number, relpath, tuning_id, ' + \
               'time_added, time_started, time_completed, ' + \
               'time_postponed from song where id = ?' 
        r = self._ExecuteRestore(obj, sql)
      
        tuning_id = -1
        if r:
            obj._title = r[0]
            obj._artist = r[1]
            obj._barCount = int(r[2])
            if int(r[3]) not in songs.song_difficulty:
                self._restoreError('Song difficulty not in range!')
            else:
                obj._difficulty = int(r[3])
            if r[4] <> None:
                obj._time = datetime.datetime.strptime(r[4], '%Y %m %d')
            if int(r[5]) not in songs.song_status:
                self._restoreError('Song status not in range!')
            else:
                obj._status = int(r[5])
            obj._lyrics = r[6]
            obj._information = r[7]
            obj._altTuning = r[8]
            obj._dateUnknown = False if r[9] == 0 else True
            obj._yearOnly = False if r[10] == 0 else True
            obj._percCompleted = r[11]
            obj._percAccuracy = r[12]
            obj._capoOnFret = r[13] if (r[13] < 16) and (r[13] > 0) else 0
            obj._relativePath = r[14]
            tuning_id = r[15]
            if r[16] <> None:
                obj._timeAdded = datetime.datetime.strptime(r[16], '%Y %m %d')
            if r[17] <> None:
                obj._timeStarted = datetime.datetime.strptime(r[17], '%Y %m %d')
            if r[18] <> None:
                obj._timeCompleted = datetime.datetime.strptime(r[18], '%Y %m %d')
            if r[19] <> None:
                obj._timePostponed = datetime.datetime.strptime(r[19], '%Y %m %d')
        else:
            self._RestoreError('Cannot restore song with id %d' % (obj._id,))

        # tuning relation
        mgr = tuning_mgr.Get()
        obj._tuning = None if tuning_id == -1 \
                           else mgr.GetTuningById(tuning_id)

        # make sure we have an empty list
        obj.tabs.prune()
        
        if all:
            self.RestoreRelations(obj)
            
        Publisher().sendMessage(signals.SONG_DB_RESTORED, obj)

    # --------------------------------------------------------------------------
    def RestoreRelations(self, obj):
        """ Restore all that belongs to the song but is not part of the body """
        self.RestoreCategories(obj)
        self.RestoreTabs(obj)
    
    # --------------------------------------------------------------------------
    def RestoreTabs(self, obj):
        """ Restore the tabs, can be invoked after Restore """
        p = SongTabListPeer(self._conn)
        p.Restore(obj)
    
    # --------------------------------------------------------------------------
    def RestoreCategories(self, obj):
        """ Restore the category relations, can be invoked after Restore """
        mgr = category_mgr.Get()
        p = SongCategoryListPeer(self._conn)
        lst = p.Restore(obj)
        obj.categories.clear()
        for cat_id in lst:
            songcat = mgr.GetCategoryById(cat_id)
            obj.categories.append(songcat)
        obj.tabs.set_restored()

    # --------------------------------------------------------------------------
    def Update(self, obj, all = True):
        if obj._id == -1:
            sql = 'insert into song (name, artist, songdate, barcount, difficulty, ' + \
                   'status, lyrics, information, tuning_alt, date_unknown, year_only, ' + \
                   'tuning_id, completed_perc, accuracy_perc, capo_number, relpath, ' + \
                   'time_added, time_started, time_completed, time_postponed) ' + \
                   'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            sig = signals.SONG_DB_INSERTED

        else:
            sql = 'update song set name = ?, artist = ?, songdate = ?, ' + \
                  'barcount = ?, difficulty = ?, status = ?, lyrics = ?, ' + \
                  'information = ?, tuning_alt = ?, date_unknown = ?, ' + \
                  'year_only = ?, tuning_id = ?, completed_perc = ?, ' + \
                  'accuracy_perc = ?, capo_number = ?, relpath = ?, ' + \
                  'time_added = ?, time_started = ?, time_completed = ?, ' + \
                  'time_postponed = ? where id = ?'
            sig = signals.SONG_DB_UPDATED

        data = (obj._title, 
                obj._artist,
                obj._time.strftime('%Y %m %d'),
                obj._barCount,
                obj._difficulty,
                obj._status,
                obj._lyrics,
                obj._information,
                obj._altTuning,
                obj._dateUnknown,
                obj._yearOnly,
                obj._GetTuningId(),
                obj._percCompleted,
                obj._percAccuracy,
                obj._capoOnFret,
                obj._relativePath,
                obj._timeAdded.strftime('%Y %m %d'),
                obj._timeStarted.strftime('%Y %m %d'),
                obj._timeCompleted.strftime('%Y %m %d'),
                obj._timePostponed.strftime('%Y %m %d')) 
        self._ExecuteUpdate(obj, sql, data)

        if all:
            self.UpdateCategories(obj)
        
            # update the relations of the tabs
            p = SongTabListPeer(self._conn)
            p.Update(obj)
        
        Publisher().sendMessage(sig, obj)
            
    # --------------------------------------------------------------------------    
    def Delete(self, obj):
        sql = 'delete from song where id = ?'
        self._ExecuteDelete(obj, sql)
        
        # delete the category relations
        p = SongCategoryListPeer(self._conn)
        p.Delete(obj)
            
        # remove all tab relations that belong to this song
        p = SongTabListPeer(self._conn)
        p.Delete(obj)
        
        # remove tabs itself
        p = tabs_peer.TabPeer(self._conn)
        for t in obj.tabs:
            p.Delete(t)
                    
        Publisher().sendMessage(signals.SONG_DB_DELETED, obj)

    # --------------------------------------------------------------------------    
    def UpdateCategories(self, obj):
        # update the categories
        p = SongCategoryListPeer(self._conn)
        p.Update(obj)    
