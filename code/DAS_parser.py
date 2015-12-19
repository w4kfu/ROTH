import os
import construct
import re

import Image

import struct

pal_0 = [
(0x00, 0x00, 0x00),(0x00, 0x00, 0x00),(0x04, 0x44, 0x20),(0x48, 0x6C, 0x50),
(0x00, 0x50, 0x28),(0x34, 0x64, 0x40),(0x08, 0x3C, 0x1C),(0x00, 0x00, 0x00),
(0x44, 0x30, 0x30),(0x00, 0x00, 0x00),(0x3C, 0x28, 0x24),(0x00, 0x00, 0x00),
(0xBC, 0x80, 0x48),(0x00, 0x00, 0x00),(0x20, 0x10, 0x14),(0x00, 0x00, 0x00),
(0x2C, 0x80, 0x5C),(0x00, 0x00, 0x00),(0x3C, 0x2C, 0x64),(0x00, 0x00, 0x00),
(0x54, 0x2C, 0x0C),(0x00, 0x00, 0x00),(0x64, 0x78, 0x9C),(0x00, 0x00, 0x00),
(0x34, 0x88, 0x5C),(0x00, 0x00, 0x00),(0x44, 0x24, 0x10),(0x00, 0x00, 0x00),
(0x40, 0x3C, 0x38),(0x00, 0x00, 0x00),(0xDC, 0xAC, 0x84),(0x00, 0x00, 0x00),
(0xFC, 0xB0, 0x64),(0xC8, 0x8C, 0x4C),(0x94, 0x68, 0x38),(0x60, 0x44, 0x24),
(0x30, 0x20, 0x10),(0x00, 0x00, 0x00),(0xD0, 0x70, 0x30),(0xB8, 0x60, 0x28),
(0xA0, 0x54, 0x24),(0x88, 0x48, 0x1C),(0x70, 0x3C, 0x18),(0x58, 0x30, 0x10),
(0x40, 0x20, 0x0C),(0x2C, 0x14, 0x08),(0x14, 0x08, 0x04),(0x00, 0x00, 0x00),
(0xAC, 0xC4, 0xE8),(0x40, 0x2C, 0x5C),(0xB4, 0xCC, 0xF0),(0x2C, 0x24, 0x50),
(0x3C, 0x3C, 0x50),(0x1C, 0x1C, 0x28),(0x00, 0x00, 0x00),(0x70, 0x50, 0xBC),
(0x60, 0x44, 0xA4),(0x50, 0x38, 0x8C),(0x44, 0x30, 0x74),(0x34, 0x24, 0x5C),
(0x28, 0x1C, 0x44),(0x18, 0x10, 0x2C),(0x08, 0x04, 0x14),(0x00, 0x00, 0x00),
(0xFC, 0xFC, 0xFC),(0xE8, 0xE8, 0xE8),(0xD8, 0xD8, 0xD8),(0xC8, 0xC8, 0xC8),
(0xB8, 0xB8, 0xB8),(0xA4, 0xA4, 0xA4),(0x94, 0x94, 0x94),(0x84, 0x84, 0x84),
(0x74, 0x74, 0x74),(0x60, 0x60, 0x60),(0x50, 0x50, 0x50),(0x40, 0x40, 0x40),
(0x30, 0x30, 0x30),(0x1C, 0x1C, 0x1C),(0x0C, 0x0C, 0x0C),(0x00, 0x00, 0x00),
(0xBC, 0xD4, 0xF8),(0x00, 0x00, 0x00),(0x9C, 0xB8, 0xEC),(0x00, 0x00, 0x00),
(0xFC, 0xFC, 0x00),(0xE4, 0xE4, 0x00),(0xCC, 0xCC, 0x00),(0xB4, 0xB4, 0x00),
(0x9C, 0x9C, 0x00),(0x88, 0x88, 0x00),(0x70, 0x70, 0x00),(0x58, 0x58, 0x00),
(0x40, 0x40, 0x00),(0x28, 0x28, 0x00),(0x14, 0x14, 0x00),(0x00, 0x00, 0x00),
(0xFC, 0xE0, 0xBC),(0x84, 0x74, 0x64),(0xFC, 0xF0, 0xCC),(0x70, 0x68, 0x60),
(0xF4, 0xCC, 0xA0),(0x00, 0x00, 0x00),(0x00, 0x00, 0x00),(0xFC, 0x00, 0x00),
(0xDC, 0x00, 0x00),(0xBC, 0x00, 0x00),(0x9C, 0x00, 0x00),(0x7C, 0x00, 0x00),
(0x5C, 0x00, 0x00),(0x3C, 0x00, 0x00),(0x1C, 0x00, 0x00),(0x00, 0x00, 0x00),
(0xE8, 0xB8, 0x90),(0xCC, 0xA0, 0x80),(0xB4, 0x8C, 0x70),(0x98, 0x78, 0x5C),
(0x80, 0x64, 0x4C),(0x64, 0x50, 0x3C),(0x48, 0x38, 0x2C),(0x30, 0x24, 0x1C),
(0x14, 0x10, 0x0C),(0x00, 0x00, 0x00),(0xD4, 0x80, 0x6C),(0x68, 0x3C, 0x34),
(0x00, 0x00, 0x00),(0xF4, 0x54, 0x00),(0xD4, 0x48, 0x00),(0xB4, 0x3C, 0x00),
(0x94, 0x30, 0x00),(0x78, 0x28, 0x00),(0x58, 0x1C, 0x00),(0x38, 0x10, 0x00),
(0x1C, 0x04, 0x00),(0x00, 0x00, 0x00),(0x00, 0xAC, 0x5C),(0x00, 0x98, 0x50),
(0x00, 0x84, 0x44),(0x00, 0x70, 0x3C),(0x00, 0x5C, 0x30),(0x00, 0x48, 0x24),
(0x00, 0x34, 0x1C),(0x00, 0x24, 0x10),(0x00, 0x10, 0x04),(0x00, 0x00, 0x00),
(0x38, 0x1C, 0x0C),(0x38, 0x74, 0x58),(0x4C, 0x28, 0x0C),(0x2C, 0x80, 0x5C),
(0x00, 0x20, 0x34),(0x38, 0x84, 0x5C),(0x80, 0x38, 0x14),(0x34, 0x88, 0x5C),
(0xC0, 0x98, 0x7C),(0xDC, 0xAC, 0x84),(0x64, 0x38, 0x10),(0x50, 0x2C, 0x64),
(0x4C, 0x14, 0x00),(0x60, 0x3C, 0x8C),(0x3C, 0x30, 0x24),(0x58, 0x18, 0x84),
(0x54, 0x44, 0x30),(0x6C, 0x44, 0x94),(0x70, 0x5C, 0x44),(0x74, 0x4C, 0x9C),
(0x08, 0x2C, 0x18),(0x84, 0x58, 0xA4),(0x6C, 0x20, 0x00),(0x8C, 0x60, 0xB0),
(0x10, 0x08, 0x24),(0x30, 0x28, 0x50),(0x24, 0x18, 0x30),(0x38, 0x28, 0x4C),
(0x20, 0x14, 0x3C),(0x30, 0x2C, 0x48),(0x3C, 0x38, 0x3C),(0x24, 0x24, 0x24),
(0x60, 0x4C, 0x2C),(0x2C, 0x2C, 0x2C),(0x68, 0x54, 0x3C),(0x18, 0x18, 0x18),
(0x28, 0x10, 0x08),(0x78, 0x60, 0x48),(0x30, 0x18, 0x0C),(0x58, 0x48, 0x40),
(0x8C, 0x70, 0x54),(0x38, 0x2C, 0x40),(0xA4, 0x84, 0x60),(0x2C, 0x28, 0x3C),
(0x54, 0x3C, 0x28),(0x24, 0x28, 0x3C),(0x48, 0x48, 0x44),(0x3C, 0x30, 0x48),
(0x58, 0x58, 0x58),(0x3C, 0x2C, 0x44),(0x34, 0x34, 0x34),(0x50, 0xAC, 0x90),
(0x38, 0x28, 0x24),(0x34, 0x94, 0x88),(0x60, 0x24, 0x04),(0x4C, 0x9C, 0x84),
(0x50, 0x18, 0x00),(0x44, 0x34, 0x80),(0x44, 0x10, 0x00),(0x5C, 0x38, 0x98),
(0x34, 0x18, 0x0C),(0x90, 0x50, 0x24),(0x00, 0x40, 0x20),(0xB0, 0x58, 0x20),
(0x2C, 0x28, 0x44),(0x00, 0x00, 0x7C),(0x80, 0x60, 0x34),(0x80, 0x6C, 0xE4),
(0x78, 0x54, 0x28),(0x8C, 0x80, 0xE8),(0xA8, 0x74, 0x40),(0x8C, 0x9C, 0xF8),
(0xBC, 0xB8, 0xDC),(0x00, 0x00, 0x00),(0x8C, 0xAC, 0xDC),(0x00, 0x00, 0x00),
(0x80, 0xA0, 0xD4),(0x00, 0x00, 0x00),(0x70, 0x8C, 0xD0),(0x00, 0x00, 0x00),
(0x78, 0x90, 0xAC),(0x64, 0x78, 0x9C),(0x00, 0x54, 0x28),(0xA0, 0xE8, 0x54),
(0x30, 0x60, 0x34),(0x10, 0x70, 0x5C),(0x58, 0x68, 0x8C),(0x54, 0x54, 0x90),
(0x50, 0x54, 0x88),(0x54, 0x58, 0x94),(0x44, 0x44, 0x80),(0x60, 0x70, 0x8C),
(0xE8, 0x9C, 0x50),(0xF8, 0xD8, 0x00),(0x18, 0xC8, 0x5C),(0xFC, 0xE4, 0x00),
(0x50, 0xDC, 0x44),(0x14, 0x04, 0x00),(0xF8, 0xC4, 0x24),(0x00, 0x00, 0x00),
(0xE4, 0x84, 0x28),(0x00, 0x00, 0x00),(0xF4, 0x7C, 0x1C),(0x00, 0x00, 0x00),
(0xFC, 0xC8, 0x50),(0x00, 0x00, 0x00),(0xFC, 0xA8, 0x3C),(0x00, 0x00, 0x00),
(0xC0, 0x88, 0x30),(0x00, 0x00, 0x00),(0x48, 0x54, 0x68),(0x70, 0x00, 0xC8)]

FILENAME = "D:\Game\Realms of the Haunting\DATA\M\DEMO1.DAS"
#FILENAME = "D:\Game\Realms of the Haunting\DATA\M\ADEMO.DAS"

DAS_SIGNATURE = 0x50534144
DAS_VERSION = 0x05

# (WORD)0x06 + (WORD)0x1A

DASHeader = construct.Struct("DASHeader",
                    construct.ULInt32("Signature"),          # + 0x00
                    construct.ULInt16("Version"),            # + 0x04
                    construct.ULInt16("unk_word_00"),        # + 0x06
                    construct.ULInt32("NS_offset"),          # + 0x08
                    construct.ULInt32("Offset_VGA_palette"), # + 0x0C
                    construct.ULInt32("NS_offset_10"),       # + 0x10
                                #construct.ULInt16("unk_word_04"),        # + 0x12
                    construct.ULInt32("Offset_Names"),       # + 0x14       // Offset 2 Names
                    construct.ULInt16("Length_Names"),        # + 0x18       // Length Names
                    construct.ULInt16("unk_word_08"),        # + 0x1A
                    construct.ULInt32("NS_offset_2"),        # + 0x1C
                    construct.ULInt16("unk_word_11"),        # + 0x20
                    construct.ULInt16("unk_word_12"),        # + 0x22
                    construct.ULInt32("NS_offset_3"),        # + 0x24
                    construct.ULInt32("NS_offset_28"),       # + 0x28
                    construct.ULInt32("NS_offset_2C"),       # + 0x2C
                    construct.ULInt16("unk_word_19"),        # + 0x30
                    construct.ULInt16("unk_word_20"),        # + 0x32
                    construct.ULInt16("unk_word_21"),        # + 0x34
                    construct.ULInt16("unk_word_22"),        # + 0x36
                    construct.ULInt32("NS_Offset_38"),       # + 0x38
                    construct.ULInt16("unk_word_25"),        # + 0x3C
                    construct.ULInt16("unk_word_26"),        # + 0x3E
                    construct.ULInt32("NS_Offset_40"),       # + 0x40
                             )
                             
NameEntry = construct.Struct("NameEntry",
                #construct.ULInt16("Length"),
                construct.ULInt16("unk_word_00"),
                construct.CString("name"),
                construct.CString("desc"))
                
Names = construct.Struct("Names",
                construct.ULInt16("unk_word_00"),
                construct.ULInt16("unk_word_01"),
                )

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

def print_info_offset(s):
    print "[+] 0x08 : 0x%08X" % s['NS_offset']
    print "[+] 0x10 : 0x%08X" % s['NS_offset_10']
    print "[+] 0x14 : 0x%08X" % s['NS_offset_14']
    print "[+] 0x1C : 0x%08X" % s['NS_offset_2']
    print "[+] 0x24 : 0x%08X" % s['NS_offset_3']
    print "[+] 0x28 : 0x%08X" % s['NS_offset_28']
    print "[+] 0x2C : 0x%08X" % s['NS_offset_2C']
    print "[+] 0x38 : 0x%08X" % s['NS_Offset_38']
    print "[+] 0x40 : 0x%08X" % s['NS_Offset_40']
    
FirstS = construct.Struct("FirstS",
                construct.ULInt32("unk_dword_00"),
                construct.ULInt16("unk_word_00"),           # width  ?
                construct.ULInt16("unk_word_01"),           # height ?
            )
    
FirstEntry = construct.Struct("FirstS",
                construct.ULInt16("NS_unk_word_00"),
                construct.ULInt16("width"),
                construct.ULInt16("height"),
                )
    
def manage_first(fd_in, s):
    saved_pos = fd_in.tell()
    
    fd_in.seek(s["NS_offset"], os.SEEK_SET)
    buf = fd_in.read(s["unk_word_00"])
    print "[+] nb = 0x%08X" % (len(buf) / 8)
    for i in xrange(0, (len(buf) / 8)):
        fs = FirstS.parse(buf[(i * 8):((i + 1) * 8)])
        if i == (len(buf) / 8) - 1:
            continue
        nfs = FirstS.parse(buf[((i + 1) * 8):((i + 2) * 8)])
        if fs["unk_dword_00"] == 0x00:
            continue
        print fs
        fd_in.seek(fs["unk_dword_00"])
        entrys = FirstEntry.parse(fd_in.read(0x06))
        print entrys
        #print hexdump(fd_in.read(0x10))
        diff = 0
        if nfs["unk_dword_00"] != 0:
            diff = nfs["unk_dword_00"] - fs["unk_dword_00"]
            print "[+] diff : 0x%08X (%d)" % (diff, diff)
        fd_in.seek(fs["unk_dword_00"] + 6)
        if entrys["width"] != 0 and entrys["height"] != 0:
            ibuf = fd_in.read(entrys["width"] * entrys["height"])
            #print hexdump(ibuf, entrys["width"])
            new_buf = ""
            for j in xrange(0, len(ibuf)):
                new_buf += chr(pal_0[ord(ibuf[j])][0]) + chr(pal_0[ord(ibuf[j])][1]) + chr(pal_0[ord(ibuf[j])][2])
            x = Image.frombuffer("RGB", (entrys["width"], entrys["height"]), new_buf)
            x = x.transpose(Image.FLIP_TOP_BOTTOM)
            x.save("res_dir/%d.png" % i)
        #if diff != 0 and (entrys["width"] * entrys["height"]) != diff - 6:
        #    print "[-] ERROR !!!"
        #    exit(0)
    get_names(fd_in)
    fs = FirstS.parse(buf[(i * 8):((i + 1) * 8)])
    print fs
    fd_in.seek(fs["unk_dword_00"])
    entrys = FirstEntry.parse(fd_in.read(0x06))
    print entrys
    exit(0)
    fd_in.seek(saved_pos, os.SEEK_SET)
    
def read_ademo(fd_in, s):
    # FIRST
    print "[+] Seek to          0x%08X" % s["NS_offset"]
    fd_in.seek(s["NS_offset"], os.SEEK_SET)
    print "[+] Reading          0x%08X bytes" % s["unk_word_00"]
    buf = fd_in.read(s["unk_word_00"])
    print "[+] After should be  0x%08X" % (s["NS_offset"] + s["unk_word_00"])
    
    manage_first(fd_in, s)
    
    # SECOND
    print "[+] Seek to          0x%08X" % s["unk_word_01"]
    fd_in.seek(s["unk_word_01"], os.SEEK_SET)
    print "[+] Reading          0x%08X bytes" % 0x300
    buf = fd_in.read(0x300)
    print hexdump(buf[0:100])
    print "[+] After should be  0x%08X" % (s["unk_word_01"] + 0x300)
    
    # ...
    print "[+] Reading          0x%08X bytes" % 0x02
    buf = fd_in.read(0x02)
    print "[+] After should be  0x%08X" % (fd_in.tell())
    # ...
    print "[+] Reading          0x%08X bytes" % 0x4000
    buf = fd_in.read(0x4000)
    print hexdump(buf[0:100])
    print "[+] After should be  0x%08X" % (fd_in.tell())
    # ...
    print "[+] Reading          0x%08X bytes" % 0x10000
    buf = fd_in.read(0x10000)
    print hexdump(buf[0:100])
    pos = [m.start() for m in re.finditer("\x00\x00\x8D\xC2\x8D\xA4\x8D\x00\xB3\x00\x0E\x00\xBC\x00\x2E\x00", buf)]
    print pos
    print len(pos)
    print "[+] After should be  0x%08X" % (fd_in.tell())
    # ...
    print "[+] Reading          0x%08X bytes" % 0x100
    buf = fd_in.read(0x100)
    print "[+] After should be  0x%08X" % (fd_in.tell())
    # ...
    print "[+] Reading          0x%08X bytes" % 0x100
    buf = fd_in.read(0x100)
    print "[+] After should be  0x%08X" % (fd_in.tell())
    
    # THIRD
    print "[+] Seek to          0x%08X" % s["NS_offset_3"]
    fd_in.seek(s["NS_offset_3"], os.SEEK_SET)
    print "[+] Reading          0x%08X bytes" % 0x800
    buf = fd_in.read(0x800)
    print "[+] After should be  0x%08X" % (fd_in.tell())
    
    # FOURTH
    print "[+] Seek to          0x%08X" % s["NS_offset_10"]
    fd_in.seek(s["NS_offset_10"], os.SEEK_SET)
    print "[+] Reading          0x%08X bytes" % 0x1000
    buf = fd_in.read(0x1000)
    print "[+] After should be  0x%08X" % (fd_in.tell())
    
    # FIVETH
    print "[+] Seek to          0x%08X" % s["NS_offset_2"]
    fd_in.seek(s["NS_offset_2"], os.SEEK_SET)
    print "[+] Reading          0x%08X bytes" % s["unk_word_08"]
    buf = fd_in.read(s["unk_word_08"])
    print "[+] After should be  0x%08X" % (fd_in.tell())
    #exit(0)
    
def get_names(fd_in):
    fd_in.seek(0x109DD62, os.SEEK_SET)
    i = 0
    try:
        while True:
            length = struct.unpack("<H", fd_in.read(0x02))[0]
            #print "[+] length : 0x%04X" % length
            buf = fd_in.read(length - 2)
            s = NameEntry.parse(buf)
            print s
            #print hexdump(buf)
            i = i + 1
    except:
        print "[+] i : 0x%08X" % i
        return
        
def is_valid_das(sdas):
    if sdas["Signature"] != DAS_SIGNATURE:
        raise ValueError("Wrong Signature")
    if sdas["Version"] != DAS_VERSION:
        raise ValueError("Wrong Version")
        
def build_markdown_info(allinfo):
    print ''.join([("|%-20s" % name) for name, sdas in allinfo])
    print "| Location | Filename     | Sha1                                     |"
    print "| -------- | ------------ | ---------------------------------------- |"
        
def get_palette(fd, sdas):
    if sdas["Offset_VGA_palette"] == 0:
        print "[-] palette not present"
        return []
    print "[+] palette present!"
    fd.seek(sdas["Offset_VGA_palette"], os.SEEK_SET)
    buf = fd.read(0x300)

    import hashlib
    m = hashlib.md5()
    m.update(buf)
    print m.hexdigest()
    palette = []
    for i in xrange(0, len(buf), 3):
        #palette.append((ord(buf[i]), ord(buf[i + 1]), ord(buf[i + 2])))
        palette.append((ord(buf[i]) * 255) / 63)
        palette.append((ord(buf[i + 1]) * 255) / 63)
        palette.append((ord(buf[i + 2]) * 255) / 63)
    for i in xrange(0, len(palette), 3):
        print "[+] i : %d => %s" % (i, (palette[i], palette[i + 1], palette[i + 2]))
    return palette
        
def get_names(fd, sdas):
    if sdas["Offset_Names"] == 0:
        return
    fd.seek(sdas["Offset_Names"], os.SEEK_SET)
    buf = fd.read(sdas["Length_Names"])
    s = Names.parse(buf)
    print "[+] s[\"unk_word_00\"] : 0x%04X" % s["unk_word_00"]
    print "[+] s[\"unk_word_01\"] : 0x%04X" % s["unk_word_01"]
    i = 0
    pos = 4
    nb_desc = 0
    nb_name = 0
    try:
        while True:
            length = struct.unpack("<H", buf[pos: pos + 2])[0]
            pos += 2
            #print "[+] length : 0x%04X" % length
            b = buf[pos: pos + length - 2]
            pos = pos + length - 2
            s = NameEntry.parse(b)
            if len(s["name"]) > 0:
                nb_name = nb_name + 1
            if len(s["desc"]) > 0:
                nb_desc = nb_desc + 1
            print s
            #print hexdump(buf)
            i = i + 1
    except:
        print "[+] i : 0x%08X" % i
        print "[+] nb_name : 0x%08X" % nb_name
        print "[+] nb_desc : 0x%08X" % nb_desc
        return
        
def info_header_files():
    l_files = [#"D:\Game\Realms of the Haunting\DATA\M\ADEMO.DAS",
               #"D:\Game\Realms of the Haunting\DATA\M\DEMO.DAS",
               #"D:\Game\Realms of the Haunting\DATA\M\DEMO1.DAS",
               #"D:\Game\Realms of the Haunting\DATA\M\DEMO2.DAS",
               "D:\Game\Realms of the Haunting\DATA\M\DEMO3.DAS",]
               #"D:\Game\Realms of the Haunting\DATA\M\DEMO4.DAS"]
    all_info = []
    for file in l_files:
        fd = open(file, "rb")
        buf_header = fd.read(0x44)
        sdas = DASHeader.parse(buf_header)
        is_valid_das(sdas)
        name = os.path.basename(file)
        all_info.append((name, sdas))
        print name
        get_names(fd, sdas)
        
        #palette = get_palette(fd, sdas)
        #print name
        #if len(palette) != 0:
        #    import build_palette
        #    build_palette.build_palette(palette, name + "_palette.png")
        
        #b = '|'.join([" 0x%08X " % x for x in sdas.values()])
        #print "%-10s | %s" % (os.path.basename(file), b)
        

        fd.close()
    #build_markdown_info(all_info)
    exit(0)
    
info_header_files()
    
fd_in = open(FILENAME, "rb")

buf_dash = fd_in.read(0x44)

s = DASHeader.parse(buf_dash)
if s["Signature"] != DAS_SIGNATURE:
    raise ValueError("Wrong Signature")
if s["NS_Version"] != DAS_VERSION:
    raise ValueError("Wrong Version")
print s
print_info_offset(s)
get_names(fd_in)
exit(0)
#read_ademo(fd_in, s)

length_unk = ((s["unk_word_21"] + s["unk_word_22"]) * 8) & 0xFFFF

print "[+] length_unk : 0x%08X" % length_unk

exit(0)

fd_in.seek(s["NS_offset"], os.SEEK_SET)
buf = fd_in.read(length_unk)
print hexdump(buf[0:100])

print "[+] unk_word_08 (0x1A) : 0x%08X" % s["unk_word_08"]

fd_in.seek(s["NS_offset_2"], os.SEEK_SET)
buf = fd_in.read(s["unk_word_08"])
print hexdump(buf)

fd_in.seek(s["NS_offset_3"], os.SEEK_SET)
buf = fd_in.read(s["unk_word_21"] * 4)
print hexdump(buf)