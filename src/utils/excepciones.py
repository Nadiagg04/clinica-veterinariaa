# src/utils/excepciones.py

class ErrorClinica(Exception):
    """Excepción base para la aplicación de la clínica veterinaria."""
    pass

class ErrorConexionDB(ErrorClinica):
    """Error al conectar con la base de datos."""
    pass

class ErrorValidacion(ErrorClinica):
    """Error en la validación de datos de entrada."""
    pass

class ErrorMascota(ErrorClinica):
    """Excepción para errores relacionados con Mascotas."""
    pass

class ErrorVeterinario(ErrorClinica):
    """Excepción para errores relacionados con Veterinarios."""
    pass
