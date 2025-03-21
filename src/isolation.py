import subprocess

def _run_subprocess(cmd, timeout: int, shell: bool = False) -> str:
    """Helper function to run subprocess commands with consistent error handling."""
    """Helper function to run subprocess commands with consistent error handling.
    
    Args:
        cmd: Command to execute as list of strings
        timeout: Maximum execution time in seconds
        shell: Whether to use shell execution
        
    Returns:
        str: Command output
        
    Raises:
        TimeoutError: If command times out
        RuntimeError: If command fails or other error occurs
    """
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(f"Command timed out after {timeout} seconds") from e
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        raise RuntimeError(f"Command failed: {error_msg}") from e
    except FileNotFoundError as e:
        raise RuntimeError(f"Command not found: {cmd[0]}") from e
    except Exception as e:
        raise RuntimeError(f"Error executing command: {str(e)}") from e

def run_container(image: str, command: str = '', timeout: int = 10) -> str:
    """Run a command in a container and return the output.
    
    Args:
        image: The container image to use
        command: The command to run in the container
        timeout: Maximum execution time in seconds
        
    Returns:
        str: The command output
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If execution fails
    """
    try:
        _validate_container_args(image, command, timeout)
    except ValueError as e:
        raise ValueError(f"Invalid container arguments: {e}") from e
        
    docker_cmd = ["docker", "run", "--rm", image]
    if command.strip():  # Only add command if not empty
        docker_cmd += ["sh", "-c", command]
        
    return _run_subprocess(docker_cmd, timeout)

def _validate_container_args(image: str, command: str, timeout: int) -> None:
    """Validate container execution arguments."""
    try:
        if not isinstance(image, str) or not image.strip():
            raise ValueError("image must be a non-empty string")
        if not isinstance(command, str):
            raise ValueError("command must be a string") 
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout must be a positive integer")
    except Exception as e:
        raise ValueError(f"Invalid container arguments: {e}") from e


class IsolatedEnvironment:
    """Provides an isolated execution environment."""
    
    def __init__(self, timeout: int = 10):
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout must be a positive integer")
        self.timeout = timeout
        
    def execute(self, command: str) -> str:
        """Execute a command in isolation.
        
        Args:
            command: The command to execute
            
        Returns:
            str: The command output
            
        Raises:
            ValueError: If command is invalid
            RuntimeError: If execution fails
        """
        if not isinstance(command, str) or not command.strip():
            raise ValueError("command must be a non-empty string")
        return _run_subprocess(["/bin/sh", "-c", command], self.timeout)
