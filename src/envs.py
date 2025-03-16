
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
        if len(input_string) >= self.char_count_penalty_start:
            # Apply penalty for each character over 10
            penalty = max(0, len(input_string) - 10)
            return max(0, count - penalty)
        return count

    def __repr__(self) -> str:
        return f"Env1(target_char={self.target_char!r}, char_count_penalty_start={self.char_count_penalty_start})"


class Env2:
    """Environment that counts characters with length-based scoring."""
    
    def __init__(self, max_char_count: int = 5):
        if not isinstance(max_char_count, int) or max_char_count <= 0:
            raise ValueError("max_char_count must be a positive integer")
        self.max_char_count = max_char_count

    def __call__(self, input_string: str) -> int:
        """Calculate score based on string length."""
        if not isinstance(input_string, str):
            raise ValueError("input_string must be a string")
            
        # Return 0 if string exceeds max length or has consecutive duplicates
        if len(input_string) > self.max_char_count:
            return 0
        if len(input_string) >= 2 and any(input_string[i] == input_string[i+1] 
               for i in range(len(input_string)-1)):
            return 0
            
        # Return length if valid
        return len(input_string)

    def __repr__(self) -> str:
        return f"Env2(max_char_count={self.max_char_count})"

