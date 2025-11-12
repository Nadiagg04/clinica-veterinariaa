class Logger:
    def info(self, mensaje: str):
        print(f"[INFO] {mensaje}")

    def error(self, mensaje: str):
        print(f"[ERROR] {mensaje}")

    def debug(self, mensaje: str):
        print(f"[DEBUG] {mensaje}")

logger = Logger()