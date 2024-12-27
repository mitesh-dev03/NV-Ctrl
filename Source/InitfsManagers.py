import os
import subprocess

class DracutManager:
    def __init__(self):
        self.ConfPath = "/etc/dracut.conf.d/Modules.conf"

    def Rebuild(self) -> None:
        Proc = subprocess.run(["dracut", "--regenerate-all", "--force"])
        if(Proc.returncode != 0):
            raise Exception("An error ocurred while rebuilding the initramfs")
    
    def Reset(self) -> None:
        if(os.path.isfile(self.ConfPath)):
            os.remove(self.ConfPath)
        print(f"Removed additional modules")

    def AddModules(self, ModuleList: list) -> None:
        Content = "force_drivers+=\""
        for Module in ModuleList:
            Content += f" {Module}"
        Content += " \"\n"
        with open(self.ConfPath, mode='w', encoding='utf-8') as File:
            File.write(Content)
        print(f"Successfully added additional modules")

# ----------------------------------------------------------------------------------------------

# [TODO] Add support for mkinitcpio