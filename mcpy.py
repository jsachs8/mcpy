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
import blockdata
import key
import nbt
import world

world.list_worlds()

wname = "4eFtYUGlAAA="
wname = "HOu3YcGsZwA="
w = world.World(wname)
# w.print_level_data()
w.print_spawner_data()
# w.print_hsa_data()
# w.print_player_data()

biome = w.get_biome(-13, -24, 886)
blk = w.get_block(-13, -24, 886)
print(f"biome={biome} block={blk}")


'''
for k, v in w.db.iterate():
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
    elif key.is_entities(k):
        pass
    elif len(v) > 0:
        print(f"{k}")
        reader = nbt.BinaryReader(v)
        while not reader.finished():
            obj = nbt.decode(reader)
            print(obj)
'''












