# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Thu Apr 26 21:04:00 2007 from D:\personal\src\GuitarPortfolio\trunk\gui\guitartportfolio.wxg

import wx

# begin wxGlade: dependencies
# end wxGlade

class NewLinkDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: NewLinkDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_24 = wx.StaticText(self, -1, "Link name")
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        self.label_33 = wx.StaticText(self, -1, "Link description")
        self.text_ctrl_2 = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.label_25 = wx.StaticText(self, -1, "Enter file or URL to open")
        self.text_ctrl_3 = wx.TextCtrl(self, -1, "")
        self.button_6 = wx.Button(self, -1, "...")
        self.checkbox_1 = wx.CheckBox(self, -1, "File path is relative to base path")
        self.static_line_6 = wx.StaticLine(self, -1)
        self.radio_btn_1 = wx.RadioButton(self, -1, "Internet URL")
        self.radio_btn_2 = wx.RadioButton(self, -1, "Acrobat Reader PDF")
        self.label_26 = wx.StaticText(self, -1, "Page")
        self.text_ctrl_4 = wx.TextCtrl(self, -1, "")
        self.radio_btn_3 = wx.RadioButton(self, -1, "Plain File")
        self.label_27 = wx.StaticText(self, -1, "Enter optional file arguments")
        self.text_ctrl_5 = wx.TextCtrl(self, -1, "")
        self.label_28 = wx.StaticText(self, -1, "Enter optional application to start")
        self.text_ctrl_6 = wx.TextCtrl(self, -1, "")
        self.button_7 = wx.Button(self, -1, "...")
        self.button_8 = wx.Button(self, wx.ID_OK, "")
        self.button_9 = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: NewLinkDialog.__set_properties
        self.SetTitle("Enter Link Properties")
        self.SetSize((671, 396))
        self.text_ctrl_3.SetMinSize((150, -1))
        self.button_6.SetMinSize((40, -1))
        self.button_7.SetMinSize((40, -1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: NewLinkDialog.__do_layout
        sizer_30 = wx.BoxSizer(wx.VERTICAL)
        sizer_35 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_3 = wx.FlexGridSizer(3, 2, 0, 0)
        sizer_32 = wx.BoxSizer(wx.VERTICAL)
        sizer_34 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_31 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_33 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_30.Add(self.label_24, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer_30.Add(self.text_ctrl_1, 0, wx.ALL|wx.EXPAND, 5)
        sizer_30.Add(self.label_33, 0, wx.LEFT|wx.RIGHT, 5)
        sizer_30.Add(self.text_ctrl_2, 1, wx.ALL|wx.EXPAND, 5)
        sizer_30.Add(self.label_25, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer_33.Add(self.text_ctrl_3, 1, wx.ALL, 5)
        sizer_33.Add(self.button_6, 0, wx.ALL, 5)
        sizer_30.Add(sizer_33, 0, wx.EXPAND, 0)
        sizer_30.Add(self.checkbox_1, 0, wx.LEFT|wx.BOTTOM, 5)
        sizer_30.Add(self.static_line_6, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        grid_sizer_3.Add(self.radio_btn_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add(self.radio_btn_2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_31.Add(self.label_26, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_31.Add(self.text_ctrl_4, 0, wx.ALL, 5)
        grid_sizer_3.Add(sizer_31, 1, wx.EXPAND, 0)
        grid_sizer_3.Add(self.radio_btn_3, 0, wx.ALL, 5)
        sizer_32.Add(self.label_27, 0, wx.ALL, 5)
        sizer_32.Add(self.text_ctrl_5, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        sizer_32.Add(self.label_28, 0, wx.LEFT|wx.RIGHT, 5)
        sizer_34.Add(self.text_ctrl_6, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_34.Add(self.button_7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_32.Add(sizer_34, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(sizer_32, 1, wx.EXPAND, 0)
        grid_sizer_3.AddGrowableRow(0)
        grid_sizer_3.AddGrowableCol(1)
        sizer_30.Add(grid_sizer_3, 0, wx.EXPAND, 0)
        sizer_35.Add(self.button_8, 0, wx.ALL, 5)
        sizer_35.Add(self.button_9, 0, wx.ALL, 5)
        sizer_30.Add(sizer_35, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizer_30)
        self.Layout()
        # end wxGlade

# end of class NewLinkDialog


