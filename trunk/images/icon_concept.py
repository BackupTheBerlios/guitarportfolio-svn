#----------------------------------------------------------------------
# This file was generated by make_images.py
#
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO, zlib


def getData():
    return zlib.decompress(
'x\xda\x01\x00\x03\xff\xfc\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\
\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\
\x08\x08\x08\x08|\x08d\x88\x00\x00\x02\xb7IDAT8\x8d\x95\x92\xddk\xd5u\x1c\
\xc7_\xdf\xdf\xf9\xfd~\xe7a;\x0fn\x1e\xddp\xabVDk>L\xb3\t\xab\x18L\xbc\x88\
\x02\xa1\xa1D\x94\x14\x82\x8d\xfe\x81\x10\xf1\xe9J\xbd\x08\xf2B\x10\xbb(\x88\
\x04\x83`\x8d\x19\xb59p\x08\xc2\x8a\x92Am\xce\xb9\xb6y\xa6\xc19\x9b{:\xbf\
\x87s~\x0f\xdf\xaf\x17cc\xe9\xb9\xf1}\xf3\xb9y\xbf_\xf0\x81\x97PJ\xb11\xcel\
\xef\'x\xeeG\x84\xce\xce\xa0de\x95\xb7,T\xd9\xb2\xa5\xef>\x14z\xa2g\xd3;\x17\
\xcen\xec\x8b5\x80\xfb\xe0\xe7z\xa4\xfcV3\x13\xefFb\x19D4\x83\xd0\x13\x08!\
\x90%\x87`q\n{\xf2\x17|knZO7\x1d\xac\xed\xbc\xf0\xcf:\xc0\xc9\xf5U)o\xe9\xa6\
\x99ij\x8b\xa4^\x04$H\x1b\x94\x87\x92\x1e \x11F\x1a!\xb2X#WY\x19\xef[0\x1a\
\xdaZ\xb6t\x9e\xcf\xeb\x00\xca\xfe\xef\xb4\x9elh\xd3\xd3/\xa3\xa4\x83\xd0\
\xe2`l[\xbd\x80\x92\x0e\xca\x9b%\xf4\x7f\'\xb9\xf7\x08\xa5\xfc\xfd\x1aon\xe6\
;\xe0=\r t\x97>\x8eT\xbf\x00\xca\x01\xa1\x83\x88\x01ru(\x1dP\x01"\x92\x02t\
\x02\xeb\x06\xa97>\xa3\x94\x9f\xe9\x04\xd0\x01\xc2R1\xabE\x93\xc8 \x0f\xc2\
\x00\xe9\xa2\xc2\x10d\x80R>By(\xcd!,O\xa1\xfcI\xcc\xf4[\x04n9\xba\x0e\x90e\
\xab\x10\x14\x0b\rz\xa6\x1a\xafp\r\xa1%p\xff\x9c\x00=\x06\xca\'\\\xc9S\xd5\
\xb1\x0fY\xba\x8b\x91\xde\x83\xb7\x90GhZ\x19@\x03@\x8b_u\xa6o!"u }V\xae\xffH\
tw\x96\xe8\x8ej\xcc\x16\x83\xc4\xdb\xaf\xb1\xf8\xfdyd\xf91zm\x17\x0b\xc3?`\
\xa4\xea\x87\xd7\x01\xba\x19;\xe9=\xfe\xf7\x9e=\xdeO\xb4\xfe\x18"\x16\x07\
\x14D\x1c\xd0mP\n\xad*I\xe2\xa5\x13\x14GFX\x1e\xfb\xadlf_\xf9|\x1d\x90n?\x13\
h\xb1\xcc\x87\xd6\xf8\xaf\xf3\xf6\xbd?0\x92;W-\t\xe3\x08\x99\x05\x14z\xcd>V\
\xeeL\xf2\xa8\xf7TP\xdd\xdcqt\xdb\x07\x17\xef\xffO$\x80\xb9\x81/\xdf\xb4\x16\
\xe6\xfbb\xce\xa3\xbaMM\x06fs\x00\xcaCNe\x98\xed\xbfM\xd1l,\xd64\xef=\xd4p\
\xf8\xca\xc03&\xaee\xe8\xda\xb9\xf7\xc7&\xa6zR\x9b\xb7\x1a\xb6=\x84e\xfb\x14\
\x16\xb7\xf3`\xf4/\xd5\xfdi\xd7\xfe\xce#g\x87*\xaa\xbc1\xa7\x8f\x7f\x91{uWG#\
\xa1\x86\xe3\xda\x14\x1d\x97\xe1\xc1\x9e\xf9\x9f\xae\x0ff\x9f\xee\xea\xcf\
\xac\x01\xcfu\x1f\xd6o\xdd\xd2\xd8\xba\xab\x95\\.\xc7\xdf\xa3ch"X\xaa\xd4\
\xad\x088\xd0\xfe\xfa\xe5o.}\xd5\xbad\x07\xf1 \xf0\x89\x9b\x94\xba\x0fw|]\
\xa9[\xf1\x85\xe7\xc9\x13n\x83@n\xee\xe9>>\x00\x00\x00\x00IEND\xaeB`\x82\x9c\
7e\xf9' )

def getBitmap():
    return BitmapFromImage(getImage())

def getImage():
    stream = cStringIO.StringIO(getData())
    return ImageFromStream(stream)
