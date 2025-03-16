from typing import Any
import subprocess

def run_container(image: str, command: str, timeout: int = 10) -> str:
    """Run a command in a container using docker.
    
    Args:
        image: Docker image to use
        command: Command to run in container
        timeout: Maximum execution time
        
    Returns:
        Command output as string
        
    Raises:
        RuntimeError: If execution fails
        TimeoutError: If command times out
    """
    try:
        result = subprocess.run(
            f"docker run --rm {image} {command}",
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(f"Command timed out after {timeout} seconds") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr}") from e
    except Exception as e:
        raise RuntimeError(f"Error executing command: {e}") from e



class IsolatedEnvironment:
    """Provides an isolated execution environment."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        
    def execute(self, command: str) -> str:
        """Execute a command in isolation."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                timeout=self.timeout
            )
            return result.stdout
        except subprocess.TimeoutExpired as e:
            raise TimeoutError("Command timed out") from e
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}") from e
        except Exception as e:
            raise RuntimeError(f"Error executing command: {e}") from e
