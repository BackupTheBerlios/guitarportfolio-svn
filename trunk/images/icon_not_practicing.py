#----------------------------------------------------------------------
# This file was generated by D:\personal\src\GuitarPortfolio\trunk\images\make_images.py
#
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO, zlib


def getData():
    return zlib.decompress(
'x\xda\x01\x99\x02f\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\
\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\
\x08\x08\x08|\x08d\x88\x00\x00\x02PIDAT8\x8d\xa5\x93\xcbN\x14A\x14\x86?\xa6\
\x07F\x0c\x10Pn:8\x81\x11%Q\x89\xc1\x8d1F"\x89\x1b\x91\xe7pc\x8c\x0b\r{]hB\
\xa2\xa2"\xde^\xc1\x95\x1a\x9f\xc0\x151\xdc"\x19t\x04\xe42\x88\x8c\x03\xcc\
\xad\xbb\xab\xba\xba\xcaE\x8f\x03B\xdc\xe8IN\xceI\xa5\xfe\xef?\xa9\xd4\x81\
\xff\x8c\x8a\xdd\x07k/\x9f]\t\xed\xab\xbaW\x11\n\xc5\x8c\xaf\x04\xda`\xb4\
\x1f1\xae\\R\xf9\xc2\xed\xe4R\xeam\xdf\xe8\xa8\xfc}?\xbcS\x9cz\xfa\xb8?\xd2\
\xdc\xf0\xa2&~(jY\x06<\x05Z\x83\xd1\xf8Rwg\x13\x8b\xaf;\n\xb9\x9b\xc0\x83=\
\x13\xac\x8c\x0c_\xaenm\x1a\xad\xeb\x8a\xb5[\x1b\x0b\x90Y\x03\xa5Ay $\xd4\
\x1dD5\x1desr\xf6kq~\xf1F|x\xe4=\x80\x158?\xec\xdf\xdf\xd2\xf4\xaa\xeeX[\xcc\
\xca\xcc\xc3z\n<?\x10\n\t\xd2\x83L\x9a\x90[ \xd2\xdey@\xda\xce\xc5k\xed\x1d\
\xb3\x8f\xc6\'\x92!\x80p\xb8r\xa8\xb6\xa3%j\xad\'au\x11\\\x0f\x1c\'H\xdb\x05\
\xdb\t@\x0bI\xc2\x9f?\xd2\x18\x8fF+\xaaBC\xe570\xda\x8fY(H-\x82o@\xa9\xc0\
\xd5+\xa5T\xa5*`.A\xb8\xa5\x1d\xb4\x8e\x95\x01Z\x08\x17G\xd4\xe2\x8a`\xf4?\
\x84\xb2\xd4{A/\x048.\xdau\xdc\xed\t\x844H\tE\xa7\xe4\xbeCX\x86\x95R\x08\x90\
\x12-\x84\xd9\x06H\xb7\x1a\xdf\x83\\\x0e\x0c;\x1cw\x01<\t\xb6\r\xda\xc7HY\r\
\x10\x02\xd0\x85\xfc\xb2\xef(\xa8o\x84\xdc\x16\x14\x8b\xc1E\xdb\x86b\xa9:6\
\xe4\xb2\xd0z\x04O\xfa\xa8|n\xb9\x0c\x10\x99\x8d\xc1\xf5\x89\xc4\xaa\x8a\x9d\
\x82\x86V\xd8\xca\x06\x90bIh;\xe8l\x16}8\x86s\xfa<+c\x13\xab\xde\xfa\xcf\xc1\
\xf2?x2>\x9d\xbc\xda\xd8\x90\x14\x85\xe2\xb9\xea\x13\xdd\xf5V~\x13\xbe\xa7\
\xc0\x13\x18G\xa0l\x1b\xdd\x16G\x9c\xb9\xc0\xda\x87\xb1\xb9\xdc\xf4\xd4\xf5\
\x9e\xe9/\xef\xf6\xec\xc2\xcc\xa5\xde\x81\xba\xae\xce\xe7\xcd\'\x8fG+\xb5\
\x87\xefyh\xad\xf1\rx\x1a\xd2\xe3\x9f\xc8OM\xde\xeaI|\xbb\xff\xd7e\x9a\xe9=;\
`\xd5\xd4\xdc\xad\x08[1\xa3\x94\xf0}E\xc8\x98\x88r\x9c%\xb5\xb9qg\xebG\xfeM_\
:-w\xeb\xfe9~\x01(zr$\xa3\xd4\x07)\x00\x00\x00\x00IEND\xaeB`\x82\x1e\xac-m' )

def getBitmap():
    return BitmapFromImage(getImage())

def getImage():
    stream = cStringIO.StringIO(getData())
    return ImageFromStream(stream)

