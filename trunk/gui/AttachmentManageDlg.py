import datetime
import os.path
import wx
import wx.xrc as xrc

import db.engine

import appcfg, xmlres

class AttachmentManageDlg(wx.Dialog):
    def __init__(self, parent, id = wx.ID_ANY):
        pre = wx.PreDialog()
        xmlres.Res().LoadOnDialog(pre, parent, "ManageAttachmentDlg")
        self.PostCreate(pre)
