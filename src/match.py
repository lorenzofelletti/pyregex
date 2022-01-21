from numpy import number


class Match:
    def __init__(self, start_idx: int, end_idx: int, string: str) -> None:
        self.name = 'default'
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.match = string[start_idx:end_idx]
