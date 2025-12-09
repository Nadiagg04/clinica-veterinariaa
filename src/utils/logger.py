class Logger:
    @staticmethod
    def info(mensaje):
        print(f"[INFO] {mensaje}")

    @staticmethod
    def error(mensaje):
        print(f"[ERROR] {mensaje}")
