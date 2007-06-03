import os.path

import wx
from objs import linkmgt
import appcfg

def executelink(link):
    if link:
        path = linkmgt.Get().GetLinkPath(link)
        if path:
            if "wxMSW" in wx.PlatformInfo:
                os.startfile(os.path.normcase(path))
            else:
                exec_cmd = appcfg.Get().Read(appcfg.CFG_LINUX_EXEC_CMD)
                if exec_cmd:
                    cmd = exec_cmd + ' ' + os.path.normcase(path).replace(' ', '\\ ')
                    if os.system(cmd) <> 0:
                        wx.MessageBox('Could not execute the following command:\n' + \
                                      '\'%s\'\n\n' % (cmd,) + \
                                      'Make sure the command is correct and a mime-type is associated with the extension', 
                                      'Cannot execute', wx.ICON_ERROR | wx.OK)
                        
                else:
                    wx.MessageBox('Please specify the shell execute command in the options', 
                                  'Cannot execute', wx.ICON_ERROR | wx.OK)
