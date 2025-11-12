from src.modelos.mascota import Mascota
from src.modelos.persona import Persona

def test_mascota_str():
    dueño = Persona("Ana", "600111222")
    m = Mascota("Luna", "Perro", 3, dueño)
    assert "Luna" in str(m)
    assert "Perro" in str(m)
    assert "Ana" in str(m)
