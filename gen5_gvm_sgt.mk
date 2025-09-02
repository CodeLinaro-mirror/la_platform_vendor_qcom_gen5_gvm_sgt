# Inherit from the base product
TARGET_SINGLE_TREE := true
TARGET_BOARD_DERIVATIVE_SUFFIX:=_sgt

include device/qcom/gen5_gvm/gen5_gvm.mk

LOCAL_PATH := $(call my-dir)

PRODUCT_NAME := gen5_gvm_sgt
PRODUCT_DEVICE := gen5_gvm_sgt
PRODUCT_BRAND := qti
PRODUCT_MODEL := gen5_gvm_sgt for arm64
#KERNEL_MODULES_OUT := out/target/product/$(PRODUCT_DEVICE)/$(KERNEL_MODULES_INSTALL)/lib/modules