LOCAL_PATH := $(call my-dir)

#----------------------------------------------------------------------
# Radio image
# ----------------------------------------------------------------------
ifeq ($(ADD_RADIO_FILES), true)
radio_dir := $(LOCAL_PATH)/radio
RADIO_FILES := $(shell cd $(radio_dir) ; ls)
$(foreach f, $(RADIO_FILES), \
        $(call add-radio-file,radio/$(f)))
endif

# Include the base products AndroidBoard.mk
include device/qcom/gen5_gvm/AndroidBoard.mk
