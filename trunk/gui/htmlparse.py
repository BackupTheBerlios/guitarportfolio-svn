import re
import os.path

from objs import songs
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
STR_ICON_RANK_X          = 'icon_rank_@.gif'

HTML_LABEL_CATNAME       = '@name@'              # only used in section!

#-------------------------------------------------------------------------------
def _ParseCommonHtml(page, subtags = {}):
    """ Parse only common html tags that can be filled in and are not based upon
        the current song or other information """

    # get images dir
    str_icon_path = appcfg.imagesdir
    if str_icon_path[-1:] != os.sep:
        str_icon_path += os.sep

    tags = { HTML_ICON_PATH:        str_icon_path,
             HTML_ICON_PRACTICING:  STR_ICON_PRACTICING,
             HTML_ICON_TODO:        STR_ICON_TODO,
             HTML_ICON_COMPLETED:   STR_ICON_COMPLETED,
             HTML_ICON_POSTPONED:   STR_ICON_POSTPONED,
             HTML_GUITAR_ICON:      STR_ICON_GUITAR }
    
    finalstr = ''
    lastpos = 0
    regexp = re.compile("@[A-Za-z_]+@")
    while 1:
        t = regexp.search(page, lastpos)
        if t:
            # collect part until matched token
            finalstr += page[lastpos:t.start()]
            lastpos = t.start() + len(t.group())
            try:
                # replace token with lookup tag
                # this can blow, do not execute code after this
                finalstr += tags[t.group()] 
            except KeyError:
                # we will leave unmatched token in text
                finalstr += t.group()
                pass
        else:
            finalstr += page[lastpos:]
            break
    
    return finalstr

#-------------------------------------------------------------------------------
def ParseSongHtml(page, song, subtags = {}):
    """ Seek and replace all given tags with the proper data, plus use conditional
        and possibly bottom up parsing of sub tags when needed.
        subtags are defined based upon their needed structure
    """
    
    # TODO: Create conditional IF tags
    
    # match all static types, in a dynamic lookup table
    tmp = _ParseCommonHtml(page)
    
    # song date
    if not song._dateUnknown:
        if not song._yearOnly:
            sdate_str = song._time.strftime('%x')
            ldate_str = song._time.strftime('%d %B %Y')
        else:
            sdate_str = song._time.strftime('%Y')
            ldate_str = song._time.strftime('In Year %Y')                    
    else:
        sdate_str = 'Unknown'
        ldate_str = 'Unknown'

    # time started
    if not song._status == songs.SS_NOT_STARTED:
        started_str = song._timeStarted.strftime('%d %B %Y')
    else:
        started_str = "Not Yet"
    
    # time added
    added_str = song._timeAdded.strftime('%d %B %Y')

    # time completed
    if song._status == songs.SS_COMPLETED:
        completed_str = song._timeCompleted.strftime('%d %B %Y')
    else:
        completed_str = 'Not yet'
    if song._status == songs.SS_POSTPONED:
        completed_str = song._timePostponed.strftime('Postponed on %d %B %Y')

    # time postponed
    postponed_str = song._timePostponed.strftime('%d %B %Y')
    
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

    # percentage completed
    percprogress_str = '%d' % song.GetProgressPerc()

    # song info, made HTML BR friendly
    str_songinfo = song._information.replace('\n', '<br>')

    # song lyrics, made HTML BR friendly
    str_songlyrics = song._lyrics.replace('\n', '<br>')
    
    # which song icon
    if song._status == songs.SS_STARTED:
        str_icon = STR_ICON_PRACTICING
    elif song._status == songs.SS_POSTPONED:
        str_icon = STR_ICON_POSTPONED
    elif song._status == songs.SS_COMPLETED:
        str_icon = STR_ICON_COMPLETED
    else:
        str_icon = STR_ICON_TODO
      
    # rank icon
    str_icon_rank = STR_ICON_RANK_X.replace('@', repr(song._difficulty))
      
    if song._barCount > 0:
        str_bar_count = repr(song._barCount) + ' Bars'
    else:
        str_bar_count = 'Not Specified'
      
    # categories, use repetative mechanism
    if HTML_LABEL_CATEGORIES in subtags:
        reptup = subtags[HTML_LABEL_CATEGORIES]
    else:
        reptup = ('', '@name@', ', ', '')

    tempstr = ''
    categories_str = reptup[0]
    for c in song.categories:
        if not tempstr:
            tempstr += reptup[1].replace(HTML_LABEL_CATNAME, c._name) 
        else:
            tempstr += reptup[2] + reptup[1].replace(HTML_LABEL_CATNAME, c._name) 
    categories_str = categories_str + tempstr + reptup[3]             
            
    tags = { HTML_LABEL_SONG:          song._title, 
             HTML_LABEL_ARTIST:        song._artist,
             HTML_LABEL_SHORTDATE:     sdate_str,
             HTML_LABEL_LONGDATE:      ldate_str,
             HTML_LABEL_TUNINGTEXT:    song.GetTuningText(),
             HTML_LABEL_TUNINGNAME:    song.GetTuningName(),
             HTML_LABEL_COLORPROGRESS: progress_str, 
             HTML_LABEL_PERCPROGRESS:  percprogress_str, 
             HTML_LABEL_SONGINFO:      str_songinfo,
             HTML_LABEL_LYRICS:        str_songlyrics,
             HTML_LABEL_TIMESTARTED:   started_str,
             HTML_LABEL_TIMEADDED:     added_str,
             HTML_LABEL_TIMECOMPLETED: completed_str,
             HTML_LABEL_TIMEPOSTPONED: postponed_str,
             HTML_LABEL_ID:            repr(song._id),
             HTML_LABEL_CATEGORIES:    categories_str,
             HTML_SONG_ICON:           str_icon,
             HTML_LABEL_RANK:          str_icon_rank,
             HTML_LABEL_BARCOUNT:      str_bar_count,      
             HTML_LABEL_CAPOTEXT:      songs.GetCapoString(song._capoOnFret) }
    
    finalstr = ''
    lastpos = 0
    regexp = re.compile("@[A-Za-z_]+@")
    while 1:
        t = regexp.search(tmp, lastpos)
        if t:
            # collect part until matched token
            finalstr += tmp[lastpos:t.start()]
            lastpos = t.start() + len(t.group())
            try:
                # replace token with lookup tag
                # this can blow, do not execute code after this
                finalstr += tags[t.group()] 
            except KeyError:
                # we will leave unmatched token in text
                finalstr += t.group()
        else:
            finalstr += tmp[lastpos:]
            break    
    # done!
    return finalstr
    
       
