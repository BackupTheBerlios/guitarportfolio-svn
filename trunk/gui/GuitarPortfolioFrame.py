import os.path

import wx
import wx.aui
from wx.lib.pubsub import Publisher

import db
import db.engine
import db.songs_peer

from objs import signals, songs, category_mgr, tuning_mgr, songfilter
from gui import SongsPanel, EditorNotebook, CurrInfoNotebook, NewSongDlg, \
                CategoriesDlg, SongFilterPanel, OptionsDlg, WelcomeDlg, xmlres
from images import icon_main_window

import appcfg

class GuitarPortfolioFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        # create menu
        self.__menuBar = wx.MenuBar()
        self.SetMenuBar(self.__menuBar)

        # file menu	
        mnu = wx.Menu()        
        self.__menuShowDatabaseWizard = wx.MenuItem(mnu, wx.NewId(), "&Show Database Wizard ...", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuShowDatabaseWizard)
        self.__menuOptions = wx.MenuItem(mnu, wx.NewId(), "&Preferences ...", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuOptions)
        mnu.AppendSeparator()
        self.__menuExit = wx.MenuItem(mnu, wx.NewId(), "E&xit\tCtrl+X", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuExit)
        self.__menuBar.Append(mnu, "&File")

        # songs menu
        mnu = wx.Menu()
        self.__menuAddNewSong = wx.MenuItem(mnu, wx.NewId(), "&Add New ...\tCtrl+A", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuAddNewSong)
        self.__menuEditSong = wx.MenuItem(mnu, wx.NewId(), "&Edit ...\tCtrl+E", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuEditSong)
        self.__menuDeleteSong = wx.MenuItem(mnu, wx.NewId(), "&Delete\tCtrl+D", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuDeleteSong)
        
        # status submenu
        
        self.__menu_status_lookup = {}
        items = [ ("&In progress", songs.SS_STARTED), 
                  ("&Not Practicing", songs.SS_POSTPONED),
                  ("&Completed!", songs.SS_COMPLETED) ]
        
        smnu = wx.Menu()
        for i in items:
            mi = wx.MenuItem(smnu, wx.NewId(), i[0], "", wx.ITEM_NORMAL)
            smnu.AppendItem(mi)
            self.__menu_status_lookup[mi.GetId()] = i[1]
            self.Bind(wx.EVT_MENU, self.__OnChangeStatus, mi)        
        
        mnu.AppendSubMenu(smnu, "Set &Status To")
        self.__menuSongStatus = smnu

        self.__menuEditReset = wx.MenuItem(mnu, wx.NewId(), "Reset &History", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuEditReset)    

        mnu.AppendSeparator()
        self.__menuEditCategories = wx.MenuItem(mnu, wx.NewId(), "Edit &Categories ...\tCtrl+Shift+C", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuEditCategories)
        self.__menuBar.Append(mnu, "&Song")
        
        # window layout
        mnu = wx.Menu()
        self.__menuRestoreLayout = wx.MenuItem(mnu, wx.NewId(), "&Restore Default Layout", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuRestoreLayout)
        mnu.AppendSeparator()
        self.__menuToggleEditView = wx.MenuItem(mnu, wx.NewId(), "Show &Editors", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuToggleEditView)
        self.__menuToggleSongSelect = wx.MenuItem(mnu, wx.NewId(), "Show &Song Selector", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuToggleSongSelect)
        self.__menuToggelSongFilter = wx.MenuItem(mnu, wx.NewId(), "Show Song &Filter", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuToggelSongFilter)
        mnu.AppendSeparator()
        self.__menuBrowserMode = wx.MenuItem(mnu, wx.NewId(), "&Browser Mode", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuBrowserMode)
        self.__menuEditorMode = wx.MenuItem(mnu, wx.NewId(), "Editor &Mode", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuEditorMode)
        self.__menuBar.Append(mnu, "&Windows")

        # set all properties
        self.SetTitle("Guitar Portfolio")
        self.Layout()

        self.Bind(wx.EVT_MENU, self.__OnShowDatabaseWizard, self.__menuShowDatabaseWizard)
        self.Bind(wx.EVT_MENU, self.__OnShowOptions, self.__menuOptions)
        self.Bind(wx.EVT_MENU, self.OnExit, self.__menuExit)
        self.Bind(wx.EVT_MENU, self.__OnAddNewSong, self.__menuAddNewSong)
        self.Bind(wx.EVT_MENU, self.__OnEditNewSong, self.__menuEditSong)
        self.Bind(wx.EVT_MENU, self.__OnDeleteSong, self.__menuDeleteSong)
        self.Bind(wx.EVT_MENU, self.__OnEditCategories, self.__menuEditCategories)
        self.Bind(wx.EVT_MENU, self.__OnRestoreLayout, self.__menuRestoreLayout)
        self.Bind(wx.EVT_MENU, self.__OnToggleEditWindow, self.__menuToggleEditView)
        self.Bind(wx.EVT_MENU, self.__OnToggleSongSelector, self.__menuToggleSongSelect)
        self.Bind(wx.EVT_MENU, self.__OnToggleFilterWindow, self.__menuToggelSongFilter)
        self.Bind(wx.EVT_MENU, self.__OnBrowserMode, self.__menuBrowserMode)
        self.Bind(wx.EVT_MENU, self.__OnEditorMode, self.__menuEditorMode)
        # end wxGlade

        self.SetIcon(wx.IconFromBitmap(icon_main_window.getBitmap()))
        self.Bind(wx.EVT_CLOSE, self.__OnClose)

        # tell AUI to manage this frame        
        self.__aui = wx.aui.AuiManager()
        self.__aui.SetManagedWindow(self)

        # construct the left panels
        self.__aui.AddPane(SongsPanel.SongsPanel(parent = self), wx.aui.AuiPaneInfo().
                           Name("songspanel").Caption("Songs").MinSize(wx.Size(280,100)).
                           BestSize(wx.Size(280, 200)).Left().MaximizeButton(True))

        self.__aui.AddPane(SongFilterPanel.SongFilterPanel(self), wx.aui.AuiPaneInfo().Name("filterpanel").Caption("Filter").
                           MinSize(wx.Size(250,100)).BestSize(wx.Size(250, 100)).Left().MaximizeButton(True))

        # construct the bottom panel
        self.__aui.AddPane(EditorNotebook.EditorNotebook(self), wx.aui.AuiPaneInfo().
                          Name("editpanel").Caption("Edit").MinSize(wx.Size(200,205)).
                          Bottom().MaximizeButton(True))

        # construct the middle part
        self.__aui.AddPane(CurrInfoNotebook.CurrInfoNotebook(self), wx.aui.AuiPaneInfo().
                           Name("currsong").Caption("Information").
                           CenterPane().CloseButton(False).MaximizeButton(True))

        self.__aui.Update()

        self._filter = songfilter.Get()

        # hook up event handlers
        Publisher().subscribe(self.__OnSongAdded, signals.SONG_DB_ADDED)
        Publisher().subscribe(self.__OnSongDeleted, signals.SONG_DB_DELETED)
        Publisher().subscribe(self.__OnSongUpdated, signals.SONG_DB_UPDATED)
        Publisher().subscribe(self.__OnSongSelected, signals.APP_CLEAR)
        Publisher().subscribe(self.__OnSongSelected, signals.SONG_VIEW_SELECTED)
        Publisher().subscribe(self.__OnSongPopulate, signals.SONG_VIEW_AFTER_SELECT)
        Publisher().subscribe(self.__OnQueryAddSong, signals.SONG_QUERY_ADD)
        Publisher().subscribe(self.__OnQueryDeleteSong, signals.SONG_QUERY_DELETE)
        Publisher().subscribe(self.__OnQueryEditSong, signals.SONG_QUERY_MODIFY)
        Publisher().subscribe(self.__OnTabAdded, signals.SONG_DB_TAB_ADDED)

        # dependent on the layout settings, we restore the old perspective, or save the default
        cfg = appcfg.Get()
        pers = cfg.Read(appcfg.CFG_LAYOUT_DEFAULT, '')
        if not pers:
            # save default for restoring
            pers = self.__aui.SavePerspective()
            cfg.Write(appcfg.CFG_LAYOUT_DEFAULT, pers)
        else:
            # load last one
            pers = cfg.Read(appcfg.CFG_LAYOUT_LAST, '')
            if pers:
                self.__aui.LoadPerspective(pers)                

        # retrieve height / width of main window
        width = cfg.ReadInt(appcfg.CFG_LAYOUT_LAST_W, 800)
        height = cfg.ReadInt(appcfg.CFG_LAYOUT_LAST_H, 800)

        self.SetSize((width, height)) 

        # open database (or not) when unsuccesful an event is posted to
        # show the wizard on the next OnIdle event
        self.__dbValid = False
        dbpath = appcfg.Get().Read(appcfg.CFG_DBPATH, '')
        if dbpath:
            status = db.engine.Get().Open(dbpath)
            self.__dbValid = (status == db.engine.DB_OPEN_OK)
        if not self.__dbValid:
            evt = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, self.__menuShowDatabaseWizard.GetId())
            self.AddPendingEvent(evt)
        else:
            self.__PopulateData()
            
    #---------------------------------------------------------------------------
    def OnExit(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.Close()

    #---------------------------------------------------------------------------
    def __OnAddNewSong(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        # callback to ourselves
        self.__OnQueryAddSong()

    #---------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ A song is selected. When we have NONE as song, we disable the 
            menus that should not be pressed when there is no song """
        self.__SyncMenuItems()

    #---------------------------------------------------------------------------
    def __OnQueryAddSong(self, message = None):
        """ We received a query from somewhere to add a new song to the database
            this is either sent from the popup menu or ourselves """
        s = songs.Song()
        s._tuning = tuning_mgr.Get().GetDefaultTuning()

        # we use the last used relative path or a default one when present
        s._relativePath = appcfg.Get().Read(appcfg.CFG_LASTRELPATH, appcfg.DEF_RELPATH)

        dlg = NewSongDlg.NewSongDlg(self, nodb = True)
        dlg.LoadFromSong(s)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.SaveToSong(s)

            # write back the last used relative path spec, for ease of use
            appcfg.Get().Write(appcfg.CFG_LASTRELPATH, s._relativePath)

            # write song to database, from here a trigger is sent
            # to add the song to all lists that are interested
            sp = db.songs_peer.SongPeer(db.engine.GetDb())
            sp.Update(s, all = True)

        dlg.Destroy()  

    #---------------------------------------------------------------------------
    def __OnQueryEditSong(self, message = None):
        s = self._filter._selectedSong
        if s <> None:
            dlg = NewSongDlg.NewSongDlg(self)
            dlg.LoadFromSong(s)
            if dlg.ShowModal() == wx.ID_OK:
                # TODO: Small problem, the category relations can be 
                # changed due to a second editor, but cancelling does not
                # show these changes.
                dlg.SaveToSong(s)

                # update the song in the database
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Update(s, all = True)                
            dlg.Destroy()

    #---------------------------------------------------------------------------
    def __OnEditNewSong(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.__OnQueryEditSong()

    #---------------------------------------------------------------------------
    def __OnQueryDeleteSong(self, message = None):
        if self._filter._selectedSong:
            res = wx.MessageBox('Are you sure you want to remove the song from the database?\n'
                                   'All related lyrics, tabs and information will be permanently lost!', 'Warning', wx.ICON_QUESTION | wx.YES_NO)
            if res == wx.YES:
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Delete(self._filter._selectedSong)             

    #---------------------------------------------------------------------------
    def __OnDeleteSong(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.__OnQueryDeleteSong()

    #---------------------------------------------------------------------------
    def __OnEditCategories(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        s = self._filter._selectedSong
        if s <> None:    
            dlg = CategoriesDlg.CategoriesDlg(self)
            dlg.SetCurrentSong(s)
            if dlg.ShowModal() == wx.ID_OK:

                # update the song in the database
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Update(s, all = True)                

            dlg.Destroy()

    #---------------------------------------------------------------------------
    def __OnChangeStatus(self, event):
        """ Set the status of the song
            NOTE: This should eventually be done by a log mechanism """
        song = songfilter.Get()._selectedSong
        if song <> None:
            # if our status differs, force an update
            if song._status <> self.__menu_status_lookup[event.GetId()]:
                song._status = self.__menu_status_lookup[event.GetId()]
                
                # update in DB
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Update(song)        

    #---------------------------------------------------------------------------
    def __OnShowOptions(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        """ Show the options dialog, all options saving is done inside the dialog 
            itself so there is no need for catching the modalresult """
        dlg = OptionsDlg.OptionsDlg(self)
        dlg.Center()
        dlg.ShowModal()
        dlg.Destroy()

    #---------------------------------------------------------------------------
    def __OnClose(self, event):
        cfg = appcfg.Get()
        cfg.Write(appcfg.CFG_LAYOUT_LAST, self.__aui.SavePerspective())  
        width, height = self.GetSize()
        cfg.WriteInt(appcfg.CFG_LAYOUT_LAST_W, width)
        cfg.WriteInt(appcfg.CFG_LAYOUT_LAST_H, height)        
        event.Skip()  

    #---------------------------------------------------------------------------
    def __OnRestoreLayout(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.__aui.LoadPerspective(appcfg.Get().Read(appcfg.CFG_LAYOUT_DEFAULT, ''), True)

    #---------------------------------------------------------------------------
    def __OnToggleEditWindow(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.__aui.GetPane("editpanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __OnToggleSongSelector(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.__aui.GetPane("songspanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __OnToggleFilterWindow(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        self.__aui.GetPane("filterpanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __OnShowDatabaseWizard(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        """ User wants to switch DB's or upgrade, or create a DB, or create a demo db.
            This can also be auto invoked by the application to let the user select a DB """

        dlg = WelcomeDlg.WelcomeDlg(self)            
        dlg.Centre()
        dlg.ShowModal()
        dlg.Destroy()

        if not db.engine.Get().IsOpened():    
            self.Close()
            return

        self.__PopulateData()

    #---------------------------------------------------------------------------
    def __PopulateData(self):
        """ Method that populates everything in all manager classes, and GUI windows
            by emitting a signals.APP_CLEAR to request emptying all lists and views """
        Publisher().sendMessage(signals.APP_CLEAR, None) # None object is crucial

        songfilter.Get().Reset()

        # make sure we have a valid DB
        if not db.engine.Get().IsOpened():
            wx.MessageBox('An error occured while reading from the database, \n' + \
                          'please restart GuitarPortfolio and try again!', 'Error',
                          wx.ICON_HAND | wx.OK)
            self.Close()
            return

        # start loading
        dbc = db.engine.GetDb()
        category_mgr.RestoreFromDb(dbc)
        tuning_mgr.RestoreFromDb(dbc)

        # load all songs, and let the callback signals
        # handle the adding to various views

        sp = db.songs_peer.SongSetPeer(dbc)
        songs = sp.Restore()

        # go restore all relations
        sp = db.songs_peer.SongPeer(dbc)
        for s in songs:
            sp.RestoreCategories(s)

        # send everyone that the DB is restored and all went well
        Publisher().sendMessage(signals.APP_READY)

    #---------------------------------------------------------------------------
    def __OnSongAdded(self, message):
        # add a song to the view filter
        self._filter.AddSong(message.data)        

    #---------------------------------------------------------------------------
    def __OnSongDeleted(self, message):
        # remove a song from the view filter
        self._filter.RemoveSong(message.data)        

    #---------------------------------------------------------------------------
    def __OnSongUpdated(self, message):
        # update a song in the view filter
        self._filter.UpdateSong(message.data)        
        self.__SyncMenuItems()

    #---------------------------------------------------------------------------
    def __OnSongPopulate(self, message):
        """ Do some tab restoring, we do this to save mem and time at start-up """
        ss = self._filter._selectedSong
        if ss:
            tlp = db.songs_peer.SongTabListPeer(db.engine.GetDb())
            tlp.Restore(ss) 

    #---------------------------------------------------------------------------
    def __OnTabAdded(self, message):
        """ Tab is added, we check if it belongs to the song that is selected
            as current, and re-route the signal to signals.SONG_VIEW_TAB_ADDED """
        song_tab = message.data
        s = songfilter.Get()._selectedSong
        if song_tab[0] == s and s:
            Publisher().sendMessage(signals.SONG_VIEW_TAB_ADDED, song_tab[1])

    #---------------------------------------------------------------------------
    def __OnBrowserMode(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        """ Show only the browser parts of GuitarPortfolio """
        self.__aui.GetPane("editpanel").Show(False)
        self.__aui.GetPane("songspanel").Show(False)
        self.__aui.GetPane("filterpanel").Show(False)
        self.__aui.Update()
        
    #---------------------------------------------------------------------------
    def __OnEditorMode(self, event): # wxGlade: GuitarPortfolioFrame.<event_handler>
        """ Show the editor parts of GuitarPortfolio """
        self.__aui.GetPane("editpanel").Show(True)
        self.__aui.GetPane("songspanel").Show(True)
        self.__aui.GetPane("filterpanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __SyncMenuItems(self):
        song = songfilter.Get()._selectedSong
        self.__menuEditSong.Enable(song <> None)
        self.__menuDeleteSong.Enable(song <> None)
        self.__menuEditCategories.Enable(song <> None)
        self.__menuEditCategories.Enable(song <> None)
        self.__menuEditReset.Enable(False)
        # enable status based upon previous status
        if song:
            for id in self.__menu_status_lookup.iterkeys():
                if self.__menu_status_lookup[id] == songs.SS_POSTPONED:
                    self.__menuSongStatus.Enable(id, song._status == songs.SS_STARTED)
                elif self.__menu_status_lookup[id] == songs.SS_STARTED:
                    self.__menuSongStatus.Enable(id, song._status == songs.SS_COMPLETED or \
                                                     song._status == songs.SS_POSTPONED)
                elif self.__menu_status_lookup[id] == songs.SS_COMPLETED:
                    self.__menuSongStatus.Enable(id, song._status == songs.SS_STARTED)
        else:
            for id in self.__menu_status_lookup.iterkeys():
                self.__menuSongStatus.Enable(id, False)        

# end of class GuitarPortfolioFrame


