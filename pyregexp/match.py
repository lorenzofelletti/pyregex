

class Match:
    """ Contains the information of a match in a regular expression."""

    def __init__(self, group_id: int, start_idx: int, end_idx: int, string: str, name: str) -> None:
        self.group_id: int = group_id
        self.name: str = name
        self.start_idx: int = start_idx
        self.end_idx: int = end_idx
        self.match: str = string[start_idx:end_idx]
