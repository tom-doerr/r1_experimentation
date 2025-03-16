import subprocess

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
    _validate_container_args(image, command, timeout)
        
    try:
        docker_cmd = ["docker", "run", "--rm", image]
        if command.strip():  # Only add command if not empty
            docker_cmd += ["sh", "-c", command]  # Execute command via shell
            
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(f"Container timed out after {timeout} seconds") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Container failed: {e.stderr}") from e
    except Exception as e:
        raise RuntimeError(f"Error running container: {e}") from e

def _validate_container_args(image: str, command: str, timeout: int) -> None:
    """Validate container execution arguments."""
    if not isinstance(image, str) or not image.strip():
        raise ValueError("image must be a non-empty string")
    if not isinstance(command, str):
        raise ValueError("command must be a string")
    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError("timeout must be a positive integer")


class IsolatedEnvironment:
    """Provides an isolated execution environment."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        
    def execute(self, command: str) -> str:
        """Execute a command in isolation."""
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
