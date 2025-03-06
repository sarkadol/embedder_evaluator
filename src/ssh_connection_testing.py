import paramiko

# Přihlašovací údaje
hostname = "osiris.ics.muni.cz"
username = "567774"
private_key_path = "C:\\Users\\sarka\\.ssh\\id_rsa"  # Nahraď cestou k privátnímu klíči

# Inicializace SSH klienta
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatické přijetí host klíče

try:
    # Připojení přes SSH pomocí klíče
    client.connect(hostname, username=username, key_filename=private_key_path)

    # Spuštění příkazu na serveru
    stdin, stdout, stderr = client.exec_command("whoami")

    # Výstup příkazu
    print("Výstup: whoami")
    print(stdout.read().decode().strip())

except Exception as e:
    print(f"Chyba při připojení: {e}")

finally:
    client.close()  # Zavření SSH spojení
