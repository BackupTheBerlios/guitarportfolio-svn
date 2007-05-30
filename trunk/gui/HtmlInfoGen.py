from objs import songs

# TODO: Rename to htmlinfogen and put in objs dir
# TODO: Put this through some testing

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

def GenerateHtmlFromSong(template, song):
    tpl = template
    # generic stuff
    tpl = tpl.replace(HTML_LABEL_SONG, song._title)
    tpl = tpl.replace(HTML_LABEL_ARTIST, song._artist)
    # date representation
    if song._dateUnknown == False:
        if song._yearOnly == False:
            tpl = tpl.replace(HTML_LABEL_SHORTDATE, song._time.strftime('%x'))
            tpl = tpl.replace(HTML_LABEL_LONGDATE, song._time.strftime('%d %B %Y'))
        else:
            tpl = tpl.replace(HTML_LABEL_SHORTDATE, song._time.strftime('%Y'))
            tpl = tpl.replace(HTML_LABEL_LONGDATE, song._time.strftime('Only Year Is Known'))                    
    else:
        tpl = tpl.replace(HTML_LABEL_SHORTDATE, '--/--/--')
        tpl = tpl.replace(HTML_LABEL_LONGDATE, 'Unknown')
    # categories                
    catstr = ''    
    for c in song.categories:
        if catstr == '':
            catstr = c._name
        else:
            catstr = catstr + ', ' + c._name
    tpl = tpl.replace(HTML_LABEL_CATEGORIES, catstr)        
    # tuning text
    tpl = tpl.replace(HTML_LABEL_TUNINGTEXT, song.GetTuningText())        
    tpl = tpl.replace(HTML_LABEL_TUNINGNAME, song.GetTuningName())
    # determine progress colored
    sprogress = ''
    if song._status == songs.SS_STARTED:
        sprogress = '<font color="#ff8e14">IN PROGRESS</font>'
    elif song._status == songs.SS_POSTPONED:
        sprogress = '<font color="#ff0000">NOT PRACTICING</font>'
    elif song._status == songs.SS_COMPLETED:
        sprogress = '<font color="#0bdc0b">COMPLETED!</font>'
    elif song._status == songs.SS_NOT_STARTED:
        sprogress = '<font color="#744bf9">TODO</font>'
    tpl = tpl.replace(HTML_LABEL_COLORPROGRESS, sprogress)
    tpl = tpl.replace(HTML_LABEL_PERCPROGRESS, '%d' % song.GetProgressPerc())
    # do song info with friendly <br>
    repl = song._information.replace('\n', '<br>')
    tpl = tpl.replace(HTML_LABEL_SONGINFO, repl)
    # do lyrics, with friendly <br>
    repl = song._lyrics.replace('\n', '<br>')
    tpl = tpl.replace(HTML_LABEL_LYRICS, repl)
    tpl = tpl.replace(HTML_LABEL_TIMESTARTED, song._timeStarted.strftime('%d %B %Y'))
    tpl = tpl.replace(HTML_LABEL_TIMEADDED, song._timeAdded.strftime('%d %B %Y'))
    tpl = tpl.replace(HTML_LABEL_TIMECOMPLETED, song._timeCompleted.strftime('%d %B %Y'))
    tpl = tpl.replace(HTML_LABEL_TIMEPOSTPONED, song._timePostponed.strftime('%d %B %Y'))
    tpl = tpl.replace(HTML_LABEL_ID, repr(song._id))
    # set the page  
    return tpl  
