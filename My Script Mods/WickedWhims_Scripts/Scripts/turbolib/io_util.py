'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import structfrom io import BytesIO
class Binary:
    __qualname__ = 'Binary'

    class Writer:
        __qualname__ = 'Binary.Writer'

        def __init__(self):
            self.stream = BytesIO()

        def write(self, data_type, *values):
            self.stream.write(struct.pack(data_type, *values))

        def write_boolean(self, value):
            self.write('?', value)

        def write_8bit_signed_int(self, value):
            self.write('b', value)

        def write_8bit_unsigned_int(self, value):
            self.write('B', value)

        def write_16bit_signed_int(self, value):
            self.write('h', value)

        def write_16bit_unsigned_int(self, value):
            self.write('H', value)

        def write_32bit_signed_int(self, value):
            self.write('i', value)

        def write_32bit_unsigned_int(self, value):
            self.write('I', value)

        def write_float(self, value):
            self.write('f', value)

        def write_double(self, value):
            self.write('d', value)

        def write_string(self, value):
            self.stream.write(value.encode('utf-8'))

        def write_padding(self, size=1):
            self.write('x'*size)

        def write_raw_bytes(self, value):
            self.stream.write(value)

        def get_bytes(self):
            self.stream.seek(0)
            return self.stream.read()

    class Reader:
        __qualname__ = 'Binary.Reader'

        def __init__(self, data_bytes):
            self.stream = data_bytes
            self.index = 0

        def read(self, size):
            value = self.stream[self.index:self.index + size]
            return value

        def shift(self, count):
            self.index = min(max(0, self.index + count), len(self.stream))

        def size(self):
            return len(self.stream)

        def read_boolean(self):
            return struct.unpack('?', self.read(1))[0]

        def read_8bit_signed_int(self):
            return struct.unpack('b', self.read(1))[0]

        def read_8bit_unsigned_int(self):
            return struct.unpack('B', self.read(1))[0]

        def read_16bit_signed_int(self):
            return struct.unpack('h', self.read(2))[0]

        def read_16bit_unsigned_int(self):
            return struct.unpack('H', self.read(2))[0]

        def read_32bit_signed_int(self):
            return struct.unpack('i', self.read(4))[0]

        def read_32bit_unsigned_int(self):
            return struct.unpack('I', self.read(4))[0]

        def read_float(self):
            return struct.unpack('f', self.read(4))[0]

        def read_double(self):
            return struct.unpack('d', self.read(8))[0]

        def read_string(self, size):
            return self.read(size).decode('utf-8')
