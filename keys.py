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
