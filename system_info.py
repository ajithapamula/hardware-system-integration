import platform
import socket
import psutil
import netifaces

def get_windows_version_name(release):
    version_map = {
        "10": "Windows 10 or 11",
        "8": "Windows 8",
        "8.1": "Windows 8.1",
        "7": "Windows 7"
    }
    return version_map.get(release, "Unknown Windows Version")

def get_system_info():
    # Get OS info
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname())
    }
    
    # Get Windows specific info
    if system_info["OS"] == "Windows":
        system_info["Windows Version"] = get_windows_version_name(platform.release())
    
    # Get CPU info
    system_info["CPU Count"] = psutil.cpu_count(logical=False)  # Physical cores
    system_info["Logical CPU Count"] = psutil.cpu_count(logical=True)  # Logical cores
    system_info["CPU Usage"] = psutil.cpu_percent(interval=1)  # Percentage of CPU usage
    
    # Get Memory info
    memory = psutil.virtual_memory()
    system_info["Total RAM"] = memory.total
    system_info["Available RAM"] = memory.available
    system_info["Used RAM"] = memory.used
    system_info["RAM Usage"] = memory.percent
    
    # Get Disk info
    disk = psutil.disk_usage('/')
    system_info["Total Disk"] = disk.total
    system_info["Used Disk"] = disk.used
    system_info["Free Disk"] = disk.free
    system_info["Disk Usage"] = disk.percent
    
    # Get Network info (including MAC address and IP address)
    network_info = {}
    for iface in netifaces.interfaces():
        iface_info = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in iface_info:  # IPv4 address
            ip_address = iface_info[netifaces.AF_INET][0]['addr']
            mac_address = iface_info.get(netifaces.AF_LINK, [{}])[0].get('addr', 'N/A')
            network_info[iface] = {
                'IP Address': ip_address,
                'MAC Address': mac_address
            }
    
    system_info["Network Interfaces"] = network_info
    
    # Get Default Gateway
    gateways = netifaces.gateways()
    default_gateway = gateways.get(netifaces.AF_INET, [])
    system_info["Default Gateway"] = default_gateway[0][0] if default_gateway else 'N/A'

    return system_info
