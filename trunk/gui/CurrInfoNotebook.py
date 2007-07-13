import wx
import wx.aui

import SongBrowserPanel
import SongLogPanel

#----------------------------------------------------------------------

class CurrInfoNotebook(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.NewId())

        self.__mNB = wx.aui.AuiNotebook(self, style = wx.aui.AUI_NB_TAB_SPLIT | 
                                                      wx.aui.AUI_NB_TAB_MOVE |
                                                      wx.aui.AUI_NB_TAB_EXTERNAL_MOVE, size = (-1, 200))
        self.__mNB.AddPage(SongBrowserPanel.SongBrowserPanel(self.__mNB), "Browser")
        self.__mNB.AddPage(SongLogPanel.SongLogPanel(self.__mNB), "Study Log")
            
        sizer = wx.BoxSizer()
        sizer.Add(self.__mNB, 1, wx.EXPAND)
        self.SetSizer(sizer)
