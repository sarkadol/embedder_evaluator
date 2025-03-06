import subprocess
#----------------------------------------------

embedder = 1  # Change to 2 for embedder_2

#----------------------------------------------

# Define your SSH details
ssh_host = "osiris.ics.muni.cz"
ssh_user = "567774"
private_key_path = "C:\\Users\\sarka\\.ssh\\id_rsa"

# Define local and remote ports
local_port = 9000  # Any unused local port
remote_port = 80  # Default HTTP port
url_file_path = f"embedder_{embedder}/url.txt"
# Read the remote host from `url.txt`
try:
    with open(url_file_path, "r") as file:
        remote_host = file.read().strip() #TODO make this select the host from the url not the whole url
except FileNotFoundError:
    print(f"Error: {url_file_path} not found! Exiting.")
    exit(1)

# Create an SSH tunnel
ssh_tunnel_command = [
    "ssh", "-i", private_key_path, "-N", "-L",
#    f"{local_port}:{remote_host}:{remote_port}",
    f"{local_port}:embedbase-ol.dyn.cloud.e-infra.cz:443",  # Remove the full URL
    f"{ssh_user}@{ssh_host}"
]

# Start SSH tunnel
try:
    subprocess.Popen(ssh_tunnel_command)
    print(f"\nSSH tunnel established: localhost:{local_port} → {remote_host}:{remote_port}")
except Exception as e:
    print(f"Error starting SSH tunnel: {e}")
