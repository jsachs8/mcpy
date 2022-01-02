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
import keys
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

    def print_hsa_data(self):
        for k in self.db.keys():
            if keys.is_hsa(k):
                data = self.db.get(k)
                reader = nbt.BinaryReader(data)
                count = reader.get4()
                while count > 0:
                    dat = HSA.decode(reader)
                    print(dat)
                    count -= 1

    def print_spawner_data(self):
        for k in self.db.keys():
            if keys.is_block_entities(k):
                data = self.db.get(k)
                reader = nbt.BinaryReader(data)
                while not reader.finished():
                    obj = nbt.decode(reader)
                    x = obj.x
                    y = obj.y
                    z = obj.z
                    what = obj.id
                    if what == 'MobSpawner':
                        which = obj.EntityIdentifier
                        print(f"{x},{y},{z},{which}")







