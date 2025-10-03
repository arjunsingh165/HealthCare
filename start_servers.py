#!/usr/bin/env python3
"""
Healthcare Management System Server Starter
Safe cross-platform server management using Python
"""

import os
import sys
import subprocess
import platform
import time
import signal
from pathlib import Path
import threading

class ServerManager:
    def __init__(self):
        self.processes = []
        self.venv_path = Path("healthcare_env")
        
        # Determine executable paths based on OS
        if platform.system() == "Windows":
            self.python_exe = self.venv_path / "Scripts" / "python.exe"
            self.npm_exe = "npm"
        else:
            self.python_exe = self.venv_path / "bin" / "python"
            self.npm_exe = "npm"
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C to gracefully shutdown servers"""
        print("\n🛑 Shutting down servers...")
        self.stop_all_servers()
        sys.exit(0)
    
    def start_django_server(self):
        """Start Django development server"""
        print("🐍 Starting Django backend server...")
        try:
            process = subprocess.Popen(
                [str(self.python_exe), "manage.py", "runserver"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(('Django Backend', process))
            return process
        except Exception as e:
            print(f"❌ Failed to start Django server: {e}")
            return None
    
    def start_react_server(self):
        """Start React development server"""
        print("⚛️  Starting React frontend server...")
        try:
            # Change to frontend directory
            frontend_path = Path("frontend")
            if not frontend_path.exists():
                print("❌ Frontend directory not found")
                return None
            
            process = subprocess.Popen(
                [self.npm_exe, "start"],
                cwd=frontend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(('React Frontend', process))
            return process
        except Exception as e:
            print(f"❌ Failed to start React server: {e}")
            return None
    
    def monitor_process(self, name, process):
        """Monitor a process and print its output"""
        def read_output(stream, prefix):
            for line in iter(stream.readline, ''):
                if line.strip():
                    print(f"[{name}] {line.strip()}")
        
        # Start threads to monitor stdout and stderr
        stdout_thread = threading.Thread(target=read_output, args=(process.stdout, f"{name} OUT"))
        stderr_thread = threading.Thread(target=read_output, args=(process.stderr, f"{name} ERR"))
        
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        
        stdout_thread.start()
        stderr_thread.start()
    
    def stop_all_servers(self):
        """Stop all running servers"""
        for name, process in self.processes:
            try:
                print(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"Error stopping {name}: {e}")
        self.processes.clear()
    
    def start_backend_only(self):
        """Start only the Django backend server"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        django_process = self.start_django_server()
        if not django_process:
            return
        
        print("\n🚀 Django backend server is running!")
        print("📍 Backend URL: http://localhost:8000")
        print("📍 Admin URL: http://localhost:8000/admin")
        print("📍 API URL: http://localhost:8000/api")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            # Monitor the Django process
            self.monitor_process("Django", django_process)
            django_process.wait()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all_servers()
    
    def start_frontend_only(self):
        """Start only the React frontend server"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        react_process = self.start_react_server()
        if not react_process:
            return
        
        print("\n🚀 React frontend server is running!")
        print("📍 Frontend URL: http://localhost:3000")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            # Monitor the React process
            self.monitor_process("React", react_process)
            react_process.wait()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all_servers()
    
    def start_both_servers(self):
        """Start both Django and React servers"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Start Django server
        django_process = self.start_django_server()
        if not django_process:
            return
        
        # Wait a moment for Django to start
        time.sleep(3)
        
        # Start React server
        react_process = self.start_react_server()
        if not react_process:
            self.stop_all_servers()
            return
        
        print("\n🚀 Both servers are running!")
        print("📍 Backend: http://localhost:8000")
        print("📍 Frontend: http://localhost:3000")
        print("📍 Admin: http://localhost:8000/admin")
        print("📍 API: http://localhost:8000/api")
        print("\nPress Ctrl+C to stop all servers")
        
        try:
            # Monitor both processes
            self.monitor_process("Django", django_process)
            self.monitor_process("React", react_process)
            
            # Wait for any process to finish
            while all(process.poll() is None for _, process in self.processes):
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all_servers()

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "both"
    
    manager = ServerManager()
    
    # Check if virtual environment exists
    if not manager.venv_path.exists():
        print("❌ Virtual environment not found. Please run setup.py first.")
        sys.exit(1)
    
    print("🏥 Healthcare Management System")
    print("==============================")
    
    if command == "backend" or command == "django":
        manager.start_backend_only()
    elif command == "frontend" or command == "react":
        manager.start_frontend_only()
    elif command == "both" or command == "all":
        manager.start_both_servers()
    else:
        print("Usage: python start_servers.py [backend|frontend|both]")
        print("  backend  - Start only Django backend server")
        print("  frontend - Start only React frontend server")
        print("  both     - Start both servers (default)")
        sys.exit(1)

if __name__ == "__main__":
    main()