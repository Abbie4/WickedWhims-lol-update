GLOBAL_VERSION = 3
SEX_VERSION = 3
NUDITY_VERSION = 4
RELEASE_BUILD_NUMBER = 129
RELEASE_HOT_FIX_SUFFIX = 5
IS_PATREON = False

def get_mod_version_str():
    return '{}.{}.{}.{}{}'.format(GLOBAL_VERSION, SEX_VERSION, NUDITY_VERSION, RELEASE_BUILD_NUMBER, get_hotfix_suffix(is_patreon=IS_PATREON))


def get_hotfix_suffix(is_patreon=False):
    if is_patreon is False:
        return str('abcdefghijklmnopqrstuvwxyz'[RELEASE_HOT_FIX_SUFFIX - 1])
    return '.' + str(RELEASE_HOT_FIX_SUFFIX)


def get_mod_version_int():
    ord3 = lambda x: '%.3d' % ord(x)
    return str(''.join(map(ord3, get_mod_version_str())))


def get_mod_version_control_data():
    return (RELEASE_BUILD_NUMBER, RELEASE_HOT_FIX_SUFFIX)


def is_patreon_release():
    return IS_PATREON

