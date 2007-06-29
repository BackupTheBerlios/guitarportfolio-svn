import os.path
import wx.tools.img2py as i2p


images = [ 'icon_completed.png', 
           'icon_in_progress.png',
           'icon_not_practicing.png',
           'icon_path_not_ok.png',
           'icon_todo.png',
           'side_art.png',
           'icon_path_ok.png',
           'icon_main_window.png',
           'icon_home.png',
           'icon_browse_next.png',
           'icon_browse_prev.png',
           'guitarportfolio_icon.png',
           'icon_attachment.png',
           'icon_ignore.png',
           'icon_status_changed.png',
           'icon_progress_changed.png'  ]


for name in images:
    root, ext = os.path.splitext(name)
    print 'Converting', name, ' to ', root + '.py'
    i2p.img2py(name, root + '.py')
