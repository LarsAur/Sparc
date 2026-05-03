from typing import List, Tuple

class TunableParameter:
    def __init__(self, name, default, min_val, max_val, c_k, r_k):
        self.name : str = name
        self.default : float = default
        self.min_val : float = min_val
        self.max_val : float = max_val
        self.c_k : float = c_k
        self.r_k : float = r_k
        self.current_value : float = default
        self.c : float = -1
        self.a : float = -1

class FixedParameter:
    def __init__(self, name, value):
        self.name : str = name
        self.value : str = value
