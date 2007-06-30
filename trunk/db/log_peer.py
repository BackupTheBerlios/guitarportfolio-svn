import datetime
from wx.lib.pubsub import Publisher

import db
from objs import songs, log

#===============================================================================
             
class LogSetPeer(db.base.Peer):
    def __init__(self, conn):
        super(LogSetPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, song_id, sort_asc = True, log_types = None, start_date = None, end_date = None):
        
        # we restore this slightly out of the given framework to 
        # speed up the restore as the log items are not standard DB objects
        # and are subject to filtering as well
        
        sql = 'select id, log_date, log_text, log_type, log_value from logentry where song_id = ?'
        
        if log_types and len(log_types) > 0:
            logtype_qry = ''
            for l in log_types:
                if logtype_qry:
                    logtype_qry += ' or '
                logtype_qry += 'log_type = %i' % l
            sql += ' and (' + logtype_qry + ')'

        sql += ' order by log_date ' + ('asc' if sort_asc else 'desc')
                    
        r = self._conn.execute(sql, (song_id,))  
        
        lst = []
        if r:
            for item in r:
                obj = log.LogItem(id = item[0])
                obj._date = datetime.datetime.strptime(item[1], '%Y %m %d %H:%M:%S')
                obj._text = item[2]
                obj._type = item[3]
                obj._value = item[4]
                lst.append(obj)
                
        return lst

    # --------------------------------------------------------------------------
    def Delete(self, obj):
        """ Delete the log entries from the DB where the song ID matches """
        
        # obj is expected to be a song object
        sql = 'delete from logentry where song_id = ?'
        self._ExecuteDelete(obj, sql)

#===============================================================================
             
class LogPeer(db.base.Peer):
    def __init__(self, conn):
        super(LogPeer, self).__init__(conn)
        
    # --------------------------------------------------------------------------
    def Update(self, obj, song_id):
        """ Update / insert this object in the database. In this case it is always 
            inserting because log entries cannot be updated """
        
        # we must be sure insert is what we are going to do
        if obj._id != -1:
            raise Exception('Cannot update a LogEntry object, only insert new ones!!')
        
        sql = 'insert into logentry (song_id, log_date, log_text, log_type, log_value) ' \
                            'values (?, ?, ?, ?, ?)'

        data = (song_id, 
                obj._date.strftime('%Y %m %d %H:%M:%S'),
                obj._text,
                obj._type,
                obj._value)
        self._ExecuteUpdate(None, sql, data)
