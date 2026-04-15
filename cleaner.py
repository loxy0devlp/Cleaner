# Copyright (c) Cleaner by Loxy0devlp
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.

import os, colorama, ctypes, sys, tempfile, pathlib, string, json, shutil

credits = {
    "tool_name"    : "Cleaner",
    "tool_version" : "1.0",
    "tool_license" : "MIT License",
    "tool_github"  : "github.com/loxy0devlp/Cleaner",
    "developer"    : "loxy0devlp",
    "gunslol"      : "guns.lol/loxy0dev"
}

colorama.init()
color  = colorama.Fore
white  = color.WHITE
reset  = color.RESET
green  = color.GREEN
blue   = color.BLUE
red    = color.RED

ERROR = f"{red  }[{white}x{red  }]"
INPUT = f"{blue }[{white}>{blue }]"
INFO  = f"{blue }[{white}!{blue }]"
ADD   = f"{green}[{white}+{green}]"

affirmative = ["y", "ye", "yes", "yeah", "yep", "ok", "okay", "o", "ou", "oui", "true", "1"]

try:    os_name     = "Windows" if sys.platform.startswith("win") else "Linux" if sys.platform.startswith("linux") else "Unknown"
except: os_name     = "Unknown"

banner = rf"""
                                   _________ .__                                     
                                   \_   ___ \|  |   ____ _____    ____   ___________ 
                                   /    \  \/|  | _/ __ \\__  \  /    \_/ __ \_  __ \
                                   \     \___|  |_\  ___/ / __ \|   |  \  ___/|  | \/
                                    \________/____/\_____>______/___|__/\_____>__|   

                                              {white + credits["tool_github"]}
"""

path_folder_tool                 = os.path.dirname(os.path.abspath(__file__))
path_folder_paths                = os.path.join(path_folder_tool,  "Paths")
path_file_path_tor               = os.path.join(path_folder_tool,  "PathTor.txt")
path_file_linux_file_paths       = os.path.join(path_folder_paths, "LinuxFilePaths.json")
path_file_linux_folder_paths     = os.path.join(path_folder_paths, "LinuxFolderPaths.json")
path_file_windows_file_paths     = os.path.join(path_folder_paths, "WindowsFilePaths.json")
path_file_windows_folder_paths   = os.path.join(path_folder_paths, "WindowsFolderPaths.json")
path_file_windows_registry_keys  = os.path.join(path_folder_paths, "WindowsRegistryKeys.json")

with open(path_file_linux_file_paths,       "r", encoding="utf-8") as file: data_linux_file_paths       = json.load(file)
with open(path_file_linux_folder_paths,     "r", encoding="utf-8") as file: data_linux_folder_paths     = json.load(file)
with open(path_file_windows_file_paths,     "r", encoding="utf-8") as file: data_windows_file_paths     = json.load(file)
with open(path_file_windows_folder_paths,   "r", encoding="utf-8") as file: data_windows_folder_paths   = json.load(file)
with open(path_file_windows_registry_keys,  "r", encoding="utf-8") as file: data_windows_registry_keys  = json.load(file)

if os_name == "Windows":
    import winreg
    path_appdata_local   = os.getenv('LOCALAPPDATA')
    path_appdata_roaming = os.getenv('APPDATA')
    path_user            = os.getenv('USERPROFILE')
    path_system_root     = os.getenv('SystemRoot')
    path_program_data    = os.getenv('ProgramData')
    
elif os_name == "Linux":
    path_user  = os.path.join("/home", os.getlogin())
    path_var   = os.path.join("/var")
    path_tmp_1 = os.path.join("/tmp")
    path_tmp_2 = tempfile.gettempdir()

def GetFirefoxFilePaths():
    firefox_file_paths = []
    if os_name == "Windows":
        path_appdata_local_firefox   = os.path.join(path_appdata_local,   "Mozilla", "Firefox", "Profiles")
        path_appdata_roaming_firefox = os.path.join(path_appdata_roaming, "Mozilla", "Firefox", "Profiles")
    elif os_name == "Linux":
        path_home_firefox = os.path.join(path_user, ".mozilla", "firefox")

    def AddExistingFiles(profile_path):
        files = [
            os.path.join(profile_path, "places.sqlite"),
            os.path.join(profile_path, "formhistory.sqlite"),
            os.path.join(profile_path, "permissions.sqlite"),
            os.path.join(profile_path, "content-prefs.sqlite"),
            os.path.join(profile_path, "cookies.sqlite"),
            os.path.join(profile_path, "cookies.sqlite-wal"),
            os.path.join(profile_path, "cache"),
            os.path.join(profile_path, "cache1"),
            os.path.join(profile_path, "cache2"),
            os.path.join(profile_path, "cache3"),
            os.path.join(profile_path, "storage"),
        ]
        return [f for f in files if os.path.exists(f)]
    
    if os_name == "Windows":
        if os.path.exists(path_appdata_roaming_firefox):
            for profile in os.listdir(path_appdata_roaming_firefox):
                if ".default" in profile:
                    profile_path = os.path.join(path_appdata_roaming_firefox, profile)
                    firefox_file_paths.extend(AddExistingFiles(profile_path))

        if os.path.exists(path_appdata_local_firefox):
            for profile in os.listdir(path_appdata_local_firefox):
                if ".default" in profile:
                    profile_path = os.path.join(path_appdata_local_firefox, profile)
                    for f in AddExistingFiles(profile_path):
                        if f not in firefox_file_paths:
                            firefox_file_paths.append(f)
    elif os_name == "Linux":
        if os.path.exists(path_home_firefox):
            for profile in os.listdir(path_home_firefox):
                if ".default" in profile:
                    profile_path = os.path.join(path_home_firefox, profile)
                    for f in AddExistingFiles(profile_path):
                        if f not in firefox_file_paths:
                            firefox_file_paths.append(f)

    return firefox_file_paths

def OverwritingFile(category_name, file_path):
    try:
        file_path = pathlib.Path(file_path)
        file_size = file_path.stat().st_size
        with open(file_path, "r+b") as file:
            file.seek(0)
            file.write(b"\x00" * file_size)
            file.truncate(file_size)
        print(f"{ADD} File overwritten ({category_name}): {white}{file_path}{reset}")
    except FileNotFoundError: pass
    except PermissionError: print(f"{ERROR} File unoverwritten ({category_name}): {white}{file_path}{red} Error: {white}Permission denied{reset}")
    except Exception as e: print(f"{ERROR} File unoverwritten ({category_name}): {white}{file_path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")

def DeleteFile(category_name, file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try: 
            OverwritingFile(category_name, file_path)
            os.remove(file_path)
            print(f"{ADD} File deleted ({category_name}): {white}{file_path}{reset}")
        except FileNotFoundError: pass
        except PermissionError: print(f"{ERROR} File not deleted ({category_name}): {white}{file_path}{red} Error: {white}Permission denied{reset}")
        except Exception as e: print(f"{ERROR} File not deleted ({category_name}): {white}{file_path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")

def DeleteFolder(category_name, folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    DeleteFile(category_name, file_path)
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(dir_path)
                        print(f"{ADD} Folder deleted ({category_name}): {white}{dir_path}{reset}")
                    except Exception as e: print(f"{ERROR} Folder not deleted ({category_name}): {white}{dir_path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")
            try:
                shutil.rmtree(folder_path)
                print(f"{ADD} Folder deleted ({category_name}): {white}{folder_path}{reset}")
            except Exception as e: print(f"{ERROR} Folder not deleted ({category_name}): {white}{folder_path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")
        except PermissionError: print(f"{ERROR} Folder not deleted ({category_name}): {white}{folder_path}{red} Error: {white}Permission denied{reset}")
        except Exception as e: print(f"{ERROR} Folder not deleted ({category_name}): {white}{folder_path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")

def DeleteAllFromFolder(category_name, folder_path):
    try:
        if not os.path.exists(folder_path): return
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isfile(full_path) or os.path.islink(full_path): DeleteFile(category_name, full_path)
            elif os.path.isdir(full_path): DeleteFolder(category_name, full_path)
    except FileNotFoundError: pass
    except PermissionError: print(f"{ERROR} Folder not deleted ({category_name}): {white}{folder_path}{red} Error: {white}Permission denied{reset}")
    except Exception as e: print(f"{ERROR} Folder not deleted ({category_name}): {white}{folder_path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")

def DeleteSubkeys(category_name, key, subkey_path, registry_key):
    try:
        with winreg.OpenKey(key, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as k:
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(k, i)
                    DeleteSubkeys(category_name, k, subkey_name, registry_key)
                except: break
                i += 1
        winreg.DeleteKey(key, subkey_path)
        print(f"{ADD} Key deleted ({category_name}): {white}{registry_key}{reset}")
    except FileNotFoundError: pass
    except PermissionError: print(f"{ERROR} Key not deleted ({category_name}): {white}{registry_key}{red} Error: {white}Permission denied{reset}")
    except Exception as e: print(f"{ERROR} Key not deleted ({category_name}): {white}{registry_key}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")
    
def DeleteRegistryKey(category_name, registry_key):
    root_keys = {
        "HKEY_CURRENT_USER"   : winreg.HKEY_CURRENT_USER,   "HKCU" : winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE"  : winreg.HKEY_LOCAL_MACHINE,  "HKLM" : winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CLASSES_ROOT"   : winreg.HKEY_CLASSES_ROOT,   "HKCR" : winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS"          : winreg.HKEY_USERS,          "HKU"  : winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG" : winreg.HKEY_CURRENT_CONFIG, "HKCC" : winreg.HKEY_CURRENT_CONFIG
    }

    try:
        key_name, subkey_path = registry_key.split("\\", 1)
        key = root_keys[key_name.upper()]
    except: return
        
    DeleteSubkeys(category_name, key, subkey_path, registry_key)

def DeleteDiskTrash():
    folders = ["$Recycle.Bin", ".Trash-1000", ".Trash"]

    if os_name == "Windows":
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                for name in folders:
                    folder_path = os.path.join(drive, name)
                    if os.path.exists(folder_path):
                        try:
                            DeleteFolder("Trash", folder_path)
                            print(f"{ADD} Recycle Bin deleted on: {white}{drive}{reset}")
                        except FileNotFoundError: pass
                        except PermissionError: print(f"{ERROR} Recycle Bin not deleted: {white}{drive}{red} Error: {white}Permission denied{reset}")
                        except Exception as e: print(f"{ERROR} Recycle Bin not deleted: {white}{drive}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")

    elif os_name == "Linux":
        path = f"/run/media/{os.getlogin()}"
        if not os.path.exists(path): return
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                for folder in folders:
                    folder_path = os.path.join(full_path, folder)
                    if os.path.exists(folder_path):
                        try:
                            DeleteFolder("Trash", folder_path)
                            print(f"{ADD} Recycle Bin deleted on: {white}{folder_path}{reset}")
                        except FileNotFoundError: pass
                        except PermissionError: print(f"{ERROR} Recycle Bin not deleted: {white}{path}{red} Error: {white}Permission denied{reset}")
                        except Exception as e: print(f"{ERROR} Recycle Bin not deleted: {white}{path}{red} Error: {white}{str(e).rsplit(": '", 1)[0]}{reset}")

def IsAdmin():
    if os_name == "Windows":
        try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: return False
    elif os_name == "Linux":
        try: return os.geteuid() == 0
        except: return False

def Title():
    if os_name == "Windows": ctypes.windll.kernel32.SetConsoleTitleW(f"{credits["tool_name"]} v{credits["tool_version"]} (by {credits["developer"]})")
    elif os_name == "Linux": sys.stdout.write(f"\x1b]2;{credits["tool_name"]} v{credits["tool_version"]} (by {credits["developer"]})\x07")

def Start():
    Title()
    print(blue + banner)
    if not os_name in ("Windows", "Linux"):
        print(f"{ERROR} Operating system not supported.")
        return
    
    if IsAdmin(): print(f"{INFO} Script launched in administrator mode.")
    else: 
        print(f"{INFO} Please run the script in administrator mode !")
        input(f"{INPUT} Press enter -> {reset}")
        return

    if os_name == "Windows":
        path_tor = None
        if os.path.exists(path_file_path_tor):
            with open(path_file_path_tor, "r", encoding="utf-8") as file: path_tor = file.read()
            if os.path.exists(path_tor):
                if os.path.basename(path_tor) == "Tor Browser":
                    path_tor = os.path.join(path_tor, "Browser")
            else:
                print(f"{ERROR} Please put the path of tor in: {white}{os.path.basename(path_file_path_tor)}{reset}")
                choice = input(f"{INPUT} Do you still want to run the script ? (y/n) -> {reset}")
                if not choice in affirmative:
                    sys.exit(0)
        else: 
            print(f"{ERROR} Please put the path of tor in: {white}{os.path.basename(path_file_path_tor)}{reset}")
            choice = input(f"{INPUT} Do you still want to run the script ? (y/n) -> {reset}")
            if not choice in affirmative:
                sys.exit(0)

        def BuildFullPath(path_parts):
            replaced_parts = [
                part.replace("%PATH_APPDATA_LOCAL%", path_appdata_local).replace("%PATH_APPDATA_ROAMING%", path_appdata_roaming)
                    .replace("%PATH_USER%", path_user).replace("%PATH_SYSTEM_ROOT%", path_system_root)
                    .replace("%PATH_PROGRAM_DATA%", path_program_data).replace("%PATH_TOR%", path_tor)
                for part in path_parts
            ]
            return os.path.join(*replaced_parts)
        
    elif os_name == "Linux":
        def BuildFullPath(path_parts):
            replaced_parts = [
                part.replace("%PATH_USER%", path_user).replace("%PATH_VAR%", path_var)
                    .replace("%PATH_TMP_1%", path_tmp_1).replace("%PATH_TMP_2%", path_tmp_2)
                for part in path_parts
            ]
            return os.path.join(*replaced_parts)

    input(f"{INPUT} Press enter to begin cleaning -> {reset}")

    DeleteDiskTrash()
    for path_file_firefox in GetFirefoxFilePaths():
        try: DeleteFile("Firefox", path_file_firefox)
        except: pass
        try: DeleteFolder("Firefox", path_file_firefox)
        except: pass
    
    if os_name == "Linux":
        for category_name, paths in data_linux_file_paths.items():
            for path_parts in paths:
                DeleteFile(category_name, BuildFullPath(path_parts))
        for category_name, paths in data_linux_folder_paths.items():
            for path_parts in paths:
                DeleteAllFromFolder(category_name, BuildFullPath(path_parts))

    if os_name == "Windows":
        for category_name, paths in data_windows_file_paths.items():
            for path_parts in paths:
                DeleteFile(category_name, BuildFullPath(path_parts))
        for category_name, paths in data_windows_folder_paths.items():
            for path_parts in paths:
                DeleteAllFromFolder(category_name, BuildFullPath(path_parts))
        for category_name, keys in data_windows_registry_keys.items():
            for registry_key in keys:
                DeleteRegistryKey(category_name, registry_key)
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000001 | 0x00000004)
    
    print(f"{INFO} Finish.")
    input(f"{INPUT} Press enter -> {reset}")

try: Start()
except Exception as e: 
    print(f"{ERROR} Error: {white}{e}")
    input(f"{INPUT} Press enter -> {reset}")