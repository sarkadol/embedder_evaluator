import subprocess

# Kill the SSH tunnel using taskkill (Windows)
subprocess.run(["taskkill", "/F", "/IM", "ssh.exe"], check=True)
