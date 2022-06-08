import subprocess
cmd = subprocess.run(["arp", "-a"], capture_output=True)
a = str(cmd).split(",")
b = a[3].replace("stdout=b'", "").replace("\\n", "\n")
print(b)
c=b.split("on wlan0")
for x in c:
    print("Device: ",x)