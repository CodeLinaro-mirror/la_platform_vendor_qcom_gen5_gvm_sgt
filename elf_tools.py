# Copyright (c) 2015, The Linux Foundation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
#  with the distribution.
#    * Neither the name of The Linux Foundation nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#Changes from Qualcomm Technologies, Inc. are provided under the following license:
#Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. 
#SPDX-License-Identifier: BSD-3-Clause-Clear

import struct
import os
import sys

# Byteorder
BO = "little"

# ELF Definitions
ELF_HDR_COMMON_SIZE = 24
ELF32_HDR_SIZE = 52
ELF32_PHDR_SIZE = 32
ELF64_HDR_SIZE = 64
ELF64_PHDR_SIZE = 56
ELFINFO_MAG0_INDEX = 0
ELFINFO_MAG1_INDEX = 1
ELFINFO_MAG2_INDEX = 2
ELFINFO_MAG3_INDEX = 3
ELFINFO_MAG0 = (0x7F).to_bytes(1, BO)
ELFINFO_MAG1 = b"E"
ELFINFO_MAG2 = b"L"
ELFINFO_MAG3 = b"F"
ELFINFO_CLASS_INDEX = 4
ELFINFO_CLASS_32 = (0x01).to_bytes(1, BO)
ELFINFO_CLASS_64 = (0x02).to_bytes(1, BO)
ELFINFO_VERSION_INDEX = 6
ELFINFO_VERSION_CURRENT = (0x01).to_bytes(1, BO)
ELF_BLOCK_ALIGN = 0x1000
ALIGNVALUE_1MB = 0x100000
ALIGNVALUE_2MB = 0x200000
ALIGNVALUE_4MB = 0x400000
ELFINFO_DATA2LSB = (0x01).to_bytes(1, BO)
ELFINFO_EXEC_ETYPE = (0x02).to_bytes(2, BO)
ELFINFO_ARM_MACHINETYPE = (0x28).to_bytes(2, BO)
ELFINFO_VERSION_EV_CURRENT = (0x01).to_bytes(4, BO)
ELFINFO_SHOFF = 0x00
ELFINFO_PHNUM = (0x01).to_bytes(2, BO)
ELFINFO_RESERVED = 0x00

# ELF Program Header Types
NULL_TYPE = 0x0
LOAD_TYPE = 0x1
DYNAMIC_TYPE = 0x2
INTERP_TYPE = 0x3
NOTE_TYPE = 0x4
SHLIB_TYPE = 0x5
PHDR_TYPE = 0x6
TLS_TYPE = 0x7

# Access Type
MI_PBT_RW_SEGMENT = 0x0
MI_PBT_RO_SEGMENT = 0x1
MI_PBT_ZI_SEGMENT = 0x2
MI_PBT_NOTUSED_SEGMENT = 0x3
MI_PBT_SHARED_SEGMENT = 0x4
MI_PBT_RWE_SEGMENT = 0x08000007

# ----------------------------------------------------------------------------
# GLOBAL VARIABLES END
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# CLASS DEFINITIONS BEGIN
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# OS Type ID Class
# ----------------------------------------------------------------------------
class OSType:
    ANDROID_BOOT_OS = 2
    LINUX_BOOT_OS = 5


# ----------------------------------------------------------------------------
# Image Type ID Class - These values must be kept consistent with mibib.h
# ----------------------------------------------------------------------------
class ImageType:
    NONE_IMG = 0
    APPSBL_IMG = 5


# ----------------------------------------------------------------------------
# Header Class Notes:
# In order to properly read and write the header structures as binary data,
# the Python Struct library is used to align and package up the header objects
# All Struct objects are initialized by a special string with the following
# notation. These structure objects are then used to decode binary data in order
# to fill out the appropriate class in Python, or they are used to package up
# the Python class so that we may write the binary data out.
# ----------------------------------------------------------------------------
"""
        Format | C Type            | Python Type | Standard Size
        -----------------------------------------------------
     1) 'X's  | char *            | string        | 'X' bytes
     2) H      | unsigned short | integer      | 2 bytes
     3) I      | unsigned int    | integer      | 4 bytes

"""

# ----------------------------------------------------------------------------
# ELF Header Class
# ----------------------------------------------------------------------------
class Elf_Ehdr_common:
    # Structure object to align and package the ELF Header
    s = struct.Struct("16sHHI")

    def __init__(self, data):
        unpacked_data = (Elf_Ehdr_common.s).unpack(data)
        self.unpacked_data = unpacked_data
        self.e_ident = unpacked_data[0]
        self.e_type = unpacked_data[1]
        self.e_machine = unpacked_data[2]
        self.e_version = unpacked_data[3]

    def printValues(self):
        print("ATTRIBUTE / VALUE")
        for attr, value in self.__dict__.items():
            print(attr, value)


# ----------------------------------------------------------------------------
# ELF Header Class
# ----------------------------------------------------------------------------
class Elf32_Ehdr:
    # Structure object to align and package the ELF Header
    s = struct.Struct("16sHHIIIIIHHHHHH")

    def __init__(self, data):
        unpacked_data = (Elf32_Ehdr.s).unpack(data)
        self.unpacked_data = unpacked_data
        self.e_ident = unpacked_data[0]
        self.e_type = unpacked_data[1]
        self.e_machine = unpacked_data[2]
        self.e_version = unpacked_data[3]
        self.e_entry = unpacked_data[4]
        self.e_phoff = unpacked_data[5]
        self.e_shoff = unpacked_data[6]
        self.e_flags = unpacked_data[7]
        self.e_ehsize = unpacked_data[8]
        self.e_phentsize = unpacked_data[9]
        self.e_phnum = unpacked_data[10]
        self.e_shentsize = unpacked_data[11]
        self.e_shnum = unpacked_data[12]
        self.e_shstrndx = unpacked_data[13]

    def printValues(self):
        print("ATTRIBUTE / VALUE")
        for attr, value in self.__dict__.items():
            print(attr, value)

    def getPackedData(self):
        values = [
            self.e_ident,
            self.e_type,
            self.e_machine,
            self.e_version,
            self.e_entry,
            self.e_phoff,
            self.e_shoff,
            self.e_flags,
            self.e_ehsize,
            self.e_phentsize,
            self.e_phnum,
            self.e_shentsize,
            self.e_shnum,
            self.e_shstrndx,
        ]

        return (Elf32_Ehdr.s).pack(*values)


# ----------------------------------------------------------------------------
# ELF Program Header Class
# ----------------------------------------------------------------------------
class Elf32_Phdr:

    # Structure object to align and package the ELF Program Header
    s = struct.Struct("I" * 8)

    def __init__(self, data):
        unpacked_data = (Elf32_Phdr.s).unpack(data)
        self.unpacked_data = unpacked_data
        self.p_type = unpacked_data[0]
        self.p_offset = unpacked_data[1]
        self.p_vaddr = unpacked_data[2]
        self.p_paddr = unpacked_data[3]
        self.p_filesz = unpacked_data[4]
        self.p_memsz = unpacked_data[5]
        self.p_flags = unpacked_data[6]
        self.p_align = unpacked_data[7]

    def printValues(self):
        print("ATTRIBUTE / VALUE")
        for attr, value in self.__dict__.items():
            print(attr, value)

    def getPackedData(self):
        values = [
            self.p_type,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_flags,
            self.p_align,
        ]

        return (Elf32_Phdr.s).pack(*values)


# ----------------------------------------------------------------------------
# ELF Header Class
# ----------------------------------------------------------------------------
class Elf64_Ehdr:
    # Structure object to align and package the ELF Header
    s = struct.Struct("16sHHIQQQIHHHHHH")

    def __init__(self, data):
        unpacked_data = (Elf64_Ehdr.s).unpack(data)
        self.unpacked_data = unpacked_data
        self.e_ident = unpacked_data[0]
        self.e_type = unpacked_data[1]
        self.e_machine = unpacked_data[2]
        self.e_version = unpacked_data[3]
        self.e_entry = unpacked_data[4]
        self.e_phoff = unpacked_data[5]
        self.e_shoff = unpacked_data[6]
        self.e_flags = unpacked_data[7]
        self.e_ehsize = unpacked_data[8]
        self.e_phentsize = unpacked_data[9]
        self.e_phnum = unpacked_data[10]
        self.e_shentsize = unpacked_data[11]
        self.e_shnum = unpacked_data[12]
        self.e_shstrndx = unpacked_data[13]

    def printValues(self):
        print("ATTRIBUTE / VALUE")
        for attr, value in self.__dict__.items():
            print(attr, value)

    def getPackedData(self):
        values = [
            self.e_ident,
            self.e_type,
            self.e_machine,
            self.e_version,
            self.e_entry,
            self.e_phoff,
            self.e_shoff,
            self.e_flags,
            self.e_ehsize,
            self.e_phentsize,
            self.e_phnum,
            self.e_shentsize,
            self.e_shnum,
            self.e_shstrndx,
        ]

        return (Elf64_Ehdr.s).pack(*values)


# ----------------------------------------------------------------------------
# ELF Program Header Class
# ----------------------------------------------------------------------------
class Elf64_Phdr:

    # Structure object to align and package the ELF Program Header
    s = struct.Struct("IIQQQQQQ")

    def __init__(self, data):
        unpacked_data = (Elf64_Phdr.s).unpack(data)
        self.unpacked_data = unpacked_data
        self.p_type = unpacked_data[0]
        self.p_flags = unpacked_data[1]
        self.p_offset = unpacked_data[2]
        self.p_vaddr = unpacked_data[3]
        self.p_paddr = unpacked_data[4]
        self.p_filesz = unpacked_data[5]
        self.p_memsz = unpacked_data[6]
        self.p_align = unpacked_data[7]

    def printValues(self):
        print("ATTRIBUTE / VALUE")
        for attr, value in self.__dict__.items():
            print(attr, value)

    def getPackedData(self):
        values = [
            self.p_type,
            self.p_flags,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_align,
        ]

        return (Elf64_Phdr.s).pack(*values)


# ----------------------------------------------------------------------------
# ELF Segment Information Class
# ----------------------------------------------------------------------------
class SegmentInfo:
    def __init__(self):
        self.flag = 0

    def printValues(self):
        print("Flag: " + str(self.flag))


# ----------------------------------------------------------------------------
# CLASS DEFINITIONS END
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# HELPER FUNCTIONS BEGIN
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Concatenates the files listed in 'sources' in order, writing to 'target'
# Overwrites 'target' if it exists
# ----------------------------------------------------------------------------
def concat_files(target, sources, input, offsets):
    i = 0
    if type(sources) is not list:
        sources = [sources]
    with open(target, "wb") as target_file:
        for fname in sources:
            with open(fname, "rb") as fl:
                while True:
                    bin_data = fl.read(65536)
                    if not bin_data:
                        break
                    target_file.write(bin_data)
        for fname in input:
            target_file.seek(offsets[i])
            i = i + 1
            with open(fname, "rb") as fl:
                while True:
                    bin_data = fl.read(65536)
                    if not bin_data:
                        break
                    target_file.write(bin_data)


# ----------------------------------------------------------------------------
# Basic verifications of file and header. Returns True if file is ok
# ----------------------------------------------------------------------------
def verify_elf(filename):
    clean = True
    with open(filename, "rb") as elf:
        elf_hdr = Elf_Ehdr_common(elf.read(ELF_HDR_COMMON_SIZE))
        elf_hdr.printValues()
        elf.seek(0)
        if elf_hdr.e_ident[ELFINFO_CLASS_INDEX] == int.from_bytes(ELFINFO_CLASS_64, BO):
            elf_hdr = Elf64_Ehdr(elf.read(ELF64_HDR_SIZE))
        elif elf_hdr.e_ident[ELFINFO_CLASS_INDEX] == int.from_bytes(
            ELFINFO_CLASS_32, BO
        ):
            elf_hdr = Elf32_Ehdr(elf.read(ELF32_HDR_SIZE))
        else:
            clean = False
            print("Error: File is neither 32- or 64-bit ELF (assuming 32)")
            sys.exit(-1)

        # (start, end) of occupied space
        pr_hdrs_span = (
            elf_hdr.e_phoff,
            elf_hdr.e_phoff + elf_hdr.e_phentsize * elf_hdr.e_phnum,
        )
        elf_hdr_span = (0, elf_hdr.e_ehsize)
        all_hdr_span = (0, max(elf_hdr_span[1], pr_hdrs_span[1]))
        # ELF header verifications
        filelen = os.stat(filename).st_size

        if pr_hdrs_span[0] < elf_hdr_span[1]:  # prog hdrs overlap elf hdr
            clean = False
            print(
                "Warning: Program Headers overlap ELF Header (0x{:X}".format(
                    pr_hdrs_span[0]
                )
            )

        if elf_hdr.e_entry % ALIGNVALUE_2MB:
            print(
                "Warning: ELF e_entry not 2 MB aligned (0x{:X}".format(elf_hdr.e_entry)
            )
            clean = False

        if elf_hdr.e_phoff > filelen:
            clean = False
            print("Warning: ELF e_phoff outside file (0x{:X})".format(elf_hdr.e_phoff))

        phdrs = []
        elf.seek(elf_hdr.e_phoff)
        for i in range(elf_hdr.e_phnum):
            if elf_hdr.e_ident[ELFINFO_CLASS_INDEX] == ELFINFO_CLASS_64:
                phdrs.append(Elf64_Phdr(elf.read(elf_hdr.e_phentsize)))
            else:
                phdrs.append(Elf32_Phdr(elf.read(elf_hdr.e_phentsize)))

            if phdrs[-1].p_offset < all_hdr_span[1] or phdrs[-1].p_offset > filelen:
                clean = False
                print(
                    "Warning: Program Header file segment outside file or within headers ({:X})".format(
                        phdrs[-1].p_offset
                    )
                )
        elf_e_entry_in_file = False
        for ph in phdrs:
            if elf_hdr.e_entry >= ph.p_paddr and elf_hdr.e_entry < (
                ph.p_paddr + ph.p_filesz
            ):
                elf_e_entry_in_file = True
            for ph_ in phdrs:
                if ph == ph_:
                    continue
                if (
                    ph.p_offset < ph_.p_offset
                    and (ph.p_offset + ph.p_filesz) > ph_.p_offset
                ):
                    print("Warning: Program Header Images overlap each other")
                    print(
                        "ph: 0x{:X} to 0x{:X}".format(
                            ph.p_offset, (ph.p_offset + ph.p_filesz)
                        )
                    )
                    print(
                        "ph: 0x{:X} to 0x{:X}".format(
                            ph_.p_offset, (ph_.p_offset + ph_.p_filesz)
                        )
                    )
                    clean = False
        if not elf_e_entry_in_file:
            print("Warning: ELF e_entry outside file (0x{:X})".format(elf_hdr.e_entry))
            clean = False
    return clean


# ----------------------------------------------------------------------------
# Write ELF Header
# ----------------------------------------------------------------------------
def create_elf_header(filename, entry, phnum, class_64=True):
    if class_64:
        addrlen = 8
        cls = ELFINFO_CLASS_64
        hd_sz = ELF64_HDR_SIZE
        ph_sz = ELF64_PHDR_SIZE
    else:
        addrlen = 4
        cls = ELFINFO_CLASS_32
        hd_sz = ELF32_HDR_SIZE
        ph_sz = ELF32_PHDR_SIZE

    with open(filename, "wb") as elf_hd:
        elf_hd.write(ELFINFO_MAG0)  # 7f
        elf_hd.write(ELFINFO_MAG1)  # E
        elf_hd.write(ELFINFO_MAG2)  # L
        elf_hd.write(ELFINFO_MAG3)  # F
        elf_hd.write(cls)  # class (32/64)
        elf_hd.write(ELFINFO_DATA2LSB)  # data  (b/l endian)
        elf_hd.write(ELFINFO_VERSION_CURRENT)  # version (ELF)
        elf_hd.write(
            (chr(ELFINFO_RESERVED) * 9).encode()
        )  # OSABI, ABIVERSION, EI_PAD (all 0x0)
        elf_hd.write(ELFINFO_EXEC_ETYPE)  # TYPE
        elf_hd.write(ELFINFO_ARM_MACHINETYPE)  # MACHINE
        elf_hd.write(ELFINFO_VERSION_EV_CURRENT)  # e_version (usu. 1)
        elf_hd.write(entry.to_bytes(addrlen, BO))  # entry
        elf_hd.write(hd_sz.to_bytes(addrlen, BO))  # phoff
        elf_hd.write(ELFINFO_SHOFF.to_bytes(addrlen, BO))  # shoff
        elf_hd.write((chr(ELFINFO_RESERVED) * 4).encode())  # flags (0)
        elf_hd.write(hd_sz.to_bytes(2, BO))  # eh_size
        elf_hd.write(ph_sz.to_bytes(2, BO))  # ph_size
        elf_hd.write(phnum.to_bytes(2, BO))  # phnum
        elf_hd.write((chr(ELFINFO_RESERVED) * 6).encode())  # shentsize, shnum, shstrndx


# ----------------------------------------------------------------------------
# Write one Program Header
# ----------------------------------------------------------------------------
def create_prog_header(filename, offset_img, offset_mem, imglen, class_64=True):
    if class_64:
        addrlen = 8
    else:
        addrlen = 4

    with open(filename, "wb") as pg_hd:
        pg_hd.write(LOAD_TYPE.to_bytes(4, BO))  # type
        if class_64:
            pg_hd.write(MI_PBT_RWE_SEGMENT.to_bytes(4, BO))  # flags (64)
        pg_hd.write(offset_img.to_bytes(addrlen, BO))  # offset
        pg_hd.write(offset_mem.to_bytes(addrlen, BO))  # vaddr (virt addr)
        pg_hd.write(offset_mem.to_bytes(addrlen, BO))  # paddr (phys addr)
        pg_hd.write(imglen.to_bytes(addrlen, BO))  # filesz
        pg_hd.write(imglen.to_bytes(addrlen, BO))  # memsz
        if not class_64:
            pg_hd.write(MI_PBT_RWE_SEGMENT.to_bytes(4, BO))  # flags (32)
        pg_hd.write(ELF_BLOCK_ALIGN.to_bytes(addrlen, BO))  # align


# ----------------------------------------------------------------------------
# Co-ordinates writing headers
# input_imgs is a list of [filename, address]: [str, int]
# ELF e_entry is set to the smallest address in the list (should be specified by user?)
# ----------------------------------------------------------------------------
def create_elf(out_img, input_imgs, class_64=True):
    offsets_imgs = []
    input_imgs.sort(key=lambda img: img[1])  # list of (filename,address pairs)
    if class_64:
        all_headers = ELF64_HDR_SIZE + ELF64_PHDR_SIZE * len(input_imgs)
    else:
        all_headers = ELF32_HDR_SIZE + ELF32_PHDR_SIZE * len(input_imgs)
    cat_files = [out_img + ".elf-hd"]
    create_elf_header(
        out_img + ".elf-hd", int(eval(input_imgs[0][1])), len(input_imgs), class_64
    )
    offset_img = (all_headers + ELF_BLOCK_ALIGN - 1) & -ELF_BLOCK_ALIGN
    offsets_imgs.append(offset_img)
    print("offset: {0:x}".format(offset_img))

    for img in input_imgs:
        create_prog_header(
            img[0] + ".prg-hd",
            offset_img,
            int(eval(img[1])),
            os.stat(img[0]).st_size,
            class_64,
        )
        cat_files.append(img[0] + ".prg-hd")
        offset_img += os.stat(img[0]).st_size
        offset_img = (offset_img + ELF_BLOCK_ALIGN - 1) & -ELF_BLOCK_ALIGN
        offsets_imgs.append(offset_img)
        print("offset: {0:x}".format(offset_img))

    concat_files(out_img, cat_files, [img[0] for img in input_imgs], offsets_imgs)


# ----------------------------------------------------------------------------
# HELPER FUNCTIONS END
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    print("This file is only intended to be imported by `image_header.py`")
