
import dircache
import os.path
import fnmatch

from wx.lib.pubsub import Publisher
from objs import signals, objlist
import xml.parsers.expat
import xml.dom.minidom

# a comprehensive list of types where extensions are translated to 
# a description, e.g. .AVI extension becomes VIDEO
_types_lookup = [ ( 'VIDEO',      [ '.avi',  '.mpg', '.mp4', '.mov', '.vlc' ] ), 
                  ( 'GUITAR RRO', [ '.gp3',  '.gp4', '.gp5' ] ),
                  ( 'IMAGE',      [ '.jpeg', '.jpg', '.png', '.gif', '.bmp' ] ),
                  ( 'AUDIO',      [ '.mp3',  '.wav', '.ogg', '.au' ] ),
                  ( 'PDF TEXT',   [ '.pdf' ] ),
                  ( 'TEXT / TAB', [ '.txt' ] ),
                  ( 'TAB FILE',   [ '.tab' ] ) ]

# remove files from auto attachment discover engine that match these extensions 
# TODO: Should be placed in an config module
_ignore_masks = [ '*.bak', '*.~*', '*.*~' ]

# file that holds extra information for all attachments
XML_ATTACHMENT_FILE = 'attachments.xml'

"""
    The link object holding information per file in the work dir, of a reference
    to another file, or an internet URL, etc.
"""
class Link(object):
    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._type = ''
        self._ignored = False
        self._comment = ''
        self._runcmd = ''
        self._in_xml = False

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
            
    def __setattr__(self, name, value):
        # always set this flag
        self.__dict__["_in_xml"] = True
        self.__dict__[name] = value
        
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
                    if os.path.isfile(os.path.join(workdir, f)) and not (f == XML_ATTACHMENT_FILE):
                        # check for match
                        okfile = True
                        for tf in _ignore_masks:
                            if fnmatch.fnmatch(f, tf):
                                okfile = False
                                break
                        if okfile:
                            l = Link(f, self._lastLinkID)
                            self.links.append(l)
                            self._lastLinkID += 1
                            l._in_xml = False   # reset the flag
                Publisher().sendMessage(signals.LINKMGR_POPULATED)
            except OSError:
                return False
        
            # now go and parse the XML file that goes with it for 
            # further information, and extend the links 
            self.__parsed_link = None
            xmlfile = os.path.join(workdir, XML_ATTACHMENT_FILE)
            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = self.__OnParseElement
            p.CharacterDataHandler = self.__OnParseElementData
            try:
                f = open(xmlfile)
                p.ParseFile(f)
            except IOError:
                pass
        else:
            return False

    # --------------------------------------------------------------------------
    def Save(self):
        # create XML document
        doc = xml.dom.minidom.Document() 
        root = doc.createElement('guitarportfolio')
        doc.appendChild(root)
        
        attachments = doc.createElement('attachments')
        root.appendChild(attachments)
        
        # write links that need to be written
        for l in self.links:
            if l._in_xml:
                attm = doc.createElement('file')
                attm.setAttribute('name', l._name)
                attm.setAttribute('ignore', "yes" if l._ignored else "no")
                if l._comment:
                    attm.setAttribute('comment', l._comment)
                if l._runcmd:
                    attm.setAttribute('runcmd', l._runcmd)
                attachments.appendChild(attm)
                            
        # save the string
        xmlfile = os.path.join(self._workPath, XML_ATTACHMENT_FILE)
        try:
            f = open(xmlfile, 'w')
            f.write(doc.toprettyxml())
            f.close()       
        except IOError:
            return

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

    # --------------------------------------------------------------------------
    def __OnParseElement(self, name, attrs):
        self.__parsed_link = None  
        if name.lower() == 'file':
            self.__parsed_link = None  
            # a file node, look up our link, and 
            # set the properties, if any present
            if 'name' in attrs:
                lname = attrs['name']
                for l in self.links:
                    if l._name.lower() == lname.lower():
                        self.__parsed_link = l
                        break
            
            link = self.__parsed_link
            if link:
                link._in_xml = True
                
                # ignore flag, to leave link out of list of attachments
                if 'ignore' in attrs:
                    ignore = attrs['ignore']
                    link._ignored = (ignore.lower() == "yes" or ignore == "1")

                # comment for the attachment
                if 'comment' in attrs:                    
                    link._comment = attrs['comment']

                # run command for the attachment
                if 'runcmd' in attrs:                    
                    link._runcmd = attrs['runcmd']


    # --------------------------------------------------------------------------
    def __OnParseElementData(self, data):
        pass
# ==============================================================================

__obj = None
def Get():
    global __obj
    if not __obj:
        __obj = LinkMgr()
    return __obj
