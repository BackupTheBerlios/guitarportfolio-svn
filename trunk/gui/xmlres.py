import wx
import wx.xrc as xrc
import os.path
import SongFilterPanel

class GpfXmlResourceHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Specify the styles recognized by objects of this type
        self.AddStyle("wxNO_3D", wx.NO_3D)
        self.AddStyle("wxTAB_TRAVERSAL", wx.TAB_TRAVERSAL)
        self.AddStyle("wxWS_EX_VALIDATE_RECURSIVELY", wx.WS_EX_VALIDATE_RECURSIVELY)
        self.AddStyle("wxCLIP_CHILDREN", wx.CLIP_CHILDREN)
        self.AddWindowStyles()

    # This method and the next one are required for XmlResourceHandlers
    def CanHandle(self, node):
        return self.IsOfClass(node, "SongFilterPanel")

    def DoCreateResource(self):
        # The simple method assumes that there is no existing
        # instance.  Be sure of that with an assert.
        assert self.GetInstance() is None

        # Now create the object
        panel = SongFilterPanel(self.GetParentAsWindow(),
                                self.GetID(),
                                self.GetPosition(),
                                self.GetSize(),
                                self.GetStyle("style", wx.TAB_TRAVERSAL),
                                self.GetName())

        # These two things should be done in either case:
        # Set standard window attributes
        self.SetupWindow(panel)
        # Create any child windows of this node
        self.CreateChildren(panel)

        return panel

# ==============================================================================
        
class GpfXmlResource(object):
    def __init__(self):
        self._res = None
    
    def Load(self, name):
        """ Load the XML file into memory for easy access """
        if os.path.exists(name) and os.path.isfile(name):
            self._res = xrc.EmptyXmlResource()
            #self._res.InsertHandler(GpfXmlResourceHandler())
            self._res.Load(name)
        else:
            raise Exception("Cannot load XML resource '%s'" % (name,))

# ==============================================================================

__obj = None
def Get():
    global __obj
    if not __obj:
        __obj = GpfXmlResource()
    return __obj
def Res():
    return Get()._res
