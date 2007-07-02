#----------------------------------------------------------------------
# This file was generated by make_images.py
#
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO, zlib


def getData():
    return zlib.decompress(
'x\xda\x01\xee\x02\x11\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\
\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\
\x08\x08\x08\x08|\x08d\x88\x00\x00\x02\xa5IDAT8\x8d\xa5\x93\xbdK\x1cQ\x14\
\xc5\xcf\xcc\xac+;\xce\xbe\xd5@\xc6%+\x06A\x89\x0bb\xd4i\x04\x9b4\x06\xb6\
\xb40]\xd2\x07;\xd9\x90"\xe9B*\xd3\x89\xf5B\xd0\x90&~\xfd\x01\x82\x8d\x1f\
\x85EX+a\x15"d\n1\x0e\xb3;:\xf3\xde\xbdoR\x84L\x02\xd1*\xb7\xbd\xdc\x1f\xe7\
\xdes\x8f\x91\xa6)\xfe\xa7rw5\xea\xf5z)M\xd3\xc2\xc8\xc8\x88\x98\x9b\x9b\xd3\
\x85B\x81NOO\xe5\xea\xeaj;I\x12\xb9\xbc\xbc\x9c\x00\x80q\x9b\x82z\xbd\x9eg\
\xe6g\x83\x83\x83/L\xd3|\xcc\xcc\xf7L\xd3Dww\xf7\x8f8\x8e\xbf\x9e\x9d\x9d}d\
\xe6\xb5\x95\x95\x95\xf4V\x05Z\xeb\xd7\x03\x03\x03\xaffff\x8a\xae\xebBJ\tf\
\x86eYn\xa7\xd3\x99\x8d\xa2h\xfa\xe2\xe2b\x08\xc0;\xf3\xef\xc1\xad\xad-c}}\
\xdd(\x95J\xaf\xe6\xe7\xe7\x8b\xd5j\x15\xa5R\t\xf9|\x1eZk\xd8\xb6\x8dJ\xa5\
\x82Z\xadV\xb4m\xfbMv\x83\xed\xedmKk\xfd\x90\x99\x1f0s~bb\xc29::\x82\xe7y\
\x10B@k\x8d4M\xa1\x94\x82eY8<<D___w\x06\xd0Z?b\xe6\xb7D\xf4\x84\x88\x9c8\x8e\
\x8dr\xb9\x8c\x83\x83\x03(\xa5\x90\xcb\xe5 \xa5\x84eYPJarr\x12;;;\xbf\\\xd8\
\xd8\xd8p\x98\xf9\xc3\xd8\xd8X\xad\xbf\xbf\x1f]]]\x08\x82\x00\xcdf\x13\x000:\
:\n\xc30\xc0\xcc "\x04A\x80 \x08 \xa5\x04\x00\x98D\xf4\xd4u\xddZ\xb9\\\xc6\
\xcd\xcd\r\xe28\x86\x10\x02\xd3\xd3\xd3(\x16\x8bh\xb5Z\xe8\xe9\xe9\x81a\x18\
\xb0m\x1b\xbe\xefg\xeb\x00\x80\xa9\x94z944\x84\xcb\xcbK\xb4\xdbm\x84a\x88N\
\xa7\x03\xc30\xe0y\x1eZ\xad\x16\xd24\x85i\x9a\xb0,\x0bR\xca\x7f\x00\xf7s\xb9\
\x1c\xce\xcf\xcf\x11\xc71\xe28F\x14E\xb8\xbe\xbe\x86\xe38\x08\xc3\x10WWW\x99\
S\xbf-\xcd\x00R\xcaoQ\x14\xa1Z\xad\xc2\xf7}\x1c\x1f\x1f#\x0cCDQ\x04\x00H\x92\
\x04I\x92@k\r\xad5\x94R\xd0Z\x83\x882\xc0\xe7\x93\x93\x138\x8e\x83\xf1\xf1qL\
MMA\x08\x01\x00PJ\x81\x99\xd1\xdb\xdb\x9bYiY\x16l\xdb\xfe\xa3`aa\xe1S\xb3\
\xd9\xfc\xb2\xbb\xbb\x0b!\x04\x84\x10(\x14\n\xb0m\x1b{{{\x18\x1e\x1e\x86\xeb\
\xba\xa8T*\x10B`vv\x16\xbe\xef\x83\x88\xbeg\x7f \xa5\x9c\xdf\xdf\xdf\xff\x12\
\x86\xe1\x9c\xe7y\x99\xd4\xcd\xcd\xcd\xd4q\x1ccii\tD\x04"\x023+f\xfe\xce\xcc\
\xde?aZ\\\\|\xae\x94zOD>\x11\xb5\x89h\xad\xd1h4\xeeJ,\x00\xfc\x04\x8c\xa2\
\x8658\xf8\xfc\xef\x00\x00\x00\x00IEND\xaeB`\x82\xb0\xf6Q\xe9' )

def getBitmap():
    return BitmapFromImage(getImage())

def getImage():
    stream = cStringIO.StringIO(getData())
    return ImageFromStream(stream)

