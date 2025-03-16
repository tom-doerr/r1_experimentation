class Env1:
    """Environment that counts target characters with penalty after threshold."""
    
    def __init__(self, target_char: str = "a", char_count_penalty_start: int = 10) -> None:
        if not isinstance(target_char, str) or len(target_char) != 1:
            raise ValueError("target_char must be a single character")
        if not isinstance(char_count_penalty_start, int) or char_count_penalty_start < 0:
            raise ValueError("char_count_penalty_start must be a non-negative integer")
            
        self.target_char = target_char
        self.char_count_penalty_start = char_count_penalty_start

    def __call__(self, input_string: str) -> int:
        if not isinstance(input_string, str):
            raise TypeError("input_string must be a string")
            
        count = input_string.count(self.target_char)
        if count == 0:
            return 0
            
        penalty = max(0, len(input_string) - self.char_count_penalty_start) * 2
        return count - penalty
