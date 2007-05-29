
# ==============================================================================

class DbException(Exception):
    pass

class Peer(object):
    # --------------------------------------------------------------------------
    def __init__(self, conn):
        self._conn = conn
        self.__log = False
        
    # --------------------------------------------------------------------------
    def Update(self, obj = None):
        """ Placeholder """
        raise DbException('Error while updating object with ID %d' % (self._id,))        
        
    # --------------------------------------------------------------------------
    def Delete(self, obj = None):
        """ Placeholder """
        raise DbException('Error while deleting object with ID %d' % (self._id,))

    # --------------------------------------------------------------------------
    def _ExecuteUpdate(self, obj, sql, data):
        # add ID if needed
        if obj and obj._id <> -1:
            ldata = data + (obj._id,)
        else:
            ldata = data
                        
        if self.__log:
            print 'SQL:', sql
            print 'SQL:', ldata

        r = self._conn.execute(sql, ldata)                                                                        

        if r:
            self._conn.commit()            
            if obj and obj._id == -1:
                obj._id = r.lastrowid
        else:
            if obj and obj._id <> -1:
                self._UpdateError(obj)
            else:
                self._InsertError(obj)

    # --------------------------------------------------------------------------
    def _ExecuteRestore(self, obj, sql, all = False):        
        if obj:
            self._CheckValidId(obj)

            if self.__log:
                print 'SQL:', sql, '(ID = %d)' % (obj._id,)    
            if not all:
                r = self._conn.execute(sql, (obj._id,)).fetchone()
            else:
                r = self._conn.execute(sql, (obj._id,))

        else:
            if self.__log:
                print 'SQL:', sql
            r = self._conn.execute(sql)
                
        if r:
            return r
        else:
            self._RestoreError(obj)

    # --------------------------------------------------------------------------
    def _ExecuteDelete(self, obj, sql):        
        if obj:
            self._CheckValidId(obj)
        
            if self.__log:
                print 'SQL:', sql, '(ID = %d)' % (obj._id,)
        
            if self._conn.execute(sql, (obj._id,)):
                self._conn.commit()
        else:
            if self.__log:
                print 'SQL:', sql
        
            if self._conn.execute(sql):
                self._conn.commit()
        
    # --------------------------------------------------------------------------
    def _RestoreError(self, obj, msg = ''):
        s = 'Error while restoring object with ID %d' % (obj._id,)
        if msg <> '':
            s = s + ". Message: '" + msg + "'"
        raise DbException(s)

    def _InsertError(self, obj):
        raise DbException('Error while inserting object with ID %d' % (obj._id,))

    def _UpdateError(self, obj):
        raise DbException('Error while updating object with ID %d' % (obj._id,))

    def _DeleteError(self, obj):
        raise DbException('Error while deleting object with ID %d' % (obj._id,))

    # --------------------------------------------------------------------------
    def _CheckValidId(self, obj):
        if obj._id < 1:
            raise DbException('No valid ID is given for update / restore or delete!')

    # --------------------------------------------------------------------------
    def EnableLog(self):
        self.__log = True

# ==============================================================================

class Object(object):
    def __init__(self, id = -1):
        """ Default constructor for the DbObject
            id: If given, should be the ID with which it can be restored 
            from the DB """
        self._id = id
        self._changed = False

    def _Changed(self, changed = True):
        """ Mark changed, so that the update action can be skipped or not """
        self._changed = changed

       
