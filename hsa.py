from enum import Enum
import nbt


class HSAType(Enum):
    FORTRESS = 1
    WITCH_HUT = 2
    MONUMENT = 3
    OUTPOST = 5


class HSA:
    def __init__(self, type, pos1, pos2):
        self.type = type
        self.pos1 = pos1
        self.pos2 = pos2

    @staticmethod
    def decode(reader):
        x1 = reader.get4()
        y1 = reader.get4()
        z1 = reader.get4()
        pos1 = (x1, y1, z1)
        x2 = reader.get4()
        y2 = reader.get4()
        z2 = reader.get4()
        pos2 = (x2, y2, z2)
        type = HSAType(reader.get1())
        return HSA(type, pos1, pos2)

    def spot(self):
        if self.type in (HSAType.WITCH_HUT, HSAType.OUTPOST):
            offset = -3
        else:
            offset = 0
        xmid = (self.pos1[0] + self.pos2[0]) // 2
        zmid = (self.pos1[2] + self.pos2[2]) // 2
        ymin = self.pos1[1]
        ymax = self.pos2[1] + offset

        return f"x={xmid} y={ymin}:{ymax} z={zmid}"

    def __str__(self):
        return f"{self.type.name} {self.pos1}->{self.pos2} hss={self.spot()}"

