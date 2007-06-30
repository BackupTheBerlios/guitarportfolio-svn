import gui.guitarportfolio as gpf
import sys, traceback, wx

# exception hook to display a wx.LogError
def excepthook(type, value, trace):
    if wx and sys and traceback:
        exc = traceback.format_exception(type, value, trace)
        for e in exc: wx.LogError(e)
        wx.LogError('Unhandled Error: %s: %s'%(str(type), str(value)))
        sys.__excepthook__(type, value, trace)

sys.excepthook = excepthook
guitarportfolio = gpf.GuitarPortfolioApp(redirect=True)
guitarportfolio.MainLoop()
