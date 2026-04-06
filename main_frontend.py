# main_frontend.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.frontend.main_window import MainWindow

if __name__ == "__main__":
    print("🚀 Iniciando VIVO OS...")
    app = MainWindow()
    app.mainloop()