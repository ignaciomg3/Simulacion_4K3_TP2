import sys
import os
import unittest

# Añadir la ruta del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    # Descubrir y ejecutar todos los tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner()
    runner.run(suite)