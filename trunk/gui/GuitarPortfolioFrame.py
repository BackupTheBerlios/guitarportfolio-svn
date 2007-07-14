import os.path

import wx
import wx.aui
from wx.lib.pubsub import Publisher
from wx.lib.wordwrap import wordwrap

import db
import db.engine
import db.songs_peer

from objs import signals, songs, category_mgr, tuning_mgr, linkmgt
from gui import SongsPanel, EditorNotebook, CurrInfoNotebook, NewSongDlg, \
                CategoriesDlg, SongFilterPanel, OptionsDlg, WelcomeDlg, \
                AttachmentManageDlg, xmlres, viewmgr, linkfile
from images import icon_main_window, guitarportfolio_icon

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
        self.__menuExit = wx.MenuItem(mnu, wx.NewId(), "E&xit", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuExit)
        self.__menuBar.Append(mnu, "&File")

        # songs menu
        mnu = wx.Menu()
        self.__menuAddNewSong = wx.MenuItem(mnu, wx.NewId(), "&Add New ...\tCtrl+N", "", wx.ITEM_NORMAL)
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
        
        # window layout menu
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

        # attachments menu
        mnu = wx.Menu()
        self.__menuCreateAttachDir = wx.MenuItem(mnu, wx.NewId(), "&Create Folder ...", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuCreateAttachDir)
        mnu.AppendSeparator()
        self.__menuAddAttachments = wx.MenuItem(mnu, wx.NewId(), "&Add ...", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuAddAttachments)
        self.__menuEditAttachments = wx.MenuItem(mnu, wx.NewId(), "&Edit ...", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuEditAttachments)
        self.__menuRefreshAttachments = wx.MenuItem(mnu, wx.NewId(), "&Refresh", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuRefreshAttachments)
        self.__menuBar.Append(mnu, "&Attachments")
        
        # help menu
        mnu = wx.Menu()
        self.__menuHelpVisitSite = wx.MenuItem(mnu, wx.NewId(), "&Visit Site .. ", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuHelpVisitSite)
        mnu.AppendSeparator()
        self.__menuHelpAbout = wx.MenuItem(mnu, wx.NewId(), "&About ...", "", wx.ITEM_NORMAL)
        mnu.AppendItem(self.__menuHelpAbout)
        self.__menuBar.Append(mnu, "&Help")
        
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
        self.Bind(wx.EVT_MENU, self.__OnVisitSite, self.__menuHelpVisitSite)
        self.Bind(wx.EVT_MENU, self.__OnAbout, self.__menuHelpAbout)
        self.Bind(wx.EVT_MENU, self.__OnCreateAttachmentsDir, self.__menuCreateAttachDir)
        self.Bind(wx.EVT_MENU, self.__OnAddAttachments, self.__menuAddAttachments)
        self.Bind(wx.EVT_MENU, self.__OnEditAttachments, self.__menuEditAttachments)
        self.Bind(wx.EVT_MENU, self.__OnRefreshAttachments, self.__menuRefreshAttachments)

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
        self.__songEditNotebook = EditorNotebook.EditorNotebook(self)
        self.__aui.AddPane(self.__songEditNotebook, wx.aui.AuiPaneInfo().
                          Name("editpanel").Caption("Edit").MinSize(wx.Size(200,205)).
                          Bottom().MaximizeButton(True))

        # construct the middle part
        self.__aui.AddPane(CurrInfoNotebook.CurrInfoNotebook(self), wx.aui.AuiPaneInfo().
                           Name("currsong").Caption("Information").
                           CenterPane().CloseButton(False).MaximizeButton(True))

        self.__aui.Update()

        self._filter = viewmgr.Get()

        # hook up event handlers
        Publisher().subscribe(self.__SignalOnQueryAddSong, viewmgr.SIGNAL_ADD_SONG)
        Publisher().subscribe(self.__SignalOnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)
        Publisher().subscribe(self.__SignalOnQueryEditSong, viewmgr.SIGNAL_EDIT_SONG)
        Publisher().subscribe(self.__SignalOnQueryDeleteSong, viewmgr.SIGNAL_DELETE_SONG)
        Publisher().subscribe(self.__SignalOnSongUpdated, viewmgr.SIGNAL_SONG_UPDATED)
        Publisher().subscribe(self.__SignalOnQueryEditAttachments, viewmgr.SIGNAL_EDIT_LINKS)
        Publisher().subscribe(self.__SignalOnOpenEditInformation, viewmgr.SIGNAL_SHOW_EDIT_INFO)
        Publisher().subscribe(self.__SignalOnOpenEditLyrics, viewmgr.SIGNAL_SHOW_EDIT_LYRICS)
        Publisher().subscribe(self.__SignalOnOpenEditProgres, viewmgr.SIGNAL_SHOW_EDIT_PROGR)
        Publisher().subscribe(self.__SignalOnCreateLinksDir, viewmgr.SIGNAL_LINKS_DIR_CREATED)
        
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
        self.Center()

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
            viewmgr.signalDbChange()
            
        # at the end, make sure we are in the correct edit state
        # TODO: Shouldn't we use OnUpdateUI event instead?
        self.__SyncMenuItems()
            
    #---------------------------------------------------------------------------
    def OnExit(self, event): 
        self.Close()

    #---------------------------------------------------------------------------
    def __OnAddNewSong(self, event): 
        """ Event handler to add a new song """
        
        # call back on a signal we catch ourselves
        viewmgr.signalAddSong()
                
    #---------------------------------------------------------------------------
    def __SignalOnSongSelected(self, message):
        """ A song is selected. When we have NONE as song, we disable the 
            menus that should not be pressed when there is no song
            Subscribed to VIEWMGR """
        
        # make sure our menu system will not permit user to do silly things
        self.__SyncMenuItems()

    #---------------------------------------------------------------------------
    def __SignalOnQueryAddSong(self, message = None):
        """ We received a query from somewhere to add a new song to the database
            this is either sent from the popup menu or ourselves 
            Subscribed to VIEWMGR """
            
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
            
            # invoke the add signal
            viewmgr.signalSongAdded(s)
            
            # check if we are visible or not, if not mention this to the user and 
            # offer them to reset the songfilter
            if s not in viewmgr.Get()._critList:
                res = wx.MessageBox('The song added is not yet visible due to filter criteria.\n' + \
                                    'Do you want to reset the song filter?', 'Not visible', wx.ICON_INFORMATION | wx.YES_NO )
                if res == wx.YES:
                    viewmgr.signalResetFilter()

        dlg.Destroy()  

    #---------------------------------------------------------------------------
    def __SignalOnQueryEditSong(self, message = None):
        """ The song needs to be edited, we catch a signal from the view manager
            to allow other GUI elements to also issue this edit action 
            Subscribed to VIEWMGR """
        
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
  
                # signal everyone the song is updated
                viewmgr.signalSongUpdated(s)

            dlg.Destroy()

    #---------------------------------------------------------------------------
    def __OnEditNewSong(self, event): 
        """ Menu handler for a song edit action. We call back on ourselves """
        
        # we callback on ourselves
        viewmgr.signalEditSong()

    #---------------------------------------------------------------------------
    def __SignalOnQueryDeleteSong(self, message = None):
        """ A signal to delete a song from the database, this is a callback signal to
            allow other GUI elements to delete the song if needed 
            Subscribed to VIEWMGR """
        
        if self._filter._selectedSong:
            res = wx.MessageBox('Are you sure you want to remove the song from the database?\n'
                                   'All related lyrics, tabs and information will be permanently lost!', 'Warning', wx.ICON_QUESTION | wx.YES_NO)
            if res == wx.YES:
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Delete(self._filter._selectedSong)   
      
                # now transmit the deletion, and let the system
                # choose a new song to display
                viewmgr.signalSongDeleted(self._filter._selectedSong)

    #---------------------------------------------------------------------------
    def __OnDeleteSong(self, event): 
        """ Menu handler for deleting a song """
        
        # callback on ourselves 
        viewmgr.signalDeleteSong()
        
    #---------------------------------------------------------------------------
    def __OnEditCategories(self, event):
        """ Menu handler to edit the categories belonging to the song """
        
        s = self._filter._selectedSong
        if s <> None:    
            dlg = CategoriesDlg.CategoriesDlg(self)
            dlg.SetCurrentSong(s)
            if dlg.ShowModal() == wx.ID_OK:

                # update the song in the database
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Update(s, all = True)     
                
                # tell all views we updated
                viewmgr.signalSongUpdated(s)

            dlg.Destroy()

    #---------------------------------------------------------------------------
    def __OnChangeStatus(self, event):
        """ Set the status of the song
            NOTE: This should eventually be done by a log mechanism """
            
        song = viewmgr.Get()._selectedSong
        if song:
            # if our status differs, force an update
            if song._status <> self.__menu_status_lookup[event.GetId()]:
                viewmgr.signalSongStatusChange(song, self.__menu_status_lookup[event.GetId()])

    #---------------------------------------------------------------------------
    def __OnShowOptions(self, event): 
        """ Show the options dialog, all options saving is done inside the dialog 
            itself so there is no need for catching the modalresult """
        dlg = OptionsDlg.OptionsDlg(self)
        dlg.Center()
        dlg.ShowModal()
        dlg.Destroy()

    #---------------------------------------------------------------------------
    def __OnClose(self, event):
        
        # send quit event first
        viewmgr.signalAppQuit()
        
        cfg = appcfg.Get()
        cfg.Write(appcfg.CFG_LAYOUT_LAST, self.__aui.SavePerspective())  
        width, height = self.GetSize()
        cfg.WriteInt(appcfg.CFG_LAYOUT_LAST_W, width)
        cfg.WriteInt(appcfg.CFG_LAYOUT_LAST_H, height)        
        event.Skip()  

    #---------------------------------------------------------------------------
    def __OnRestoreLayout(self, event): 
        self.__aui.LoadPerspective(appcfg.Get().Read(appcfg.CFG_LAYOUT_DEFAULT, ''), True)

    #---------------------------------------------------------------------------
    def __OnToggleEditWindow(self, event): 
        self.__aui.GetPane("editpanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __OnToggleSongSelector(self, event): 
        self.__aui.GetPane("songspanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __OnToggleFilterWindow(self, event): 
        self.__aui.GetPane("filterpanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __OnShowDatabaseWizard(self, event): 
        """ User wants to switch DB's or upgrade, or create a DB, or create a demo db.
            This can also be auto invoked by the application to let the user select a DB """

        dlg = WelcomeDlg.WelcomeDlg(self)            
        dlg.Centre()
        dlg.ShowModal()
        dlg.Destroy()

        if not db.engine.Get().IsOpened():    
            self.Close()
            return

        viewmgr.signalDbChange()

    #---------------------------------------------------------------------------
    def __SignalOnSongUpdated(self, message):
        """ Song is updated, we need to make sure the user cannot select menu items that make 
            no sense. Subscribed to VIEWMGR """
            
        # update a song in the view filter
        self.__SyncMenuItems()

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
    def __OnAbout(self, event):
        """ Show the about dialog with information about the application """
        
        info = wx.AboutDialogInfo()
        info.Icon = wx.IconFromBitmap(guitarportfolio_icon.getBitmap())
        info.Name = appcfg.APP_TITLE
        info.Version = appcfg.APP_VERSION
        info.Copyright = "(C) 2007 Jorgen Bodde, ImpossibleSoft"
        info.Description = wordwrap(appcfg.description, 350, wx.ClientDC(self))
        info.WebSite = (appcfg.site_url[0], appcfg.site_url[1])
        info.Developers = [ "Jorgen Bodde (jorgb@xs4all.nl)" ]
        info.License = wordwrap(appcfg.licensetext, 500, wx.ClientDC(self))
        wx.AboutBox(info)
        
    #---------------------------------------------------------------------------
    def __OnVisitSite(self, event):
        """ Execute the internet page as an external link """

        # use execute_uri
        linkfile.execute_uri('http://guitarportfolio.berlios.de')

    #---------------------------------------------------------------------------
    def __SyncMenuItems(self):
        """ Synchronize disabled / enabled state of some of the menu items so 
            that the user is not tempted to click anything that does nothing 
            anyway. """
        
        song = viewmgr.Get()._selectedSong
        self.__menuEditSong.Enable(song <> None)
        self.__menuDeleteSong.Enable(song <> None)
        self.__menuEditCategories.Enable(song <> None)
        self.__menuEditCategories.Enable(song <> None)
        self.__menuEditReset.Enable(False)

        # check if we have a valid song work directory, and 
        # enable all menu items that go with it
        validWorkDir = False
        if song:
            validWorkDir = os.path.exists(appcfg.GetAbsWorkPathFromSong(song))

        self.__menuCreateAttachDir.Enable(song <> None and not validWorkDir)
        self.__menuAddAttachments.Enable(validWorkDir)
        self.__menuEditAttachments.Enable(validWorkDir)
        self.__menuRefreshAttachments.Enable(validWorkDir)

        # enable status based upon previous status
        if song:
            for id in self.__menu_status_lookup.iterkeys():
                if self.__menu_status_lookup[id] == songs.SS_POSTPONED:
                    self.__menuSongStatus.Enable(id, song._status == songs.SS_STARTED)
                elif self.__menu_status_lookup[id] == songs.SS_STARTED:
                    self.__menuSongStatus.Enable(id, song._status == songs.SS_COMPLETED or \
                                                     song._status == songs.SS_POSTPONED or \
                                                     song._status == songs.SS_NOT_STARTED)
                elif self.__menu_status_lookup[id] == songs.SS_COMPLETED:
                    self.__menuSongStatus.Enable(id, song._status == songs.SS_STARTED)
        else:
            for id in self.__menu_status_lookup.iterkeys():
                self.__menuSongStatus.Enable(id, False) 
        
    #---------------------------------------------------------------------------
    def __OnCreateAttachmentsDir(self, event):
        """ 
        We received a menu event and need to create the attachments dir
        """
        viewmgr.signalOnCreateAttachmentsDir(viewmgr.Get()._selectedSong)   

    #---------------------------------------------------------------------------
    def __OnAddAttachments(self, event):
        pass

    #---------------------------------------------------------------------------
    def __OnEditAttachments(self, event):
        viewmgr.signalEditAttachments()

    #---------------------------------------------------------------------------
    def __OnRefreshAttachments(self, event):
        pass
        
    #---------------------------------------------------------------------------
    def __SignalOnQueryEditAttachments(self, message):
        dlg = AttachmentManageDlg.AttachmentManageDlg(self)
        dlg.SetData()
        dlg.ShowModal()
        dlg.Destroy()        
        
        # save the contents to the existing work directory
        linkmgt.Get().Save()
        
        # reload the attachments
        viewmgr.signalRefreshLinks()

    #---------------------------------------------------------------------------
    def __SignalOnOpenEditInformation(self, message):
        """ 
        We received a signal to open the editor pane if not opened yet, and select the 
        edit tab for the song info. Let's do so
        """
        self.__songEditNotebook.SelectSongInfoTab()
        self.__aui.GetPane("editpanel").Show(True)
        self.__aui.Update()
        
    #---------------------------------------------------------------------------
    def __SignalOnOpenEditLyrics(self, message):
        """ 
        We received a signal to open the editor pane if not opened yet, and select the 
        edit tab for the song lyrics. Let's do so
        """
        self.__songEditNotebook.SelectSongLyricsTab()
        self.__aui.GetPane("editpanel").Show(True)
        self.__aui.Update()
        
    #---------------------------------------------------------------------------
    def __SignalOnOpenEditProgres(self, message):
        """ 
        We received a signal to open the editor pane if not opened yet, and select the 
        edit tab for the song progress. Let's do so
        """
        self.__songEditNotebook.SelectSongProgressTab()
        self.__aui.GetPane("editpanel").Show(True)
        self.__aui.Update()

    #---------------------------------------------------------------------------
    def __SignalOnCreateLinksDir(self, message):
        """
        We received a signal that the links dir is created, update our menu items
        """
        self.__SyncMenuItems()    
