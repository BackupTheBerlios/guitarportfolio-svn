import datetime
import os.path
import sys

import wx
import wx.xrc as xrc

import db.engine
from objs import linkmgt
from images import icon_attachment, icon_ignore
import appcfg, xmlres, linkfile

class AttachmentManageDlg(wx.Dialog):
    def __init__(self, parent, id = wx.ID_ANY):
        pre = wx.PreDialog()
        xmlres.Res().LoadOnDialog(pre, parent, "ManageAttachmentDlg")
        self.PostCreate(pre)

        self.SetSize(wx.Size(400,400))

        self._list = xrc.XRCCTRL(self, "ID_PRESENT_ATTACHMENTS")
        self._buttonIgnore = xrc.XRCCTRL(self, "ID_IGNORE")
        self._buttonAllow = xrc.XRCCTRL(self, "ID_ALLOW")
        self._buttonRename = xrc.XRCCTRL(self, "ID_RENAME")
        self._buttonDelete = xrc.XRCCTRL(self, "ID_DELETE")
        self._comment = xrc.XRCCTRL(self, "ID_COMMENT")
        self._run_cmd = xrc.XRCCTRL(self, "ID_RUN_CMD")
        self._buttonTest = xrc.XRCCTRL(self, "ID_TEST_FILE")
        
        self._list.InsertColumn(0, "Type", width = 90)
        self._list.InsertColumn(1, "Name", width = 270)

        # create an image list, ignore or attachment icon
        self._icons = wx.ImageList(16, 16)
        self._icons.Add(icon_attachment.getBitmap())
        self._icons.Add(icon_ignore.getBitmap())
        self._list.SetImageList(self._icons, wx.IMAGE_LIST_SMALL)

        # hook up some events
        self.Bind(wx.EVT_BUTTON, self.__OnIgnore, self._buttonIgnore)
        self.Bind(wx.EVT_BUTTON, self.__OnAllow, self._buttonAllow)
        self.Bind(wx.EVT_BUTTON, self.__OnRename, self._buttonRename)
        self.Bind(wx.EVT_BUTTON, self.__OnDelete, self._buttonDelete)
        self.Bind(wx.EVT_TEXT, self.__OnTextChanged, self._comment)
        self.Bind(wx.EVT_TEXT, self.__OnTextChanged, self._run_cmd)
        self.Bind(wx.EVT_BUTTON, self.__OnTestFile, self._buttonTest)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.__OnItemSelected, self._list)

        self._currLink = None

    #---------------------------------------------------------------------------
    def SetData(self):
        """ Loads all data to the dialog, so that we can adjust the links """

        # populate the data in the attachment list
        links = linkmgt.Get().links
        self._list.DeleteAllItems()
        for l in links:
            index = self._list.InsertStringItem(sys.maxint, l._type)
            self._list.SetStringItem(index, 1, l._name)
            self._list.SetItemData(index, l._id)
            if l._ignored:
                self._list.SetItemImage(index, 1, 1)
            else:
                self._list.SetItemImage(index, 0, 0)
        
        self.__SyncEditState()

    #---------------------------------------------------------------------------
    def __SyncEditState(self):
        """ Synchronize the edit state of the fields, and the buttons to make
            sure the user cannot press anything stupid """
            
        global_enable = False
        ignore_enable = False
        self._currLink = None      
        
        idx = self._list.GetFirstSelected()
        if idx != wx.NOT_FOUND:
            l = linkmgt.Get().links.find_id(self._list.GetItemData(idx))
            if l:
                self._currLink = l
                global_enable = True
                # switch ignore / show flag
                if not l._ignored:
                    ignore_enable = True
                    self._list.SetItemImage(idx, 0, 0)
                else:
                    self._list.SetItemImage(idx, 1, 1)
                
                self._comment.ChangeValue(l._comment)
                self._run_cmd.ChangeValue(l._runcmd)
                    
        # no item selected, grey out all
        if global_enable:
            self._buttonIgnore.Enable(ignore_enable)
            self._buttonAllow.Enable(not ignore_enable)
        else:
            self._buttonIgnore.Enable(False)
            self._buttonAllow.Enable(False) 
        
        self._buttonRename.Enable(global_enable)
        self._buttonDelete.Enable(global_enable)
        self._comment.Enable(global_enable)
        self._run_cmd.Enable(global_enable)
        
        if not global_enable:
            # nothing to show when we have none selected
            self._comment.SetValue('')
            self._run_cmd.SetValue('')
            
    #---------------------------------------------------------------------------
    def __OnIgnore(self, event):
        """ Ignore the link in the attachment list """
        
        if self._currLink:
            self._currLink._ignored = True
            self.__SyncEditState()
            
    #---------------------------------------------------------------------------
    def __OnAllow(self, event):
        if self._currLink:
            self._currLink._ignored = False
            self.__SyncEditState()
        
    #---------------------------------------------------------------------------
    def __OnRename(self, event):
        pass
        
    #---------------------------------------------------------------------------
    def __OnTestFile(self, event):
        """ Handler of the test file button to execute the filename """
        
        if self._currLink:
            linkfile.executelink(self._currLink)    
        
    #---------------------------------------------------------------------------
    def __OnDelete(self, event):
        """ Handler to delete the link object. This also means deleting from
            disk. """
        
        if self._currLink:
            the_filename = linkmgt.Get().GetLinkPath(self._currLink)
            res = wx.MessageBox('Are you sure you want to delete the file:\n' + 
                                "'%s'" % (the_filename,) + '\n' + 
                                'Be aware that the file will be removed from disk!', 
                                'Warning', wx.ICON_QUESTION | wx.YES | wx.NO)
            if res == wx.YES:
                # attempt a remove action, set flag accordingly
                # when we are succesful
                removed_ok = False
                try:
                    os.remove(the_filename)
                    removed_ok = True                    
                except OSError:
                    wx.MessageBox('Cannot remove the file. Check file permissions and if it is not in use',
                                  'Warning', wx.ICON_ERROR | wx.OK)
                                  
                # when we removed it ok, let's remove the link and refresh
                if removed_ok:
                    linkmgt.Get().links.remove(self._currLink)
                    self.SetData()
                else:
                    # in our eternal struggle to please the user, the best we 
                    # can do, is set the ignore flag on the link as deleting 
                    # is not going to happen
                    self._currLink._ignored = True
                    self.SetData()
                    
    #---------------------------------------------------------------------------
    def __OnItemSelected(self, event):
        self.__SyncEditState()

    #---------------------------------------------------------------------------
    def __OnTextChanged(self, event):

        # sync the edit state back to the link
        if self._currLink:
            self._currLink._comment = self._comment.GetValue()
            self._currLink._runcmd = self._run_cmd.GetValue()
