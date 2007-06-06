import wx
import wx.xrc as xrc

from wx.lib.pubsub import Publisher
from objs import signals, songs, tabs, songfilter
from db import tabs_peer, songs_peer
import db.engine
import xmlres

class GuitarTabEditPanel(wx.Panel):
    def __init__(self, parent, id = wx.ID_ANY):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "EditTabPanel")
        self.PostCreate(pre)

        self.__addSongTab = xrc.XRCCTRL(self, "ID_ADD_BUTTON")
        self.__tabSelect = xrc.XRCCTRL(self, "ID_TAB_DESCRIPTION")
        self.__tabText = xrc.XRCCTRL(self, "ID_TAB_TEXT")
        self.__applySelect = xrc.XRCCTRL(self, "ID_APPLY_ACTION")
        self.__apply = xrc.XRCCTRL(self, "wxID_APPLY")
        
        self.Bind(wx.EVT_BUTTON, self.__OnAddTab, self.__addSongTab)
        self.Bind(wx.EVT_COMBOBOX, self.__OnTabSelect, self.__tabSelect)
        self.Bind(wx.EVT_BUTTON, self.__OnApply, self.__apply)

        self.__applySelect.SetSelection(0)
        self.__tab = None

        Publisher().subscribe(self.__OnSongSelected, signals.SONG_VIEW_SELECTED)
        Publisher().subscribe(self.__OnTabUpdated, signals.TAB_DB_UPDATED)
        Publisher().subscribe(self.__OnTabRestored, signals.TAB_DB_RESTORED)
        Publisher().subscribe(self.__OnSongSelected, signals.APP_CLEAR)
        Publisher().subscribe(self.__OnTabAdded, signals.TAB_DB_INSERTED)

        # change font to modern look on Windows
        if 'wxMSW' in wx.PlatformInfo:
            fnt = self.__tabText.GetFont()
            fnt.Family = wx.FONTFAMILY_MODERN
            fnt.FaceName = "Courier New"
            self.__tabText.SetFont(fnt)
        # TODO: we might need to force this on Linux as well
        
    #---------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ We received an select signal for the song """
        # en/disable the view
        s = message.data
        
        self.__addSongTab.Enable(s <> None)
        self.__tabSelect.Clear()
        self.__tabText.SetValue('')
        self.__applySelect.SetSelection(0)
        self.__tab = None

        # no tabs in the song 
        self.__EnableEditing(self.__tab <> None)            

    #---------------------------------------------------------------------------
    def __OnTabRestored(self, message):
        t = message.data
        if t:
            idx = self.__tabSelect.Append(t._name)
            self.__tabSelect.SetClientData(idx, t)
            
            if not self.__tab:
                self.__DoSelectTab(self.__tabSelect.GetClientData(0))

    #---------------------------------------------------------------------------
    def __OnApply(self, event): # wxGlade: GuitarTabEditPanel.<event_handler>
        if self.__tab <> None:
            if self.__applySelect.GetSelection() == 0:     
                # update in DB
                self.__DoUpdateTab()
                            
            elif self.__applySelect.GetSelection() == 1:  
                 # revert to DB
                self.__DoRevertTab()
                
            elif self.__applySelect.GetSelection() == 2:
                 # delete
                 self.__DoDeleteTab()

            # revert to save, always
            self.__applySelect.SetSelection(0)    
    
    #---------------------------------------------------------------------------
    def __OnTabAdded(self, message):
        if self.__tab:
            # check first if our edit fields are changed
            if (self.__tab._text <> self.__tabText.GetValue()) or \
               (self.__tab._name <> self.__tabSelect.GetStringSelection()):
                
                res = wx.MessageBox('Do you want to save the current tab first?', 'Warning',
                                    wx.ICON_WARNING | wx.YES | wx.NO)
                if res == wx.YES:
                    self.__DoUpdateTab()
                        
        tab = message.data
        # add the tab to the list here
        idx = self.__tabSelect.Append(tab._name)
        self.__tabSelect.SetClientData(idx, tab)    
        self.__DoSelectTab(tab)
    
    #---------------------------------------------------------------------------
    def __DoUpdateTab(self):
        """ Update tab in the DB, and update all fields """
        if self.__tab:
            self.__tab._name = self.__tabSelect.GetValue()
            self.__tab._text = self.__tabText.GetValue()
            
            tp = tabs_peer.TabPeer(db.engine.GetDb())
            tp.Update(self.__tab)
        
    #---------------------------------------------------------------------------
    def __DoRevertTab(self):
        if self.__tab:
            idx = self.__tabSelect.GetSelection()
            self.__tabSelect.SetValue(self.__tab._name)
            self.__tabText.SetValue(self.__tab._text)
            self.__tabSelect.SetSelection(idx)
    
    #---------------------------------------------------------------------------
    def __DoDeleteTab(self):
        if wx.MessageBox('Are you sure you want to delete this tab?', 
                         'Warning', wx.ICON_HAND | wx.YES_NO) == wx.YES:
            # remove it from the collection
            s = songfilter.Get()._selectedSong
            if s and self.__tab:                
                # update relations
                s.tabs.remove(self.__tab)
                slp = songs_peer.SongTabListPeer(db.engine.GetDb())
                slp.Update(s)
                
                # remove tab
                tp = tabs_peer.TabPeer(db.engine.GetDb())
                tp.Delete(self.__tab)

            # find the tab by client data and remove it
            for i in xrange(0, self.__tabSelect.GetCount()):
                if self.__tabSelect.GetClientData(i) == self.__tab:
                    self.__tabSelect.Delete(i)
                    if self.__tabSelect.GetCount() > 0:
                        self.__DoSelectTab(self.__tabSelect.GetClientData(0))
                    else:
                        self.__tab = None
                        self.__EnableEditing(False)
                    break
            
    #---------------------------------------------------------------------------
    def __OnTabUpdated(self, message):
        # find the tab by client data and replace and select
        tab = message.data
        if tab:
            idx = self.__tabSelect.GetSelection()
            for i in xrange(0, self.__tabSelect.GetCount()):
                if self.__tabSelect.GetClientData(i) == tab:
                    self.__tabSelect.SetString(i, tab._name)
                    self.__tabSelect.SetSelection(i)
                    break

    #---------------------------------------------------------------------------
    def __OnAddTab(self, event): # wxGlade: GuitarTabEditPanel.<event_handler>
        # create a new tab to be added
        s = songfilter.Get()._selectedSong
        if s <> None:
            
            # first check if the current tab needs to be stored
            tab = tabs.Tab()
            tab._name = 'Tab #%d' % (s.tabs.count() + 1)
            
            tp = tabs_peer.TabPeer(db.engine.GetDb())
            tp.Update(tab) 
            
            # update the tab collection, so that the song owns the tab
            # from here an add message is emitted which we can use to 
            # sync our list
            s.tabs.append(tab)
            tlp = songs_peer.SongTabListPeer(db.engine.GetDb())
            tlp.Update(s)
            
                                   
    #---------------------------------------------------------------------------
    def __DoSelectTab(self, tab):
        """ Fill edit area with tab data """
        self.__tab = tab
        if tab:
            for i in xrange(0, self.__tabSelect.GetCount()):
                if self.__tabSelect.GetClientData(i) == tab:
                    self.__tabSelect.SetSelection(i)
                    self.__tabText.SetValue(tab._text)
                    self.__EnableEditing(True)
                    return
        
        self.__tabText.SetValue('')
        self.__EnableEditing(False)
        
    #---------------------------------------------------------------------------
    def __EnableEditing(self, status):
        """ Dissalow the user to edit if there is no tab selected or added """
        self.__tabSelect.Enable(status)
        self.__applySelect.Enable(status)
        self.__apply.Enable(status)
        self.__tabText.Enable(status)
        if status == False:
            self.__tabText.SetValue('')
            self.__tabSelect.SetValue('')
            self.__tabSelect.Clear()

    #---------------------------------------------------------------------------
    def __OnTabSelect(self, event): # wxGlade: GuitarTabEditPanel.<event_handler>
        self.__tab = None
        idx = self.__tabSelect.GetSelection()
        if idx == wx.NOT_FOUND:
            self.__EnableEditing(False)
            return
        else:
            self.__DoSelectTab(self.__tabSelect.GetClientData(idx))

# end of class GuitarTabEditPanel


