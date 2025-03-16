from typing import Protocol, Generator
from abc import abstractmethod
import subprocess
import shlex
from shutil import which

class Tool(Protocol):
    """Protocol defining interface for command execution tools."""
    
    @abstractmethod
    def stream(self, command: str) -> Generator[str, None, None]:
        """Stream command output."""
        raise NotImplementedError

    def run(self, command: str) -> str:
        """Execute a command and return the result.
        
        Args:
            command: The command to execute
            
        Returns:
            str: The command output
            
        Raises:
            ValueError: If command is invalid
            RuntimeError: If execution fails
        """
        raise NotImplementedError
        
    @abstractmethod 
    def __call__(self, command: str) -> str:
        """Make tool callable for convenience.
        
        Args:
            command: The command to execute
            
        Returns:
            str: The command output
        """
        return self.run(command)
        
    @abstractmethod
    def __repr__(self) -> str:
        """Return string representation of tool."""
        return f"{self.__class__.__name__}()"
        
    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if tool is available for use.
        
        Returns:
            bool: True if tool is available, False otherwise
        """
        raise NotImplementedError

class ShellCodeExecutor(Tool):
    """Safely executes whitelisted shell commands with strict validation."""
    
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp', 'sudo', 'sh', 'bash', 'wget', 'curl', 'ssh'}
    whitelisted_commands = {'ls', 'date', 'pwd', 'echo', 'whoami', 'uname', 'hostname'}
    max_command_length = 100
    
    def __init__(self):
        """Initialize the shell code executor."""
        self._available = which('sh') is not None
        
    def __call__(self, command: str) -> str:
        """Execute a command by delegating to run().
        
        Args:
            command: The command to execute
            
        Returns:
            str: The command output
        """
        return self.run(command)

    def __repr__(self) -> str:
        """Return string representation of the executor.
        
        Returns:
            str: String representation
        """
        return f"ShellCodeExecutor(whitelist={self.whitelisted_commands})"
        
    @property
    def is_available(self) -> bool:
        """Check if shell commands can be executed.
        
        Returns:
            bool: True if shell is available, False otherwise
        """
        return self._available

    def _validate_command(self, command: str) -> None:
        """Validate command before execution.
        
        Args:
            command: The command to validate
            
        Raises:
            ValueError: If command is invalid
            PermissionError: If command is blacklisted
        """
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be a non-empty string")
        if any(char in command for char in ['\n', '\r', '\0', ';', '|', '&', '`', '$', '(', ')', '>', '<']):
            raise ValueError(f"Command contains invalid characters: {command}")
        if len(command) > self.max_command_length:
            raise ValueError(f"Command exceeds maximum length of {self.max_command_length} characters")
            
        parts = command.strip().split()
        if not parts:
            raise ValueError("Empty command")
            
        cmd = parts[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} is blacklisted")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} is not whitelisted")
            
        # Additional validation for command arguments
        if len(parts) > 1:
            for arg in parts[1:]:
                if any(char in arg for char in ['\n', '\r', '\0', ';', '|', '&', '`', '$', '(', ')', '>', '<']):
                    raise ValueError(f"Invalid character in argument: {arg}")

    def run(self, command: str) -> str:
        """Execute a shell command with strict validation.
        
        Args:
            command: The command to execute
            
        Returns:
            str: The command output
            
        Raises:
            ValueError: If command is invalid
            PermissionError: If command is blacklisted
            TimeoutError: If command times out
            RuntimeError: If command fails
        """
        self._validate_command(command)
        try:
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return result.stdout
        except subprocess.TimeoutExpired as e:
            raise TimeoutError("Command timed out") from e
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}") from e
        except Exception as e:
            raise RuntimeError(f"Error executing command: {e}") from e

    def stream(self, command: str) -> Generator[str, None, None]:
        """Stream command output."""
        self._validate_command(command)
        try:
            process = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    yield output
                    
            process.stdout.close()
            return_code = process.wait()
            if return_code != 0:
                raise RuntimeError(f"Command failed with code {return_code}")
        except Exception as e:
            raise RuntimeError(f"Error executing command: {e}") from e
