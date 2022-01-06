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
class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def get(self, key):
        size = struct.calcsize(key)
        obj = struct.unpack(key, self.data[self.pos:self.pos + size])[0]
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
        obj = struct.unpack(f"<{size}s", self.data[self.pos:self.pos + size])[0]
        self.pos += size
        return obj

    def getstr(self):
        size = self.get2()
        obj = struct.unpack(f"<{size}s", self.data[self.pos:self.pos + size])[0]
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
class Writer:
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
        self.data.append(struct.pack(f"<{len(string)}s", string))

    def put_bytes(self, string):
        self.data.append(struct.pack(f"<{len(string)}s", string))

    def get_data(self):
        return b"".join(self.data)

    def __repr__(self):
        return str(self.data)

    