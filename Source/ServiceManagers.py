import os
import subprocess

class RunitManager:
    def __init__(self):
        self.ServicePath = "/etc/sv/"
        self.ServiceLink = "/var/service/"

    def IsRunning(self, Service: str) -> bool:
        return os.path.islink(self.ServiceLink + Service)
    
    def Enable(self, Service: str) -> None:
        if(not self.IsRunning(Service)):
            os.symlink(self.ServicePath + Service, self.ServiceLink + Service)
            print(f"Successfully enabled {Service} service")
        
    def Disable(self, Service: str) -> None:
        if(self.IsRunning(Service)):
            os.unlink(self.ServiceLink + Service)
            print(f"Successfully disabled {Service} service")
                     
# ----------------------------------------------------------------------------------------------

class SystemdManager:
    def IsRunning(self, Service: str) -> bool:
        Proc = subprocess.run(["systemctl", "is-active", "--quiet", Service])
        return Proc.returncode == 0

    def Enable(self, Service: str) -> None:
        if(not self.IsRunning(Service)):
            Proc = subprocess.run(["systemctl", "enable", Service])
            if(Proc.returncode == 0):
                print(f"Successfully enabled {Service}")
                return
            raise Exception(f"Failed to enable {Service}")

    def Disable(self, Service: str) -> None:
        if(self.IsRunning(Service)):
            Proc = subprocess.run(["systemctl", "disable", Service])
            if(Proc.returncode == 0):
                print(f"Successfully disabled {Service}")
                return
            raise Exception(f"Failed to disable {Service}")