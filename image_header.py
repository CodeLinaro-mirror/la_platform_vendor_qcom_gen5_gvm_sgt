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

import sys
import elf_tools
import argparse

p = argparse.ArgumentParser(
    description="Packages a list of Binary Images into ELF Format"
)
p.add_argument("output", help="Output constructed ELF file")
p.add_argument(
    "images",
    type=lambda x: str.split(x, ","),
    nargs="+",
    help="List of <filename>,<img_dest>",
    metavar="input,destination",
)
p.add_argument(
    "--32", action="store_true", help="Indicates a 32-bit ELF. Default is 64-bit"
)
ap = p.parse_args()

elf_tools.create_elf(ap.output, ap.images, class_64=(not vars(ap)["32"]))
if not elf_tools.verify_elf(ap.output):
    sys.exit(1)
