from enum import Enum


class WaitType(Enum):
    DEFAULT = 20
    SHORT = 5
    LONG = 60
    FLUENT = 10
    WEB_DRIVER_WAIT = 60
    ACTION_DELAY = 2
    DOWNLOAD_WAIT_TIME = 20
