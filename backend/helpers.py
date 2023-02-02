import platform, subprocess

if platform.system() == "Windows": # Objectively the best OS
    from helpers_windows import *
else:
    from helpers_linux import *

def call(args : list) -> subprocess.CompletedProcess:
    if (args[0] == "chmod"):
        return call_chmod(args[1:])
    elif (args[0] == "chown"):
        return call_chown(args[1:])

    return subprocess.call(args)