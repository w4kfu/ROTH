import os
import construct

from utils import conv_build_palette

FILENAME = "D:\Game\Realms of the Haunting\DATA\GDV\GREMLOGO.GDV"

# Sound Flags

SoundFlags = construct.BitStruct("SoundFlags",
    construct.Padding(4),
    construct.FlagsEnum(construct.BitField("PackedData", 1),            # BIT 3
        PCM                 = 0x00,
        DPCM                = 0x01,
    ),
    construct.FlagsEnum(construct.BitField("SampleWidth", 1),           # BIT 2
        BIT_8               = 0x00,
        BIT_16              = 0x01,
    ),
    construct.FlagsEnum(construct.BitField("AudioChannels", 1),         # BIT 1
        MONO                = 0x00,
        STEREO              = 0x01,
    ),
    construct.FlagsEnum(construct.BitField("AudioPresent", 1),          # BIT 0
        AUDIO_NOT_PRESENT   = 0x00,
        AUDIO_PRESENT       = 0x01,
    ),
    construct.Padding(8),
)

# Image type

ImageType = construct.BitStruct("ImageType",
    construct.Padding(5),
    construct.Enum(construct.BitField("Video_depth", 3),                # BIT 0-2
        PIXEL_8_BITS        = 0x01,
        PIXEL_15_BITS       = 0x02,
        PIXEL_16_BITS       = 0x03,
        PIXEL_24_BITS       = 0x04,
    ),
    construct.Padding(8),
)

# Video frame header

VideoFrameHeader = construct.Struct("VideoFrameHeader",
    construct.Anchor("start_VideoFrameHeader"),
    construct.Magic("\x05\x13"),                                    # + 0x00
    construct.ULInt16("Length"),                                    # + 0x02
    construct.ULInt32("TypeFlags"),                                 # + 0x04
)

# GDV header

GDVHeader = construct.Struct("GDVHeader",
    construct.Anchor("start_GDVHeader"),
    construct.Magic("\x94\x19\x11\x29"),                            # + 0x00
    construct.ULInt16("Size_ID"),                                   # + 0x04
    construct.ULInt16("Nb_frames"),                                 # + 0x06
    construct.ULInt16("Framerate"),                                 # + 0x08
    SoundFlags,                                                     # + 0x0A
    construct.ULInt16("Playback_frequency"),                        # + 0x0C
    ImageType,                                                      # + 0x0E
    construct.ULInt16("Frame_size"),                                # + 0x10
    construct.ULInt8("unk_byte_00"),                                # + 0x12
    construct.ULInt8("Losiness"),                                   # + 0x13
    construct.ULInt16("Frame_width"),                               # + 0x14
    construct.ULInt16("Frame_height"),                              # + 0x16
    construct.Anchor("end_GDVHeader"),
    
    # 768-byte palette if the video is palettized (image type indicates 8 bits/pixel)
    construct.If(lambda ctx: ctx["ImageType"]["Video_depth"] == "PIXEL_8_BITS",
        construct.OnDemandPointer(lambda ctx: ctx.end_GDVHeader,
            construct.Array(0x300, construct.ULInt8("Palette"))
        )
    ),
    # Compute our own anchor
    construct.IfThenElse("start_chunks", lambda ctx: ctx["ImageType"]["Video_depth"] == "PIXEL_8_BITS",
        construct.Value("value", lambda ctx: ctx["end_GDVHeader"] + 0x300),
        construct.Value("value", lambda ctx: ctx["end_GDVHeader"])
    ),
    
    # CHUNKS
        # Audio data
        construct.If(lambda ctx: ctx["SoundFlags"]["AudioPresent"]["AUDIO_PRESENT"] == True,
            construct.OnDemandPointer(lambda ctx: ctx.start_chunks,
            construct.Array(lambda ctx: compute_amount_of_audio_data(ctx), construct.ULInt8("Audio_data"))
            )
        ),
        # Compute our own anchor
        construct.IfThenElse("start_vfh", lambda ctx: ctx["SoundFlags"]["AudioPresent"]["AUDIO_PRESENT"] == True,
            construct.Value("value", lambda ctx: ctx["start_chunks"] + compute_amount_of_audio_data(ctx)),
            construct.Value("value", lambda ctx: ctx["start_chunks"])
        ),
        # Video Frame Header
        construct.OnDemandPointer(lambda ctx: ctx.start_vfh, VideoFrameHeader)
        
)

def compute_amount_of_audio_data(gs):
    amount = 0
    if gs["SoundFlags"]["AudioPresent"]["AUDIO_NOT_PRESENT"] == True:
        return 0
    amount = gs["Playback_frequency"] / gs["Framerate"]
    if gs["SoundFlags"]["AudioChannels"]["STEREO"] == True:
        amount = amount + amount
    if gs["SoundFlags"]["SampleWidth"]["BIT_16"] == True:
        amount = amount + amount
    if gs["SoundFlags"]["PackedData"]["DPCM"] == True:
        amount = amount >> 1
    return amount
    
fd = open(FILENAME, "rb")
buf = fd.read()
gs = GDVHeader.parse(buf)

#conv_build_palette(gs.Palette.read())

print gs

print gs["VideoFrameHeader"].read()

#print gs["Audio_data"].read()

#print "[+] start_chunks = 0x%08X" % (gs["start_chunks"])
#print "[+] compute_amount_of_audio_data = 0x%08X" % (compute_amount_of_audio_data(gs))

#print gs["SoundFlags"]["AudioPresent"]
#print gs["SoundFlags"]["AudioChannels"]
#
#print gs["Imagetype"]["Video_depth"]
#
## 0x106
#
#print hex(gs["end_GDVHeader"] + 0x300)
#
#length_audio_data = (gs["Nb_frames"] / gs["Framerate"])
#
## amount_of_audio_data = (sample_rate / frames_per_second) * (number_of_channels) * (bits_per_sample / 8)
##                        (21168 / 12) * (1) * (16 / 8)
#
#print "[+] gs[\"Playback_frequency\"] / gs[\"Framerate\"] = 0x%08X (%d)" % (gs["Playback_frequency"] / gs["Framerate"], gs["Playback_frequency"] / gs["Framerate"])
#
#print "[+] length_audio_data : 0x%08X" % length_audio_data
#
##print SoundFlags.parse("\x00\x01")["AudioPresent"]