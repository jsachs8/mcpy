import binary
import nbt


class LevelData:
    def __init__(self, path: str):
        with open(path, 'rb') as f:
            self.path = path
            data = f.read()
            reader = binary.Reader(data)
            self.version = reader.get('<i')
            reader.get('<i')  # ignore length - not needed in Python
            self.nbt = nbt.decode(reader)

    def save(self):
        with open(self.path, 'wb') as f:
            payload = binary.Writer()
            nbt.encode(self.nbt, payload)
            buf = payload.get_data()
            size = len(buf)
            header = binary.Writer()
            header.put4(self.version)
            header.put4(size)
            f.write(header.get_data())
            f.write(buf)
