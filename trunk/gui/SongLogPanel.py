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
        # UGLY HACK!
        song = viewmgr.Get()._selectedSong
        
        if song:
            lp = db.log_peer.LogSetPeer(db.engine.GetDb())
            objs = lp.Restore(song._id)
            if objs:
                str = ''
                for obj in objs:
                    str += obj.tostr() + '<br>'
                self._logArea.SetPage(str)
            else:
                self._logArea.SetPage('')
                
