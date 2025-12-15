"""
Punto de entrada principal del descargador (Wrapper para compatibilidad).

Este archivo mantiene la compatibilidad con versiones anteriores.
Para nueva funcionalidad, usa directamente cli/main.py o el módulo core.
"""

# Importar y ejecutar el CLI principal
from cli.main import main

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        print(f"\nError inesperado: {e}")
