import os, os.path, sys, datetime

import wx
from wx.lib.pubsub import Publisher
import wx.xrc as xrc
import db, db.engine, db.log_peer
from objs import log, linkmgt
import appcfg, xmlres, viewmgr, htmlparse
             
class SongLogPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongLogPanel")
        self.PostCreate(pre)
        
        self._refreshButton = xrc.XRCCTRL(self, "ID_REFRESH")
        self._logArea = xrc.XRCCTRL(self, "ID_LOGAREA")
        self._critSelectTime = xrc.XRCCTRL(self, "ID_TIME_PERIOD")
        self._critProgress = xrc.XRCCTRL(self, "ID_CRIT_PROGRESS")
        self._critStudyTime = xrc.XRCCTRL(self, "ID_CRIT_STUDYTIME")
        self._critStatus = xrc.XRCCTRL(self, "ID_CRIT_STATUS")
        self._critComment = xrc.XRCCTRL(self, "ID_CRIT_COMMENT")
        self._sortAsc = xrc.XRCCTRL(self, "ID_SORT_ASCENDING")
        self._sortDesc = xrc.XRCCTRL(self, "ID_SORT_DESCENDING")
        
        self.Bind(wx.EVT_BUTTON, self.__OnRefresh, self._refreshButton)
        
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_CLEAR_DATA)
        Publisher().subscribe(self.__OnAppReady, viewmgr.SIGNAL_APP_READY)
        Publisher().subscribe(self.__OnAppQuit, viewmgr.SIGNAL_APP_QUIT)
        
    # --------------------------------------------------------------------------
    def __OnRefresh(self, event):
        song = viewmgr.Get()._selectedSong
        
        # determine which types should be restored
        log_types = []
        if self._critProgress.GetValue():
            log_types.append(log.LOG_PROGRESS_CHANGE_ACC)
            log_types.append(log.LOG_PROGRESS_CHANGE_CMP)
        if self._critStudyTime.GetValue():
            log_types.append(log.LOG_STUDYTIME)
        if self._critStatus.GetValue():
            log_types.append(log.LOG_STATUSCHANGE)
        if self._critComment.GetValue():
            log_types.append(log.LOG_COMMENT)
        
        # if we have no log types selected, we make the list
        # none again, so that the restore peer does not use the criteria
        if len(log_types) == 0:
            log_types = None
            
        # when we have an end date selected, constuct one
        end_date = None
        date_select = self._critSelectTime.GetSelection()
        if date_select > 0:
            end_date = datetime.datetime.now() 
            if date_select == 1:        # this day
               end_date -= datetime.timedelta(days = 1)
            elif date_select == 2:        # last week
               end_date -= datetime.timedelta(weeks = 1)
            elif date_select == 3:        # last month
               end_date -= datetime.timedelta(weeks = 4)
            elif date_select == 4:        # last six months
               end_date -= datetime.timedelta(days = 183)
            elif date_select == 5:        # last year
               end_date -= datetime.timedelta(days = 365)
               
        # restore all log entries that match the criteria
        if song:
            lp = db.log_peer.LogSetPeer(db.engine.GetDb())
            objs = lp.Restore(song._id, self._sortAsc.GetValue(), log_types, end_date)
            
            # create a log 
            if objs:
                page = htmlparse.ParseSongLog(song, objs)
                self._logArea.SetPage(page)                
            else:
                self._logArea.SetPage('')

    # --------------------------------------------------------------------------
    def __OnAppReady(self, message):
        """ Handler to set all the configuration from the settings in the controls """
        
        cfg = appcfg.Get()
        if cfg.HasGroup('log'):
            self._critSelectTime.SetSelection(cfg.ReadInt(appcfg.CFG_LOG_SELECTTIME, 0))
            self._critProgress.SetValue(cfg.ReadInt(appcfg.CFG_LOG_PROGRESS, 0) != 0)
            self._critStudyTime.SetValue(cfg.ReadInt(appcfg.CFG_LOG_STUDY, 0) != 0)
            self._critStatus.SetValue(cfg.ReadInt(appcfg.CFG_LOG_STATUS, 0) != 0)
            self._critComment.SetValue(cfg.ReadInt(appcfg.CFG_LOG_COMMENT, 0) != 0)
            if cfg.ReadInt(appcfg.CFG_LOG_SORT, 0) == 0: 
                self._sortAsc.SetValue(True)
            else:
                self._sortDesc.SetValue(True)        

    # --------------------------------------------------------------------------
    def __OnAppQuit(self, message):
        """ Handler to store all configuration to the settings """
        
        cfg = appcfg.Get()
        cfg.WriteInt(appcfg.CFG_LOG_SELECTTIME, self._critSelectTime.GetSelection())
        cfg.WriteInt(appcfg.CFG_LOG_PROGRESS, 1 if self._critProgress.GetValue() else 0)
        cfg.WriteInt(appcfg.CFG_LOG_STUDY, 1 if self._critStudyTime.GetValue() else 0)
        cfg.WriteInt(appcfg.CFG_LOG_STATUS, 1 if self._critStatus.GetValue() else 0)
        cfg.WriteInt(appcfg.CFG_LOG_COMMENT, 1 if self._critComment.GetValue() else 0)
        cfg.WriteInt(appcfg.CFG_LOG_SORT, 0 if self._sortAsc.GetValue() else 1)

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
        self._critProgress.Enable(song != None)
        self._critStudyTime.Enable(song != None)
        self._critStatus.Enable(song != None)
        self._critComment.Enable(song != None)
        self._sortAsc.Enable(song != None)
        self._sortDesc.Enable(song != None)
        
