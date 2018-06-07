GLOBAL_VERSION = '3'
SEX_VERSION = '3'
NUDITY_VERSION = '4'
RELEASE_BUILD_NUMBER = '129c'

def get_mod_version_str():
    return GLOBAL_VERSION + '.' + SEX_VERSION + '.' + NUDITY_VERSION + '.' + RELEASE_BUILD_NUMBER


def get_mod_version_int():
    ord3 = lambda x: '%.3d' % ord(x)
    return str(''.join(map(ord3, get_mod_version_str())))

