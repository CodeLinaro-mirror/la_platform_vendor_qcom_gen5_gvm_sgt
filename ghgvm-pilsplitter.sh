
#!/bin/sh
# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear
###############################################################################################
# This is the script to generate split PIL bins for Gunyah hypervisor                         #
# Need to run this script from the device/qcom/gen5_gvm_sgt directory                             #
# Before running this script full android build should be done and below directory is present #
# device/qcom/msmnile-kernel with dtbs and Image present in the directory                     #
###############################################################################################
PWD=`pwd`;
#echo "$PWD"
PIL_PATH="$PWD"
#echo "$PIL_PATH"
ROOT_DIR="$PWD/../../../"
#echo "$ROOT_DIR"
MKDTBOIMGPY_PATH=$ROOT_DIR/system/libufdt/utils/src
#echo "$MKDTBOIMGPY_PATH"
IMG_PATH="$PWD/../gen5-kernel"
RADIO_PATH="$PWD/radio"
#echo "$IMG_PATH"
cd $IMG_PATH
OUTPATH="$PWD/../../../out/target/product/gen5_gvm_sgt"
ABSQC_PATH="$ROOT_DIR/$QCPATH"
#echo "$OUTPATH"
if [[ -z "${QCPATH}" ]]; then
    echo "ERROR: QCPATH is empty and must be set for all vendor references."
    echo "Please set it by invoking the below command from the root directory."
    echo "source build/envsetup.sh"
    exit 1
fi
#echo "$ABSQC_PATH"
SECURITY_PROFILE_PATH="$ABSQC_PATH/securemsm/security_profiles"
cd $OUTPATH
# Create scratch folder to copy the images for creating split PIL images
if [ -d "$OUTPATH/scratch" ]
then
	rm -Rf scratch
fi
mkdir scratch
# Create dtb.img with DT table structure
# ref: https://source.android.com/docs/core/architecture/dto/partitions
DTB_FILE_LIST=$(find $IMG_PATH/dtbs -name "*.dtb" | sort)
if [ -z "${DTB_FILE_LIST}" ]; then
	echo "No *.dtb files found in $IMG_PATH/dtbs"
	exit 1
else
	echo "Creating the dtb.img"
	python3 $MKDTBOIMGPY_PATH/mkdtboimg.py create $OUTPATH/scratch/dtb.img $DTB_FILE_LIST
fi
cp $IMG_PATH/Image $OUTPATH/scratch/
cp $OUTPATH/ramdisk.img $OUTPATH/scratch/
cp $IMG_PATH/kernel-abl/abl-*/LinuxLoader.efi $OUTPATH/scratch/
cp $ABSQC_PATH/guest-bootloader/FVMAIN_COMPACT.Fv $OUTPATH/scratch/
cd $OUTPATH/scratch
python3 $PIL_PATH/image_header.py autogvm-boot.elf Image,0x0 \
	dtb.img,0x3000000 ramdisk.img,0x3100000 --32
python3 $PIL_PATH/image_header.py autogvm-bootloader.elf FVMAIN_COMPACT.Fv,0x0 \
	dtb.img,0x0FC00000 LinuxLoader.efi,0x10100000 --32
$ABSQC_PATH/sectools/Linux/sectools secure-image autogvm-boot.elf \
	--image-id GVM1 \
	--security-profile $SECURITY_PROFILE_PATH/nord_security_profile.xml \
	--sign --signing-mode TEST \
	--outfile autogvm_signed-boot.elf
$ABSQC_PATH/sectools/Linux/sectools secure-image autogvm-bootloader.elf \
	--image-id GVM1 \
	--security-profile $SECURITY_PROFILE_PATH/nord_security_profile.xml \
	--sign --signing-mode TEST \
	--outfile autogvm_signed-bootloader.elf
$ABSQC_PATH/sectools/Linux/sectools secure-image autogvm-boot.elf --inspect
$ABSQC_PATH/sectools/Linux/sectools secure-image autogvm-bootloader.elf --inspect
if [ -d "$OUTPATH/scratch/boot" -o -d "$OUTPATH/scratch/bootloader" ]
then
	rm -Rf boot bootloader
fi
mkdir boot bootloader
python3 $PIL_PATH/pil-splitter.py autogvm_signed-boot.elf boot/autoghgvm
python3 $PIL_PATH/pil-splitter.py autogvm_signed-bootloader.elf bootloader/autoghgvm
echo "Creating the vm-boot.img"
$ROOT_DIR/out/host/linux-x86/bin/mkuserimg_mke2fs $OUTPATH/scratch/boot \
	$OUTPATH/vm-boot.img ext4 / 70000000
echo "Creating the vm-bootloader.img"
$ROOT_DIR/out/host/linux-x86/bin/mkuserimg_mke2fs $OUTPATH/scratch/bootloader \
	$OUTPATH/vm-bootloader.img ext4 / 8388608 \
	--journal_size=0

# Ensure the target directory exists
if [ ! -d "$RADIO_PATH" ]; then
    mkdir -p "$RADIO_PATH"
fi

if [ ! -f "$OUTPATH/vm-bootloader.img" ]; then
    echo "ERROR: vm-bootloader.img not found at $OUTPATH"
    exit 1
fi

echo "Copying vm-bootloader.img to the radio folder"
cp -f "$OUTPATH/vm-bootloader.img" "$RADIO_PATH/" || {
    echo "ERROR: Failed to copy vm-bootloader.img to $RADIO_PATH"
    exit 1
}
