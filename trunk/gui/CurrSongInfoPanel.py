# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sun May 13 11:47:41 2007 from D:\personal\src\GuitarPortfolio\branches\db_revival\gui\guitarportfolio.wxg

import wx
import wx.xrc as xrc
import wx.html as html
import xmlres
import time

from wx.lib.pubsub import Publisher
from objs import signals, songs, songfilter
import wikiparser

songinfo = """
No song info available
"""

class CurrSongInfoPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongInfoPanel")
        self.PostCreate(pre)

        self.__songInfo = xrc.XRCCTRL(self, "ID_SONGINFO")
        if "gtk2" in wx.PlatformInfo:
            self.__songInfo.SetStandardFonts()
            
        self.__songInfo.SetPage(wikiparser.WikiParser().Parse(songinfo))
                
        Publisher().subscribe(self.__OnSelectSong, signals.SONG_VIEW_SELECTED)
        Publisher().subscribe(self.__OnSelectSong, signals.SONG_VIEW_UPDATED)
        
    # --------------------------------------------------------------------------
    def __OnSelectSong(self, message):
        """ Select signal when a new song is selected by SongList, we react on it """
        # replace all items and display text
        parser = wikiparser.WikiParser()
        if message.data == None:
            self.__songInfo.SetPage(parser.Parse(songinfo))
        else:
            if songfilter.Get()._selectedSong == message.data:                   
                self.__songInfo.SetPage(parser.Parse(message.data._information))
