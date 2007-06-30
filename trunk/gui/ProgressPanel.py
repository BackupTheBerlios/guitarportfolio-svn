import wx
import wx.xrc as xrc
from wx.lib.pubsub import Publisher
import xmlres, viewmgr
from objs import songs

class ProgressPanel(wx.Panel):
    def __init__(self, parent, id = wx.ID_ANY):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "ProgressPanel")
        self.PostCreate(pre)

        self.__logDate = xrc.XRCCTRL(self, "ID_LOGDATE")
        self.__accuracy = xrc.XRCCTRL(self,"ID_ACC_SLIDER")
        self.__accuracyNr = xrc.XRCCTRL(self,"ID_GRADE_ACC")
        self.__estimated = xrc.XRCCTRL(self,"ID_COMP_SLIDER")
        self.__estimatedNr = xrc.XRCCTRL(self,"ID_GRADE_COMP")
        self.__percent = xrc.XRCCTRL(self,"ID_COMPLETED")
        self.__minutes = xrc.XRCCTRL(self,"ID_MIN_STUDIED")
        self.__minuteButton = xrc.XRCCTRL(self,"ID_ADD_STUDYTIME")
        self.__status = xrc.XRCCTRL(self,"ID_NEW_STATUS")
        self.__statusButton = xrc.XRCCTRL(self,"ID_CHANGE_STATUS")
        self.__log = xrc.XRCCTRL(self,"ID_LOG_TEXT")
        self.__submitButton = xrc.XRCCTRL(self,"ID_SUBMIT")
        self.__useCustom = xrc.XRCCTRL(self, "ID_USE_CUSTOM")
        self.__customTime = xrc.XRCCTRL(self, "ID_CUSTOM_TIME")

        self.__status.SetSelection(0)

        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.__OnAccuracyEnd, self.__accuracy)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.__OnAccuracyScroll, self.__accuracy)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.__OnCompletedEnd, self.__estimated)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.__OnCompletedScroll, self.__estimated)
        self.Bind(wx.EVT_BUTTON, self.__OnSubmitComment, self.__submitButton)
        self.Bind(wx.EVT_CHECKBOX, self.__OnUseCustomDate, self.__useCustom) 
        self.Bind(wx.EVT_BUTTON, self.__OnStudyTimeSubmit, self.__minuteButton)

        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_CLEAR_DATA)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_UPDATED)

    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message): 
        """ Handler to update the view when a song is selected """

        song = message.data

        # set all controls to enabled / disabled
        self.__UpdateAllowEdit(song)
        
        # by default, we do not set a custom date / time
        self.__useCustom.SetValue(False)                 
        self.__log.SetValue('')
        
        if song:                    
            self.__accuracy.SetValue(song._percAccuracy)
            self.__estimated.SetValue(song._percCompleted)
            self.__accuracyNr.SetLabel('[%.02i]' % (song._percAccuracy,))
            self.__estimatedNr.SetLabel('[%.02i]' % (song._percCompleted,))            
            self.__percent.SetLabel('%i %%' % (((song._percCompleted * 10) + (song._percAccuracy * 10)) / 2))   
        else:
            self.__accuracyNr.SetLabel('[00]')
            self.__estimatedNr.SetLabel('[00]')
            self.__percent.SetLabel('0%')
            self.__accuracy.SetValue(0)
            self.__estimated.SetValue(0)
    
    #---------------------------------------------------------------------------
    def __OnSongUpdated(self, message):
        """ Handle an updated song """
        
        # when status is updated, some stuff needs to be disabled
        self.__UpdateAllowEdit(message.data)

    #---------------------------------------------------------------------------
    def __UpdateAllowEdit(self, song):
        """ Allow or disallow editing based upon a song being present or
            not, etc """
    
        allow_edit = True if (song and (song._status != songs.SS_POSTPONED and \
                                        song._status != songs.SS_NOT_STARTED)) else False
        
        self.__accuracy.Enable(allow_edit)
        self.__estimated.Enable(allow_edit)
        self.__minutes.Enable(allow_edit)
        self.__minuteButton.Enable(allow_edit)
        self.__log.Enable(allow_edit)
        self.__submitButton.Enable(allow_edit)
        self.__logDate.Enable(allow_edit)
        self.__useCustom.Enable(allow_edit)
        self.__customTime.Enable(allow_edit)    

        # we dissalow changing the status when we set he flag
        # to back-annotate some things..
        custom = self.__useCustom.GetValue()
        self.__status.Enable(allow_edit and not custom)
        self.__statusButton.Enable(allow_edit and not custom)

    # --------------------------------------------------------------------------
    def __OnUseCustomDate(self, event):
        """ Event handler for setting a custom date to be logged in the database
            log. Very handy if people want to back-annotate their progress """
        
        # unfortunately, we do not support status changes in the past
        # as it is very hard to verify which status a song had at a given
        # time and date. Maybe some time when I find out how to perform 
        # complex queries
        self.__UpdateAllowEdit(viewmgr.Get()._selectedSong)
        
    # --------------------------------------------------------------------------
    def __OnSubmitComment(self, event):
        """ Submit text to the log """
        
        # signal the change to the view manager, and update the song
        song = viewmgr.Get()._selectedSong
        if song:                    
            viewmgr.signalAddComment(song, self.__log.GetValue())
            self.__log.SetValue('')
         
    # --------------------------------------------------------------------------
    def __OnAccuracyEnd(self, event): 
        """ Handler to update the song with the % completed accuracy """

        # signal the change to the view manager, and update the song
        song = viewmgr.Get()._selectedSong
        if song:                    
            viewmgr.signalAccuracyChange(song, self.__accuracy.GetValue())

    # --------------------------------------------------------------------------
    def __OnAccuracyScroll(self, event): 
        """ Handler to show live update on the accuracy """
        
        song = viewmgr.Get()._selectedSong
        if song:                    
            # determine the accuracy % and the total % and live update 
            acc_number = self.__accuracy.GetValue()
            self.__accuracyNr.SetLabel('[%.2i]' % (acc_number,))
            self.__percent.SetLabel('%i %%' % (((song._percCompleted * 10) + (acc_number * 10)) / 2))
        
    # --------------------------------------------------------------------------
    def __OnCompletedEnd(self, event):
        """ Handler to update the song with the % completed percentage """

        # signal the change to the view manager, and update the song
        song = viewmgr.Get()._selectedSong
        if song:                    
            viewmgr.signalCompletedChange(song, self.__estimated.GetValue())

    # --------------------------------------------------------------------------
    def __OnCompletedScroll(self, event):
        """ Handler to show the live update of the completed status """     

        song = viewmgr.Get()._selectedSong
        if song:                    
            # determine the accuracy % and the total % and live update 
            cmp_number = self.__estimated.GetValue()
            self.__estimatedNr.SetLabel('[%.2i]' % (cmp_number,))
            self.__percent.SetLabel('%i %%' % (((song._percAccuracy * 10) + (cmp_number * 10)) / 2))

    # --------------------------------------------------------------------------
    def __OnStudyTimeSubmit(self, event):
        """ Handler to add study time to the log """
        
        # add studytime to log, notify user when the 
        # time is illegal
        song = viewmgr.Get()._selectedSong
        if song:                    
            studytime = 0
            try:
                studytime = int(self.__minutes.GetValue())
            except ValueError:
                pass
                
            if studytime:
                viewmgr.signalAddStudyTime(song, studytime)
            else:
                wx.MessageBox('The studytime is invalid, please enter a number!', 'Error', wx.ICON_HAND | wx.OK)
