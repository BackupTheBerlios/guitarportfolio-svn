import os
import os.path
import sys

import wx
from wx.lib.pubsub import Publisher
import wx.lib.mixins.listctrl as listmix
import wx.xrc as xrc

from images import icon_path_ok, icon_path_not_ok
from objs import signals, linkmgt
import appcfg, xmlres
                
class LinksPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "EditLinkDialog")
        self.PostCreate(pre)

        # TODO: Make a wx.ListCtrl, listmix.ListCtrlAutoWidthMixin custom class for XRC
        self._links = xrc.XRCCTRL(self, "ID_LINK_LIST")
        self._links.InsertColumn(0, "Name", width = 200)
        self._links.InsertColumn(1, "Type", width = 75)        
        self._links.InsertColumn(2, "Link", width = 300)
        self.__basePath = xrc.XRCCTRL(self, "ID_LINK_PATH")
        self.__pathOK = xrc.XRCCTRL(self, "ID_PATH_STATUS")
        self.__create = xrc.XRCCTRL(self, "ID_BTN_CREATE")
        self.__refresh = xrc.XRCCTRL(self, "ID_BTN_REFRESH")
        self.__addURL = xrc.XRCCTRL(self, "ID_BTN_ADD")
        self.__ignoreFile = xrc.XRCCTRL(self, "ID_BTN_IGNORE")
        self.__manage = xrc.XRCCTRL(self, "ID_BTN_EDIT")
       
        self.Bind(wx.EVT_BUTTON, self.__OnCreateBasePath, self.__create)
        self.Bind(wx.EVT_BUTTON, self.__OnRefresh, self.__refresh)
        self.Bind(wx.EVT_BUTTON, self.__OnAddURL, self.__addURL)
        self.Bind(wx.EVT_BUTTON, self.__OnIgnoreFile, self.__ignoreFile)
        self.Bind(wx.EVT_BUTTON, self.__OnManageFiles, self.__manage)

        Publisher().subscribe(self.__OnSongSelected, signals.APP_CLEAR)
        Publisher().subscribe(self.__OnSongSelected, signals.SONG_VIEW_SELECTED)
        Publisher().subscribe(self.__OnSongUpdated, signals.SONG_VIEW_UPDATED)
        Publisher().subscribe(self.__OnConfigUpdated, signals.CFG_UPDATED)
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__OnExecuteLink, self._links)

        self._song = None

    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ A song is selected. When we get an empty song, disable and clear
            when we get a song, get the signals, set the work path and also
            sync the icon to verify if the path already exists or not """
        
        self._song = message.data
        self.__create.Enable(self._song <> None)        
        self.__SyncWorkDirState()
        
        if self._song:
            self.__PopulateLinks()
        else:
            self._links.DeleteAllItems()
        
    # --------------------------------------------------------------------------
    def __OnSongUpdated(self, message):
        """ A song is updated, we need to resync the state of the work dir """
        self.__SyncWorkDirState()

    # --------------------------------------------------------------------------
    def __OnConfigUpdated(self, message):
        """ Config is updated, we need to resync the state of the work dir """
        self.__SyncWorkDirState()
        
    # --------------------------------------------------------------------------
    def __SyncWorkDirState(self):
        """ Syncs the work dir and enables / disables the buttons and shows the 
            latest workdir for the user. Returns True when there is a valid
            work directory """
        if self._song:
            path = appcfg.GetAbsWorkPathFromSong(self._song)
            path_ok = os.path.exists(path)
            if path_ok:
                self.__pathOK.SetBitmap(icon_path_ok.getBitmap())
            else:
                self.__pathOK.SetBitmap(icon_path_not_ok.getBitmap())

            self.__create.Enable(not path_ok)
            self.__SyncButtonState(path_ok)
            self.__basePath.SetLabel(path)

            return path_ok            
        else:
            self.__basePath.SetLabel('N/A')
            self.__pathOK.SetBitmap(icon_path_not_ok.getBitmap())
            self.__SyncButtonState(False)
            
        return False
         
    # --------------------------------------------------------------------------
    def __SyncButtonState(self, valid_path):
        """ Enable / Disable a group of buttons when this is needed """
        self._links.Enable(valid_path)
        self.__refresh.Enable(valid_path)
        self.__addURL.Enable(valid_path)
        self.__ignoreFile.Enable(valid_path)
        self.__manage.Enable(valid_path) 

    def __PopulateLinks(self):
        """ Populate the links in the link list view """
        self._links.DeleteAllItems()
        for l in linkmgt.Get().links:
            index = self._links.InsertStringItem(sys.maxint, l._name)
            self._links.SetStringItem(index, 1, l._type)
            self._links.SetStringItem(index, 2, '')
            self._links.SetItemData(index, l._id)
            # TODO: Set icon in front of link            

    # --------------------------------------------------------------------------
    def __RefreshLinks(self):
        """ Refreshes the view, can be called from multiple handlers """
        linkmgt.Get().Load(appcfg.GetAbsWorkPathFromSong(self._song))
            
    # --------------------------------------------------------------------------
    def __OnCreateBasePath(self, event): # wxGlade: LinksPanel.<event_handler>
        path = appcfg.GetAbsWorkPathFromSong(self._song)
        if os.path.isabs(path):        
            result = wx.MessageBox('Would you like to create the work directory for this song?', 'Warning', wx.ICON_QUESTION | wx.YES_NO)
            if result == wx.YES:
                try:
                    os.makedirs(path)
                    wx.MessageBox('Path creation succesful!\n'
                                  'Now copy your gathered song files to this directory', 'Succes', wx.ICON_INFORMATION | wx.OK)                
                except EnvironmentError:
                    wx.MessageBox('Path creation unsuccesful\n'
                                  'Please check for a valid base path, file rights and retry', 'Error', wx.ICON_ERROR | wx.OK)
                self.__SyncWorkDirState()
        else:
            # warn about relative path
            wx.MessageBox('Cannot create a relative work directory\n'
                          'Please fill in your base directory in the Preferences', 'Error', wx.ICON_ERROR | wx.OK)
            
    # --------------------------------------------------------------------------
    def __OnExecuteLink(self, event):
        l = linkmgt.Get().links.find_id(event.GetData())
        linkfile.executelink(l)
    # --------------------------------------------------------------------------
    def __OnRefresh(self, event): 
        """ Refresh button is pressed, check if the directory is valid
            and if so, repopulate the links """
        if self.__SyncWorkDirState():
            self.__RefreshLinks()

    # --------------------------------------------------------------------------
    def __OnAddURL(self, event): 
        print "Event handler `__OnAddURL' not implemented!"
        event.Skip()

    # --------------------------------------------------------------------------
    def __OnIgnoreFile(self, event): 
        print "Event handler `__OnIgnoreFile' not implemented!"
        event.Skip()

    # --------------------------------------------------------------------------
    def __OnManageFiles(self, event): 
        print "Event handler `__OnManageFiles' not implemented!"
        event.Skip()


