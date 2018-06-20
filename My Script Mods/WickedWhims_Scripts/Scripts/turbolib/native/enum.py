import enum

class TurboEnum(enum.Int, export=False):
    __qualname__ = 'TurboEnum'
    __doc__ = '\n    Copy of the native sims enum class.\n    '

