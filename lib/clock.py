from typing import (
    Any,
    Callable,
)

import ntptime
from time import (
    sleep,
    sleep_us,
    time,
    localtime,
)


GMT_9_SEC = 9 * 60 * 60


class Clock:

    def __init__(
            self,
            target_func: Callable[..., None],
            target_args: tuple = (),
            sync_hms: tuple = (1, 0, 0),) -> None:
        self.current_time = localtime(time())
        self.target_func = target_func
        self.target_args = target_args
        self.sync_hms = sync_hms
        self.is_updated = False

    