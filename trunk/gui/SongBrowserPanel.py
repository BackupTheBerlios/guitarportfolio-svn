# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sun May 13 11:47:41 2007 from D:\personal\src\GuitarPortfolio\branches\db_revival\gui\guitarportfolio.wxg

import os.path

import wx
import wx.xrc as xrc
import wx.html as html
import time

from wx.lib.pubsub import Publisher
from objs import signals, songs, songfilter
from images import icon_home, icon_browse_next, icon_browse_prev
import HtmlInfoGen, xmlres, appcfg, htmlparse

# TODO: Put the text inside the DB!
startupinfo = """
<html><body>
<font size="16">GuitarPortfolio v1.0</font><br>
Created by Jorgen Bodde<br><br>

GuitarPortfolio is a songs collection manager application that can keep track of the songs you are 
practicing and the progress you are making. Some features are;<br><br>

<ul>
<li>Storing song background information</li>
<li>Storing links to sites or external files</li>
<li>Storing attachments inside the database like MP3's, AVI's or PDF's</li>
<li>Storing multiple music tabs</li>
<li>Keeping track of your progress bar by bar</li>
<li>A study log, with time tracking to see when you studied what songs</li>
<li>And much more!</li>
</ul><br><br>

The reason why this application is written, is to maintain a list of songs I am already able to play, 
and songs which are still a bit hard, but when time progresses could get into my reach. For example,
whenever you hear a nice song on the radio, you can place an entry in GuitarPortfolio and when you have 
the time, play it or investigate it. <br><br>

Have fun playing!
</body></html>
"""

# TODO: Substitute version number / appname in HTML text
# TODO: Put inside the DB!

home_page = """
<html><body>
@songs_practicing@
@songs_todo@
@songs_completed@
@songs_postponed@
</body></html>
"""

songs_practicing = """
<font size="16"><img src="@icon_path@@icon_practicing@"/>&nbsp;Songs Currently Practicing</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Started</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="35%"><b><font size="+1">Title</font></b></td>
      <td valign="top" width="15%"><b><font size="+1">Progress</font></b></td></tr>
  @song_row@
</table>
</font>
<br><br><br>
"""

songs_todo = """
<font size="16"><img src="@icon_path@@icon_todo@"/>&nbsp;Songs Still To Play</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Added</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="50%"><b><font size="+1">Title</font></b></td></tr>
  @song_todo_row@
</table>
</font>
<br><br><br>
"""

song_todo_row = """
  <tr><td>@time_added@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td></tr>
"""

songs_completed = """
<font size="16"><img src="@icon_path@@icon_completed@" />&nbsp;Songs Completed</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Date</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="35%"><b><font size="+1">Title</font></b></td>
      <td valign="top" width="15%"><b><font size="+1">Progress</font></b></td></tr>
  @song_completed_row@
</table>
</font>
<br><br><br>
"""

song_completed_row = """
  <tr><td>@time_completed@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td><td>@percprogress@%</td></tr>
"""

songs_postponed = """
<font size="16"><img src="@icon_path@@icon_postponed@"/>&nbsp;Songs Not Practicing</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Date</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="35%"><b><font size="+1">Title</font></b></td>
      <td valign="top" width="15%"><b><font size="+1">Progress</font></b></td></tr>
  @song_postponed_row@
</table>
</font>
<br><br><br>
"""

song_postponed_row = """
  <tr><td>@time_postponed@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td><td>@percprogress@%</td></tr>
"""

song_row = """
  <tr><td>@time_started@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td><td>@percprogress@%</td></tr>
"""

songinfo = """<html><body>
<table border=0 cellspacing=0 cellpadding=0>
<tr><td><img src="@icon_path@@guitar_icon@" /></td><td><i><font size="16" color="#0000ff">@song@</font><br>
<font size="+3" color="#0000ff">By @artist@</font></i></td></tr>
</table>
<br><br>
<font size="+1">
<table border=0 bgcolor="#eeeef6">
  <tr><td valign="top"><b>Song Date</b></td><td>@ldate@</td></tr>
  <tr><td valign="top"><b>Categories</b></td><td>@categories@</td></tr>
  <tr><td valign="top"><b>Tuning</b></td><td>@tuning_text@ (@tuning_name@)</td></tr>
  <tr><td valign="top"><b>Capo On</b></td><td>@capo_text@</td></tr>
  <tr><td valign="top"><b>Number of bars</b></td><td>@bar_count@</td></tr>
  <tr><td valign="top"><b>Progress</b></td><td><b>@cprogress@</b>&nbsp;<img src="@icon_path@@song_status_icon@" />&nbsp;(@percprogress@%)</td></tr>
  <tr><td valign="top"><b>Difficulty</b></td><td><img src="@icon_path@@song_rank@" /></td></tr>
  <tr><td valign="top"><b>Added In Database</b></td><td>@time_added@</td></tr>
  <tr><td valign="top"><b>Started Practicing</b></td><td>@time_started@</td></tr>
  <tr><td valign="top"><b>Completed Practicing</b></td><td>@time_completed@</td></tr>
</table>
</font>
<br><br><font size="+2">Attachments</font><br><br>
<font size="+1">
<table border=0 bgcolor="#eeeef6">
  <tr><td><b>Name</b></td><td><b>Type</b></td><td><b>Description</b></td></tr>
  @song_links_row@
</table>
</font>
</body></html>
"""

link_row_info = """
  <tr><td>@link_name@</td><td>@link_type@</td><td>@link_description@</td></tr>\n
"""

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
        self.__songBrowser.SetPage(startupinfo)
        
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
        self.__songBrowser.SetPage(startupinfo)
        
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
            self.__songBrowser.SetPage(startupinfo)
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
        
        # now render the page in sections
        spage = self.__DoRenderSongSection(page = home_page, 
                                           section = ("@songs_practicing@", songs_practicing),
                                           songrow = ("@song_row@", song_row),
                                           songs = stats[songs.SS_STARTED])
                                          
        spage = self.__DoRenderSongSection(page = spage, 
                                           section = ("@songs_todo@", songs_todo),
                                           songrow = ("@song_todo_row@", song_todo_row),
                                           songs = stats[songs.SS_NOT_STARTED])
                                          
        spage = self.__DoRenderSongSection(page = spage, 
                                           section = ("@songs_completed@", songs_completed),
                                           songrow = ("@song_completed_row@", song_completed_row),
                                           songs = stats[songs.SS_COMPLETED])

        spage = self.__DoRenderSongSection(page = spage, 
                                           section = ("@songs_postponed@", songs_postponed),
                                           songrow = ("@song_postponed_row@", song_postponed_row),
                                           songs = stats[songs.SS_POSTPONED])

        self.__songBrowser.SetPage(spage)
        
    def __DoRenderSongSection(self, page, section, songrow, songs):
        """ Render a section of the page, based upon the type of song, template etc """
        # we work bottom up, first gather all songs and slowly replace
        # the tags one by one
        if len(songs) > 0:
            songrows = ''
            for s in songs:
                songrows = songrows + htmlparse.ParseSongHtml(songrow[1], s) + '\n'
            pg = section[1].replace(songrow[0], songrows)
            pg = page.replace(section[0], pg)
            # render some icons
            pg = htmlparse._ParseCommonHtml(pg)
            return pg
        else:
            # no songs, we replace the contents with an empty page
            return page.replace(section[0], '')

    # --------------------------------------------------------------------------
    def __RenderSongPage(self, song):
        """ We render the homepage containing all song statuses divided in sections """
        taginfo = { htmlparse.HTML_LABEL_CATEGORIES:  ('', 
                                                       '@name@',
                                                       '<br>', 
                                                       '' ), 
                    htmlparse.HTML_LABEL_LINKS:       (link_row_info) 
                  }        

        pg = htmlparse.ParseSongHtml(songinfo, song, taginfo)

        self.__songBrowser.SetPage(pg)
        self._currPage = song._id

    #---------------------------------------------------------------------------
    def __OnLinkClicked(self, event):
        tag = event.GetLinkInfo().GetHref()
        # check if we need to select a song
        if tag.startswith('#song:'):
            song_nr = tag[6:]
            if song_nr:
                songfilter.Get().SelectSong(int(song_nr))
        
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
