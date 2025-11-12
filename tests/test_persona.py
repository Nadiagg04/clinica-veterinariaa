from src.modelos.persona import Persona

def test_str():
    p = Persona("Ana", "600111222")
    assert "Ana" in str(p)
