import re
import os.path
import appcfg
from objs import songfilter


        
def maketable(page):
    """ Create table from || ... || syntax which is very convenient
        in simple markups to create a HTML table without much fuss 
        
        Example:
        
        || this is a || table ||
        || neat      || huh   ||
        
        Becomes:
        
        <table>
          <tr>
            <td>this is a</td>
            <td>table</td>
          </tr>
          <tr>
            <td>neat</td>
            <td>huh</td>
          </tr>
        </table>
    """
         
    table_rex = re.compile("((\|\|.+\|\|)+(.+\|\|){0,1}[\n]{1})+")

    finalstr = ''
    lastpos = 0
    while 1:
        t = table_rex.search(page, lastpos)
        if t:
            start, end = t.span()
            # get part before match
            finalstr += page[lastpos:start]
            lastpos = end
            # process the table
            finalstr += __convertTableToHTML(t.group())                
        else:
            finalstr += page[lastpos:]
            break
    
    return finalstr      
    
# ------------------------------------------------------------------------------
def __convertTableToHTML(raw_table):
    """ Processes the raw contents of the table to HTML """
    
    tr_data = []
    
    # first get all rows in a seperate list (\n delimited)
    rows = raw_table.splitlines()
    
    # break the lines in TD and TR sections
    for raw_row in rows:
        td_data = []
        row_data = raw_row.split("||")
        for column in row_data:
            if column:
                formatting, text = __extractSpecialTags(column)
                td_data.append((formatting, text))
        if len(td_data) > 0:
            tr_data.append(td_data)
    
    # now we have a tr_data list containing td_row lists
    # we can start building up the table now
    table_data = '<table>\n'
    for trs in tr_data:
        table_data += '<tr>\n'
        for formatting, text in trs:
            table_data += '<td' + formatting + '>' + text + '</td>\n'   
        table_data += '</tr>\n'
    table_data += '</table>\n'
    
    return table_data 

#-------------------------------------------------------------------------------
def __extractSpecialTags(column):
    """ Extract the special chars right at the beginning, like ||^ hello || for
        valign to top, or ||{2} test || colspan="2", etc """
    special_tags = { '^': ' VALIGN="TOP"',
                     '<': ' ALIGN="LEFT"',
                     '>': ' ALIGN="RIGHT"',
                     '-': ' ALIGN="CENTER"',
                     '_': ' VALIGN="BOTTOM"' }
    
    text = column
    formatting = ''
    while len(text) > 0:
        if text[0] in special_tags:               # simple tags
            formatting += special_tags[text[0]]
            text = text[1:]
        elif text[0] == '{':                      # colspan="x"
            pos = text.find('}', 1)
            if pos > 0:
                num = text[1:pos]
                if not num:
                    break
                try:
                    colspan = int(num)
                except ValueError:
                    break
                formatting += ' colspan="' + num + '"'
                text = text[pos + 1:]
        else:
            break
    return formatting, text.strip()

#-------------------------------------------------------------------------------
def parse_urls(instr):
    """ Search regexp and replace files and links with the proper A HREF tag
        the files are scanned in the current work directory of the song. If that does not 
        exist the global directory is used. If that does not exist either, tough luck 
        
        format:  attachment(somefile.txt) --> will become clickable and executable attachment
                 http://www.something.org --> will become an URL that opens a browser window
        """

    # found on: http://www.truerwords.net/articles/ut/urlactivation.html
    urlreg = "(^|[ \t\r\n])((ftp|http|https|gopher|mailto|news|nntp|telnet|wais|file|prospero|aim|webcal):" + \
             "(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-]))"

    r = re.compile(urlreg)
    lastpos = 0
    endstring = ''
    for c in r.finditer(instr):
        endstring += instr[lastpos:c.start()] + \
                     '<a href="' + c.group().strip() + '">' + c.group().strip() + '</a>'
        lastpos = c.end()
    endstring += instr[lastpos:]
    return endstring

#-------------------------------------------------------------------------------
def __doImgSrcPictureTag(instr):
    """ Tries a number of paths to return the img source, starting from the song mask, 
        then the work dir itself, then the images dir of the application """
    pic = instr[6:-1]
    
    # check for special tags
    # TODO: These do not work. Why???
    properties = ''
    while 1:
        if pic.startswith('right;'):
            properties += 'align="Center" '
            pic = pic[6:]
        elif pic.startswith('border;'):
            properties += 'border="1" '
            pic = pic[7:]
        elif pic.startswith('center;'):
            properties += 'align="Center" '
            pic = pic[7:]
        else:
            break
    
    paths = [os.path.join(appcfg.GetAbsWorkPath(), pic),
             os.path.join(appcfg.imagesdir, pic) ]

    song = songfilter.Get()._selectedSong
    if song:
        # when song is present, do this one first
        paths.insert(0, os.path.join(appcfg.GetAbsWorkPathFromSong(song), pic))

    # try all possible paths
    for p in paths:
        if os.path.isfile(p):
            return '<img src="' + p + '" ' + properties + ' >'

    # not found, means do not show anything
    return ''

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
    (r"__.*?__",           lambda winst : '<u>' + winst._currtok[2: -2] + '</u>'),
    (r"\*.*?\*",           lambda winst : '<b>' + winst._currtok[1:-1] + '</b>'),
    (r"(={5}.+?={5})\n",   lambda winst : '<h5>' + winst._currtok[5:-6] + '</h5>'),
    (r"(={4}.+?={4})\n",   lambda winst : '<h4>' + winst._currtok[4:-5] + '</h4>'),
    (r"(={3}.+?={3})\n",   lambda winst : '<h3>' + winst._currtok[3:-4] + '</h3>'),
    (r"(={2}.+?={2})\n",   lambda winst : '<h2>' + winst._currtok[2:-3] + '</h2>'),
    (r"(={1}.+?={1})\n",   lambda winst : '<h1>' + winst._currtok[1:-2] + '</h1>'),
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
    
        # first convert all the tables
        workstring = maketable(page)
        
        # parse all urls 
        workstring = parse_urls(workstring)
        
        # do simple tags now
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

        # append <BR>'s only in the sections that supposed to have them
        r = re.compile("(<.+?>\s*)+")
        lastpos = 0
        endstring = ''
        for c in r.finditer(workstring):
            lpos = workstring.rfind('>', c.start(), c.end())
            endstring += workstring[lastpos:c.start()].replace('\n', '<br>') + \
                         workstring[c.start():lpos]
            if lpos < c.end():
                # we need to do this, because the last piece of whitespaces actually
                # belong to the text and not the html, so we transform that as well
                endstring += workstring[lpos:c.end()].replace('\n', '<br>')
            lastpos = c.end()
        endstring += workstring[lastpos:].replace('\n', '<br>')
            
        # finish up the HTML, replace all '\n' with <br> to aid the user
        workstring = '<html><body><font size="+1">\n' + \
                     endstring + \
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
    
