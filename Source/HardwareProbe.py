import subprocess

class HardwareProbe:
    def GetiGPUVendor(self) -> str:
        if(len(subprocess.getoutput("lspci | grep -i Intel | grep -i vga")) > 0):
            return "Intel"
        if(len(subprocess.getoutput("lspci | grep -i AMD | grep -i vga")) > 0):
            return "AMD"
        return "Unidentified"
    
    def GetNVBusInfo(self) -> str:
        BusInfo = subprocess.getoutput("lspci | grep -i nvidia | grep -i vga")
        if(len(BusInfo) > 0):
            BusInfo = BusInfo.split()[0].replace("0000:", "")
            print(f"Found Nvidia GPU at {BusInfo}")
            BusID, DeviceInfo = BusInfo.split(":")
            DeviceID, FunctionID = DeviceInfo.split(".")
            
            # Return Bus data as 'PCI:bus:device:function'
            # also perform hexadecimal to decimal conversion
            return f"PCI:{int(BusID, 16)}:{int(DeviceID, 16)}:{int(FunctionID, 16)}"
        raise Exception("Could not find a Nvidia GPU")