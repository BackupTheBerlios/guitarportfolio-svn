import os.path

import wx
import wx.xrc as xrc
import wx.html as html
import time

from wx.lib.pubsub import Publisher
from objs import songs, linkmgt
import db
import db.songs_peer
from images import icon_home, icon_browse_next, icon_browse_prev
import xmlres, appcfg, htmlparse, linkfile, htmlmarkup, wikiparser, viewmgr

class SongBrowserPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongBrowserPanel")
        self.PostCreate(pre)
        
        self._currPage = -1 # id of song in queue, -1 is home
        
        self.__homeButton = xrc.XRCCTRL( self, "ID_BTN_HOME")
        self.__browseBack = xrc.XRCCTRL( self, "ID_BTN_BACK")
        self.__browseForward = xrc.XRCCTRL( self, "ID_BTN_FORWARD")
        self.__songBrowser = xrc.XRCCTRL(self, "ID_BROWSER_WINDOW")
        
        if "gtk2" in wx.PlatformInfo:
            self.__songBrowser.SetStandardFonts()
            
        self.Bind(html.EVT_HTML_LINK_CLICKED, self.__OnLinkClicked, self.__songBrowser)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseHome, self.__homeButton)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseForward, self.__browseForward)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseBack, self.__browseBack)

        # signals for song selection dropdown
        Publisher().subscribe(self.__UpdateSong, viewmgr.SIGNAL_SONG_UPDATED)  
        Publisher().subscribe(self.__DeleteSong, viewmgr.SIGNAL_SONG_DELETED)  
        Publisher().subscribe(self.__ClearSongs, viewmgr.SIGNAL_CLEAR_DATA)  
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)  
        Publisher().subscribe(self.__AddSongs, viewmgr.SIGNAL_DATA_RESTORED) 
        Publisher().subscribe(self.__CriteriaListChanged, viewmgr.SIGNAL_CRITLIST_CHANGED) 
        Publisher().subscribe(self.__OnSetHomepage, viewmgr.SIGNAL_SET_HOMEPAGE)
        Publisher().subscribe(self.__LinksRefreshed, viewmgr.SIGNAL_LINKS_REFRESHED)

        # add some nice buttons
        self.__homeButton.SetBitmapLabel(icon_home.getBitmap())
        self.__browseBack.SetBitmapLabel(icon_browse_prev.getBitmap())
        self.__browseForward.SetBitmapLabel(icon_browse_next.getBitmap())
        
        # set the start page
        wp = wikiparser.WikiParser()
        self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
        
    # --------------------------------------------------------------------------
    def __AddSongs(self, message):
        # if we are on the homepage, update the report
        if self._currPage == -1:
            self.__RenderHomepage()
      
    # --------------------------------------------------------------------------
    def __UpdateSong(self, message):
        
        # if we are on the homepage, update the report
        if self._currPage == message.data._id:
            # we are on the song page, update
            self.__RenderSongPage(message.data)

    # --------------------------------------------------------------------------
    def __DeleteSong(self, message):
        # if we are on the current page of the song, render homepage
        if self._currPage == message.data._id:
            self._currPage = -1
            self.__RenderHomePage()

    # --------------------------------------------------------------------------
    def __ClearSongs(self, message):
        """ Clear list, we are changing databases """
        wp = wikiparser.WikiParser()
        self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
        
    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Another song is selected, sync our list """
        if message.data:
            # render the song info page
            self.__RenderSongPage(message.data)
        else:
            self.__RenderHomepage()

    # --------------------------------------------------------------------------
    def __LinksRefreshed(self, message):
        """ Handler for refreshed links """
        
        # we refresh the selected page, we assume the selected song
        # got the links refresh event
        
        song = viewmgr.Get()._selectedSong
        if song != None and self._currPage == song._id:
            self.__RenderSongPage(song)

    # --------------------------------------------------------------------------
    def __CriteriaListChanged(self, message):
        
        # if we are on the main page, render
        if self._currPage == -1:
            self.__RenderHomepage()
            
    # --------------------------------------------------------------------------
    def __RenderHomepage(self):
        """ We render the homepage containing all song statuses divided in sections """
        criteria = viewmgr.Get()._critList
        if not len(criteria):
            wp = wikiparser.WikiParser()
            self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
            return
        
        stats = { songs.SS_STARTED:     [],
                  songs.SS_POSTPONED:   [],
                  songs.SS_COMPLETED:   [],
                  songs.SS_NOT_STARTED: [] }
        
        # go by the songs list, and get lists per status
        for stat_key in stats.iterkeys():
            lst = stats[stat_key]
            
            for s in criteria:
                if s._status == stat_key:
                    lst.append(s)
        
        # set the markup for the rendering engine
        songs_section = { htmlparse.HTML_SECTION_PRACTICING: (stats[songs.SS_STARTED],
                                                              htmlmarkup.songs_practicing_begin,
                                                              htmlmarkup.songs_practicing_row,
                                                              htmlmarkup.songs_practicing_end),
                          htmlparse.HTML_SECTION_TODO:       (stats[songs.SS_NOT_STARTED],
                                                              htmlmarkup.songs_todo_begin,
                                                              htmlmarkup.songs_todo_row,
                                                              htmlmarkup.songs_todo_end),
                          htmlparse.HTML_SECTION_COMPLETED:  (stats[songs.SS_COMPLETED],
                                                              htmlmarkup.songs_completed_begin,
                                                              htmlmarkup.songs_completed_row,
                                                              htmlmarkup.songs_completed_end),
                          htmlparse.HTML_SECTION_POSTPONED:  (stats[songs.SS_POSTPONED], 
                                                              htmlmarkup.songs_postponed_begin,
                                                              htmlmarkup.songs_postponed_row,
                                                              htmlmarkup.songs_postponed_end)
                        }
                              
        page = htmlparse.ParseSongsByStatus(htmlmarkup.home_page, songs_section)
        self.__songBrowser.SetPage(page)
        
    # --------------------------------------------------------------------------
    def __RenderSongPage(self, song):
        """ We render the homepage containing all song statuses divided in sections """
        taginfo = { htmlparse.HTML_LABEL_CATEGORIES:  (htmlmarkup.categories_begin, 
                                                       htmlmarkup.categories_row, 
                                                       htmlmarkup.categories_append,
                                                       htmlmarkup.categories_end), 
                    htmlparse.HTML_LABEL_LINKS:       (htmlmarkup.song_links_begin,
                                                       htmlmarkup.song_links_row,
                                                       htmlmarkup.song_links_end),
                    htmlparse.HTML_LINK_CREATEPATH:   (htmlmarkup.links_path_not_ok,
                                                       htmlmarkup.links_path_ok),
                    htmlparse.HTML_LABEL_STATCHANGE:  ({ songs.SS_STARTED:   htmlmarkup.change_status_in_progress,
                                                         songs.SS_POSTPONED: htmlmarkup.change_status_in_postponed,
                                                         songs.SS_COMPLETED: htmlmarkup.change_status_in_completed },
                                                       htmlmarkup.change_status_start,
                                                       htmlmarkup.change_status_append,
                                                       htmlmarkup.change_status_end )
                  }        

        pg = htmlparse.ParseSongHtml(htmlmarkup.songinfo, song, taginfo)

        self.__songBrowser.SetPage(pg)
        self._currPage = song._id

    #---------------------------------------------------------------------------
    def __OnLinkClicked(self, event):
        tag = event.GetLinkInfo().GetHref()
        # check if we need to select a song
        if tag.startswith('#song:'):
            song_nr = tag[6:]
            if song_nr:
                song = viewmgr.Get()._list.find_id(int(song_nr))
                if song:
                    viewmgr.signalSetSong(song)
                
        # check for execution of a link
        elif tag.startswith('#link:'):
            link_nr = tag[6:]
            if link_nr:
                link = linkmgt.Get().links.find_id(int(link_nr))
                if link:
                    linkfile.executelink(link)
        # check for execution of a command
        elif tag.startswith('#cmd:'):
            cmd = tag[5:]
            commands = { "status_practicing": lambda : self.__DoSetSongStatus(songs.SS_STARTED),
                         "status_postponed":  lambda : self.__DoSetSongStatus(songs.SS_POSTPONED),
                         "status_completed":  lambda : self.__DoSetSongStatus(songs.SS_COMPLETED)
                       }
            
            try:
                exec_func = commands[cmd]
                exec_func()
            except KeyError:
                wx.MessageBox("Command '%s' not implemented!" % (cmd,), 'Error', wx.ICON_ERROR | wx.OK)

    #---------------------------------------------------------------------------
    def __DoSetSongStatus(self, status):
        """ Song status must be changed, issued by the browser component which will trigger
            a change in status """
        
        song = viewmgr.Get()._selectedSong
        if song:
            # signal a status change so we can enter a log
            viewmgr.signalSongStatusChange(song, status)
        
    #---------------------------------------------------------------------------
    def __OnBrowseHome(self, event):
        """ User click to get to the homepage. This is indirectly done by the view manager """
        viewmgr.signalSetHomepage()
        
    #---------------------------------------------------------------------------
    def __OnSetHomepage(self, message):
        """ Signal is received that we have to switch to the homepage """
        
        self._currPage = -1
        self.__RenderHomepage()        
        
    #---------------------------------------------------------------------------
    def __OnBrowseForward(self, event):
        """ We are going to browse forward. This means we will emit a signal that
            will determine the best song to be selected for us """
        
        # emit, and all will change
        viewmgr.signalSelectPreviousSong()

    #---------------------------------------------------------------------------
    def __OnBrowseBack(self, event):
        """ We are going to browse back. This means we will emit a signal that
            will determine the best song to be selected for us """
        
        # emit, and all will change
        viewmgr.signalSelectNextSong()
