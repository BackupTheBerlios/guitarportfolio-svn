import os.path

import wx
import wx.xrc as xrc
import wx.html as html
import time

from wx.lib.pubsub import Publisher
from objs import songs, linkmgt
import db
import db.songs_peer
from images import icon_home, icon_browse_next, icon_browse_prev, \
                   icon_song_next, icon_song_previous, icon_song
import xmlres, appcfg, htmlparse, linkfile, htmlmarkup, wikiparser, \
       viewmgr, browserstack

PAGE_HOMEPAGE    = 0
PAGE_SONG        = 1
PAGE_SONG_INFO   = 2
PAGE_SONG_TAB    = 3
PAGE_SONG_LYRICS = 4

# these pages are not allowed in the history of the browse stack. So what we do
# is simply removing them from the past pages. This is done to make sure the 
# pages are not shown when the selected song is not the song belonging to the
# info shown. When the user clicks 'back' the first page that is valid is shown
# usually the song belonging to the info, lyrics or song tab(s)
forbidden_history = [PAGE_SONG_INFO, PAGE_SONG_LYRICS, PAGE_SONG_TAB]

songtaginfo = { htmlparse.HTML_LABEL_CATEGORIES:  (htmlmarkup.categories_begin, 
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
                                                   htmlmarkup.change_status_end ),
                htmlparse.HTML_SONG_INFO:          htmlmarkup.song_info_header
          }        


#===============================================================================

class SongBrowserPanel(wx.Panel):
    def __init__(self, parent, id = -1):
        pre = wx.PrePanel()
        xmlres.Res().LoadOnPanel(pre, parent, "SongBrowserPanel")
        self.PostCreate(pre)
        
        # stack of items in the browser
        self.stack = browserstack.BrowserStack()
        self.stack.callbackOnChange = self.__OnRenderCurrPage
                
        self.__homeButton = xrc.XRCCTRL( self, "ID_BTN_HOME")
        self.__browseBack = xrc.XRCCTRL( self, "ID_BTN_BACK")
        self.__browseForward = xrc.XRCCTRL( self, "ID_BTN_FORWARD")
        self.__songBrowser = xrc.XRCCTRL(self, "ID_BROWSER_WINDOW")
        self.__browseSongBack = xrc.XRCCTRL( self, "ID_PREV_SONG")
        self.__browseSongForward = xrc.XRCCTRL( self, "ID_NEXT_SONG")
        self.__songIcon = xrc.XRCCTRL(self, "ID_SONG_BMP")
        
        self.__browseBack.Enable(False)
        self.__browseForward.Enable(False)

        
        if "gtk2" in wx.PlatformInfo:
            self.__songBrowser.SetStandardFonts()
            
        self.Bind(html.EVT_HTML_LINK_CLICKED, self.__OnLinkClicked, self.__songBrowser)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseHome, self.__homeButton)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseForward, self.__browseSongForward)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseBack, self.__browseSongBack)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseHistoryBack, self.__browseBack)
        self.Bind(wx.EVT_BUTTON, self.__OnBrowseHistoryForward, self.__browseForward)

        # signals for song selection dropdown
        Publisher().subscribe(self.__UpdateSong, viewmgr.SIGNAL_SONG_UPDATED)  
        Publisher().subscribe(self.__DeleteSong, viewmgr.SIGNAL_SONG_DELETED)  
        Publisher().subscribe(self.__ClearSongs, viewmgr.SIGNAL_CLEAR_DATA)  
        Publisher().subscribe(self.__OnSongSelected, viewmgr.SIGNAL_SONG_SELECTED)  
        Publisher().subscribe(self.__AddSongs, viewmgr.SIGNAL_DATA_RESTORED) 
        Publisher().subscribe(self.__CriteriaListChanged, viewmgr.SIGNAL_CRITLIST_CHANGED) 
        Publisher().subscribe(self.__OnSetHomepage, viewmgr.SIGNAL_SET_HOMEPAGE)
        Publisher().subscribe(self.__LinksRefreshed, viewmgr.SIGNAL_LINKS_REFRESHED)

        # add some nice images
        self.__homeButton.SetBitmapLabel(icon_home.getBitmap())
        self.__browseBack.SetBitmapLabel(icon_browse_prev.getBitmap())
        self.__browseForward.SetBitmapLabel(icon_browse_next.getBitmap())
        self.__browseSongBack.SetBitmapLabel(icon_song_previous.getBitmap())
        self.__browseSongForward.SetBitmapLabel(icon_song_next.getBitmap())
        self.__songIcon.SetBitmap(icon_song.getBitmap())
        
        # set the start page
        wp = wikiparser.WikiParser()
        self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
        
    # --------------------------------------------------------------------------
    def __AddSongs(self, message):
        # if we are on the homepage, update the report
        if self.stack.IsCurrentPage((PAGE_HOMEPAGE,)):
            self.__OnRenderCurrPage()        
        else:
            self.stack.Push((PAGE_HOMEPAGE,))
      
    # --------------------------------------------------------------------------
    def __UpdateSong(self, message):
        """
        Update the song information (tab, lyrics, info) if the song receives
        an update event 
        """
        
        if self.__IsSongPageDisplayed(message.data):
            self.__OnRenderCurrPage()        
    
    # --------------------------------------------------------------------------
    def __DeleteSong(self, message):
        """
        A song is deleted, check if we are looking at it, else take some action
        """
        if self.__IsSongPageDisplayed(message.data):
            self.stack.ResetAndPush((PAGE_HOMEPAGE,))
        else:
            self.stack.Truncate()

    # --------------------------------------------------------------------------
    def __ClearSongs(self, message):
        """ Clear list, we are changing databases """
        self.stack.ResetAndPush((PAGE_HOMEPAGE,))
                
    # --------------------------------------------------------------------------
    def __OnSongSelected(self, message):
        """ Another song is selected, sync our list """
        song = message.data
        if song:
            # if we are looking at it, do not push it only refresh
            if not self.stack.IsCurrentPage((PAGE_SONG, song)):
                self.stack.Push((PAGE_SONG, song), forbidden_history)
        else:
            # we push the homepage on the stack only when not looking
            if not self.stack.IsCurrentPage((PAGE_HOMEPAGE,)):
                self.stack.Push((PAGE_HOMEPAGE,), forbidden_history)
        
        # always render
        self.__OnRenderCurrPage()
            
    # --------------------------------------------------------------------------
    def __LinksRefreshed(self, message):
        """ Handler for refreshed links """
        
        # we refresh the selected page, we assume the 
        # selected song got the links refresh event        
        song = viewmgr.Get()._selectedSong
        if song and self.stack.IsCurrentPage((PAGE_SONG, song)):
            self.__OnRenderCurrPage()

    # --------------------------------------------------------------------------
    def __CriteriaListChanged(self, message):
        """
        We received a message that the filter criteria is changed, so when
        looking at the homepage, change the list
        """
        
        # if we are on the main page, render
        if self.stack.IsCurrentPage((PAGE_HOMEPAGE,)):
            self.__RenderHomepage()
            
    # --------------------------------------------------------------------------
    def __RenderHomepage(self):
        """ 
        We render the homepage containing all song statuses divided in sections 
        """
        
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

        songs_section_info = { htmlparse.HTML_SECTION_PRACTICING: (stats[songs.SS_STARTED],
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
                                      
        page = htmlparse.ParseSongsByStatus(htmlmarkup.home_page, songs_section_info)
        self.__songBrowser.SetPage(page)
        
    # --------------------------------------------------------------------------
    def __RenderSongPage(self, song):
        """ 
        We render the homepage containing all song statuses divided in sections 
        """
    
        pg = htmlparse.ParseSongHtml(htmlmarkup.songinfo, song, songtaginfo)

        self.__songBrowser.SetPage(pg)
        self._currPage = song._id

    #---------------------------------------------------------------------------
    def __OnLinkClicked(self, event):
        tag = event.GetLinkInfo().GetHref()
        
        if linkfile.is_valid_external_link(tag):
            linkfile.execute_uri(tag)

        # check if we need to select a song
        elif tag.startswith('#song:'):
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

        # check for execution of a tab
        elif tag.startswith('#tab:'):
            tab_nr = tag[5:]
            if tab_nr:
                song = viewmgr.Get()._selectedSong
                if song:
                    tab = song.tabs.find_id(int(tab_nr))
                    if tab:
                        # push the tab on the stack, and refresh the view
                        self.stack.Push((PAGE_SONG_TAB, song, tab))
                        
        # check for execution of a command
        elif tag.startswith('#cmd:'):
            cmd = tag[5:]
            commands = { "status_practicing": lambda : self.__DoSetSongStatus(songs.SS_STARTED),
                         "status_postponed":  lambda : self.__DoSetSongStatus(songs.SS_POSTPONED),
                         "status_completed":  lambda : self.__DoSetSongStatus(songs.SS_COMPLETED),
                         "edit_info":         self.__DoShowEditInfo,
                         "edit_lyrics":       self.__DoShowEditLyrics,
                         "enter_comment":     self.__DoEnterComment,
                         "edit_progress":     self.__DoShowEditProgress,
                         "show_lyrics":       self.__DoShowLyrics,
                         "show_info":         self.__DoShowInfo                
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
    def __DoShowEditInfo(self):
        """
        The edit panel needs to be visible, and shown. We do this through the 
        view mgr because on this level we do not have access to that frame
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            # signal an edit request
            viewmgr.signalSongEditInfo(song)

    #---------------------------------------------------------------------------
    def __DoShowEditLyrics(self):
        """
        The edit panel needs to be visible, and shown. We do this through the 
        view mgr because on this level we do not have access to that frame
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            # signal an edit request
            viewmgr.signalSongEditLyrics(song)

    #---------------------------------------------------------------------------
    def __DoShowEditProgress(self):
        """
        The edit progress panel needs to be visible, and shown. We do this through the 
        view mgr because on this level we do not have access to that frame
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            # signal an edit request
            viewmgr.signalSongEditProgress(song)

    #---------------------------------------------------------------------------
    def __DoEnterComment(self):
        """
        Popup a text dialog so that the user can enter a comment for the log
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            dlg = wx.TextEntryDialog(self, 'Enter a comment for the log',
                                     'Enter comment', '')
    
            if dlg.ShowModal() == wx.ID_OK and dlg.GetValue():
                viewmgr.signalAddComment(song, dlg.GetValue())

    #---------------------------------------------------------------------------
    def __DoShowLyrics(self):
        """
        Show the lyrics HTML of the current song
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            self.stack.Push((PAGE_SONG_LYRICS, song))

    #---------------------------------------------------------------------------
    def __DoShowInfo(self):
        """
        Show the lyrics HTML of the current song
        """
        
        song = viewmgr.Get()._selectedSong
        if song:
            self.stack.Push((PAGE_SONG_INFO, song))

    #---------------------------------------------------------------------------
    def __OnBrowseHome(self, event):
        """ 
        User click to get to the homepage. This is indirectly done by the view manager 
        """
        viewmgr.signalSetHomepage()
        
    #---------------------------------------------------------------------------
    def __OnSetHomepage(self, message):
        """
        Signal is received that we have to switch to the homepage
        """
        self.stack.Push((PAGE_HOMEPAGE,))        
        
    #---------------------------------------------------------------------------
    def __OnBrowseForward(self, event):
        """ 
        We are going to browse forward. This means we will emit a signal that
        will determine the best song to be selected for us 
        """
                    
        # emit, and all will change
        viewmgr.signalSelectPreviousSong()

    #---------------------------------------------------------------------------
    def __OnBrowseBack(self, event):
        """ 
        We are going to browse back. This means we will emit a signal that
        will determine the best song to be selected for us
        """
        
        # emit, and all will change
        viewmgr.signalSelectNextSong()

    #---------------------------------------------------------------------------
    def __OnRenderCurrPage(self, pageTuple = None):
        """
        Handler to render the page on the HTML browser whenever a navigation 
        action is done, can be called seperately too, to force a redraw
        """
        
        page = self.stack.CurrentPage()
        if page:
            # render homepage
            if page[0] == PAGE_HOMEPAGE:
                self.__RenderHomepage()
    
            # else get song, and render
            elif page[0] == PAGE_SONG:  
                self.__RenderSongPage(page[1])
                
            # else get info, and render
            elif page[0] == PAGE_SONG_INFO:
                pg = htmlparse.ParseSongHtml(htmlmarkup.song_info_header, page[1])
                self.__songBrowser.SetPage(pg)
                
            # else get lyrics, and render
            elif page[0] == PAGE_SONG_LYRICS:
                pg = htmlparse.ParseSongHtml(htmlmarkup.song_lyrics_header, page[1])
                self.__songBrowser.SetPage(pg)
                
            # else try tabs
            elif page[0] == PAGE_SONG_TAB:
                tags = { "tabdata": page[2] }
                pg = htmlparse.ParseSongHtml(htmlmarkup.song_tab_header, page[1], tags)
                self.__songBrowser.SetPage(pg)
        else:
            wp = wikiparser.WikiParser()
            self.__songBrowser.SetPage(wp.Parse(htmlmarkup.startupinfo))
            
        # based upon back or forward being present, 
        # disable or enable buttons
        self.__browseBack.Enable(self.stack.CanBrowseBack())
        self.__browseForward.Enable(self.stack.CanBrowseForward())


    #---------------------------------------------------------------------------
    def __OnBrowseHistoryBack(self, event):
        """
        Handler to browse back into history
        """
        if self.stack.HistoryBack():
            page = self.stack.CurrentPage()
            self.__SyncPageWithStack(page)
        
    #---------------------------------------------------------------------------
    def __OnBrowseHistoryForward(self, event):
        """
        Handler to browse back into history
        """
        if self.stack.HistoryForward():
            page = self.stack.CurrentPage()
            self.__SyncPageWithStack(page)
            
    #---------------------------------------------------------------------------
    def __SyncPageWithStack(self, page):
        """
        Sync the selection mechanism with the current stack page. Simply viewing 
        the previous or next page is not enough, if we look at a different
        song, the selection mechanism should kick in and show it
        """
        if page[0] == PAGE_SONG:
            viewmgr.signalSetSong(page[1])
        elif page[0] == PAGE_HOMEPAGE:
            viewmgr.signalSetSong(None)
        else:
            self.__OnRenderCurrPage()   # default   

    #---------------------------------------------------------------------------
    def __IsSongPageDisplayed(self, song):
        """
        Test if the song or any sub page of that song is currently displayed
        as first item on the browserstack, so we know when to update the view
        """

        page = self.stack.CurrentPage()
        if page:
            if page[0] in [PAGE_SONG, PAGE_SONG_INFO, 
                           PAGE_SONG_LYRICS, PAGE_SONG_TAB]:
                return page[1] == song
        return False
    
