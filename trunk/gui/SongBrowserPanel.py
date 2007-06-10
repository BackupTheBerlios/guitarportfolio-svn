import os.path

import wx
import wx.xrc as xrc
import wx.html as html
import time

from wx.lib.pubsub import Publisher
from objs import signals, songs, songfilter, linkmgt
import db
import db.songs_peer
from images import icon_home, icon_browse_next, icon_browse_prev
import xmlres, appcfg, htmlparse, linkfile, htmlmarkup, wikiparser

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
        Publisher().subscribe(self.__AddSong, signals.SONG_DB_ADDED)  
        Publisher().subscribe(self.__UpdateSong, signals.SONG_DB_UPDATED)  
        Publisher().subscribe(self.__DeleteSong, signals.SONG_DB_DELETED)  
        Publisher().subscribe(self.__ClearSongs, signals.APP_CLEAR)  
        Publisher().subscribe(self.__OnSongSelected, signals.SONG_VIEW_SELECTED)  

        Publisher().subscribe(self.__SongsRestored, signals.APP_READY)  

        # add some nice buttons
        self.__homeButton.SetBitmapLabel(icon_home.getBitmap())
        self.__browseBack.SetBitmapLabel(icon_browse_prev.getBitmap())
        self.__browseForward.SetBitmapLabel(icon_browse_next.getBitmap())
        
        # set the start page
        wp = wikiparser.WikiParser()
        self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
        
    # --------------------------------------------------------------------------
    def __AddSong(self, message):
        # TODO: Sort the items in the choice
        sl = self.__songList
        idx = sl.Append(message.data._title)
        sl.SetClientData(idx, message.data)
        
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
            songfilter.Get().SelectSong(s._id)

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
    def __SongsRestored(self, message):
        """ ALl songs are restored, if we are on the main homepage, we update the 
            table else we ignore """
        if self._currPage == -1:
            self.__RenderHomepage()
            
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
                songfilter.Get().SelectSong(int(song_nr))
        # check for execution of a link
        elif tag.startswith('#link:'):
            link_nr = tag[6:]
            if link_nr:
                link = linkmgt.Get().links.find_id(int(link_nr))
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
        else:
            # attempt gnome start execution
            linkfile.executelink(tag)
        
    #---------------------------------------------------------------------------
    def __DoSetSongStatus(self, status):
        song = songfilter.Get()._selectedSong
        if song:
            if song._status <> status:
                # update in DB
                song._status = status
                sp = db.songs_peer.SongPeer(db.engine.GetDb())
                sp.Update(song)                
        
    #---------------------------------------------------------------------------
    def __OnBrowseHome(self, event):
        self._currPage = -1
        self.__RenderHomepage()
        
    #---------------------------------------------------------------------------
    def __OnBrowseForward(self, event):
        if self._currPage == -1:
            # take first (if any)
            if self.__songList.GetCount() > 0:
                s = self.__songList.GetClientData(0)
                songfilter.Get().SelectSong(s._id)
                return
        else:
            # find the next song in the list
            i = self.__songList.GetSelection()
            if i < (self.__songList.GetCount() - 1) and i != -1:
                s = self.__songList.GetClientData(i + 1)
                songfilter.Get().SelectSong(s._id)
                return
                
    #---------------------------------------------------------------------------
    def __OnBrowseBack(self, event):
        if self._currPage == -1:
            # take last (if any)
            if self.__songList.GetCount() > 0:
                s = self.__songList.GetClientData(self.__songList.GetCount() - 1)
                songfilter.Get().SelectSong(s._id)
                return
        else:
            # find the previous song in the list
            i = self.__songList.GetSelection()
            if i > 0:
                s = self.__songList.GetClientData(i - 1)
                songfilter.Get().SelectSong(s._id)
                return
