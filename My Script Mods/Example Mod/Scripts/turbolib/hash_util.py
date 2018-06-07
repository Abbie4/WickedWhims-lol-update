'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
class FNV:
    __qualname__ = 'FNV'

    @staticmethod
    def fnv(string, hash_init, fnv_prime, fnv_size):
        string_bytes = string.lower().encode()
        _get_byte = lambda c: c
        hash_value = hash_init
        for byte in string_bytes:
            hash_value = hash_value*fnv_prime % fnv_size
            hash_value = hash_value ^ _get_byte(byte)
        return hash_value

    @staticmethod
    def fnv32(string, hval_init=2166136261):
        return FNV.fnv(string, hval_init, 16777619, 4294967296)

    @staticmethod
    def fnv64(string, hval_init=14695981039346656037):
        return FNV.fnv(string, hval_init, 1099511628211, 18446744073709551616)
