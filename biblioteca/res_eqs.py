import logging
from typing import Callable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def bissecao(f: Callable[[float], float], a: float, b: float, tol: float) -> float:
    """
    Implementação do Método da Bisseção para encontrar raízes de uma função.

    Parâmetros:
    f   : função contínua
    a   : limite inferior do intervalo
    b   : limite superior do intervalo
    tol : tolerância para o erro

    Retorna:
    A raiz aproximada da função no intervalo [a, b].
    """

    logging.debug(f"Intervalo inicial: [a, b] = [{a}, {b}]")

    if f(a) * f(b) >= 0:
        raise ValueError("A função deve ter sinais opostos nos extremos do intervalo [a, b].")

    iteracao = 0
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        logging.debug(f"Iteração {iteracao}: a = {a}, b = {b}, c = {c}, f(c) = {f(c)}")
        if f(c) == 0: 
            return c
        elif f(a) * f(c) < 0:
            b = c 
        else:
            a = c 
        iteracao += 1

    return (a + b) / 2 