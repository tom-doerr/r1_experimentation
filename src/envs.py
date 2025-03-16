
class Env1:
    """Environment that counts target characters with penalty after threshold."""
    
    def __init__(self, target_char: str = "a", char_count_penalty_start: int = 23) -> None:
        if not isinstance(target_char, str) or len(target_char) != 1:
            raise ValueError("target_char must be a single character")
        if not isinstance(char_count_penalty_start, int) or char_count_penalty_start < 0:
            raise ValueError("char_count_penalty_start must be a non-negative integer")
            
        self.target_char = target_char
        self.char_count_penalty_start = char_count_penalty_start

    def __call__(self, input_string: str) -> int:
        """Calculate score based on target character count and length penalty."""
        if not isinstance(input_string, str) or not input_string:
            raise ValueError("input_string must be a non-empty string")
            
        count = input_string.count(self.target_char)
        penalty = max(0, len(input_string) - self.char_count_penalty_start) * 1  # Reduced penalty multiplier
        score = count - penalty
        return max(score, -2) if len(input_string) >= self.char_count_penalty_start else count

    def __repr__(self) -> str:
        return f"Env1(target_char={self.target_char!r}, char_count_penalty_start={self.char_count_penalty_start})"


class Env2:
    """Environment that counts characters with length-based scoring."""
    
    def __init__(self, max_char_count: int = 5):
        if not isinstance(max_char_count, int) or max_char_count <= 0:
            raise ValueError("max_char_count must be a positive integer")
        self.max_char_count = max_char_count

    def __call__(self, input_string: str) -> int:
        """Calculate score based on consecutive duplicate characters."""
        if not isinstance(input_string, str):
            raise ValueError("input_string must be a string")
        if len(input_string) > self.max_char_count:
            return 0
        # Calculate mirror character matches
        score = 0
        n = len(input_string)
        for i in range(n // 2):
            if input_string[i] == input_string[n - i - 1]:
                score += 1
        return score

    def __repr__(self) -> str:
        return f"Env2(max_char_count={self.max_char_count})"

