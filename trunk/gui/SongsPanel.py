# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sun May 13 11:47:41 2007 from D:\personal\src\GuitarPortfolio\branches\db_revival\gui\guitarportfolio.wxg

import sys
import wx
import wx.lib.mixins.listctrl as listmix
from wx.lib.pubsub import Publisher

import images
from objs import songs
from db import songs_peer 
import db.engine
import viewmgr

# begin wxGlade: dependencies
# end wxGlade

"""
    ListCtrl with project options, an auto width control
    with images and columns.
"""
class SongsListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style = wx.LC_REPORT | 
                                                                  wx.BORDER_NONE | 
                                                                  wx.LC_SORT_ASCENDING | 
                                                                  wx.LC_SINGLE_SEL)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        self.InsertColumn(0, "Song", width = 170)
        self.InsertColumn(1, "%", width = 30, format = wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(2, "Artist", width = 170)
        self.InsertColumn(3, "Capo", width = 50)
        self.InsertColumn(4, "Tuning", width = 100)
        self.InsertColumn(5, "Started On")

        # create an image list
        self.__statToIcon = {}
        self.__icons = wx.ImageList(16, 16)
        self.__statToIcon[songs.SS_COMPLETED]   = self.__icons.Add(images.icon_completed.getBitmap())
        self.__statToIcon[songs.SS_NOT_STARTED] = self.__icons.Add(images.icon_todo.getBitmap())
        self.__statToIcon[songs.SS_STARTED]     = self.__icons.Add(images.icon_in_progress.getBitmap())
        self.__statToIcon[songs.SS_POSTPONED]   = self.__icons.Add(images.icon_not_practicing.getBitmap())
        self.SetImageList(self.__icons, wx.IMAGE_LIST_SMALL)
        
        # hook up our event
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.__OnItemSelected, self)
        
        if "wxGTK" in wx.PlatformInfo:
            # in wxGTK, there is no right click event
            self.Bind(wx.EVT_RIGHT_UP, self.__OnRightClick)
        else:
            self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.__OnRightClick)
            
        # attach signal to get informed about songs
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)  
        Publisher().subscribe(self.__AddSong, viewmgr.SONG_VIEW_ADDED)  
        Publisher().subscribe(self.__UpdateSong, viewmgr.SONG_VIEW_UPDATED)  
        Publisher().subscribe(self.__DeleteSong, viewmgr.SONG_VIEW_DELETED)  
        Publisher().subscribe(self.__ClearSongs, viewmgr.SIGNAL_CLEAR_DATA)

    # --------------------------------------------------------------------------
    def __OnItemSelected(self, event):
        """ Select the song """
        song = viewmgr.Get()._list.find_id(event.GetData())
        viewmgr.signalSetSong(song)
        
    # --------------------------------------------------------------------------
    def __AddSong( self, message ):
        """ Signal that is emitted when a song is added to the list (restored or 
            added in the database """
        index = self.InsertStringItem(sys.maxint, message.data._title)
        self.SetStringItem(index, 1, '%d' % message.data.GetProgressPerc())
        self.SetStringItem(index, 2, message.data._artist)
        self.SetStringItem(index, 3, songs.GetCapoString(message.data._capoOnFret))
        self.SetItemData(index, message.data._id)
        self.SetItemImage(index, self.__statToIcon[message.data._status],
                                 self.__statToIcon[message.data._status])

    # --------------------------------------------------------------------------
    def __UpdateSong(self, message ):
        """ We received an update now we are going to find and update """
        if message.data <> None:
            index = self.FindItemData(-1, message.data._id)
            if index <> wx.NOT_FOUND:
                self.SetStringItem(index, 0, message.data._title)
                self.SetStringItem(index, 2, message.data._artist)
                self.SetStringItem(index, 1, '%d' % message.data.GetProgressPerc())
                self.SetItemImage(index, self.__statToIcon[message.data._status],
                                         self.__statToIcon[message.data._status])
                self.SetStringItem(index, 3, songs.GetCapoString(message.data._capoOnFret))
                
    # --------------------------------------------------------------------------
    def __DeleteSong(self, message):
        """ Delete song from the list """
        index = self.FindItemData(-1, message.data._id)
        if index <> wx.NOT_FOUND:
            self.DeleteItem(index)
        
    # --------------------------------------------------------------------------
    def __ClearSongs(self, message):
        """ Clear all songs from the views, probably because of a database reload """
        self.DeleteAllItems()        
        
    # --------------------------------------------------------------------------
    def __OnRightClick(self, event):
        """ Right click to present a menu to the user, to add a new song, edit
            a song, or change quick properties """

        # add popup menu
        menu = wx.Menu()

        m1 = wx.MenuItem(menu, wx.NewId(), "&Add New Song", "", wx.ITEM_NORMAL)
        menu.AppendItem(m1)
        m2 = wx.MenuItem(menu, wx.NewId(), "&Edit ...", "", wx.ITEM_NORMAL)
        menu.AppendItem(m2)
        m3 = wx.MenuItem(menu, wx.NewId(), "&Delete", "", wx.ITEM_NORMAL)
        menu.AppendItem(m3)
        menu.AppendSeparator()
        
        # submenu for changing status. only show it when we have a valid
        # selected song to work on
        self.__statusMap = {}
        items = [ ]
        song = viewmgr.Get()._selectedSong
        if song:
            if song._status == songs.SS_STARTED:
                items.append(("&Not Practicing", songs.SS_POSTPONED))
                items.append(("&Completed!", songs.SS_COMPLETED))
            elif song._status == songs.SS_NOT_STARTED or \
                 song._status == songs.SS_POSTPONED or \
                 song._status == songs.SS_COMPLETED:
                items.append(("&In Progress", songs.SS_STARTED))

            smenu = wx.Menu()
            for i in items:
                mi = wx.MenuItem(smenu, wx.NewId(), i[0], "", wx.ITEM_NORMAL)
                smenu.AppendItem(mi)
                self.__statusMap[mi.GetId()] = i[1]
                self.Bind(wx.EVT_MENU, self.__OnChangeStatus, mi)
                
            menu.AppendMenu(wx.NewId(), "Change &Status To ..", smenu)

            self.Bind(wx.EVT_MENU, self.__OnAddNewSong, m1)
            self.Bind(wx.EVT_MENU, self.__OnModifySong, m2)
            self.Bind(wx.EVT_MENU, self.__OnDeleteSong, m3)

            # Popup the menu.  If an item is selected then its handler
            # will be called before PopupMenu returns.
            self.PopupMenu(menu)
            menu.Destroy()

    # --------------------------------------------------------------------------
    def __OnAddNewSong(self, event):
        """ Send a query message to add a new song. This way the main frame
            will pick it up and we do not have to include the main frame in here """
        viewmgr.signalAddSong()
        
    # --------------------------------------------------------------------------
    def __OnModifySong(self, event):
        """ Send a query message to modify the clicked song. This way the main frame
            will pick it up and we do not have to include the main frame in here """
        viewmgr.signalEditSong()
        
    # --------------------------------------------------------------------------
    def __OnDeleteSong(self, event):
        """ Send a query message to delete the clicked song. """
        viewmgr.signalDeleteSong()

    # --------------------------------------------------------------------------
    def __OnChangeStatus(self, event):
        """ Change the status of the song by context menu """
        song = viewmgr.Get()._selectedSong
        if song <> None:
            # if our status differs, force an update
            if song._status <> self.__statusMap[event.GetId()]:                
                viewmgr.signalSongStatusChange(song, self.__statusMap[event.GetId()])
                
    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Select a new song, this usually means sync with the existing song """
        song = viewmgr.Get()._selectedSong
        if song <> None:
            idx = self.FindItemData(start = -1, data = song._id)
            if idx <> wx.NOT_FOUND and not self.IsSelected(idx):
                self.Select(idx)
        
class SongsPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SongsPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.__songListCtrl = SongsListCtrl(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SongsPanel.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SongsPanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.__songListCtrl, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        # end wxGlade

# end of class SongsPanel


