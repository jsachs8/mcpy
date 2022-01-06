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
import world
import binary
import key
import nbt


world.list_worlds()

wname = "4eFtYUGlAAA="
# wname = "HOu3YcGsZwA="
wname = "ceHVYYiJAAA="
w = world.World(wname)
w.print_level_data()
w.print_spawner_data()
w.print_hsa_data()
w.print_player_data()

# biome = w.get_biome(0, -64, 0)
biome = None
blk = w.get_block(0, 0, 0)
print(f"biome={biome} block={blk}")


def check(world):
    flag = True
    flag62 = True
    for k, v in world.db.iterate():
        if key.is_block_storage(k):
            pass
        elif key.is_version(k):
            pass
        elif key.is_legacy_generation(k):
            pass
        elif key.is_finalization(k):
            pass
        elif key.is_data_3d(k):
            pass
        elif key.is_tile_entities(k):
            pass
        elif key.is_hsa(k):
            pass
        elif key.is_pending_block_ticks(k):
            pass
        elif key.is_random_block_ticks(k):
            pass
        elif key.is_map(k):
            pass
        elif key.is_biome_states(k):
            pass
        # elif key.is_entities(k):
        #    pass
        elif key.is_data_2d(k):
            pass
        elif key.is_tagged(k, 62):
            # unknown
            if flag62:
                print(k, v)
                flag62 = False
            pass
        elif key.is_tagged(k, 59):
            # checksums
            pass
        elif key.is_tagged(k, 55):
            # conversion data
            if flag:
                print(k, v)
                flag = False
            pass
        elif key.is_tagged(k, 118):
            # legacy version
            pass
        elif k.startswith(b"VILLAGE_"):
            pass
        elif len(v) > 0 and v[0] == 10:
            print(f"{k}")
            reader = binary.Reader(v)
            while not reader.finished():
                obj = nbt.decode(reader)
                print(obj)
        else:
            print(f"******** {k} --> {v} ********")


check(w)

exit(0)

worlds = world.get_worlds()
for w in worlds:
    print(w)
    ldb = world.World(w[0])
    check(ldb)










