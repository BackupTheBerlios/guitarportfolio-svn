import datetime
import os.path
import wx
import wx.xrc as xrc

import db.engine
import db.songs_peer

from objs import tuning_mgr, songs

import appcfg, xmlres, viewmgr
import CategoriesDlg

class NewSongDlg(wx.Dialog):
    def __init__(self, parent, id = wx.ID_ANY, nodb = False):
        pre = wx.PreDialog()
        xmlres.Res().LoadOnDialog(pre, parent, "NewSongPanel")
        self.PostCreate(pre)

        # if set we can use the category database peer to update the 
        # song in the DB, if not set, the song is not yet in the DB
        # and a higher update will take care of it
        self.__dbAllowed = not nodb

        self.__artist = xrc.XRCCTRL(self, "ID_ARTIST")
        self.__title = xrc.XRCCTRL(self, "ID_TITLE")
        self.__barCount = xrc.XRCCTRL(self, "ID_BARCOUNT")
        self.__capoSelect = xrc.XRCCTRL(self, "ID_CAPO")
        self.__songDate = xrc.XRCCTRL(self, "ID_SONG_DATE")
        self.__difficulty  = xrc.XRCCTRL(self, "ID_DIFFICULTY")
        self.__dateUnknown = xrc.XRCCTRL(self, "ID_DATE_UNKNOWN")
        self.__yearOnly = xrc.XRCCTRL(self, "ID_YEAR_ONLY")
        self.__tuningPre = xrc.XRCCTRL(self, "ID_STANDARD")
        self.__tuningSelect = xrc.XRCCTRL(self, "ID_TUNING_SELECT")
        self.__tuningText = xrc.XRCCTRL(self, "ID_TUNING_TEXT")
        self.__tuningCustom = xrc.XRCCTRL(self, "ID_CUSTOM")
        self.__customTuning = xrc.XRCCTRL(self, "ID_CUSTOM_TEXT")
        self.__workDir = xrc.XRCCTRL(self, "ID_WORK_SUBDIR")
        self.__workDirExample = xrc.XRCCTRL(self, "ID_EXAMPLE_TEXT")
        self.__songType = xrc.XRCCTRL(self, "ID_SONG_RIFF")
        
        self.__capoSelect.SetSelection(-1)
        self.__difficulty.SetSelection(1)
        self.__tuningPre.SetValue(1)
        self.__workDir.SetSelection(-1)
                
        self.Bind(wx.EVT_TEXT, self.__OnChangeRelPathExample, self.__artist)
        self.Bind(wx.EVT_COMBOBOX, self.__OnChangeRelPathExample, self.__artist)
        self.Bind(wx.EVT_TEXT, self.__OnChangeRelPathExample, self.__title)
        self.Bind(wx.EVT_CHECKBOX, self.__OnDateUnknown, self.__dateUnknown)
        self.Bind(wx.EVT_CHOICE, self.OnSelectItem, self.__tuningSelect)
        self.Bind(wx.EVT_BUTTON, self.__OnEditCategories, xrc.XRCCTRL(self, "ID_EDIT_CATS"))
        self.Bind(wx.EVT_TEXT, self.__OnWorkDirChange, self.__workDir)
        self.Bind(wx.EVT_COMBOBOX, self.__OnWorkDirChange, self.__workDir)
        self.Bind(wx.EVT_BUTTON, self.OnOk, xrc.XRCCTRL(self, "wxID_OK"))

        # TODO: Artists which are mistyped (lower / upper) should not appear twice
        sp = db.songs_peer.SongArtistSetPeer(db.engine.GetDb())
        artists = sp.Restore(unique = True)

        self.__artist.Clear()
        for a in artists:
            self.__artist.Append(a)    

        # populate the tunings
        self.__tuningSelect.Clear()
        for t in tuning_mgr.Get()._list:
            self.__tuningSelect.Append(t._tuningName, t._id)
        
        # fill out the Capo combo
        self.__capoSelect.Clear()
        self.__capoSelect.Append('No Capo')
        for i in xrange(1, 15):
          self.__capoSelect.Append('Fret %d' % i)

        self.__song = None

        self.__artist.SetFocus()

    # --------------------------------------------------------------------------
    def SaveToSong(self, song):
        song._artist = self.__artist.GetValue()
        song._title = self.__title.GetValue()
        song._barCount = self.__barCount.GetValue()
        song._difficulty = self.__difficulty.GetSelection()
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
        song._songType = songs.ST_TUTORIAL if self.__songType.GetValue() else songs.ST_NORMAL
                        
    # --------------------------------------------------------------------------
    def LoadFromSong(self, song):
        self.__song = song
        self.__artist.SetValue(song._artist)
        self.__title.SetValue(song._title)
        self.__barCount.SetValue(song._barCount)
        self.__difficulty.SetSelection(song._difficulty)

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
            self.__tuningSelect.SetSelection(-1)
            self.__tuningText.SetLabel('[Custom Selection]')

        self.__customTuning.SetValue(song._altTuning)
        self.__dateUnknown.SetValue(song._dateUnknown)
        self.__songDate.Enable(not song._dateUnknown)
        self.__yearOnly.SetValue(song._yearOnly)
        self.__yearOnly.Enable(not song._dateUnknown)
        self.__capoSelect.SetSelection(song._capoOnFret)
        self.__workDir.SetValue(song._relativePath)
        self.__songType.SetValue(song._songType == songs.ST_TUTORIAL)
        self.__SyncExamplePath()

    # --------------------------------------------------------------------------
    def OnOk(self, event): 
        """
        Handler to either close the song dialog and save settings or deny this
        """
        
        if self.__barCount.GetValue() < 0:
            wx.MessageBox('Please enter the number of bars in the song, or 0 for none', style = wx.ICON_EXCLAMATION | wx.OK)
            return
        if self.__artist.GetValue().strip() == '':
            wx.MessageBox('Please enter a valid artist', style = wx.ICON_EXCLAMATION | wx.OK)
            return
        if self.__title.GetValue().strip() == '':
            wx.MessageBox('Please enter a valid song title', style = wx.ICON_EXCLAMATION | wx.OK)
            return
        
        # go by all songs, and match case insensitive if a title already exists 
        # like the one added, to prevent double songs
        if not self.__dbAllowed:
            title = self.__title.GetValue().strip().upper()
            for s in viewmgr.Get()._list:
                if s != self.__song and (title == s._title.upper()):
                    res = wx.MessageBox('A similar song title already exists in the database.\nAre you sure you want to add this song?',
                                        'Warning', wx.ICON_QUESTION | wx.YES_NO)
                    if res != wx.YES:
                        return
                    else:
                        break
        
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
            if dlg.ShowModal() == wx.ID_OK and self.__dbAllowed:
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
