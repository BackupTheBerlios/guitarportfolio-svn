# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sun May 13 11:47:41 2007 from D:\personal\src\GuitarPortfolio\branches\db_revival\gui\guitarportfolio.wxg

import wx
import wx.html as html
from wx.lib.pubsub import Publisher

import wx.xrc as xrc
from objs import signals, songs
import HtmlInfoGen, xmlres

# begin wxGlade: dependencies
# end wxGlade

tabinfo = """<html><body>
<pre>@currenttab@</pre>
</body></html>
"""

# TODO: Make sure song information can also be substituted in the tab
                    
class GuitarTabPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongTabPanel")
        self.PostCreate(pre)

        self.__tabSelect = xrc.XRCCTRL(self, "ID_TABSELECT")
        self.__tabWindow = xrc.XRCCTRL(self, "ID_HTMLWINDOW")

        if "gtk2" in wx.PlatformInfo:
            self.__tabWindow.SetStandardFonts()

        self.Bind(wx.EVT_CHOICE, self.__OnSelectTab, self.__tabSelect)

        # hook up a select signal
        Publisher().subscribe(self.__OnSongSelected, signals.SONG_VIEW_SELECTED)
        Publisher().subscribe(self.__OnTabAdded, signals.TAB_DB_ADDED)
        Publisher().subscribe(self.__OnTabDeleted, signals.TAB_DB_DELETED)
        Publisher().subscribe(self.__OnTabUpdated, signals.TAB_DB_UPDATED)

    # --------------------------------------------------------------------------
    def SetTab(self, tab):
        if tab == None:
            self.__tabWindow.SetPage('No Tabs')
        else:
            page = tabinfo.replace('@currenttab@', tab._text)
            self.__tabWindow.SetPage(page)

    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Select signal when a new song is selected by SongList, we react on it """
        self.SetTab(None)
        self.__tabSelect.Clear()
        self.__tabSelect.Enable(message.data == None)
                         
    # --------------------------------------------------------------------------
    def __OnTabAdded(self, message):
        """ Add a restored tab or a fresh added tab """
        if message.data <> None:
            self.__tabSelect.Enable(True)
            idx = self.__tabSelect.Append(message.data._name)
            self.__tabSelect.SetClientData(idx, message.data)
            if self.__tabSelect.GetSelection() == wx.NOT_FOUND:
                self.__tabSelect.SetSelection(0)
                self.SetTab(message.data)     
              
    # --------------------------------------------------------------------------
    def __OnTabDeleted(self, message):
        """ Remove from list, select other one if we are watching """
        for i in xrange(0, self.__tabSelect.GetCount()):
            data = self.__tabSelect.GetClientData(i)
            if data == message.data:
                self.__tabSelect.Delete(i)
                if self.__tabSelect.GetCount() > 0:
                    self.__tabSelect.SetSelection(0)
                    self.SetTab(self.__tabSelect.GetClientData(0))
                else:
                    self.__tabSelect.Enable(False)
                    self.SetTab(None)
                break

    # --------------------------------------------------------------------------
    def __OnTabUpdated(self, message):
        """ Update in list, select other one if we are watching """
        for i in xrange(0, self.__tabSelect.GetCount()):
            data = self.__tabSelect.GetClientData(i)
            oldsel = self.__tabSelect.GetSelection()
            if data == message.data:
                self.__tabSelect.SetString(i, data._name)
                if oldsel == i:
                    self.SetTab(data)
                    self.__tabSelect.SetSelection(oldsel)
                break
  
    # --------------------------------------------------------------------------
    def __OnSelectTab(self, event):
        tab = self.__tabSelect.GetClientData(self.__tabSelect.GetSelection())
        self.SetTab(tab)         
    

