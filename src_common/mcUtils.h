/*******************************************************************************
*   Ledger Ethereum App
*   (c) 2016-2019 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************/

#ifndef _MCUTILS_H_
#define _MCUTILS_H_

#include <stdint.h>

#include "cx.h"

bool rlpDecodeLength(uint8_t *buffer, uint32_t bufferLength,
                     uint32_t *fieldLength, uint32_t *offset, bool *list);

bool rlpCanDecode(uint8_t *buffer, uint32_t bufferLength, bool *valid);


void getMcAddressFromKey(cx_ecfp_public_key_t *publicKey, uint8_t *out,
                                cx_sha3_t *sha3Context);

void getMcAddressStringFromKey(cx_ecfp_public_key_t *publicKey, uint8_t *out,
                                cx_sha3_t *sha3Context);

void getMcAddressStringFromBinary(uint8_t *address, uint8_t *out,
                                   cx_sha3_t *sha3Context);

bool adjustDecimals(char *src, uint32_t srcLength, char *target,
                    uint32_t targetLength, uint8_t decimals);

#endif /* _MCUTILS_H_ */