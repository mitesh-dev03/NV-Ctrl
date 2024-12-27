import os
import subprocess
import xml.etree.ElementTree as ET

from HardwareProbe import *
from InitfsManagers import *
from ServiceManagers import *
from ScriptGenerator import *

class HostEnvironment:
    
    def __init__(self, ConfPath: str):
        ConfDoc = ET.parse(ConfPath)
        DocRoot = ConfDoc.getroot()

        if(DocRoot.find("./initramfs_generator").text == "dracut"):
            self.InitfsManager = DracutManager()
        else:
            raise Exception("Unsupported initramfs. generator")

        if(DocRoot.find("./initsystem").text == "runit"):
            self.ServiceManager = RunitManager()
        elif(DocRoot.find("./initsystem").text == "systemd"):
            self.ServiceManager = SystemdManager()
        else:
            raise Exception("Unsupported init. system")

        self.DisplayManager = DocRoot.find("./display_manager").text
        self.ScriptManager = ScriptGenerator()
        self.SystemProbe = HardwareProbe()


    def IsRoot(self) -> bool:
        return os.geteuid() == 0

    def Reset(self) -> None:
        self.InitfsManager.Reset()
        self.ScriptManager.Purge()

    def SwitchGraphics(self, SwitchTo: str) -> None:
        if(not self.IsRoot()):
            raise Exception("Root privileges required")

        print(f"Switching to \"{SwitchTo}\" mode ...")
        if(SwitchTo == "Integrated"):
            self.ScriptManager.Purge()
            self.ScriptManager.Generate("UdevRules", "NVDisable")
            self.ScriptManager.Generate("NvidiaBlacklist", "NVBlacklist")
            self.ServiceManager.Disable("nvidia-persistenced")
            self.InitfsManager.Reset()
            self.InitfsManager.Rebuild()

        elif(SwitchTo == "Hybrid"):
            self.ScriptManager.Purge()
            self.ScriptManager.Generate("Modeset", "Default")
            self.ServiceManager.Enable("nvidia-persistenced")
            self.InitfsManager.Reset()
            self.InitfsManager.Rebuild()

        elif(SwitchTo == "Nvidia"):
            self.ScriptManager.Purge()
            self.ScriptManager.Generate("Modeset", "Default")

            # Xorg Configs
            NvidiaInfo = self.SystemProbe.GetNVBusInfo()
            iGPUVendor = self.SystemProbe.GetiGPUVendor()
            if(iGPUVendor == "Intel"):
                self.ScriptManager.Generate("XorgConfig", "Intel", {"BusInfo": NvidiaInfo})
            elif(iGPUVendor == "AMD"):
                self.ScriptManager.Generate("XorgConfig", "AMD", {"BusInfo": NvidiaInfo})

            if(self.DisplayManager == "lightdm"):
                self.ScriptManager.Generate("DMConfig", "LightDM_Xrandr", {"iGPU": iGPUVendor})
                self.ScriptManager.Generate("DMConfig", "LightDM_Conf")
            elif(self.DisplayManager == "sddm"):
                self.ScriptManager.Generate("DMConfig", "SDDM_Xrandr", {"iGPU": iGPUVendor})
            else:
                print("Warning: Unsupported display manager")

            self.ServiceManager.Enable("nvidia-persistenced")
            self.InitfsManager.AddModules(["nvidia", "nvidia_modeset", "nvidia_uvm", "nvidia_drm"])
            self.InitfsManager.Rebuild()
        
        else:
            raise Exception(f"Invalid mode \"{SwitchTo}\"")