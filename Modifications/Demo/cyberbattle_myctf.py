# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import my_ctf
from cyberbattle._env import cyberbattle_env


class CyberBattleMyCtf(cyberbattle_env.CyberBattleEnv):
    """CyberBattle simulation based on my own CTF exercise"""

    def __init__(self, **kwargs):
        super().__init__(
            initial_environment=my_ctf.new_environment(),
            **kwargs)
