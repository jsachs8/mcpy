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
import struct


class KeyType(Enum):
    Data3D = 43             # TODO: what is the format
    Version = 44            # byte
    Data2D = 45             # TODO: what is the format
    BlockStorage = 47       # see blockdata.py
    TileEntities = 49       # count followed by NBT objects
    Entities = 50           # sequence of NBT objects
    PendingBlockTicks = 51  # NBT
    BiomeStates = 53        # TODO: what is the format
    Finalization = 54       # int32
    HardCodedSpawnAreas = 57  # see hsa.py
    RandomBlockTicks = 58   # NBT
    OldGeneration = 61      # byte


def is_hsa(k):
    if len(k) == 9 and k[8] == KeyType.HardCodedSpawnAreas.value:
        return True
    if len(k) == 13 and k[12] == KeyType.HardCodedSpawnAreas.value:
        return True
    return False


def is_tile_entities(k):
    if len(k) == 9 and k[8] == KeyType.TileEntities.value:
        return True
    if len(k) == 13 and k[12] == KeyType.TileEntities.value:
        return True
    return False


def is_block_storage(k):
    if len(k) == 10 and k[8] == KeyType.BlockStorage.value:
        return True
    if len(k) == 14 and k[12] == KeyType.BlockStorage.value:
        return True
    return False


def is_version(k):
    if len(k) == 9 and k[8] == KeyType.Version.value:
        return True
    if len(k) == 13 and k[12] == KeyType.Version.value:
        return True
    return False


def is_finalization(k):
    if len(k) == 9 and k[8] == KeyType.Finalization.value:
        return True
    if len(k) == 13 and k[12] == KeyType.Finalization.value:
        return True
    return False


def is_legacy_generation(k):
    if len(k) == 9 and k[8] == KeyType.OldGeneration.value:
        return True
    if len(k) == 13 and k[12] == KeyType.OldGeneration.value:
        return True
    return False


def is_entities(k):
    if len(k) == 9 and k[8] == KeyType.Entities.value:
        return True
    if len(k) == 13 and k[12] == KeyType.Entities.value:
        return True
    return False


def is_pending_block_ticks(k):
    if len(k) == 9 and k[8] == KeyType.PendingBlockTicks.value:
        return True
    if len(k) == 13 and k[12] == KeyType.PendingBlockTicks.value:
        return True
    return False


def is_random_block_ticks(k):
    if len(k) == 9 and k[8] == KeyType.RandomBlockTicks.value:
        return True
    if len(k) == 13 and k[12] == KeyType.RandomBlockTicks.value:
        return True
    return False


def is_data_3d(k):
    if len(k) == 9 and k[8] == KeyType.Data3D.value:
        return True
    if len(k) == 13 and k[12] == KeyType.Data3D.value:
        return True
    return False


def is_map(k):
    if k.startswith(b"map_"):
        return True
    return False


def is_biome_states(k):
    if len(k) == 9 and k[8] == KeyType.BiomeStates.value:
        return True
    if len(k) == 13 and k[12] == KeyType.BiomeStates.value:
        return True
    return False


def data3d_key(x, z, dim=0):
    xc = x // 16
    zc = z // 16
    if dim == 0:
        # print(f"chunk {xc}, {zc}")
        return struct.pack("<iib", xc, zc, 43)
    else:
        return struct.pack("<iiib", xc, zc, dim, 43)
