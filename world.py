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
import os
import datetime as dt

import nbt
import key
import blockdata
from hsa import HSA


from libs.leveldb import LevelDB


mcpe_datadir = os.path.expandvars(r'%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe')
worlds_data_dir = os.path.join(mcpe_datadir, r'LocalState/games/com.mojang/minecraftWorlds')


def list_worlds():
    worlds = os.listdir(worlds_data_dir)
    tuples = []
    for world in worlds:
        wpath = os.path.join(worlds_data_dir, world)
        lpath = os.path.join(wpath, "level.dat")
        if os.path.isfile(lpath):
            obj = read_leveldat(lpath)
            tuples.append((world, obj.LevelName, dt.datetime.fromtimestamp(obj.LastPlayed)))
    tuples = sorted(tuples, key=lambda x: x[2], reverse=True)
    for tup in tuples:
        print(f"{tup[0]} -- {tup[2]} -- {tup[1]}")


def read_leveldat(path):
    with open(path, 'rb') as f:
        data = f.read()
        reader = nbt.BinaryReader(data)
        version = reader.get('<i')
        length = reader.get('<i')
        obj = nbt.decode(reader)
    return obj


class World:
    def __init__(self, wname):
        self.dpath = os.path.join(worlds_data_dir, wname, 'db')
        self.lpath = os.path.join(worlds_data_dir, wname, 'level.dat')
        self.db = LevelDB(self.dpath, create_if_missing=False)
        self.obj = read_leveldat(self.lpath)

    def print_hsa_data(self):
        for k in self.db.keys():
            if key.is_hsa(k):
                data = self.db.get(k)
                reader = nbt.BinaryReader(data)
                count = reader.get4()
                while count > 0:
                    dat = HSA.decode(reader)
                    print(dat)
                    count -= 1

    def get_tile_entities(self):
        entities = []
        for k in self.db.keys():
            if key.is_block_entities(k):
                data = self.db.get(k)
                reader = nbt.BinaryReader(data)
                while not reader.finished():
                    obj = nbt.decode(reader)
                    entities.append(obj)
        return entities

    def print_spawner_data(self):
        for entity in self.get_tile_entities():
            if entity.id == 'MobSpawner':
                print(f"{entity.x},{entity.y},{entity.z},{entity.EntityIdentifier}")

    def print_player_data(self):
        for item in self.get_player_data():
            print(f"{item[0]}: {item[1]}")

    def get_player_data(self):
        players = []
        for k in self.db.keys():
            if k == b"~local_player" or k.startswith(b"player_"):
                data = self.db.get(k)
                reader = nbt.BinaryReader(data)
                p = nbt.decode(reader)
                players.append((k, p))
        return players

    def get_level_data(self):
        return read_leveldat(self.lpath)

    def print_level_data(self):
        print(f"level.dat: {self.get_level_data()}")

    def get_block(self, x, y, z, dim=0):
        k = blockdata.key(x, y, z, dim)
        # print(k)
        try:
            v = self.db.get(k)
        except KeyError:
            print('Chunk not found')
            return

        r = nbt.BinaryReader(v)
        version = r.get1()
        count = r.get("B")
        if version == 9:
            offset = r.get("b")
        st = blockdata.read_storage(r)
        if count == 2:
            wl = blockdata.read_storage(r)  # water logging info

        xo = x % 16
        yo = y % 16
        zo = z % 16

        offset = xo * 256 + zo * 16 + yo
        i = st[1][offset]
        b = st[0][i]
        print(f"{x},{y},{z},{b}")

    def dump_subchunk(self, x, y, z, dim=0):
        k = blockdata.key(x, y, z, dim)
        # print(k)
        try:
            v = self.db.get(k)
        except KeyError:
            print('Chunk not found')
            return

        r = nbt.BinaryReader(v)
        version = r.get1()
        count = r.get("B")
        if version == 9:
            offset = r.get("b")
        st = blockdata.read_storage(r)
        if count == 2:
            wl = blockdata.read_storage(r)

        for o in range(4096):
            i = st[1][o]
            b = st[0][i]
            print(f"{hex(o)}, {i}, {b.name}")

        print(len(st[1]))








