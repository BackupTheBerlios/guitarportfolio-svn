#----------------------------------------------------------------------
# This file was generated by D:\personal\src\GuitarPortfolio\trunk\images\make_images.py
#
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO, zlib


def getData():
    return zlib.decompress(
"x\xda\x01x\x01\x87\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\
\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\
\x08\x08\x08|\x08d\x88\x00\x00\x01/IDAT8\x8dc`\x18\x12 k\xe6\xfd\xf6\x94\x19\
\x0f\xbe`\x93c!\xa49y\xc6\xdd\xf6\xef\x7f\x19\xcb\xbf\xff\xfc\xc3\x88M\x9e\t\
\x9f\xe6\xb8)\xb7\xfb\xc4x\xd9+,\xd48\x19?~\xff\x83U\rN\x17D\xf6\xdd\x9a'\
\xc6\xcf\x9e(/\xca\xc2\xf0\xfb\xcf?\x86\x0f_\x7f\x13o@`\xcf\x8d%\xe2\x82\xac\
\xd1*\xe2l\x0co\xbf\xfca`gfd\xf8\xf0\x8dH\x03\xfc\xdbo<\x92\x14`\x97U\x91\
\xe0`x\xf1\xe1\x17\xc3\xc7o\x7f\x18\x04yX\x18>~\xfe\x85\xd5\x00\x8c0\xf8\xf8\
\xe3\xcf\xc5/?\xfe0|\xfb\xfd\x97\xe1\xdb\xcf\xbf\x0c_\x7f\xfee\xf8\xfe\xf3\
\x1f\xc3\xbf\xef\x7f\x893\xe0\xc1\x83\xd3\x81\xc7o|X\xbb\xf7\xd2G\x06VVF\x86\
\xff\xff\xfe3|\xff\xfd\x97\xe1\xdf7\xec.\xc0\xf0\xc2\x83\x85\x89\x7f\x18\x18\
\x18B>G\x1f^\xf9\xf5\xd3\xaf0C\r^\x86\x1f\xbf\xfe1\xfc\xfbJ\xa4\x0b`\xe0\xc5\
R\xdb\xf0\x9b\x97\xdf.>y\xe6\r\xc3\xcf_\xff\x18\xfe\xff$1\x1a\x19\x18\x18\
\x18^ow\x89\xfbk\xb1\xf9\xdf\xaf/\xbf\xe3\xff\xff\xfc\x87O)~\xc0\xaf\xb7~\
\xb6\xa0\xd1\xe6\xff\xe4\x9b@K\x00\x00\x88z\x83\xe3\xc8\xe9\xde\xa8\x00\x00\
\x00\x00IEND\xaeB`\x82\x0c#\xb5\x07" )

def getBitmap():
    return BitmapFromImage(getImage())

def getImage():
    stream = cStringIO.StringIO(getData())
    return ImageFromStream(stream)

