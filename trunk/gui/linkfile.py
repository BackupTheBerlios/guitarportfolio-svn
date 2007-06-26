import os.path

import wx
from objs import linkmgt
import appcfg

# tags that are allowed as external link
# use is_valid_link(url) to check on these
allowed_tags = [ 'ftp', 'http', 'https', 'gopher', 'mailto', 
                 'news', 'nntp', 'telnet', 'wais', 'file', 'prospero', 
                 'aim', 'webcal']

def is_valid_external_link(url):
    """ Checks if the protocol specification is defined in one of the 
        above, so it can be executed in a browser """
    pos = url.find(':')
    if pos > 0:
        return url[:pos] in allowed_tags
    
    return False
        
# ------------------------------------------------------------------------------
def executelink(link):
    """ Execute a LINK object """

    cmd = ''
    if link:
        cmd = linkmgt.Get().GetLinkPath(link)
            
    __doExecuteCommand(cmd)

# ------------------------------------------------------------------------------
def execute_uri(link):
    """ Executes an URI or file, located in the directory in the current song """
    cmd = ''

    if link:
        # if we have an url, we do not have to get the path for the attachment
        if is_valid_external_link(link):
            cmd = link
        else:
            # TODO: The path needs to be determined to start the file
            return
            
    # determine how to execute the command 
    __doExecuteCommand(cmd)

# ------------------------------------------------------------------------------
def __doExecuteCommand(cmd):
    """ The execute command string """
    cmdstr = ''
    # we check if we execute an URI or a normal file
    if is_valid_external_link(cmd):
        cmdstr = cmd
    else:
        # in linux we must escape the spaces
        if "wxGTK" in wx.PlatformInfo:
            cmdstr = '"' + cmd + '"'
        else:
            cmdstr = os.path.normcase(cmd)

    if cmdstr:
        if "wxMSW" in wx.PlatformInfo:
            # simple shell execute.
            # TODO: Is there a way to get a status back?
            os.startfile(os.path.normcase(cmdstr))
        else:
            exec_cmd = appcfg.Get().Read(appcfg.CFG_LINUX_EXEC_CMD)
            if exec_cmd:
                runcmd = exec_cmd + ' ' + cmdstr 
                if os.system(runcmd) <> 0:
                    wx.MessageBox('Could not execute the following command:\n' + \
                                  '\'%s\'\n\n' % (runcmd,) + \
                                  'Make sure the command is correct and a mime-type is associated with the extension', 
                                  'Cannot execute', wx.ICON_ERROR | wx.OK)
                    
            else:
                wx.MessageBox('Please specify the shell execute command in the options', 
                              'Cannot execute', wx.ICON_ERROR | wx.OK)
    else:
        wx.MessageBox('No command to execute!', 'Cannot execute', wx.ICON_ERROR | wx.OK)
    
