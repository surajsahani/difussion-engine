#!/usr/bin/env python3
"""
Easy startup script that opens browser automatically
"""

import webbrowser
import time
import threading
from run_dashboard import main

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:8080')

if __name__ == "__main__":
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the dashboard
    main()