
from wx.lib.pubsub import Publisher

import signals
import dbobject

class Tab(dbobject.DbObject):
    """ This class manages a list of tabs from the database restored with the ID
        of the current song """

    def __init__(self, id = -1):
        super(Tab, self).__init__(id) 
        self._name = ''
        self._text = '' 
        self._song = None      
    
    def Insert(self, song_id, conn):
        r = conn.execute(
                         , 
                         )
        if r:
            self.id = r.lastrowid
            conn.commit()
        else:
            self._insertError()

    def Update(self, conn):
        # perform an update
        r = conn.execute('update tabs set name = ?, text = ? where id = ?', 
                         (self._Name, self._Text, self.id))                                                                        
        if r:
            conn.commit()
        else:
            self._updateError()

    def Delete(self, conn):
        r = conn.execute('delete from tabs where id = ?', (self.id,))
        if r:
            conn.commit()
        else:
            self._deleteError()
    
    
#------------------------------------------------------------------------------

class TabList(object):
    """ This class manages a list of tabs from the database restored with the ID
        of the current song """

    def __init__(self):     
        self._List = []
                      
    def PopulateTabs(self, song_id, conn):
        """ Populate the tabs that belong to the song """
        # TODO: Issue a tabs clear??
        self._List = []
        r = conn.execute('select id from tabs where song_id = ?' , (song_id,))
        for t in r:
            tab = Tab(t[0])
            tab.Restore(conn)
            self._List.append(tab)
            Publisher().sendMessage(signals.TAB_RESTORED, tab)

    def UpdateTab(self, tab, conn):
        """ Update the tab in the database """
        if tab in self._List:
            tab.Update(conn)
            Publisher().sendMessage(signals.TAB_UPDATED, tab)
    
    def DeleteTab(self, tab, conn):
        """ Delete the tab from the database """
        if tab in self._List:
            self._List.remove(tab)
            tab.Delete(conn)
            Publisher().sendMessage(signals.TAB_DELETED, tab)

    def AddTab(self, tab, song_id, conn):
        """ Add a tab to the database """
        if tab not in self._List:
            tab.Insert(song_id, conn)
            self._List.append(tab)
            Publisher().sendMessage(signals.TAB_ADDED, tab)

    def getCount(self): return len(self._List)

