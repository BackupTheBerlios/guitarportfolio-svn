# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sun May 13 11:47:41 2007 from D:\personal\src\GuitarPortfolio\branches\db_revival\gui\guitarportfolio.wxg

import wx

# begin wxGlade: dependencies
# end wxGlade

class DbProgressDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DbProgressDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_31 = wx.StaticText(self, -1, "Creating / Upgrading Database ...")
        self.__log = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.__quitButton = wx.Button(self, wx.ID_EXIT, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.__OnExit, self.__quitButton)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: DbProgressDlg.__set_properties
        self.SetTitle("Database Creator")
        self.SetSize((400, 300))
        self.label_31.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DbProgressDlg.__do_layout
        sizer_40 = wx.BoxSizer(wx.VERTICAL)
        sizer_41 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_40.Add(self.label_31, 0, wx.ALL, 5)
        sizer_40.Add(self.__log, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        sizer_41.Add(self.__quitButton, 0, wx.ALL, 5)
        sizer_40.Add(sizer_41, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizer_40)
        self.Layout()
        # end wxGlade

    def __OnExit(self, event): # wxGlade: DbProgressDlg.<event_handler>
        print "Event handler `__OnExit' not implemented!"
        event.Skip()

# end of class DbProgressDlg


