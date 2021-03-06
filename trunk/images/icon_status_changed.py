#----------------------------------------------------------------------
# This file was generated by make_images.py
#
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO, zlib


def getData():
    return zlib.decompress(
'x\xda\x01\xa0\x02_\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\
\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\
\x08\x08\x08|\x08d\x88\x00\x00\x02WIDAT8\x8d}\xd0MK\x1ba\x10\xc0\xf1\xff\xbe\
$em\x15\x8a\xac1&iQ\xf1\x10\t\x8a`\xd1\x9a\xb3z.1\xbd\xf7\xd4\xcf\xd4C\xbf@\
\x89 \nJ\xddv\xc1\x83V\x10\n\xc1ZE\x92\x95\xaa\xd1f\x93\xc6\xa2\x89\x9a\xa4\
\x9d\xa7\'\x83\xf5mN\x033\xf3cf\xb4\xad\xad-\xa5\x94BDPJq=\x17\x91\xae\xd1\
\xd1\xd1\x12\x0f\x84\xb6\xb9\xb9\xa9\x06\x07\x07o\x15\x8e\x8f\x8f)\x16\x8b4\
\x9b\xcd\xae\xb1\xb1\xb1{\x11])\x05@\xa1P \x9b\xcdrpp\x00@8\x1c\xc6\xb6m\x0c\
\xc3\xf0WWW\xed{\x01\x11\x01\xa0T*122\xa2\xf9\xbe\xff\xf5\xfc\xfc\x1c\x11!\
\x12\x89\xb4\x90\x95\x95\x95;\x91\x16\xd0\xd9\xd9\xc9\xc6\xc6F]Dl\xd349)5X\
\xffT&\x16\x8b\x11\n\x850\x0c\xc3w]\xf7\x16b^\x9d\x10\x8b\xc5\x88F\xa3\xc1f\
\xb3\x19\xab\x9d\xc2\xec\xfb\x02\x8dK\x85R\xf0r\xf29"\xc2\xe1\xe1\xa1\xbf\
\xbc\xbc\xdc555U\xba\xbe\xc1E\xa5R\x01@D8;\x11>\xbc;\xe0\xf1\x13\x13;\xfc\
\x88o\x1b\xa7|q\xca\xf4\xf6\xf6\xd2\xd3\xd3\x83i\x9a\xfe\xe2\xe2\xa2}\x1d\
\x98\xce\xe5r\x17\xe5r\x19\xc30\xa8\x94\x1a4\xeb\nM\xd70L\x8d\x8e\xa7\x81\
\x16\xd2\xdf\xdfO4\x1a\xc54M\x7f~~\xde\x06\xd0\x94R\xac\xad\xad%E\xc4\x19\
\x18\x18\xb0l\xdb\xc6\xdb>\xc3\x99-\xd2\xf14H \xa8\xf3\xf7\x8f\xe2\xf7\xaf\
\x06\x89\x17\x1d$\xa7mvww\xf1<\x8fz\xbd\xde\xa5\x03LLL\xac\x8a\xc8\xe4\xce\
\xce\xce\x85\xef\xfb\xf4\xc5\xdb\x99L\x858=i\xd0l\x08\x9a\x0e\x81\xa0\xcev\
\xb6\x82\x88B\xd7ut]GD\xda\xb4\xab\'\x02\xb8\xae\x9bTJ9\xf1x\xdc\xea\xee\xee\
\xc6\xdb>\xe3c\xe6\'\x81\x80A[;\xbcz\x13\xa5p\xb4\x8f\xe7y\xd4j\xb5\xbeT*\
\xb5\xf7\x1f\x00\xe08NRD\x9cD"a\x85\xc3a\xf2\xdfOY\xff\\\xe1\xf5\xdbg\xfc\
\xd8\xf7\xf0<\x8fj\xb5\xda733\xb3\xd7\xfa\xc1\xcdXZZJ\x8a\x88344dE"\x11\x00r\
\xb9\x1c\xf9|\x9eZ\xad\xd6\x1a\xbe\x17\x00XXX\x18WJ\xb9\xc3\xc3\xc3\xd6\xe5\
\xe5ek\xed\xeb\xc3\x0f\x02\x00sss\xe3"\xe2Z\x96eU\xab\xd5\xbet:\xbdw\xb3\xe7\
A\x00 \x93\xc9\x8c+\xa5\x8e\xd2\xe9\xf4\xfe]\xf5\x7f1~U\xed!\x88\xf5"\x00\
\x00\x00\x00IEND\xaeB`\x82w\xdc;4' )

def getBitmap():
    return BitmapFromImage(getImage())

def getImage():
    stream = cStringIO.StringIO(getData())
    return ImageFromStream(stream)

