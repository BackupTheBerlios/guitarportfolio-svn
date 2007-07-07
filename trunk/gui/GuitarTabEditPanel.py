import wx
import wx.xrc as xrc

from wx.lib.pubsub import Publisher
from objs import songs, tabs
from db import tabs_peer, songs_peer
import db.engine
import xmlres, viewmgr

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

        Publisher().subscribe(self.__OnSongClear, viewmgr.SIGNAL_CLEAR_DATA)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)
        Publisher().subscribe(self.__OnTabAdded, viewmgr.SIGNAL_TAB_ADDED)
        
        # change font to modern look on Windows
        if 'wxMSW' in wx.PlatformInfo:
            fnt = self.__tabText.GetFont()
            fnt.Family = wx.FONTFAMILY_MODERN
            fnt.FaceName = "Courier New"
            self.__tabText.SetFont(fnt)
        # TODO: we might need to force this on Linux as well
        
    #---------------------------------------------------------------------------
    def __OnSongClear(self, message):
        """ We received a clear signal, db change or initialization for the app """

        self.__addSongTab.Enable(False)
        self.__tabSelect.Clear()
        self.__tabText.SetValue('')
        self.__applySelect.SetSelection(0)
        self.__tab = None

        # no tabs in the song 
        self.__EnableEditing(False)     
        
    #---------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Populate this with tabs, we have a selected song """
        
        song = message.data
        self.__applySelect.SetSelection(0)
        self.__tab = None
        self.__tabSelect.Clear()
        self.__tabSelect.SetValue('')
        self.__tabText.SetValue('')

        # populate tabs in the list
        if song:
            if song.tabs.count() > 0:
                for t in song.tabs:
                    idx = self.__tabSelect.Append(t._name)
                    self.__tabSelect.SetClientData(idx, t)
                
                # we select the first tab in the list
                self.__DoSelectTab(self.__tabSelect.GetClientData(0))
            else:
                # we have no tabs yet only enable the add and the list
                self.__tabText.Enable(False)
                self.__applySelect.Enable(False)
        else:
            self.__EnableEditing(False)
        
        self.__addSongTab.Enable(song != None)

    #---------------------------------------------------------------------------
    def __OnApply(self, event):
        if self.__tab:
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
                        
        # add the tab to the list here
        tab = message.data
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
            
            viewmgr.signalTabUpdated(self.__tab, viewmgr.Get()._selectedSong)
        
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
            s = viewmgr.Get()._selectedSong
            if s and self.__tab:                
                # update relations
                s.tabs.remove(self.__tab)
                slp = songs_peer.SongTabListPeer(db.engine.GetDb())
                slp.Update(s)
                
                # remove tab
                tp = tabs_peer.TabPeer(db.engine.GetDb())
                tp.Delete(self.__tab)

                # we just deleted a tab (krikey!)
                viewmgr.signalTabDeleted(self.__tab, s)

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
    def __OnAddTab(self, event): 
        """ We received an event that a tab is added (we initiated it ourselves (DUH)) """
        
        # create a new tab to be added
        s = viewmgr.Get()._selectedSong
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
            
            # tell the world we have a tab again
            viewmgr.signalTabAdded(tab, s)
            
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
    def __OnTabSelect(self, event): 
        self.__tab = None
        idx = self.__tabSelect.GetSelection()
        if idx == wx.NOT_FOUND:
            self.__EnableEditing(False)
            return
        else:
            self.__DoSelectTab(self.__tabSelect.GetClientData(idx))


