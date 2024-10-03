import subprocess
ps1 = r"C:\Users\Lenovo\.cursor-tutor\MassGrave.ps1"
subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1])