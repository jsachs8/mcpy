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
import nbt


class HSAType(Enum):
    FORTRESS = 1
    SWAMPHUT = 2
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
        if self.type in (HSAType.SWAMPHUT, HSAType.OUTPOST):
            offset = -3
        else:
            offset = 0
        xmid = (self.pos1[0] + self.pos2[0] + 1) // 2
        zmid = (self.pos1[2] + self.pos2[2] + 1) // 2
        ymin = self.pos1[1]
        ymax = self.pos2[1] + offset

        return f"x={xmid} y={ymin}:{ymax} z={zmid}"

    def __str__(self):
        return f"{self.type.name} {self.pos1}->{self.pos2} hss @ {self.spot()}"

