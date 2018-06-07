from turbolib.hash_util import FNV
from turbolib.io_util import Binary


class StblBuilder:
    __qualname__ = 'StblBuilder'

    def __init__(self):
        self.version = 5
        self.is_compressed = 0
        self.reserved = [0, 0]
        self.string_length = 0
        self.entries = []

    def append(self, string, fnv=None, flags=0):
        string_fnv = fnv or FNV.fnv32(string)
        self.entries.append((string_fnv, flags, string))
        return self

    def get_bytes(self):
        stream = Binary.Writer()
        stream.write_32bit_unsigned_int(_get_header('STBL'))
        stream.write_16bit_unsigned_int(self.version)
        stream.write_boolean(self.is_compressed)
        stream.write_32bit_unsigned_int(len(self.entries))
        stream.write_padding(size=2)
        stream.write_padding(size=4)
        stream.write_32bit_unsigned_int(self.string_length)
        for (fnv, flags, string) in self.entries:
            stream.write_32bit_unsigned_int(fnv)
            stream.write_8bit_unsigned_int(flags)
            stream.write_16bit_unsigned_int(len(string.encode('utf-8')))
            stream.write_string(string)
        return stream.get_bytes()


def _get_header(string_header):
    i = 0
    for j in reversed(range(len(string_header))):
        i += ord(string_header[j]) << j*8
    return i

