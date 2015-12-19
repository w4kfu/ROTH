# DAS

## Files

| Location | Filename     | Sha1                                     |
| -------- | ------------ | ---------------------------------------- |
| M/       | ADEMO.DAS    | bfcc53ba388cbdec764a93ffca6a07a75b4d2621 |
| M/       | DEMO.DAS     | cd628fad3471a2c0722216b04ef29d2172ce1a5b |
| M/       | DEMO1.DAS    | 92bc738ccdf75656b367f921b8f8d760abbb7e9d |
| M/       | DEMO2.DAS    | 87604aa39db0c7414de5c0e6cc51fd7b0e5e0aa1 |
| M/       | DEMO3.DAS    | 6c4b0aa65facbb3f01c75587a0a5cabf2ae8cb06 |
| M/       | DEMO4.DAS    | d8ece340470f886ad369e3f925650acd289b322f |


## DEMO VS ADEMO

There is two differents methods for parsing them in ROTH.EXE:

* 0x0002EFFB: ADEMO.DAS
* 0x0002F1B4: DEMO\<X\>.DAS

## File format

Data are stored in Little-Endian.

* Signature: *44 41 53 50* **'DASP'**
* Version: 5

### Header

* Length: 0x44 (68) bytes

Structure:

    +0x00       SIGNATURE           [DWORD]
    +0x04       VERSION             [DWORD]
    +0x06       LENGTH_IMG_LIST     [WORD]
    +0x08       OFFSET_IMG_LIST     [DWORD]
    +0x0C       OFFSET_VGA_PALETTE  [DWORD]
    +0x10       NS_offset_10        [DWORD]
    +0x14       OFFSET_NAMES        [DWORD]
    +0x18       SIZE_NAMES          [WORD]
    
Signature must be equal to 0x50534144.

Version must be equal to 0x05.
    
### IMG_LIST

Stored at offset *OFFSET_IMG_LIST*.

Number of items can be retrieved using: *LENGTH_IMG_LIST* / 8

Structure:

    +0x00       IMG_DATA            [DWORD]
    +0x04       UNK_WORD_00         [WORD]
    +0x06       UNK_WORD_01         [WORD]
    
### IMG_DATA

Img data: 8bit per pixel

    +0x00       UNK_WORD_00         [WORD]
    +0x02       WIDTH               [WORD]
    +0x04       HEIGHT              [WORD]
    +0x06       IMG_DATA            [BYTE] * (WIDTH * HEIGHT)
    
### NS_offset_10

* Length: 0x1000

UNKNOW ?!

### NAMES

Stored at offset *OFFSET_NAMES*.

Structure:

    +0x00       UNK_WORD_00         [WORD]
    +0x02       UNK_WORD_01         [WORD]
    +0x04       LIST_OF_NAMES       [NAME] * (UNK_WORD_00 + UNK_WORD_01)

Structure *NAME*:

    +0x00       LENGTH_DATA         [WORD]      (sizeof(LENGTH_DATA) + sizeof(ID) + strlen(NAME) + 1 + strlen(DESCRIPTION) + 1)
    +0x02       ID                  [WORD]
    +0x04       NAME                [CString]   // String NULL terminated
    +0xXX       DESCRIPTION         [CString]   // String NULL terminated

### NS_offset_2

* Length: *unk_word_08*
    
## Palette

* Length: 0x300 (768) bytes

VGA palette, 6-bit RGB (only the lower six bits of each byte are used).

To convert to 8-bit RGB:

    eight_bit_value = (six_bit_value * 255) / 63

A Palette is only present in *DEMO.DAS*, *DEMO1.DAS*, *DEMO2.DAS*, *DEMO3.DAS*, *DEMO4.DAS*.

| Filename     | MD5 PALETTE                      |
| ------------ | -------------------------------- |
| ADEMO.DAS    | [-] NOT PRESENT                  |
| DEMO.DAS     | 5c3365736a5f9ed6266421b1232b5760 |
| DEMO1.DAS    | 5c3365736a5f9ed6266421b1232b5760 |
| DEMO2.DAS    | 5c3365736a5f9ed6266421b1232b5760 |
| DEMO3.DAS    | 3b2873f10e385236dd841ad375fa5993 |
| DEMO4.DAS    | 3b2873f10e385236dd841ad375fa5993 |

The only difference is the RGB value at index 241 (723 / 3):

| Filename                       | Index  | 6-bit     | 8-bit      |
| ------------------------------ | ------ |---------- | ---------- |
| DEMO.DAS, DEMO1.DAS, DEMO2.DAS | 241    | (5, 1, 0) | (20, 4, 0) |
| DEMO3.DAS, DEMO4.DAS           | 241    | (0, 0, 0) | (0, 0, 0)  |

![das_palette.png][1]

## INFO

| Filename   | Signature  | Version    | LENGTH_IMG_LIST | OFFSET_IMG_LIST | OFFSET_VGA_PALETTE | NS_offset_10 | OFFSET_NAMES | SIZE_NAMES  | unk_word_08 | NS_offset_2 | unk_word_11 | unk_word_12 | NS_offset_3 | NS_offset_28 | NS_offset_2C | unk_word_19 | unk_word_20 | unk_word_21 | unk_word_22 | NS_Offset_38 | unk_word_25 | unk_word_26 | NS_Offset_40 |
| ---------- | ---------- | ---------- | --------------- | --------------- | ------------------ | ------------ | ------------ | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ------------ | ------------ | ----------- | ----------- | ----------- | ----------  | ------------ | ----------- | ----------- | ------------ |
| ADEMO.DAS  | 0x50534144 | 0x00000005 |      0x00001850 |      0x00000044 |     0x00000000     | 0x00000000   | 0x0128ED3A   | 0x00002A96  | 0x000000DC  | 0x0128DC5A  | 0x00000000  | 0x00000000  | 0x0128DD36  | 0x0128E1CA   | 0x00000B60   | 0x00000000  | 0x00000000  | 0x00000125  | 0x000001E5  | 0x0128ED2A   | 0x0000000A  | 0x00000006  | 0x0128ED34   |
| DEMO.DAS   | 0x50534144 | 0x00000005 |      0x000088F0 |      0x00000044 |     0x00008934     | 0x0001CE36   | 0x00F1143E   | 0x00005578  | 0x00000050  | 0x00F10FEE  | 0x00000000  | 0x00000000  | 0x00F1103E  | 0x00000000   | 0x00000000   | 0x00000F00  | 0x00000100  | 0x00000100  | 0x0000001E  | 0x00000000   | 0x00000000  | 0x00000000  | 0x00000000   |
| DEMO1.DAS  | 0x50534144 | 0x00000005 |      0x00008928 |      0x00000044 |     0x0000896C     | 0x0001CE6E   | 0x0109DD5E   | 0x00006316  | 0x0000008C  | 0x0109D8D2  | 0x00000000  | 0x00000001  | 0x0109D95E  | 0x00000000   | 0x00000000   | 0x00000F00  | 0x00000100  | 0x00000100  | 0x00000025  | 0x00000000   | 0x00000000  | 0x00000000  | 0x00000000   |
| DEMO2.DAS  | 0x50534144 | 0x00000005 |      0x000081C0 |      0x00000044 |     0x00008204     | 0x0001C706   | 0x0040EA26   | 0x000012D6  | 0x00000000  | 0x00000000  | 0x00000000  | 0x00000001  | 0x0040E626  | 0x00000000   | 0x00000000   | 0x00000F00  | 0x00000100  | 0x00000038  | 0x00000000  | 0x00000000   | 0x00000000  | 0x00000000  | 0x00000000   |
| DEMO3.DAS  | 0x50534144 | 0x00000005 |      0x00008128 |      0x00000044 |     0x0000816C     | 0x0001C66E   | 0x006F0F68   | 0x00001EF2  | 0x00000000  | 0x00000000  | 0x00000000  | 0x00000001  | 0x006F0B68  | 0x00000000   | 0x00000000   | 0x00000F00  | 0x00000100  | 0x00000025  | 0x00000000  | 0x00000000   | 0x00000000  | 0x00000000  | 0x00000000   |
| DEMO4.DAS  | 0x50534144 | 0x00000005 |      0x00008948 |      0x00000044 |     0x0000898C     | 0x0001CE8E   | 0x00C68AB8   | 0x00005732  | 0x00000050  | 0x00C68668  | 0x00000000  | 0x00000000  | 0x00C686B8  | 0x00000000   | 0x00000000   | 0x00000F00  | 0x00000100  | 0x00000100  | 0x00000029  | 0x00000000   | 0x00000000  | 0x00000000  | 0x00000000   |

[1]:das_palette.png