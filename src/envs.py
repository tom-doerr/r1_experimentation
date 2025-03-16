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
        """Calculate score based on target character count and length penalty.
        
        Args:
            input_string: String to evaluate (must be non-empty)
            
        Returns:
            int: Score calculated as:
                - target_char count minus length penalty if any targets found
                - -2 if no targets and string length >= penalty start
                - 0 if no targets and string length < penalty start
                
        Raises:
            ValueError: If input_string is empty
        """
        if not isinstance(input_string, str) or not input_string:
            raise ValueError("input_string must be a non-empty string")
            
        count = input_string.count(self.target_char)
        if count > 0:
            penalty = max(0, len(input_string) - self.char_count_penalty_start)
            return count - penalty
            
        # No targets found
        return -2 if len(input_string) >= self.char_count_penalty_start else 0

    def __repr__(self) -> str:
        return f"Env1(target_char={self.target_char!r}, char_count_penalty_start={self.char_count_penalty_start})"
