import db
from wx.lib.pubsub import Publisher

class TabPeer(db.base.Peer):
    def __init__(self, conn):
        super(TabPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, obj):
        sql = 'select name, text from tabs where id = ?'
        
        r = self._ExecuteRestore(obj, sql)
        obj._name = r[0]
        obj._text = r[1]
                
    # --------------------------------------------------------------------------
    def Update(self, obj):
        data = (obj._name, 
                obj._text) 

        if obj._id == -1:
            sql = 'insert into tabs (name, text) values (?, ?)'
        else:
            sql = 'update tabs set name = ?, text = ? where id = ?'                                                                        
        
        self._ExecuteUpdate(obj, sql, data)

    # --------------------------------------------------------------------------
    def Delete(self, obj):
        sql = 'delete from tabs where id = ?'
        self._ExecuteDelete(obj, sql)

