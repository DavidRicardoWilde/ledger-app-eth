#*******************************************************************************
#   Ledger App
#   (c) 2017 Ledger
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#*******************************************************************************

ifeq ($(BOLOS_SDK),)
$(error Environment variable BOLOS_SDK is not set)
endif
include $(BOLOS_SDK)/Makefile.defines

DEFINES_LIB = USE_LIB_ETHEREUM
#DEFINES_LIB = USE_LIB_MOAC
APP_LOAD_PARAMS= --curve secp256k1 $(COMMON_LOAD_PARAMS)
# Allow the app to use path 45 for multi-sig (see BIP45).
APP_LOAD_PARAMS += --path "45'"

APPVERSION_M=1
APPVERSION_N=2
APPVERSION_P=3
APPVERSION=$(APPVERSION_M).$(APPVERSION_N).$(APPVERSION_P)
# APP_LOAD_FLAGS= --appFlags 0x240 --dep Ethereum:$(APPVERSION)
APP_LOAD_FLAGS= --appFlags 0x240 --dep Moac:$(APPVERSION)

ifeq ($(CHAIN),)
# CHAIN=ethereum
CHAIN=moac
endif

# ifeq ($(CHAIN),ethereum)
ifeq ($(CHAIN),moac)
# Lock the application on its standard path for 1.5. Please complain if non compliant
APP_LOAD_PARAMS += --path "44'/60'"
# DEFINES += CHAINID_UPCASE=\"ETHEREUM\" CHAINID_COINNAME=\"ETH\" CHAIN_KIND=CHAIN_KIND_ETHEREUM CHAIN_ID=0
DEFINES += CHAINID_UPCASE=\"MOAC\" CHAINID_COINNAME=\"MC\" CHAIN_KIND=CHAIN_KIND_MOAC CHAIN_ID=101
# APPNAME = "Ethereum"
APPNAME = "Moac"
DEFINES_LIB=
APP_LOAD_FLAGS=--appFlags 0xa40
else ifeq ($(CHAIN),ellaism)
APP_LOAD_PARAMS += --path "44'/163'"
DEFINES += CHAINID_UPCASE=\"ELLA\" CHAINID_COINNAME=\"ELLA\" CHAIN_KIND=CHAIN_KIND_ELLAISM CHAIN_ID=64
APPNAME = "Ellaism"
else ifeq ($(CHAIN),wanchain)
APP_LOAD_PARAMS += --path "44'/5718350'"
DEFINES += CHAINID_UPCASE=\"WAN\" CHAINID_COINNAME=\"WAN\" CHAIN_KIND=CHAIN_KIND_WANCHAIN CHAIN_ID=1
APPNAME = "Wanchain"
else
ifeq ($(filter clean,$(MAKECMDGOALS)),)
$(error Unsupported CHAIN - use moac, ellaism, wanchain)
endif
endif

APP_LOAD_PARAMS += $(APP_LOAD_FLAGS) --path "44'/1'"
DEFINES += $(DEFINES_LIB)

#prepare hsm generation
#需要增加相应的图标
ifeq ($(TARGET_NAME),TARGET_BLUE)
ICONNAME=blue_app_$(CHAIN).gif 
else
ifeq ($(TARGET_NAME), TARGET_NANOX)
ICONNAME=nanox_app_$(CHAIN).gif
else
ICONNAME=nanos_app_$(CHAIN).gif
endif
endif

################
# Default rule #
################
all: default

############
# Platform #
############

DEFINES   += OS_IO_SEPROXYHAL IO_SEPROXYHAL_BUFFER_SIZE_B=128
DEFINES   += HAVE_BAGL HAVE_SPRINTF
DEFINES   += HAVE_PRINTF PRINTF=screen_printf
# DEFINES += HAVE_SPRINTF HAVE_PRINTF PRINTF=screen_printf
DEFINES   += PRINTF\(...\)=
DEFINES   += HAVE_IO_USB HAVE_L4_USBLIB IO_USB_MAX_ENDPOINTS=6 IO_HID_EP_LENGTH=64 HAVE_USB_APDU
DEFINES   += LEDGER_MAJOR_VERSION=$(APPVERSION_M) LEDGER_MINOR_VERSION=$(APPVERSION_N) LEDGER_PATCH_VERSION=$(APPVERSION_P)

# U2F
DEFINES   += HAVE_U2F HAVE_IO_U2F
DEFINES   += U2F_PROXY_MAGIC=\"w0w\"
DEFINES   += USB_SEGMENT_SIZE=64
DEFINES   += BLE_SEGMENT_SIZE=32 #max MTU, min 20

WEBUSB_URL     = www.ledgerwallet.com
DEFINES       += HAVE_WEBUSB WEBUSB_URL_SIZE_B=$(shell echo -n $(WEBUSB_URL) | wc -c) WEBUSB_URL=$(shell echo -n $(WEBUSB_URL) | sed -e "s/./\\\'\0\\\',/g")

DEFINES   += UNUSED\(x\)=\(void\)x
DEFINES   += APPVERSION=\"$(APPVERSION)\"

DEFINES   += CX_COMPLIANCE_141

ifeq ($(TARGET_NAME),TARGET_NANOX)
DEFINES   += HAVE_BLE BLE_COMMAND_TIMEOUT_MS=2000
DEFINES   += HAVE_BLE_APDU # basic ledger apdu transport over BLE

DEFINES   += HAVE_GLO096 HAVE_UX_LEGACY
DEFINES   += HAVE_BAGL BAGL_WIDTH=128 BAGL_HEIGHT=64
DEFINES   += HAVE_BAGL_ELLIPSIS # long label truncation feature
DEFINES   += HAVE_BAGL_FONT_OPEN_SANS_REGULAR_11PX
DEFINES   += HAVE_BAGL_FONT_OPEN_SANS_EXTRABOLD_11PX
DEFINES   += HAVE_BAGL_FONT_OPEN_SANS_LIGHT_16PX
endif

ifneq ($(NOCONSENT),)
DEFINES   += NO_CONSENT
endif

DEFINES   += HAVE_TOKENS_LIST # Do not activate external ERC-20 support yet

##############
#  Compiler  #
##############
ifneq ($(BOLOS_ENV),)
$(info BOLOS_ENV=$(BOLOS_ENV))
CLANGPATH := $(BOLOS_ENV)/clang-arm-fropi/bin/
GCCPATH := $(BOLOS_ENV)/gcc-arm-none-eabi-5_3-2016q1/bin/
else
$(info BOLOS_ENV is not set: falling back to CLANGPATH and GCCPATH)
endif
ifeq ($(CLANGPATH),)
$(info CLANGPATH is not set: clang will be used from PATH)
endif
ifeq ($(GCCPATH),)
$(info GCCPATH is not set: arm-none-eabi-* will be used from PATH)
endif

CC       := $(CLANGPATH)clang

#CFLAGS   += -O0
CFLAGS   += -O3 -Os

AS     := $(GCCPATH)arm-none-eabi-gcc

LD       := $(GCCPATH)arm-none-eabi-gcc
LDFLAGS  += -O3 -Os
LDLIBS   += -lm -lgcc -lc

# import rules to compile glyphs(/pone)
include $(BOLOS_SDK)/Makefile.glyphs

### variables processed by the common makefile.rules of the SDK to grab source files and include dirs
APP_SOURCE_PATH  += src_common src
SDK_SOURCE_PATH  += lib_stusb lib_stusb_impl lib_u2f
ifeq ($(TARGET_NAME),TARGET_NANOX)
SDK_SOURCE_PATH  += lib_blewbxx lib_blewbxx_impl
SDK_SOURCE_PATH  += lib_ux
endif

load: all
	python -m ledgerblue.loadApp $(APP_LOAD_PARAMS)

delete:
	python -m ledgerblue.deleteApp $(COMMON_DELETE_PARAMS)

# import generic rules from the sdk
include $(BOLOS_SDK)/Makefile.rules

#add dependency on custom makefile filename
dep/%.d: %.c Makefile

listvariants:
	@echo VARIANTS CHAIN ethereum ethereum_classic expanse poa rsk rsk_testnet ubiq wanchain kusd pirl akroma atheios callisto ethersocial ether1 gochain musicoin ethergem mix ellaism reosc hpb tomochain tobalaba
:
