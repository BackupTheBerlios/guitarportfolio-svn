
import dircache
import os.path

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
    # --------------------------------------------------------------------------
    def __init__(self, name, id):
        self.__mName = name
        self.__mID = id
        self.__mType = ''

        # set type, based upon a dictionary
        root, ext = os.path.splitext(name)
        if ext:            
            for type_name, type_exts in _types_lookup:                
                if ext.lower() in type_exts:
                    self.__mType = type_name
                    break
            if not self.__mType:
                self.__mType = ext
        else:
            self.__mType = 'UNKNOWN'
        
    # --------------------------------------------------------------------------
    def getName(self): return self.__mName
    def setName(self, value): self.__mName = value
    
    def getType(self): return self.__mType
    
    def getID(self): return self.__mID
    id = property(fget = getID)
    
    
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
        self.__mWorkPath = ''
        self.__mLastLinkID = 0
        self.Clear()
        
    # --------------------------------------------------------------------------
    def Load(self, workdir):
        """ Checks the work dir, loads all files present, and adjusts the list
            based upon the XML file present (or not) in the direstory """
        self.Clear()
        self.__mWorkPath = ''
        if os.path.exists(workdir):
            # gather files, sort and process
            self.__mWorkPath = workdir
            items = dircache.listdir(workdir)
            for f in items:
                if os.path.isfile(os.path.join(workdir, f)):
                    l = Link(f, self.__mLastLinkID)
                    self.__mLinks.append(l)
                    self.__mLastLinkID += 1        
        else:
            return False

    # --------------------------------------------------------------------------
    def Clear(self):
        self.__mLinks = []
        self.__mLastLinkID = 0

    # --------------------------------------------------------------------------
    def getLinks(self): return self.__mLinks
    links = property(fget = getLinks)
    
    # --------------------------------------------------------------------------
    def FindLinkByID(self, id):
        """ Return link by ID """
        for l in self.__mLinks:
            if l.id == id:
                return l
        return None
    
    # --------------------------------------------------------------------------
    def GetLinkPath(self, link):
        """ Returns the full link name + path that can be used to execute the file """
        result = ''
        if link in self.__mLinks:
            result = os.path.join(self.__mWorkPath, link.getName())
        return result
        
