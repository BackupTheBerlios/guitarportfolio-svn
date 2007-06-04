# TODO: Put the text inside the DB!

# TODO: Substitute version number / appname in HTML text
# TODO: Put inside the DB!

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
<table border=0 bgcolor="#eeeef6" width="95%">
  <tr><td valign="top" width="20%"><b><font size="+1">Started</font></b></td>
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
<tr><td><img src="@icon_path@@guitar_icon@" /></td><td><i><font size="16" color="#0000ff">@song@</font><br>
<font size="+3" color="#0000ff">By @artist@</font></i></td></tr>
</table>
<br><br>
<font size="+1">
<table border=0 bgcolor="#eeeef6">
  <tr><td valign="top"><b>Song Date:</b></td><td>@ldate@</td></tr>
  <tr><td valign="top"><b>Categories:</b></td><td>@categories@</td></tr>
  <tr><td valign="top"><b>Tuning:</b></td><td>@tuning_text@ (@tuning_name@)</td></tr>
  <tr><td valign="top"><b>Capo On:</b></td><td>@capo_text@</td></tr>
  <tr><td valign="top"><b>Number Of Bars:</b></td><td>@bar_count@</td></tr>
  <tr><td valign="top"><b>Progress:</b></td><td><b>@cprogress@</b>&nbsp;<img src="@icon_path@@song_status_icon@" />&nbsp;(@percprogress@%)</td></tr>
  <tr><td valign="top"><b>Difficulty:</b></td><td><img src="@icon_path@@song_rank@" /></td></tr>
  <tr><td valign="top"><b>Added In Database:</b></td><td>@time_added@</td></tr>
  <tr><td valign="top"><b>Started Practicing:</b></td><td>@time_started@</td></tr>
  <tr><td valign="top"><b>Completed Practicing:</b></td><td>@time_completed@</td></tr>
</table>
</font>
@song_status_change@
@song_links@
</body></html>
"""

# ==============================================================================

song_links_begin = """
<br><br><font size="+3"><img src="@icon_path@attach_icon.gif"/>&nbsp;<i>Attachments</i></font><br><br>
<font size="+1">
<table border=0 bgcolor="#eeeef6">
  <tr bgcolor="#c8c8cf"><td colspan="3" rowspan="1"><img src="@icon_path@folder_go.png"/><b>&nbsp;@song_path@</b></td></tr>
  <tr><td><b><br>Name</b></td><td><b><br>Type</b></td><td><b><br>Description</b></td></tr>
"""
song_links_row = """  
  <tr><td>@link_path@</td><td>@link_type@</td><td>@link_description@</td></tr>\n
"""
song_links_end = """
</table></font>
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
<font size="+1"><br><br>Change status to: 
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
</font>
"""
