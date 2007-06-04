
import dircache
import os.path
from wx.lib.pubsub import Publisher
from objs import signals, objlist

# a comprehensive list of types where extensions are translated to 
# a description, e.g. .AVI extension becomes VIDEO
_types_lookup = [ ( 'VIDEO',      [ '.avi',  '.mpg', '.mp4', '.mov', '.vlc' ] ), 
                  ( 'GUITAR RRO', [ '.gp3',  '.gp4', '.gp5' ] ),
                  ( 'IMAGE',      [ '.jpeg', '.jpg', '.png', '.gif', '.bmp' ] ),
                  ( 'AUDIO',      [ '.mp3',  '.wav', '.ogg', '.au' ] ),
                  ( 'PDF TEXT',   [ '.pdf' ] ),
                  ( 'TEXT / TAB', [ '.txt' ] ),
                  ( 'TAB FILE',   [ '.tab' ] ) ]

"""
    The link object holding information per file in the work dir, of a reference
    to another file, or an internet URL, etc.
"""
class Link(object):
    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._type = ''

        # set type, based upon a dictionary
        root, ext = os.path.splitext(name)
        if ext:            
            for type_name, type_exts in _types_lookup:                
                if ext.lower() in type_exts:
                    self._type = type_name
                    break
            if not self._type:
                self._type = ext
        else:
            self._type = 'UNKNOWN'

# ==============================================================================

"""
    Link manager object, responsible for reading the link information and storing
    it in link objects. The object can either auto discover link information from
    a base directory or read from XML files what to do with the discovered files and
    add extra information to it.
"""
class LinkMgr(object):
    # --------------------------------------------------------------------------
    def __init__(self):
        self._workPath = ''
        self._lastLinkID = 0
        self.links = objlist.ObjList(class_name = Link)
        self.Clear()

    # --------------------------------------------------------------------------
    def Load(self, workdir):
        """ Checks the work dir, loads all files present, and adjusts the list
            based upon the XML file present (or not) in the direstory """
        self.Clear()        
        self._workPath = ''
        if os.path.exists(workdir):
            # gather files, sort and process
            self._workPath = workdir
            try:
                items = dircache.listdir(workdir)
                for f in items:
                    if os.path.isfile(os.path.join(workdir, f)):
                        l = Link(f, self._lastLinkID)
                        self.links.append(l)
                        self._lastLinkID += 1
                Publisher().sendMessage(signals.LINKMGR_POPULATED)
            except OSError:
                return False
        else:
            return False

    # --------------------------------------------------------------------------
    def Clear(self):
        Publisher().sendMessage(signals.LINKMGR_CLEAR)
        self.links.clear()
        self._lastLinkID = 0
    
    # --------------------------------------------------------------------------
    def GetLinkPath(self, link):
        """ Returns the full link name + path that can be used to execute the file """
        result = ''
        if self.links.has_item(link):
            result = os.path.join(self._workPath, link._name)
        return result

# ==============================================================================

__obj = None
def Get():
    global __obj
    if not __obj:
        __obj = LinkMgr()
    return __obj
