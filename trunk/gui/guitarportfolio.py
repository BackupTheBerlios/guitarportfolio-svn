
import os

import wx
from GuitarPortfolioFrame import GuitarPortfolioFrame
import appcfg, xmlres

class GuitarPortfolioApp(wx.App):
    #def __init__(self, redirect = True, filename = None, useBestVisual = False, clearSigInt = True):
    #    super(GuitarPortfolioApp, self).__init__(redirect, filename, useBestVisual, clearSigInt)    
    #    pass 

    def OnInit(self):
        wx.InitAllImageHandlers()

        # load XML handler
        res = xmlres.Get().Load(appcfg.CFG_XRCFILE)

        self.SetAppName(appcfg.CFG_APPNAME)
        
        cwd = os.getcwd()
        imgpath = os.path.join(cwd, 'images')
        if not os.path.exists(imgpath):
            print 'Images path not found! Please run application from the root dir!'
            return 0
        else:
            appcfg.imagesdir = imgpath
        
        # init frame, and show
        MainFrame = GuitarPortfolioFrame(None, -1, "")
        self.SetTopWindow(MainFrame)
        MainFrame.Show()
        return 1

    def OnExit(self):
        """ Exit the application """
        appcfg.Get().Flush()


if __name__ == "__main__":
    guitarportfolio = GuitarPortfolioApp(0)
    guitarportfolio.MainLoop()
