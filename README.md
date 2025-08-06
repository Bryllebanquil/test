# Neural Control Hub - Unified Agent/Controller System

A powerful, unified system that combines advanced agent capabilities with a modern web-based controller, featuring full SSL encryption and 25+ UAC bypass techniques.

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Usage

**Agent Mode (Default):**
```bash
python main.py
```

**Controller Mode with SSL:**
```bash
python main.py --mode controller --port 8080
# Access at: https://localhost:8080
```

**Combined Mode (Agent + Controller):**
```bash
python main.py --mode both --port 8080
```

**Development Mode (No SSL):**
```bash
python main.py --mode controller --port 8080 --no-ssl
# Access at: http://localhost:8080
```

## 🔒 SSL Security Features

- **Automatic SSL Certificate Generation**: Self-signed certificates created automatically
- **Secure SocketIO**: All agent-controller communications encrypted
- **HTTPS Web Dashboard**: Modern neural-themed interface with SSL
- **Protocol Auto-Detection**: Seamless ws/wss WebSocket handling

## ⚡ Key Features

### Agent Capabilities
- 25+ Advanced UAC bypass techniques (UACME-inspired)
- High-performance 60+ FPS screen streaming
- Windows Defender disabling & stealth operations
- Cross-platform support (Windows/Linux)
- Anti-VM and anti-debugging evasion
- Multiple persistence mechanisms

### Controller Features
- Modern neural-themed web dashboard
- Real-time agent management
- Live streaming (screen/camera/audio)
- Interactive command execution
- SSL-encrypted communications

## 📋 Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --mode {agent,controller,both}  Run mode (default: agent)
  --host HOST                     Controller host (default: 0.0.0.0)
  --port PORT                     Controller port (default: 8080)
  --no-ssl                        Disable SSL for controller
  --help                          Show help message
```

## 🛡️ Security Notice

This tool is for educational and authorized testing purposes only. The SSL implementation uses self-signed certificates which will show browser warnings (this is normal). For production use, replace with CA-signed certificates.

## 📄 Documentation

See `INTEGRATION_SUMMARY.md` for complete technical details and architecture information.

---

**Status**: ✅ Complete with SSL encryption enabled 
