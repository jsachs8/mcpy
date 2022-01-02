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


# Allows for easy sequential reading of binary data
class BinaryReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def get(self, key):
        size = struct.calcsize(key)
        obj = struct.unpack(key, self.data[self.pos :self.pos + size])[0]
        self.pos += size
        return obj

    def get1(self):
        return self.get("<b")

    def get2(self):
        return self.get("<h")

    def get4(self):
        return self.get("<i")

    def get8(self):
        return self.get("<q")

    def getf(self):
        return self.get("<f")

    def getd(self):
        return self.get("<d")

    def getbytes(self, size):
        obj = struct.unpack("<{}s".format(size), self.data[self.pos:self.pos + size])[0]
        self.pos += size
        return obj

    def getstr(self):
        size = self.get2()
        obj = struct.unpack("<{}s".format(size), self.data[self.pos:self.pos + size])[0]
        self.pos += size
        try:
            obj = obj.decode("utf-8")
        except UnicodeDecodeError:
            pass
        return obj

    def finished(self):
        return self.pos >= len(self.data)

    def __repr__(self):
        return str(self.data[self.pos:])


# Allows for easy sequential writing of binary data.
class BinaryWriter:
    def __init__(self):
        self.data = []

    def put(self, key, *data):
        self.data.append(struct.pack(key, *data))
  
    def put1(self, val):
        return self.put("<b", val)

    def put2(self, val):
        return self.put("<h", val)

    def put4(self, val):
        return self.put("<i", val)

    def put8(self, val):
        return self.put("<q", val)

    def putf(self, val):
        return self.put("<f", val)

    def putd(self, val):
        return self.put("<d", val)

    def putstr(self, string):
        if not isinstance(string, bytes):
            string = string.encode("utf-8")
        self.put2(len(string))
        self.data.append(struct.pack("<{}s".format(len(string)), string))

    def put_bytes(self, string):
        self.data.append(struct.pack("<{}s".format(len(string)), string))

    def get_data(self):
        return b"".join(self.data)

    def __repr__(self):
        return str(self.data)


class TAG_Byte:
    def __init__(self, val=None):
        self.val = val
        self.tag = 1

    def decode(self, reader):
        self.val = reader.get1()
        return self.val

    def encode(self, writer):
        writer.put1(self.val)

    def __repr__(self):
        return f"TAG_Byte({self.val})"

    def __str__(self):
        return f"{self.val}"

class TAG_Short:
    def __init__(self, val=None):
        self.val = val
        self.tag = 2

    def decode(self, reader):
        self.val = reader.get2()
        return self.val

    def encode(self, writer):
        writer.put2(self.val)

    def __repr__(self):
        return f"TAG_Short({self.val})"


class TAG_Int:
    def __init__(self, val=None):
        self.val = val
        self.tag = 3 

    def decode(self, reader):
        self.val = reader.get4()
        return self.val

    def encode(self, writer):
        writer.put4(self.val)

    def __repr__(self):
        return f"TAG_Int({self.val})"

    def __str__(self):
        return f"{self.val}"


class TAG_Long:
    def __init__(self, val=None):
        self.val = val
        self.tag = 4 

    def decode(self, reader):
        self.val = reader.get8()
        return self.val

    def encode(self, writer):
        writer.put8(self.val)

    def __repr__(self):
        return f"TAG_Long({self.val})"

    def __str__(self):
        return f"{self.val}"


class TAG_Float:
    def __init__(self, val=None):
        self.val = val
        self.tag = 5

    def decode(self, reader):
        self.val = reader.getf()
        return self.val

    def encode(self, writer):
        writer.putf(self.val)

    def __repr__(self):
        return f"TAG_Float({self.val})"

    def __str__(self):
        return f"{self.val}"


class TAG_Double:
    def __init__(self, val=None):
        self.val = val
        self.tag = 6 

    def decode(self, reader):
        self.val = reader.getd()
        return self.val

    def encode(self, writer):
        writer.putd(self.val)

    def __repr__(self):
        return f"TAG_Double({self.val})"


class TAG_Byte_Array:
    def __init__(self, val=None):
        self.val = val
        self.tag = 7 

    def decode(self, reader):
        size = reader.get4()
        data = reader.getbytes(size)
        self.val = data 
        return self.val

    def encode(self, writer):
        writer.put4(len(self.val))
        writer.put_bytes(self.val)

    def __repr__(self):
        return f"TAG_Byte_Array({self.val})"

    def __len__(self):
        return len(self.val)

    def __iter__(self):
        return iter(self.val)

    def __contains__(self, item):
        return item in self.val

    def __getitem__(self, ndx):
        return self.val[ndx]

    def __str__(self):
        return '[' + ",".join([str(x) for x in self.val]) + ']'


class TAG_String:
    def __init__(self, val=None):
        self.val = val
        self.tag = 8 

    def decode(self, reader):
        size = reader.get2()
        data = reader.getbytes(size)
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError:
            pass
        self.val = data 
        return self.val

    def encode(self, writer):
        string = self.val.encode("utf-8")
        writer.put2(len(string))
        writer.put_bytes(string)

    def __repr__(self):
        return f"TAG_String({self.val})"

    def __str__(self):
        return f"{self.val}"


class TAG_List:
    def __init__(self, val=None):
        self.val = val
        self.tag = 9 
        self.item_id = None

    def decode(self, reader):
        self.item_id = reader.get1()
        size = reader.get4()
        data = []
        for i in range(size):
            obj = tags[self.item_id]()
            obj.decode(reader)
            data.append(obj)
        self.val = data 
        return self.val

    def encode(self, writer):
        writer.put1(self.item_id)
        size = len(self.val)
        writer.put4(size)
        for elem in self.val:
            elem.encode(writer)

    def __repr__(self):
        return f"TAG_List({self.val})"

    def __str__(self):
        return f"{self.val}"


class TAG_Compound:
    def __init__(self, val=None):
        self.val = val
        self.tag = 10 

    def decode(self, reader):
        data = {} 
        tag = reader.get1() 
        while tag != 0:
            name = TAG_String()
            name.decode(reader)
            obj = tags[tag]()
            obj.decode(reader)
            data[name.val] = obj
            tag = reader.get1()
        self.val = data 
        return self.val

    def encode(self, writer):
        for k, v in self.val.items():
            writer.put1(v.tag)
            writer.putstr(k)
            v.encode(writer)
        writer.put1(0)

    def __repr__(self):
        return f"TAG_Compound({self.val})"

    def __str__(self):
        return f"{self.val}"

    def __getitem__(self, item):
        return self.val[item]

    def __getattr__(self, item):
        return self.val[item].val

    def __iter__(self):
        return self.val.__iter__()


class TAG_Int_Array:
    def __init__(self, val=None):
        self.val = val
        self.tag = 11 

    def decode(self, reader):
        size = reader.get4()
        data = []
        for i in range(size):
            v = reader.get4()
            data.append(v)
        self.val = data 
        return self.val

    def encode(self, writer):
        size = len(self.val)
        writer.put4(size)
        for elem in self.val:
            writer.put4(elem)

    def __repr__(self):
        return f"TAG_Int_Array({self.val})"


class TAG_Long_Array:
    def __init__(self, val=None):
        self.val = val
        self.tag = 12 

    def decode(self, reader):
        size = reader.get4()
        data = []
        for i in range(size):
            v = reader.get8()
            data.append(v)
        self.val = data 
        return self.val

    def encode(self, writer):
        size = len(self.val)
        writer.put4(size)
        for elem in self.val:
            writer.put8(elem)

    def __repr__(self):
        return f"TAG_Long_Array({self.val})"


tags = [None,
        TAG_Byte,
        TAG_Short,
        TAG_Int,
        TAG_Long,
        TAG_Float,
        TAG_Double,
        TAG_Byte_Array,
        TAG_String,
        TAG_List,
        TAG_Compound,
        TAG_Int_Array,
        TAG_Long_Array]


def decode(reader):
    tag = reader.get1()
    name = reader.getstr()
    obj = tags[tag]()
    obj.decode(reader)
    return obj


def encode(obj, writer):
    tag = obj.tag
    writer.put1(obj.tag)
    writer.put2(0)
    obj.encode(writer)
