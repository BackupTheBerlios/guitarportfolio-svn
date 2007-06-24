import os

import wx
import wx.xrc as xrc
import xmlres, appcfg, viewmgr

class OptionsDlg(wx.Dialog):
    def __init__(self, parent, id = wx.ID_ANY):
        pre = wx.PreDialog()
        xmlres.Res().LoadOnDialog(pre, parent, "OptionsDialog")
        self.PostCreate(pre)

        self.__absPath = xrc.XRCCTRL(self, "ID_BASE_PATH")
        self.__execPath = xrc.XRCCTRL(self, "ID_SHELL_EXEC")
        
        self.Bind(wx.EVT_BUTTON, self.__OnBrowsePath, xrc.XRCCTRL(self, "ID_BROWSE"))
        self.Bind(wx.EVT_BUTTON, self.__OnOK,  xrc.XRCCTRL(self, "wxID_OK"))

        self.SetSize(wx.Size(400,300))
        
        # read settings
        self.__absPath.SetValue(appcfg.Get().Read(appcfg.CFG_ABSWORKPATH, ''))

        # if we are under linux, we show some elements
        if "wxMSW" in wx.PlatformInfo:
            self.__execPath.Enable(False)
            self.__execPath.SetValue("N/A");
        else:
            self.__execPath.SetValue(appcfg.Get().Read(appcfg.CFG_LINUX_EXEC_CMD, 'gnome-open'))        

    # --------------------------------------------------------------------------
    def __OnBrowsePath(self, event): 
        path = wx.DirSelector('Select the absolute work directory', self.__absPath.GetValue())
        if path:
            self.__absPath.SetValue(path)   

    # --------------------------------------------------------------------------
    def __OnOK(self, event): 
        """ Press OK, verify the path and notify if the path is not valid """

        path = self.__absPath.GetValue()
        if not os.path.exists(path):        
            wx.MessageBox('The path specified is not a valid path!', 'Error', wx.ICON_ERROR | wx.OK)
            return
        appcfg.Get().Write(appcfg.CFG_ABSWORKPATH, path)
        if "wxGTK" in wx.PlatformInfo:
            appcfg.Get().Write(appcfg.CFG_LINUX_EXEC_CMD, self.__execPath.GetValue())        
        
        # issue a change of settings
        viewmgr.signalSettingsChanged()
        event.Skip()


