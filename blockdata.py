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

import struct
import nbt


def key(x, y, z, dim=0):
    xc = x // 16
    yc = y // 16
    zc = z // 16
    if dim == 0:
        # print(f"chunk {xc}, {zc}")
        return struct.pack("<iibb", xc, zc, 47, yc)
    else:
        return struct.pack("<iiibb", xc, zc, dim, 47, yc)


def read_storage(reader):
    data = []
    flags = reader.get("B")
    if flags == 255:
        return
    bits_per_block = flags >> 1
    # print(f"bits per block = {bits_per_block}")
    if bits_per_block == 0:
        for i in range(4096):
            data.append(0)
        palette_count = 1
    else:
        blocks_per_word = 32 // bits_per_block
        num_words = (4096 + blocks_per_word - 1) // blocks_per_word
        mask = (1 << bits_per_block) - 1  # assume 2-s complement

        pos = 0
        for i in range(num_words):
            word = reader.get("<I")
            for _ in range(blocks_per_word):
                val = word & mask
                if pos == 4096:
                    break
                data.append(val)
                word = word >> bits_per_block
                pos += 1

        palette_count = reader.get("<I")

    # read the palette
    # print(count)
    # print(reader)
    palette = []
    for i in range(palette_count):
        item = nbt.decode(reader)
        palette.append(item)
    # print(palette)
    # print(data)
    return palette, data







