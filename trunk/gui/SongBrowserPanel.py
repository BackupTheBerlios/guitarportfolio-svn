import os.path

import wx
import wx.xrc as xrc
import wx.html as html
import time

from wx.lib.pubsub import Publisher
from objs import songs, songfilter, linkmgt
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
        
        self.__songList = xrc.XRCCTRL( self, "ID_SONG_SELECTOR" )
        self.__homeButton = xrc.XRCCTRL( self, "ID_BTN_HOME")
        self.__browseBack = xrc.XRCCTRL( self, "ID_BTN_BACK")
        self.__browseForward = xrc.XRCCTRL( self, "ID_BTN_FORWARD")
        self.__songBrowser = xrc.XRCCTRL(self, "ID_BROWSER_WINDOW")
        
        if "gtk2" in wx.PlatformInfo:
            self.__songBrowser.SetStandardFonts()
            
        self.Bind(wx.EVT_CHOICE, self.__OnSongSelect, self.__songList)
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
        Publisher().subscribe(self.__OnSetHomepage, viewmgr.SIGNAL_SET_HOMEPAGE)

        # add some nice buttons
        self.__homeButton.SetBitmapLabel(icon_home.getBitmap())
        self.__browseBack.SetBitmapLabel(icon_browse_prev.getBitmap())
        self.__browseForward.SetBitmapLabel(icon_browse_next.getBitmap())
        
        # set the start page
        wp = wikiparser.WikiParser()
        self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
        
    # --------------------------------------------------------------------------
    def __AddSongs(self, message):
        sl = self.__songList
        for song in viewmgr.songs:
            idx = sl.Append(song._title)
            sl.SetClientData(idx, song)
        
        # if we are on the homepage, update the report
        if self._currPage == -1:
            self.__RenderHomepage()
          
    # --------------------------------------------------------------------------
    def __DeleteSong(self, message):
        sl = self.__songList
        for i in xrange(0, sl.GetCount()):
            if sl.GetClientData(i) == message.data:
                sl.Delete(i)
                break

        # if we are on the homepage, update the report
        if self._currPage == -1 or self._currPage == message.data._id:
            self._currPage = -1
            self.__RenderHomepage()

    # --------------------------------------------------------------------------
    def __UpdateSong(self, message):
        sl = self.__songList
        for i in xrange(0, sl.GetCount()):
            if sl.GetClientData(i) == message.data:
                sl.SetString(i, message.data._title)
                break

        # if we are on the homepage, update the report
        if self._currPage == -1:
            self.__RenderHomepage()
        elif self._currPage == message.data._id:
            # we are on the song page, update
            self.__RenderSongPage(message.data)

    # --------------------------------------------------------------------------
    def __ClearSongs(self, message):
        """ Clear list, we are changing databases """
        self.__songList.Clear()
        wp = wikiparser.WikiParser()
        self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
        
    # --------------------------------------------------------------------------
    def __OnSongSelect(self, event): 
        """ User selects a song, we set the song filter and the other
            components should show the proper info """
        idx = self.__songList.GetSelection()
        if idx <> wx.NOT_FOUND:
            s = self.__songList.GetClientData(idx)
            viewmgr.signalSetSong(s)

    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Another song is selected, sync our list """
        if message.data:
            # render the song info page
            self.__RenderSongPage(message.data)
        
            # if we already stand on the song, we do nothing
            sl = self.__songList
            idx = sl.GetSelection()
            if idx <> wx.NOT_FOUND:
                if message.data == self.__songList.GetClientData(idx):
                    return
    
            for i in xrange(0, sl.GetCount()):
                if sl.GetClientData(i) == message.data:
                    sl.SetSelection(i)
                    return
        else:
            self.__RenderHomepage()
            self.__songList.SetSelection(-1)

    # --------------------------------------------------------------------------
    def __RenderHomepage(self):
        """ We render the homepage containing all song statuses divided in sections """
        if not self.__songList.GetCount():
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
            for i in xrange(0, self.__songList.GetCount()):
                s = self.__songList.GetClientData(i)
                if s._status == stat_key:
                    lst.append(s)
        
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
        print tag
        # check if we need to select a song
        if tag.startswith('#song:'):
            song_nr = tag[6:]
            if song_nr:
                song = songfilter.Get()._list.find_id(int(song_nr))
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
        
        song = songfilter.Get()._selectedSong
        if song:
            if song._status <> status:
                # update in DB
                song._status = status
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Update(song)

                # issue a song update
                viewmgr.signalSongUpdated(song)
        
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
        viewmgr.signalSelectNextSong()

    #---------------------------------------------------------------------------
    def __OnBrowseBack(self, event):
        """ We are going to browse back. This means we will emit a signal that
            will determine the best song to be selected for us """
        
        # emit, and all will change
        viewmgr.signalSelectPreviousSong()
