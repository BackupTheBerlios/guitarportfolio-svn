import db

class Tab(db.base.Object):
    def __init__(self, id = -1):
        super(Tab, self).__init__(id) 
        self._name = ''
        self._text = ''     
    
# =============================================================================
    
class TabList(db.base.Object):
    def __init__(self):     
        self._list = []
                                                
    # -------------------------------------------------------------------------
    def DeleteTab(self, tab):
        """ Delete the tab from the database """
        if tab in self._list:
            self._list.remove(tab)
            tab.Delete(conn)

    # -------------------------------------------------------------------------
    def AddTab(self, tab):
        """ Add a tab to the database """
        if tab not in self._list:
            self._list.append(tab)

    # -------------------------------------------------------------------------
    def GetCount(self): return len(self.__mList)

