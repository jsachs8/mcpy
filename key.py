"""
Copyright (c) 2021 Joseph W. Sachs (joesachs.123@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from enum import Enum


class KeyType(Enum):
    Data3D = 43
    Version = 44
    Data2D = 45
    BlockStorage = 47
    BlockEntities = 49
    Entities = 50
    PendingBlockTicks = 51
    HardCodedSpawnAreas = 57


def is_hsa(k):
    if len(k) == 9 and k[8] == KeyType.HardCodedSpawnAreas.value:
        return True
    if len(k) == 13 and k[12] == KeyType.HardCodedSpawnAreas.value:
        return True
    return False


def is_block_entities(k):
    if len(k) == 9 and k[8] == KeyType.BlockEntities.value:
        return True
    if len(k) == 13 and k[12] == KeyType.BlockEntities.value:
        return True
    return False