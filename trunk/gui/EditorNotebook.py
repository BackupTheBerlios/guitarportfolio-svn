import wx
import wx.aui

import ProgressPanel
import InfoPanel
import LinksPanel
import LyricsPanel
import GuitarTabEditPanel

#----------------------------------------------------------------------

class EditorNotebook(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.NewId())

        self.__mNB = wx.aui.AuiNotebook(self, style = wx.aui.AUI_NB_TAB_SPLIT | 
                                                       wx.aui.AUI_NB_TAB_MOVE |
                                                       wx.aui.AUI_NB_TAB_EXTERNAL_MOVE, size = (-1, 200))
        self.__mNB.AddPage(LinksPanel.LinksPanel(self.__mNB), "Edit Links")
        self.__mNB.AddPage(ProgressPanel.ProgressPanel(self.__mNB), "Edit Progress")
        self.__mNB.AddPage(InfoPanel.InfoPanel(self.__mNB), "Edit Information")
        self.__mNB.AddPage(LyricsPanel.LyricsPanel(self.__mNB), "Edit Lyrics")
        self.__mNB.AddPage(GuitarTabEditPanel.GuitarTabEditPanel(self.__mNB), "Edit Tabs")
            
        sizer = wx.BoxSizer()
        sizer.Add(self.__mNB, 1, wx.EXPAND)
        self.SetSizer(sizer)
