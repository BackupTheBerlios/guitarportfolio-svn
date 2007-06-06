import re
import os.path

from objs import songs, linkmgt, songfilter
import appcfg
 
# SONG RELATED HTML TAGS
HTML_LABEL_SONG          = '@song@'
HTML_LABEL_ARTIST        = '@artist@'
HTML_LABEL_SHORTDATE     = '@sdate@'
HTML_LABEL_LONGDATE      = '@ldate@'
HTML_LABEL_CATEGORIES    = '@categories@' 
HTML_LABEL_TUNINGTEXT    = '@tuning_text@'
HTML_LABEL_TUNINGNAME    = '@tuning_name@'
HTML_LABEL_COLORPROGRESS = '@cprogress@'
HTML_LABEL_PERCPROGRESS  = '@percprogress@'
HTML_LABEL_SONGINFO      = '@songinfo@'
HTML_LABEL_LYRICS        = '@lyrics@'
HTML_LABEL_TIMESTARTED   = '@time_started@'
HTML_LABEL_TIMEADDED     = '@time_added@'
HTML_LABEL_TIMECOMPLETED = '@time_completed@'
HTML_LABEL_TIMEPOSTPONED = '@time_postponed@'
HTML_LABEL_ID            = '@song_id@'
HTML_SONG_ICON           = '@song_status_icon@'
HTML_LABEL_RANK          = '@song_rank@'
HTML_LABEL_BARCOUNT      = '@bar_count@'
HTML_LABEL_CAPOTEXT      = '@capo_text@'
HTML_LABEL_LINKS         = '@song_links@'
HTML_LABEL_STATCHANGE    = "@song_status_change@"
HTML_LABEL_SONGPATH      = '@song_path@'
HTML_SONG_TYPE_ICON      = '@song_type_icon@'

# LINKS HTML TAGS
HTML_LINK_NAME           = '@link_name@'
HTML_LINK_TYPE           = '@link_type@'
HTML_LINK_DESC           = '@link_description@'
HTML_LINK_PATH           = '@link_path@'
HTML_LINK_CREATEPATH     = '@create_links_path@'

# COMMON HTML TAGS
HTML_ICON_PRACTICING     = '@icon_practicing@'
HTML_ICON_TODO           = '@icon_todo@'
HTML_ICON_COMPLETED      = '@icon_completed@'
HTML_ICON_POSTPONED      = '@icon_postponed@'
HTML_GUITAR_ICON         = '@guitar_icon@'
HTML_ICON_PATH           = '@icon_path@'

# FILE NAME CONSTANTS
STR_ICON_TODO            = 'icon_todo.png'
STR_ICON_POSTPONED       = 'icon_not_practicing.png'
STR_ICON_PRACTICING      = 'icon_in_progress.png'
STR_ICON_COMPLETED       = 'icon_completed.png'
STR_ICON_GUITAR          = 'guitar_icon.png'
STR_ICON_TUTORIAL        = 'tutorial_icon.png'
STR_ICON_RANK_X          = 'icon_rank_@.gif'

# SONG SECTION PARTS
HTML_SECTION_PRACTICING  = "@songs_practicing@"
HTML_SECTION_POSTPONED   = "@songs_postponed@"
HTML_SECTION_TODO        = "@songs_todo@"
HTML_SECTION_COMPLETED   = "@songs_completed@"

HTML_LABEL_CATNAME       = '@name@'              # only used in section!

# ------------------------------------------------------------------------------
def __getIconPath(tags):
    str_icon_path = appcfg.imagesdir
    if str_icon_path[-1:] != os.sep:
        str_icon_path += os.sep
    return str_icon_path  

# ------------------------------------------------------------------------------
def __getSongShortDate(tags, song):
    # song date
    if not song._dateUnknown:
        if not song._yearOnly:
            sdate_str = song._time.strftime('%x')
        else:
            sdate_str = song._time.strftime('%Y')
    else:
        sdate_str = 'Unknown'
    return sdate_str
    
# ------------------------------------------------------------------------------
def __getSongLongDate(tags, song):
    # song date
    if not song._dateUnknown:
        if not song._yearOnly:
            ldate_str = song._time.strftime('%d %B %Y')
        else:
            ldate_str = song._time.strftime('In Year %Y')                    
    else:
        ldate_str = 'Unknown'
    return ldate_str

# ------------------------------------------------------------------------------
def __getSongProgress(tags, song):
    # color progress
    progress_str = ''
    if song._status == songs.SS_STARTED:
        progress_str = '<font color="#ff8e14">IN PROGRESS</font>'
    elif song._status == songs.SS_POSTPONED:
        progress_str = '<font color="#ff0000">NOT PRACTICING</font>'
    elif song._status == songs.SS_COMPLETED:
        progress_str = '<font color="#0bdc0b">COMPLETED!</font>'
    elif song._status == songs.SS_NOT_STARTED:
        progress_str = '<font color="#744bf9">TODO</font>'
    return progress_str
    
# ------------------------------------------------------------------------------
def __getSongTimeStarted(tags, song):
    # time started
    if not song._status == songs.SS_NOT_STARTED:
        started_str = song._timeStarted.strftime('%d %B %Y')
    else:
        started_str = "Not Yet"
    return started_str
            
# ------------------------------------------------------------------------------
def __getSongTimeCompleted(tags, song):
    # time completed
    if song._status == songs.SS_COMPLETED:
        completed_str = song._timeCompleted.strftime('%d %B %Y')
    else:
        completed_str = 'Not yet'

    if song._status == songs.SS_POSTPONED:
        completed_str = song._timePostponed.strftime('Postponed on %d %B %Y')
    return completed_str
    
# ------------------------------------------------------------------------------
def __getSongTimePostponed(tags, song):
    # time postponed
    if song._status == songs.SS_POSTPONED:
        postponed_str = song._timePostponed.strftime('%d %B %Y')
    else:
        postponed_str = 'N/A'
    return postponed_str

# ------------------------------------------------------------------------------
def __getSongCategories(tags, song):
    # categories, use repetative mechanism
    if HTML_LABEL_CATEGORIES in tags:
        reptup = tags[HTML_LABEL_CATEGORIES]
    else:
        reptup = ('',                   # pre html tag 
                  '@name@',             # repeat tag 
                  ', ',                 # append tag
                  '')                   # post html tag
    
    tempstr = ''
    categories_str = reptup[0]
    for c in song.categories:
        if not tempstr:
            tempstr += reptup[1].replace(HTML_LABEL_CATNAME, c._name) 
        else:
            tempstr += reptup[2] + reptup[1].replace(HTML_LABEL_CATNAME, c._name) 
    categories_str = categories_str + tempstr + reptup[3]
    return categories_str

# ------------------------------------------------------------------------------
def __getSongIcon(tags, song):
    # which song icon
    if song._status == songs.SS_STARTED:
        str_icon = STR_ICON_PRACTICING
    elif song._status == songs.SS_POSTPONED:
        str_icon = STR_ICON_POSTPONED
    elif song._status == songs.SS_COMPLETED:
        str_icon = STR_ICON_COMPLETED
    else:
        str_icon = STR_ICON_TODO
    return str_icon
    
# ------------------------------------------------------------------------------
def __getSongBarCount(tags, song):
    if song._barCount > 0:
        str_bar_count = repr(song._barCount) + ' Bars'
    else:
        str_bar_count = 'Not Specified'
    return str_bar_count
    
# ------------------------------------------------------------------------------
def __getSongLinks(tags, song):
    # construct links if present
    str_links = ''
    
    if tags != None:
        stags = tags
    else:
        stags = {}

    if HTML_LABEL_LINKS in stags:
        linkstr = tags[HTML_LABEL_LINKS]
        if linkmgt.Get().links.count() > 0:
            str_links = linkstr[0]
            for l in linkmgt.Get().links:
                str_links += _DoParseHtmlTags(linkstr[1], link_tags, stags,  l)
            str_links += linkstr[2]
    return str_links
    
# ------------------------------------------------------------------------------
def __getSongCreatePath(tags, song):
    # if there is a links path, do not display the create html code
    str_link_create = ''
    path = appcfg.GetAbsWorkPathFromSong(song)
    if HTML_LINK_CREATEPATH in tags:
        paths = tags[HTML_LINK_CREATEPATH]
        if not os.path.exists(path):
            str_link_create = paths[0]
        else:
            str_link_create = paths[1]
            
    return str_link_create

# ------------------------------------------------------------------------------
def __getLinkPath(tags, link):
    if link:
        str_link_path = '<a href="#link:' + repr(link._id) + '">' + \
                        link._name + "</a>"
    else:
        str_link_path =  'None'
    return str_link_path

# ------------------------------------------------------------------------------
def __getSongStatusSection(tags, section_tag):
    # get proper section to do
    songrows = ''
    if section_tag in tags:
        htmltags = tags[section_tag]

        # we work bottom up, first gather all song rows, and replace this later on
        songs = htmltags[0]
        if len(songs) > 0:
            songrows = htmltags[1]
            for s in songs:
                songrows = songrows + ParseSongHtml(htmltags[2], s) + '\n'
            songrows = songrows + htmltags[3]

    return songrows

# ------------------------------------------------------------------------------
def __getCurrentSongPath(tags):
    song = songfilter.Get()._selectedSong
    if song:
        result = appcfg.GetAbsWorkPathFromSong(song)
    else:
        result = ''
    return result

# ------------------------------------------------------------------------------
def __getStatusCommands(tags, song):
    result = ''
    if HTML_LABEL_STATCHANGE in tags:
        stats = tags[HTML_LABEL_STATCHANGE]
        song_stats = stats[0]
        result += stats[1]
        if song._status == songs.SS_NOT_STARTED or \
           song._status == songs.SS_POSTPONED or \
           song._status == songs.SS_COMPLETED:
            result += song_stats[songs.SS_STARTED]
        elif song._status == songs.SS_STARTED:
            result += song_stats[songs.SS_POSTPONED] + \
                      stats[2] + \
                      song_stats[songs.SS_COMPLETED]
        result += stats[3]
    
    return result
        
common_tags = { HTML_ICON_PATH:            __getIconPath,
                HTML_ICON_PRACTICING:      lambda tags : STR_ICON_PRACTICING,
                HTML_ICON_TODO:            lambda tags : STR_ICON_TODO,
                HTML_ICON_COMPLETED:       lambda tags : STR_ICON_COMPLETED,
                HTML_ICON_POSTPONED:       lambda tags : STR_ICON_POSTPONED,
                HTML_GUITAR_ICON:          lambda tags : STR_ICON_GUITAR,
                HTML_LABEL_SONGPATH:       __getCurrentSongPath
              }

song_tags   =  { HTML_LABEL_SONG:          lambda tags, song : song._title, 
                 HTML_LABEL_ARTIST:        lambda tags, song : song._artist,
                 HTML_LABEL_SHORTDATE:     __getSongShortDate,
                 HTML_LABEL_LONGDATE:      __getSongLongDate,
                 HTML_LABEL_TUNINGTEXT:    lambda tags, song : song.GetTuningText(),
                 HTML_LABEL_TUNINGNAME:    lambda tags, song : song.GetTuningName(),
                 HTML_LABEL_COLORPROGRESS: __getSongProgress, 
                 HTML_LABEL_PERCPROGRESS:  lambda tags, song : '%d' % song.GetProgressPerc(), 
                 HTML_LABEL_SONGINFO:      lambda tags, song : WikiParse(song._information),
                 HTML_LABEL_LYRICS:        lambda tags, song : WikiParse(song._lyrics),
                 HTML_LABEL_TIMESTARTED:   __getSongTimeStarted,
                 HTML_LABEL_TIMEADDED:     lambda tags, song : song._timeAdded.strftime('%d %B %Y'),
                 HTML_LABEL_TIMECOMPLETED: __getSongTimeCompleted,
                 HTML_LABEL_TIMEPOSTPONED: __getSongTimePostponed,
                 HTML_LABEL_STATCHANGE:    __getStatusCommands,
                 HTML_LABEL_ID:            lambda tags, song : repr(song._id),
                 HTML_LABEL_CATEGORIES:    __getSongCategories,
                 HTML_SONG_ICON:           __getSongIcon,
                 HTML_LABEL_RANK:          lambda tags, song : STR_ICON_RANK_X.replace('@', repr(song._difficulty)),
                 HTML_LABEL_BARCOUNT:      __getSongBarCount,      
                 HTML_LABEL_CAPOTEXT:      lambda tags, song : songs.GetCapoString(song._capoOnFret),
                 HTML_LABEL_LINKS:         __getSongLinks,
                 HTML_LINK_CREATEPATH:     __getSongCreatePath,
                 HTML_SONG_TYPE_ICON:      lambda tags, song : STR_ICON_GUITAR if song._songType == songs.ST_NORMAL \
                                                                               else STR_ICON_TUTORIAL
                }

link_tags    = { HTML_LINK_NAME:           lambda tags, link : link._name if link else 'None', 
                 HTML_LINK_TYPE:           lambda tags, link : link._type if link else 'N/A', 
                 HTML_LINK_DESC:           lambda tags, link : 'None',
                 HTML_LINK_PATH:           __getLinkPath}

song_status_tags = { HTML_SECTION_PRACTICING: lambda tags : \
                                              __getSongStatusSection(tags, HTML_SECTION_PRACTICING), 
                     HTML_SECTION_POSTPONED:  lambda tags : \
                                              __getSongStatusSection(tags, HTML_SECTION_POSTPONED),
                     HTML_SECTION_TODO:       lambda tags : \
                                              __getSongStatusSection(tags, HTML_SECTION_TODO),   
                     HTML_SECTION_COMPLETED:  lambda tags : \
                                              __getSongStatusSection(tags, HTML_SECTION_COMPLETED) }

#-------------------------------------------------------------------------------
def ParseCommonHtml(page):
    """ Convenience function for parsing only the common tags on a HTML template """
    return _DoParseHtmlTags(page, common_tags) 

#-------------------------------------------------------------------------------
def _DoParseHtmlTags(page, htmltags, subtags = None, *args):
    finalstr = ''
    lastpos = 0
    regexp = re.compile("@[A-Za-z_]+@")

    stags = subtags if subtags != None else {}    
    
    while 1:
        t = regexp.search(page, lastpos)
        if t:
            # collect part until matched token
            finalstr += page[lastpos:t.start()]
            lastpos = t.start() + len(t.group())
            try:
                # replace  token with lookup function tag
                # this can blow, do not execute code after this
                get_str = htmltags[t.group()]
                finalstr += get_str(stags, *args)
                
            except KeyError:
                # we will leave unmatched token in text
                finalstr += t.group()
        else:
            finalstr += page[lastpos:]
            break
    
    return finalstr      

#-------------------------------------------------------------------------------
def ParseSongHtml(page, song, subtags = None):
    """ Seek and replace all given tags with the proper data, plus use conditional
        and possibly bottom up parsing of sub tags when needed.
        subtags are defined based upon their needed structure
    """

    # parse song tags then parse common tags
    stags = subtags if subtags != None else {}
    tmp = _DoParseHtmlTags(page, song_tags, stags, song)
    return _DoParseHtmlTags(tmp, common_tags, stags)
    
#-------------------------------------------------------------------------------
def ParseSongsByStatus(page, subtags):
    """ Parse the main page using the songs tags, every sub section can render the page 
        individually """
    # first parse the song list tags then the common ones
    tmp = _DoParseHtmlTags(page, song_status_tags, subtags)
    return _DoParseHtmlTags(tmp, common_tags, subtags)    

