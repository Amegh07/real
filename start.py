import subprocess
import sys
import time
import os

def main():
    print("\n🌍 Starting Reality Simulator Engine...")
    
    # 1. Start Backend in the background
    print("▶ Booting FastAPI Backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "main.py", "--server"],
        cwd=os.path.join(os.getcwd(), "backend")
    )
    
    time.sleep(2) # Give the backend a second to ignite
    
    # 2. Start Frontend
    print("▶ Booting React Dashboard...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=os.path.join(os.getcwd(), "frontend")
    )
    
    print("\n✅ All systems nominal. You can view the dashboard and logs above.")
    print("Press CTRL+C at any time to shut everything down concurrently.\n")
    
    try:
        # Wait for processes to be interrupted
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down environment safely...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
