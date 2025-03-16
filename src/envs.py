class Env1:
    """Environment that counts target characters with penalty after threshold."""
    
    def __init__(self, target_char: str, char_count_penalty_start: int) -> None:
        self.target_char = target_char
        self.char_count_penalty_start = char_count_penalty_start

    def __call__(self, input_string: str) -> int:
        count = input_string.count(self.target_char)
        penalty = max(0, count - self.char_count_penalty_start) * 2
        return count - penalty
