import wx
import wx.xrc as xrc
import xmlres

class ProgressPanel(wx.Panel):
    def __init__(self, parent, id = wx.ID_ANY):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "ProgressPanel")
        self.PostCreate(pre)

        self.__accuracy = xrc.XRCCTRL(self,"ID_ACC_SLIDER")
        self.__accuracyNr = xrc.XRCCTRL(self,"ID_GRADE_ACC")
        self.__estimated = xrc.XRCCTRL(self,"ID_COMP_SLIDER")
        self.__estimatedNr = xrc.XRCCTRL(self,"ID_GRADE_COMP")
        self.__percent = xrc.XRCCTRL(self,"ID_COMPLETED")
        self.__minutes = xrc.XRCCTRL(self,"ID_MIN_STUDIED")
        self.__minuteButton = xrc.XRCCTRL(self,"ID_ADD_STUDYTIME")
        self.__status = xrc.XRCCTRL(self,"ID_NEW_STATUS")
        self.__statusButton = xrc.XRCCTRL(self,"ID_CHANGE_STATUS")
        self.__log = xrc.XRCCTRL(self,"ID_LOG_TEXT")
        self.__submitButton = xrc.XRCCTRL(self,"ID_SUBMIT")
                     
        self.__status.SetSelection(0)

        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.__OnAccuracyEnd, self.__accuracy)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.__OnAccuracyScroll, self.__accuracy)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.__OnCompletedEnd, self.__estimated)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.__OnCompletedScroll, self.__estimated)

    def __OnAccuracyEnd(self, event): 
        print "Event handler `__OnAccuracyEnd' not implemented!"
        event.Skip()

    def __OnAccuracyScroll(self, event): 
        print "Event handler `__OnAccuracyScroll' not implemented!"
        event.Skip()

    def __OnCompletedEnd(self, event):
        print "Event handler `__OnCompletedEnd' not implemented!"
        event.Skip()

    def __OnCompletedScroll(self, event):
        print "Event handler `__OnCompletedScroll' not implemented!"
        event.Skip()

# end of class ProgressPanel


