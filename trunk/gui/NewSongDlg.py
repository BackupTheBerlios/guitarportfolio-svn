# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sun May 13 11:47:41 2007 from D:\personal\src\GuitarPortfolio\branches\db_revival\gui\guitarportfolio.wxg

import datetime
import os.path
import wx

import db.engine
import db.songs_peer

from objs import tuning_mgr

import appcfg
import CategoriesDlg

# begin wxGlade: dependencies
# end wxGlade

class NewSongDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: NewSongDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "Enter Artist")
        self.__artist = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_2 = wx.StaticText(self, -1, "Enter Song Title")
        self.__title = wx.TextCtrl(self, -1, "")
        self.label_4 = wx.StaticText(self, -1, "Song Options")
        self.label_5 = wx.StaticText(self, -1, "Number Of Bars")
        self.__barCount = wx.SpinCtrl(self, -1, "1", min=0, max=100)
        self.label_15 = wx.StaticText(self, -1, "Capo")
        self.__capoSelect = wx.ComboBox(self, -1, choices=["No Capo"], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_6 = wx.StaticText(self, -1, "Song Date")
        self.__songDate = wx.DatePickerCtrl(self, -1, style=wx.DP_SHOWCENTURY)
        self.__dateUnknown = wx.CheckBox(self, -1, "Date is unknown")
        self.__yearOnly = wx.CheckBox(self, -1, "Year Only")
        self.label_7 = wx.StaticText(self, -1, "Difficulty")
        self.__difficulty = wx.Choice(self, -1, choices=["Easy", "Normal", "Intermediate", "Advanced", "Hard", "Impossible"])
        self.label_9 = wx.StaticText(self, -1, "Status Of Song")
        self.__songStatus = wx.Choice(self, -1, choices=["In Progress", "Not Practicing", "Completed!", "TODO"])
        self.label_11 = wx.StaticText(self, -1, "Guitar Tuning")
        self.__tuningPre = wx.RadioButton(self, -1, "Select")
        self.__tuningSelect = wx.Choice(self, -1, choices=[])
        self.__tuningText = wx.StaticText(self, -1, "E  A  D  G  B  E")
        self.__tuningCustom = wx.RadioButton(self, -1, "Custom")
        self.__customTuning = wx.TextCtrl(self, -1, "")
        self.label_3 = wx.StaticText(self, -1, "Song Categories")
        self.__editCategories = wx.Button(self, -1, "&Edit ...")
        self.label_24 = wx.StaticText(self, -1, "Work Subdirectory")
        self.__workDir = wx.ComboBox(self, -1, choices=["{artist}\\{title}", "{artist}", "{title}", "{artist} - {title}", "{title}\\{artist}"], style=wx.CB_DROPDOWN)
        self.label_25 = wx.StaticText(self, -1, "Example:")
        self.__workDirExample = wx.StaticText(self, -1, "d:\\somedir\\{artist}-{title}")
        self.__Ok = wx.Button(self, wx.ID_OK, "")
        self.__Cancel = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.__OnChangeRelPathExample, self.__artist)
        self.Bind(wx.EVT_COMBOBOX, self.__OnChangeRelPathExample, self.__artist)
        self.Bind(wx.EVT_TEXT, self.__OnChangeRelPathExample, self.__title)
        self.Bind(wx.EVT_CHECKBOX, self.__OnDateUnknown, self.__dateUnknown)
        self.Bind(wx.EVT_CHOICE, self.OnSelectItem, self.__tuningSelect)
        self.Bind(wx.EVT_BUTTON, self.__OnEditCategories, self.__editCategories)
        self.Bind(wx.EVT_TEXT, self.__OnWorkDirChange, self.__workDir)
        self.Bind(wx.EVT_COMBOBOX, self.__OnWorkDirChange, self.__workDir)
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.__Ok)
        # end wxGlade
        
        # go and find all unique artists, and add them to the combo
        # TODO: Artists which are mistyped (lower / upper) should not appear twice
        sp = db.songs_peer.SongArtistSetPeer(db.engine.GetDb())
        artists = sp.Restore(unique = True)

        self.__artist.Clear()
        for a in artists:
            self.__artist.Append(a)    

        # populate the tunings205
        self.__tuningSelect.Clear()
        for t in tuning_mgr.Get()._list:
            self.__tuningSelect.Append(t._tuningName, t._id)
        
        # fill out the Capo combo
        self.__capoSelect.Clear()
        self.__capoSelect.Append('No Capo')
        for i in xrange(1, 15):
          self.__capoSelect.Append('Fret %d' % i)

        self.__song = None

    # --------------------------------------------------------------------------
    def __set_properties(self):
        # begin wxGlade: NewSongDlg.__set_properties
        self.SetTitle("Enter Song properties")
        self.__capoSelect.SetSelection(-1)
        self.__difficulty.SetSelection(1)
        self.__songStatus.SetSelection(3)
        self.__tuningPre.SetValue(1)
        self.__tuningText.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.__workDir.SetSelection(-1)
        self.__workDirExample.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.__Ok.SetDefault()
        # end wxGlade

    # --------------------------------------------------------------------------
    def __do_layout(self):
        # begin wxGlade: NewSongDlg.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(9, 2, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(2, 2, 0, 0)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_1, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer_5.Add(self.__artist, 0, wx.ALL|wx.EXPAND, 5)
        sizer_5.Add(self.label_2, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer_5.Add(self.__title, 0, wx.ALL|wx.EXPAND, 5)
        sizer_5.Add(self.label_4, 0, wx.ALL, 5)
        sizer_6.Add((10, 20), 0, 0, 0)
        grid_sizer_1.Add(self.label_5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add(self.__barCount, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add(self.label_15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add(self.__capoSelect, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(sizer_21, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.__songDate, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.__dateUnknown, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.__yearOnly, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(sizer_10, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.__difficulty, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.label_9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.__songStatus, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(self.__tuningPre, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_9.Add(self.__tuningSelect, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_9.Add(self.__tuningText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(sizer_9, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.__tuningCustom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(self.__customTuning, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.__editCategories, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.label_24, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.__workDir, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_25, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.__workDirExample, 0, wx.ALL, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        sizer_6.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_7.Add(self.__Ok, 0, wx.ALL, 5)
        sizer_7.Add(self.__Cancel, 0, wx.ALL, 5)
        sizer_5.Add(sizer_7, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizer_5)
        sizer_5.Fit(self)
        self.Layout()
        # end wxGlade

    # --------------------------------------------------------------------------
    def SaveToSong(self, song):
        song._artist = self.__artist.GetValue()
        song._title = self.__title.GetValue()
        song._barCount = self.__barCount.GetValue()
        song._difficulty = self.__difficulty.GetSelection()
        song._status = self.__songStatus.GetSelection()
        dt = self.__songDate.GetValue()
        song._time = datetime.datetime(dt.GetYear(), dt.GetMonth() + 1, dt.GetDay())
        idx = self.__tuningSelect.GetSelection()
        if self.__tuningPre.GetValue() and idx <> -1:
            song._tuning = tuning_mgr.Get().GetTuningById(self.__tuningSelect.GetClientData(idx))
        else:
            song._tuning = None
        song._altTuning = self.__customTuning.GetValue()
        song._dateUnknown = self.__dateUnknown.GetValue()
        song._yearOnly = self.__yearOnly.GetValue()
        song._capoOnFret = self.__capoSelect.GetSelection()
        song._relativePath = self.__workDir.GetValue()
                        
    # --------------------------------------------------------------------------
    def LoadFromSong(self, song):
        self.__song = song
        self.__artist.SetValue(song._artist)
        self.__title.SetValue(song._title)
        self.__barCount.SetValue(song._barCount)
        self.__difficulty.SetSelection(song._difficulty)
        self.__songStatus.SetSelection(song._status)

        dt = song._time
        self.__songDate.SetValue(wx.DateTimeFromDMY(dt.day, dt.month - 1, dt.year))

        # do tuning, if we have a relation, look it up else make it custom
        if song._tuning:
            self.__tuningPre.SetValue(True)
            idx = self.__tuningSelect.FindString(song._tuning._tuningName)
            if idx <> wx.NOT_FOUND:
                self.__tuningSelect.SetSelection(idx)
                self.__tuningText.SetLabel(song._tuning._tuningText)
            else:
                self.__tuningCustom.SetValue(True)
        else:
            self.__tuningCustom.SetValue(True)
            self.__tuning.SetSelection(-1)
            self.__tuningText.SetLabel('[Custom Selection]')

        self.__customTuning.SetValue(song._altTuning)
        self.__dateUnknown.SetValue(song._dateUnknown)
        self.__songDate.Enable(not song._dateUnknown)
        self.__yearOnly.SetValue(song._yearOnly)
        self.__yearOnly.Enable(not song._dateUnknown)
        self.__capoSelect.SetSelection(song._capoOnFret)
        self.__workDir.SetValue(song._relativePath)
        self.__SyncExamplePath()

    # --------------------------------------------------------------------------
    def OnOk(self, event): # wxGlade: NewSongDlg.<event_handler>
        if self.__barCount.GetValue() < 0:
            wx.MessageBox('Please enter the number of bars in the song, or 0 for none', style = wx.ICON_EXCLAMATION | wx.OK)
            return
        if self.__artist.GetValue().strip() == '':
            wx.MessageBox('Please enter a valid artist', style = wx.ICON_EXCLAMATION | wx.OK)
            return
        if self.__title.GetValue().strip() == '':
            wx.MessageBox('Please enter a valid song title', style = wx.ICON_EXCLAMATION | wx.OK)
            return
        event.Skip()

    # --------------------------------------------------------------------------
    def OnSelectItem(self, event): # wxGlade: NewSongDlg.<event_handler>
        idx = self.__tuningSelect.GetSelection()
        if idx <> wx.NOT_FOUND:
            t = tuning_mgr.Get().GetTuningById(self.__tuningSelect.GetClientData(idx))
            self.__tuningText.SetLabel(t._tuningText)
            self.__tuningPre.SetValue(True)
        else:
            self.__tuningCustom.SetValue(True)

    # --------------------------------------------------------------------------
    def __OnEditCategories(self, event): # wxGlade: NewSongDlg.<event_handler>
        if self.__song:    
            dlg = CategoriesDlg.CategoriesDlg(self)
            dlg.SetCurrentSong(self.__song)
            if dlg.ShowModal() == wx.ID_OK:
                # update the categories
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.UpdateCategories(self.__song)            
            dlg.Destroy()
            
    # --------------------------------------------------------------------------
    def __OnDateUnknown(self, event): # wxGlade: NewSongDlg.<event_handler>
        self.__songDate.Enable(not self.__dateUnknown.GetValue())
        self.__yearOnly.Enable(not self.__dateUnknown.GetValue())

    # --------------------------------------------------------------------------
    def __OnWorkDirChange(self, event): # wxGlade: NewSongDlg.<event_handler>
        self.__SyncExamplePath()
        
    # --------------------------------------------------------------------------
    def __SyncExamplePath(self):
        """ Synchronise the example static text with the current song title and 
            artist, based upon the mask set in the WorkDir dropdown """
        text = appcfg.GetAbsWorkPath(workmask = self.__workDir.GetValue(), 
                                     artist = self.__artist.GetValue(),
                                     title = self.__title.GetValue())
        if text:
            self.__workDirExample.SetLabel(text)
        else:
            self.__workDirExample.SetLabel('N/A')        

    # --------------------------------------------------------------------------
    def __OnChangeRelPathExample(self, event): # wxGlade: NewSongDlg.<event_handler>
        """ Synchronize the relative path example upon changes to:
            - Artist field
            - Title field """
        self.__SyncExamplePath()

# end of class NewSongDlg
