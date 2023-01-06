import subprocess

# Execute esse arquivo para instalar as dependências de forma  automática
try:
    subprocess.call(["sudo", "apt", "install", "python3-tk"])
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
except Exception as e:
    print(f"Error log: {e}")
