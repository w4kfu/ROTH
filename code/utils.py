import Image
import ImageDraw

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')
    
def build_palette(palette, out="out.png"):
    im = Image.new("P", (512, 512), 0)
    im.putpalette(palette)
    d = ImageDraw.ImageDraw(im)
    d.setfill(1)
    x = 0
    y = 0
    for i in xrange(0, 256):
        d.setink(i)
        d.rectangle((x, y, x + 32, y + 32))
        x = (x + 32)
        if x % 512 == 0:
            y = (y + 32)
            x = 0
    im.save(out)