import os
import os.path
import sys

import wx
from wx.lib.pubsub import Publisher
import wx.lib.mixins.listctrl as listmix
import wx.xrc as xrc

from images import icon_path_ok, icon_path_not_ok
from objs import linkmgt
import appcfg, xmlres, viewmgr
                
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
        #self.__addURL = xrc.XRCCTRL(self, "ID_BTN_ADD")
        self.__ignoreFile = xrc.XRCCTRL(self, "ID_BTN_IGNORE")
        self.__manage = xrc.XRCCTRL(self, "ID_BTN_EDIT")
       
        self.Bind(wx.EVT_BUTTON, self.__OnCreateBasePath, self.__create)
        self.Bind(wx.EVT_BUTTON, self.__OnRefresh, self.__refresh)
        #self.Bind(wx.EVT_BUTTON, self.__OnAddURL, self.__addURL)
        self.Bind(wx.EVT_BUTTON, self.__OnIgnoreFile, self.__ignoreFile)
        self.Bind(wx.EVT_BUTTON, self.__OnManageFiles, self.__manage)

        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_CLEAR_DATA)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_UPDATED)
        Publisher().subscribe(self.__OnRefreshLinks, viewmgr.SIGNAL_SETTINGS_CHANGED)
        Publisher().subscribe(self.__OnRefreshLinks, viewmgr.SIGNAL_LINKS_REFRESHED)
        Publisher().subscribe(self.__OnRefreshLinks, viewmgr.SIGNAL_LINKS_DIR_CREATED)
        
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__OnExecuteLink, self._links)

    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ A song is selected. When we get an empty song, disable and clear
            when we get a song, get the signals, set the work path and also
            sync the icon to verify if the path already exists or not """
        
        song = message.data
        self.__create.Enable(song <> None)        
        self.__SyncWorkDirState()
        
        if song:
            self.__PopulateLinks()
        else:
            self._links.DeleteAllItems()
        
    # --------------------------------------------------------------------------
    def __OnRefreshLinks(self, message):
        """ We do not change the assigned song, we only refresh the links as there are
            changes in either the populated link list, or the work directory """
        
        self.__SyncWorkDirState()
        
        song = viewmgr.Get()._selectedSong
        if song:
            self.__PopulateLinks()
        else:
            self._links.DeleteAllItems()
                
    # --------------------------------------------------------------------------
    def __SyncWorkDirState(self):
        """ Syncs the work dir and enables / disables the buttons and shows the 
            latest workdir for the user. Returns True when there is a valid
            work directory """
        song = viewmgr.Get()._selectedSong
        if song:
            path = appcfg.GetAbsWorkPathFromSong(song)
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
        #self.__addURL.Enable(valid_path)
        self.__ignoreFile.Enable(valid_path)
        self.__manage.Enable(valid_path) 

    # --------------------------------------------------------------------------
    def __PopulateLinks(self):
        """ Populate the links in the link list view """
        self._links.DeleteAllItems()
        for l in linkmgt.Get().links:
            if not l._ignored:
                index = self._links.InsertStringItem(sys.maxint, l._name)
                self._links.SetStringItem(index, 1, l._type)
                self._links.SetStringItem(index, 2, l._comment)
                self._links.SetItemData(index, l._id)         
                
    # --------------------------------------------------------------------------
    def __OnCreateBasePath(self, event): 
        """
        Create the base path. We emit a signal that will be cought in the 
        main frame where the same menu option exists
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            viewmgr.signalOnCreateAttachmentsDir(song)
            
    # --------------------------------------------------------------------------
    def __OnExecuteLink(self, event):
        l = linkmgt.Get().links.find_id(event.GetData())
        linkfile.executelink(l)

    # --------------------------------------------------------------------------
    def __OnRefresh(self, event): 
        """ Refresh button is pressed, check if the directory is valid
            and if so, repopulate the links """
        if self.__SyncWorkDirState():
            viewmgr.signalRefreshLinks()

    # --------------------------------------------------------------------------
    #def __OnAddURL(self, event): 
    #    print "Event handler `__OnAddURL' not implemented!"
    #    event.Skip()

    # --------------------------------------------------------------------------
    def __OnIgnoreFile(self, event): 
        """ Handler for ignoring the selected file """
        
        # get the link, and set the ignore flag. Then we refresh the 
        # links by issuing a signal through the view manager
        idx = self._links.GetFirstSelected()
        if idx != -1:
            link_id = self._links.GetItemData(idx)
            link = linkmgt.Get().links.find_id(link_id)
            if link:
                link._ignored = True
                # write XML file back
                linkmgt.Get().Save()                            
                viewmgr.signalRefreshLinks()

    # --------------------------------------------------------------------------
    def __OnManageFiles(self, event): 
        viewmgr.signalEditAttachments()
        event.Skip()
