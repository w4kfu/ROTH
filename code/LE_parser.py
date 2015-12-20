import os
import construct

from utils import hexdump

##################################
# LINEAR-EXECUTABLE informations:
#
# * http://unavowed.vexillium.org/pub/doc/LE
#
##################################

FILENAME = "D:\Game\Realms of the Haunting\ROTH\ROTH.EXE"

# Linear Executable module type

LEModuleType = construct.BitStruct("LEModuleType",
    construct.Padding(2),
    # Only for DLL
    construct.FlagsEnum(construct.BitField("Initialization", 1),
        GLOBAL          = 0x00,
        PER_PROCESS     = 0x01,
    ),
    construct.Padding(1),
    construct.Flag("No_internal_fixup_in_exe_image"),
    construct.Flag("No_external_fixup_in_exe_image"),
    construct.Padding(2),
    construct.FlagsEnum(construct.BitField("Comp", 3),
        UNKNOW          = 0x00,
        INCOMPATIBLE    = 0x01,
        COMPATIBLE      = 0x02,
        PM_WINDOWING    = 0x03
    ),
    construct.Padding(2),
    construct.Flag("Module_not_loadable"),
    construct.Padding(1),
    construct.Flag("Module_DLL"),
    construct.Padding(16),
)

# Object flags

ObjectFlags = construct.BitStruct("ObjectFlags",
    construct.Flag("Readable"),
    construct.Flag("Writable"),
    construct.Flag("Executable"),
    construct.Flag("Resource"),
    construct.Flag("Discardable"),
    construct.Flag("Shared"),
    construct.Flag("Preloaded"),
    construct.Flag("Invalid"),
    construct.FlagsEnum(construct.BitField("Type", 2),
        NORMAL              = 0x00,
        ZERO_FILLED         = 0x01,
        RESIDENT            = 0x02,
        RESIDENT_CONTIGUOUS = 0x03,
    ),
    construct.Flag("RESIDENT_LONG_LOCABLE"),
    construct.Padding(1),
    construct.Flag("16_ALIAS"),
    construct.Flag("BIG"),
    construct.Flag("Conforming"),
    construct.Flag("Object_i/o_privilage_level"),
    construct.Padding(16),
)

# Object table entry

ObjectHeader = construct.Struct("ObjectHeader",
    construct.ULInt32("Virtual_size"),                          # + 0x00
    construct.ULInt32("Relocation_base"),                       # + 0x04
    ObjectFlags,                                                # + 0x08
    construct.ULInt32("Page_map_index"),                        # + 0x0C
    construct.ULInt32("Page_map_entries"),                      # + 0x10
    construct.Padding(0x04),                                    # + 0x14
)

# Object page map table entry

ObjectPageMapHeader = construct.Struct("ObjectPageMapHeader",
    construct.ULInt8("unk_byte_00"),                            # + 0x00
    construct.ULInt16("Index"),                                 # + 0x01
    construct.ULInt8("Type"),                                   # + 0x03
)

# Header resident name table

ResidentNameHeader = construct.Struct("ResidentNameHeader",
    construct.UBInt8("Size"),                                   # + 0x00
    construct.Bytes("String", lambda ctx: ctx.Size),            # + 0x01
    construct.ULInt16("Index"),                                 # + 0xXX
)

LEHeader = construct.Struct("LEHeader",
    construct.Anchor("start_LEHeader"),
    construct.Magic("LE"),                                      # + 0x00
    construct.ULInt8("Byte_order"),                             # + 0x02
    construct.ULInt8("Word_order"),                             # + 0x03
    construct.ULInt32("Format_level"),                          # + 0x04
    construct.Enum(construct.ULInt16("CPU_type"),               # + 0x08
        INTEL_80286     = 0x01,
        INTEL_80386     = 0x02,
        INTEL_80486     = 0x03,
        INTEL_80586     = 0x04,
        INTEL_i860      = 0x20,
        INTEL_N11       = 0x21,
        MIPS_MARK_I     = 0x40,
        MIPS_MARK_II    = 0x41,
        MIPS_MARK_III   = 0x42,
    ),
    construct.Enum(construct.ULInt16("Target_os"),              # + 0x0A
        OS_2            = 0x01,
        WINDOWS         = 0x02,
        EUROPEAN_DOS_4  = 0x03,
        WINDOWS_386     = 0x04,
    ),
    construct.ULInt32("Module_version"),                        # + 0x0C
    LEModuleType,                                               # + 0x10
    construct.ULInt32("Nb_memory_pages"),                       # + 0x14
    construct.ULInt32("Initial_CS"),                            # + 0x18
    construct.ULInt32("Initial_EIP"),                           # + 0x1C
    construct.ULInt32("Initial_SS"),                            # + 0x20
    construct.ULInt32("Initial_ESP"),                           # + 0x24
    construct.ULInt32("Memory_page_size"),                      # + 0x28
    construct.ULInt32("Bytes_last_page"),                       # + 0x2C
    construct.ULInt32("Fixup_section_size"),                    # + 0x30
    construct.ULInt32("Fixup_section_checksum"),                # + 0x34
    construct.ULInt32("Loader_section_size"),                   # + 0x38
    construct.ULInt32("Loader_section_checksum"),               # + 0x3C
    construct.ULInt32("Object_table_offset"),                   # + 0x40
    construct.ULInt32("Nb_object_entries"),                     # + 0x44
    construct.ULInt32("Object_page_map_offset"),                # + 0x48
    construct.ULInt32("Object_iterate_data_map_offset"),        # + 0x4C
    construct.ULInt32("Resource_table_offset"),                 # + 0x50
    construct.ULInt32("Resource_table_entries"),                # + 0x54
    construct.ULInt32("Resident_names_table_offset"),           # + 0x58
    construct.ULInt32("Entry_table_offset"),                    # + 0x5C
    construct.ULInt32("Module_directives_table_offset"),        # + 0x60
    construct.ULInt32("Module_directives_entries"),             # + 0x64
    construct.ULInt32("Fixup_page_table_offset"),               # + 0x68
    construct.ULInt32("Fixup_record_table_offset"),             # + 0x6C
    construct.ULInt32("Imported_modules_name_table_offset"),    # + 0x70
    construct.ULInt32("Imported_modules_count"),                # + 0x74
    construct.ULInt32("Imported_procedures_name_table_offset"), # + 0x78
    construct.ULInt32("PerPage_checksum_table_offset"),         # + 0x7C
    construct.ULInt32("Data_pages_offset"),                     # + 0x80
    construct.ULInt32("Preload_page_count"),                    # + 0x84
    construct.ULInt32("Non_resident_names_table_offset"),       # + 0x88
    construct.ULInt32("Non_resident_names_table_length"),       # + 0x8C
    construct.ULInt32("Non_resident_names_checksum"),           # + 0x90
    construct.ULInt32("Automatic_data_object"),                 # + 0x94
    construct.ULInt32("Debug_information_offset"),              # + 0x98
    construct.ULInt32("Debug_information_length"),              # + 0x9C
    construct.ULInt32("Preload_instance_pages_number"),         # + 0xA0
    construct.ULInt32("Demand_instance_pages_number"),          # + 0xA4
    construct.ULInt32("Extra_heap_information"),                # + 0xA8
    construct.Padding(0x0C),                                    # + 0xAC
    construct.ULInt32("Offset_versioninfo_resource"),           # + 0xB8
    construct.ULInt32("unk_dword_00"),                          # + 0xBC
    construct.ULInt16("Device_id"),                             # + 0xC0
    construct.ULInt16("DDK_version"),                           # + 0xC2

    # Object table
    construct.OnDemandPointer(lambda ctx: ctx.start_LEHeader + ctx.Object_table_offset,
        construct.Array(lambda ctx: ctx.Nb_object_entries, ObjectHeader)
    ),

    # Object page map table
    construct.OnDemandPointer(lambda ctx: ctx.start_LEHeader + ctx.Object_page_map_offset,
        construct.Array(lambda ctx: ctx.Nb_memory_pages, ObjectPageMapHeader)
    ),

    # Resident-Name Table
    construct.OnDemandPointer(lambda ctx: ctx.start_LEHeader + ctx.Resident_names_table_offset,
        construct.RepeatUntil(lambda obj, ctx: obj.Size == 0x00, ResidentNameHeader)
    ),

    # Fixup Page Table
    construct.OnDemandPointer(lambda ctx: ctx.start_LEHeader + ctx.Fixup_page_table_offset,
        construct.Array(lambda ctx: ctx.Nb_memory_pages + 1, construct.ULInt32("Offset_fixup"))
    ),

)

# MS-DOS header

MZHeader = construct.Struct("MZHeader",
    construct.Anchor("start_MZHeader"),
    construct.Magic("MZ"),                                      # + 0x00
    construct.ULInt16("Extra_Bytes"),                           # + 0x02
    construct.ULInt16("Pages"),                                 # + 0x04
    construct.ULInt16("Relocation_items"),                      # + 0x06
    construct.ULInt16("Header_size"),                           # + 0x08
    construct.ULInt16("Min_allocation"),                        # + 0x0A
    construct.ULInt16("Max_allocation"),                        # + 0x0C
    construct.ULInt16("Initial_SS"),                            # + 0x0E
    construct.ULInt16("Initial_SP"),                            # + 0x10
    construct.ULInt16("Checksum"),                              # + 0x12
    construct.ULInt16("Initial_IP"),                            # + 0x14
    construct.ULInt16("Initial_CS"),                            # + 0x16
    construct.ULInt16("Relocation_table"),                      # + 0x18
    construct.ULInt16("Overlay_number"),                        # + 0x1A
    construct.Array(0x04, construct.ULInt8("UNK")),             # + 0x1C
    construct.Padding(0x1C),                                    # + 0x20
    construct.ULInt32("LE_header_offset"),                      # + 0x3C

    # LE Header
    construct.If(lambda ctx: ctx["Relocation_table"] >= 0x40,
        construct.Pointer(lambda ctx: ctx.start_MZHeader + ctx.LE_header_offset,
            LEHeader,
        ),
    ),
)

fd = open(FILENAME, "rb")
buf = fd.read()
hs = MZHeader.parse(buf)
if hs["Relocation_table"] < 0x40:
    raise ValueError("[-] Not linear executable")
les = hs["LEHeader"]
print les
print les["ObjectHeader"].read()
