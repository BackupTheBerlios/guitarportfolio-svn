# TODO: Put the text inside the DB!

# TODO: Substitute version number / appname in HTML text
# TODO: Put inside the DB!

startupinfo = """
== Welcome To GuitarPortfolio ==
GuitarPortfolio is an application that can keep track of the songs you are playing on the guitar, or are going to play. It's purpose is to provide a centralized repository on which you can add the songs you like to play with the following '''__extensive__''' information:

<ul>
<li>Artist, Title of Song</li>
<li>Song Information page</li>
<li>One or more guitar tabs</li>
<li>Date Song is released  (year, full date or unknown)</li>
<li>Song difficulty classification (easy, normal ... impossible)</li>
<li>Progress tracking (% accuracy, % completed, practice time, etc)</li>
<li>Which capo position the song is played on</li>
<li>Classification in categories for easy search</li>
<li>Distinction between tutorials / riffs and real songs</li>
<li>Attachments, to start up PDF's or Mp3's with a click</li>
<li>A log for progress and user notes for practice history</li>
</ul>

==== The main flow of GuitarPorfolio ====
__*Storing songs you wish to play in the future*__<br>
image(icon_todo.png)&nbsp;For example, you hear a neat song on the radio or a great lick you wish to practice. You create a new song in GuitarPortfolio and store information along with it, such as a tab found on the net, or links to a site, and even as attachment, the mp3 or a movie on your harddrive to accompany you when playing. '''Is the song still too difficult?''' Rate it as 'Intermediate' or 'Advanced' so that you will not see the songs that you are not able to play yet in your selection list.

__*Starting the practice*__<br>
image(icon_in_progress.png)&nbsp;When you're in the mood for a new song, browse through the list of songs and pick one marked as '''TODO''' image(icon_todo.png)&nbsp;and change it's status to '''IN PROGRESS'''. This enables the logging system, marks the date you started and will make it easier for you to find it back in your list of songs you are working on. You can use the log to check for progress, total time studied, notes and changes in your % accuracy and % completion of the song. 

__*Tired of practicing?*__<br>
image(icon_not_practicing.png)&nbsp;You can postpone a song you are not practicing anymore. It does not mean you are done with it. It simply means you stopped with it for a while. Sometimes you wish to continue once you mastered a new level, or a sudden shift of interest brings new songs.

__*Done playing the song?*__<br>
image(icon_completed.png)&nbsp;Once you mastered a song, mark it as completed for the record. The date is recorded that you last worked on it, so that in years from now you can still see when you studied a particular song, and what problems you had with it. Are you in the mood of playing it again or perfecting it? Change the status back to image(icon_in_progress.png)&nbsp; and you can work on it once again. The completed date will not change anymore, the log however will provide a trace of your progress.
==== Other features of GuitarPortfolio ====

*__Categories__*
GuitarPortfolio provides *categories* which act as labels. You can attach one or more labels to the song, marking a specific styles the song has. If you wish to study songs with such a style, the song filter panel will allow you to narrow down the song selection list 

*__Wiki HTML Editing__*
The song information and lyrics can be edited using a simple wiki markup language, which will be easier then writing plain HTML. Images and tables can be embedded in the information view, this will allow you to create a fancy page containing all information you need. You can store pictures in the artist / song's data directory or in the global data directory to use the images in HTML, keeping everything together.

*__Browser Mode__*
GuitarPortfolio can be set in Browser mode which will allow you to use as much as the mouse only to navigate through your songs, making it easier to obtain the information you need to work on your song. Switching to editor mode will allow you to modify the song's information

*__Database Storage__*
If for some odd reason GuitarPortfolio crashes unexpectedly, no data is lost. A database backend is used to store all information and it is stored upon change so restarting GuitarPortfolio after a crash, will show exactly the same data. Ofcourse if crashes occur, please report this to me (jorgb@xs4all.nl)

*__Cross Platform!__*
Ohh yeah, do you wish to switch to Linux / MacOS, or do you switch often? GuitarPortfolio is written in wxPython and therefor runs on; 
<ul>
<li>Windows</li>
<li>Linux</li>
<li>HP-UX</li>
<li>MacOS</li>
<li>...</li>
</ul>
<br>
The database should be accessible from any platform without converting it. Setting the global data directory in the preferences should also make sure all your song information and attachments are accessible under any platform. 

*Have fun!*
- Jorgen Bodde
"""

# ==============================================================================

home_page = """
<html><body>
@songs_practicing@
@songs_todo@
@songs_completed@
@songs_postponed@
</body></html>
"""

# ==============================================================================

songs_practicing_begin = """
<font size="16"><img src="@icon_path@@icon_practicing@"/>&nbsp;Songs Currently Practicing</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table  valign="top" border=0 bgcolor="#eeeef6" width="95%">
  <tr><td width="20%"><b><font size="+1">Started</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="35%"><b><font size="+1">Title</font></b></td>
      <td valign="top" width="15%"><b><font size="+1">Progress</font></b></td></tr>
"""
songs_practicing_row = """
  <tr><td>@time_started@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td><td>@percprogress@%</td></tr>
"""
songs_practicing_end = """
</table>
</font>
<br><br><br>
"""

# ==============================================================================

songs_todo_begin = """
<font size="16"><img src="@icon_path@@icon_todo@"/>&nbsp;Songs Still To Play</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Added</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="50%"><b><font size="+1">Title</font></b></td></tr>
"""
songs_todo_row = """
  <tr><td>@time_added@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td></tr>
"""
songs_todo_end = """
</table>
</font>
<br><br><br>
"""

# ==============================================================================

songs_completed_begin = """
<font size="16"><img src="@icon_path@@icon_completed@" />&nbsp;Songs Completed</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Date</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="35%"><b><font size="+1">Title</font></b></td>
      <td valign="top" width="15%"><b><font size="+1">Progress</font></b></td></tr>
"""
songs_completed_row = """
  <tr><td>@time_completed@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td><td>@percprogress@%</td></tr>
"""
songs_completed_end = """
</table>
</font>
<br><br><br>
"""

# ==============================================================================

songs_postponed_begin = """
<font size="16"><img src="@icon_path@@icon_postponed@"/>&nbsp;Songs Not Practicing</font><br><br>
<font size="+1" face="Arial, Lucida Grande, sans-serif">
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Date</font></b></td>
      <td valign="top" width="30%"><b><font size="+1">Artist</font></b></td>
      <td valign="top" width="35%"><b><font size="+1">Title</font></b></td>
      <td valign="top" width="15%"><b><font size="+1">Progress</font></b></td></tr>
"""
songs_postponed_row = """
  <tr><td>@time_postponed@</td><td>@artist@</td><td><a href="#song:@song_id@">@song@</a></td><td>@percprogress@%</td></tr>
"""
songs_postponed_end = """
</table>
</font>
<br><br><br>
"""

# ==============================================================================

songinfo = """<html><body>
<table border=0 cellspacing=0 cellpadding=0>
<tr><td><img src="@icon_path@@song_type_icon@" /></td><td>&nbsp;<i><font size="16" color="#0000ff">@song@</font><br>
<font size="+3" color="#0000ff">By @artist@</font></i></td></tr>
</table>
<br><br>
<font size="+1">
<table valign="top" border=0 bgcolor="#eeeef6">
  <tr>
    <td><b>Song Date:</b></td><td>@ldate@</td>
    <td><b>Song Info:</b></td><td>@song_info_link@</td>
  </tr>
  <tr><td><b>Tuning:</b></td><td>@tuning_text@ (@tuning_name@)</td><td><b>Song Lyrics:</b></td><td>@song_lyrics_link@</td></tr>
  <tr><td><b>Measures:</b></td><td>@bar_count@</td><td><b>Capo On:</b></td><td>@capo_text@</td></tr>
  <tr><td><b>Categories:</b></td><td>@categories@</td><td><b>Tabs:</b></td><td>@song_label_tabs@</td></tr>
  <tr><td><b>Difficulty:</b></td><td><img src="@icon_path@@song_rank@" /></td>
    <td><b>Progress:</b></td>
    <td><b>@cprogress@</b>&nbsp;<img src="@icon_path@@song_status_icon@" />&nbsp;<a href="#cmd:edit_progress"><img src="@icon_path@icon_edit.png"/></a><br>@progress_info@ (@percprogress@%)</td></tr>
  <tr><td><b>Added In Database:</b></td><td>@time_added@</td><td></td><td></td></tr>
  <tr><td><b>Started Practicing:</b></td><td>@time_started@</td><td></td><td></td></tr>
  <tr><td><b>Completed Practicing:</b></td><td>@time_completed@</td><td></td><td></td></tr>
</table>
</font>
<br><br><ul>
@song_status_change@
<li><font size="+1">Enter <a href="#cmd:enter_comment">a comment</a> while studying ...</font></li>
</ul>
@song_links@
</body></html>
"""

# ==============================================================================

song_links_begin = """
<br><br><font size="+3"><img src="@icon_path@attach_icon.png"/><i>Attachments</i></font><br><br>
<font size="+1">
<table valign="top" border=0 bgcolor="#DDDDED">
  <tr bgcolor="#eeeef6"><td colspan="3" rowspan="1"><img src="@icon_path@folder_go.png"/><b>&nbsp;@song_path@</b></td></tr>
  <tr><td><b><br>Name</b></td><td><b><br>Type</b></td><td><b><br>Description</b></td></tr>
"""
song_links_row = """  
  <tr><td>@link_path@</td><td>@link_type@</td><td>@link_description@</td></tr>\n
"""
song_links_end = """
</table></font>
"""

# ==============================================================================

song_info_header = """
<font size="+3"><img src="@icon_path@icon_info.png"/><i>&nbsp;@song@ - @artist@</i></font><br><br>
@song_info@
"""

# ==============================================================================

song_lyrics_header = """
<font size="+3"><img src="@icon_path@icon_lyrics.png"/><i>&nbsp;@song@ - @artist@</i></font><br><br>
@lyrics@
"""

# ==============================================================================

song_tab_header = """
<font size="+3"><img src="@icon_path@icon_tab.png"/><i>&nbsp;@song@ - @song_tab_name@</i></font>
<pre>@song_tab@</pre>
"""

# ==============================================================================

categories_begin = """
"""
categories_row = """
@name@
"""
categories_append = """
<br>
"""
categories_end = """
\n
"""

# ==============================================================================

#links_path_not_ok = """
#<font size="+1"><br><br>Attachments directory invalid: 
#<a href = "#cmd:createlinks">create directory</a><br></font>
#"""
links_path_not_ok = """
\n
"""
links_path_ok = """
\n
"""

# ==============================================================================
change_status_start = """
<li><font size="+1">Change status to: 
"""
change_status_in_progress = """
<a href="#cmd:status_practicing">In Progress&nbsp;<img src="@icon_path@@icon_practicing@"/></a>
"""
change_status_in_postponed = """
<a href="#cmd:status_postponed">Not Practicing&nbsp;<img src="@icon_path@@icon_postponed@"/></a>
"""
change_status_in_completed = """
<a href="#cmd:status_completed">Completed&nbsp;<img src="@icon_path@@icon_completed@"/></a>
"""
change_status_append = """
, 
"""
change_status_end = """
</font></li>
"""
