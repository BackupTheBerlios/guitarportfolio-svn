import os
import os.path
import sys

import wx
from wx.lib.pubsub import Publisher
import wx.xrc as xrc
import db, db.engine, db.log_peer
from objs import songfilter

from objs import linkmgt
import appcfg, xmlres, viewmgr, htmlparse
             
class SongLogPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongLogPanel")
        self.PostCreate(pre)
        
        self._refreshButton = xrc.XRCCTRL(self, "ID_REFRESH")
        self._logArea = xrc.XRCCTRL(self, "ID_LOGAREA")
        self._critSelectTime = xrc.XRCCTRL(self, "ID_TIME_PERIOD")
        self._critSelectAll = xrc.XRCCTRL(self, "ID_ALL_CRITERIA")
        self._critProgress = xrc.XRCCTRL(self, "ID_CRIT_PROGRESS")
        self._critStudyTime = xrc.XRCCTRL(self, "ID_CRIT_STUDYTIME")
        self._critStatus = xrc.XRCCTRL(self, "ID_CRIT_STATUS")
        self._critComment = xrc.XRCCTRL(self, "ID_CRIT_COMMENT")
        self._sortAsc = xrc.XRCCTRL(self, "ID_SORT_ASCENDING")
        self._sortDesc = xrc.XRCCTRL(self, "ID_SORT_DESCENDING")
        
        self.Bind(wx.EVT_BUTTON, self.__OnRefresh, self._refreshButton)
        
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_CLEAR_DATA)
        
    # --------------------------------------------------------------------------
    def __OnRefresh(self, event):
        song = viewmgr.Get()._selectedSong
        
        # restore all log entries that match the criteria
        if song:
            lp = db.log_peer.LogSetPeer(db.engine.GetDb())
            objs = lp.Restore(song._id)
            
            # create a log 
            if objs:
                page = htmlparse.ParseSongLog(song, objs)
                self._logArea.SetPage(page)                
            else:
                self._logArea.SetPage('')

    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Event submitted when a song is selected or no selection is present
            or the application is initialized """
        
        # always refresh the log to blank
        self._logArea.SetPage('')
        
        # enable controls based upon a song or not
        song = message.data            
        self._critSelectTime.Enable(song != None)
        self._refreshButton.Enable(song != None)
        self._logArea.Enable(song != None)
        self._critSelectAll.Enable(song != None)
        self._critProgress.Enable(song != None)
        self._critStudyTime.Enable(song != None)
        self._critStatus.Enable(song != None)
        self._critComment.Enable(song != None)
        self._sortAsc.Enable(song != None)
        self._sortDesc.Enable(song != None)
        
