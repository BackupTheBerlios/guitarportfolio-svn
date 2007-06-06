import re
import os.path
import appcfg
from objs import songfilter

#-------------------------------------------------------------------------------
def __doImgSrcPictureTag(instr):
    """ Tries a number of paths to return the img source, starting from the song mask, 
        then the work dir itself, then the images dir of the application """
    pic = instr[6:-1]
    paths = [os.path.join(appcfg.GetAbsWorkPath(), pic),
             os.path.join(appcfg.imagesdir, pic) ]

    song = songfilter.Get()._selectedSong
    if song:
        # when song is present, do this one first
        paths.insert(0, os.path.join(appcfg.GetAbsWorkPathFromSong(song), pic))

    # try all possible paths
    for p in paths:
        if os.path.isfile(p):
            return '<img src="' + p + '" />'

    # not found!
    return '<font color="#ff0000"><b>image(' + pic + ')</b></font>'

#-------------------------------------------------------------------------------

def __doPreTag(winst):
    """ Write the proper HTML tag for pre formatted text, based upon the 
        token and the state of the object's pre_tag_level. """   
    
    # push the close tag on the stack, so that we can also
    # report an error when the open and close tags are not
    # properly matched 
    if winst._currtok == '{{{':
        winst._tag_stack.append(('</pre>'))
        return '<pre>'
    else:
        tmpstr = winst._UnrollTag('</pre>')
        winst._in_pre_mode = '</pre>' in winst._tag_stack
        return tmpstr
    
    # don't know what to return, so we return the same tag
    return winst._currtok

#===============================================================================

regexp_convert_tab = [ 
    (r"'''.*?'''",         lambda winst : '<i>' + winst._currtok[3: -3] + '</i>'),
    (r"\*.*?\*",           lambda winst : '<b>' + winst._currtok[1:-1] + '</b>'),
    (r"={5}.+?={5}",       lambda winst : '<h5>' + winst._currtok[5:-5] + '</h5>'),
    (r"={4}.+?={4}",       lambda winst : '<h4>' + winst._currtok[4:-4] + '</h4>'),
    (r"={3}.+?={3}",       lambda winst : '<h3>' + winst._currtok[3:-3] + '</h3>'),
    (r"={2}.+?={2}",       lambda winst : '<h2>' + winst._currtok[2:-2] + '</h2>'),
    (r"={1}.+?={1}",       lambda winst : '<h1>' + winst._currtok[1:-1] + '</h1>'),
    (r"image\(.+?\)",      lambda winst : __doImgSrcPictureTag(winst._currtok)),
    (r"(\{\{\{)|(\}\}\})", __doPreTag )
    ]

class WikiParser(object):
    def __init__(self):
        # the stack of tags that are still open and need closing
        self._tag_stack = []
        self._currtok = ''          # current matching token
        self._in_pre_mode = False   # pre mode means no parsing except '}}}'
    
    def Parse(self, page):
        """ Parse the page as it were a WIKI. Simple markup is provided to avoid as much HTML as possible:
            *this line is bold*        - <b>this line is bold</>
            '''This line is italic'''  - <i>this line is italic</i>
            image:your_pic.png         - <img src="{path of song}|{global path}your_pic.png" />
        """
        self._tag_stack = []
    
        # convert all wiki items we can
        workstring = page
        for regstr, get_str in regexp_convert_tab:
            chunkstr = ''
            lastpos = 0
            regexp = re.compile(regstr)
            while 1:
                t = regexp.search(workstring, lastpos)
                if t:
                    chunkstr += workstring[lastpos:t.start()]
                    lastpos = t.start() + len(t.group())
                    self._currtok = t.group()
                    chunkstr += get_str(self)
                else:
                    chunkstr += workstring[lastpos:]
                    break
            workstring = chunkstr
        
        # go close all forgotten orphan tags
        while len(self._tag_stack) > 0:
            workstring += self._tag_stack.pop()

        # finish up the HTML, replace all '\n' with <br> to aid the user
        workstring = '<html><body><font size="+1">\n' + \
                     workstring.replace("\n", "<br>") + \
                     '</font></html></body>'
    
        return workstring    
    
    # --------------------------------------------------------------------------
    def _UnrollTag(self, tag):
        """ Unroll an expected tag from te stack. If this tag is not found on the 
            stack, simply ignore it, and return an empty string. At the end the
            tags will be cleaned up anyway, albeit the markup is not what the user
            expected """
        if len(self._tag_stack) > 0:
            if tag == self._tag_stack[-1]:
                return self._tag_stack.pop()
        return ''                   
    
