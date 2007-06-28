import os
import os.path
import sys

import wx
from wx.lib.pubsub import Publisher
import wx.xrc as xrc
import db, db.engine, db.log_peer
from objs import songfilter

from objs import linkmgt
import appcfg, xmlres, viewmgr
             
class SongLogPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongLogPanel")
        self.PostCreate(pre)
        
        self._refreshButton = xrc.XRCCTRL(self, "ID_REFRESH")
        self._logArea = xrc.XRCCTRL(self, "ID_LOGAREA")
        
        self.Bind(wx.EVT_BUTTON, self.__OnRefresh, self._refreshButton)
        
    # --------------------------------------------------------------------------
    def __OnRefresh(self, event):
        song = viewmgr.Get()._selectedSong
        
        # restore all log entries that match the criteria
        if song:
            lp = db.log_peer.LogSetPeer(db.engine.GetDb())
            objs = lp.Restore(song._id)
            
            # create a log 
            if objs:
                str = '<html><body>\n' + \
                      '<table><tr><td><b>Date</b></td><td><b>Time</b></td><td><b>Type</b></td><td><b>Information</b></td></tr>'
                alt = False
                for obj in objs:
                    str += '<tr><td nowrap>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (obj._date.strftime('%d %B %Y'),
                                                                                        obj._date.strftime('%H:%M'),
                                                                                        'Bla', 
                                                                                        obj._text)
                str += '</table></body></html>' 
                self._logArea.SetPage(str)
            else:
                self._logArea.SetPage('')
                
