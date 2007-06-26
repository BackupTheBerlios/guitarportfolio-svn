import os
import os.path
import sys

import wx
from wx.lib.pubsub import Publisher
import wx.xrc as xrc

from objs import linkmgt
import appcfg, xmlres, viewmgr
                
class SongLogPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongLogPanel")
        self.PostCreate(pre)
