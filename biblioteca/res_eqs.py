import logging
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

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

def newton(f: Callable[[float], float], a: float, b: float, tol: float, max_iter: int = 50, plot:bool = False) -> float:
    """
    Implementação do Método de Newton para encontrar raízes de uma função, utilizando
    a lógica baseada na implementação fornecida.

    Parâmetros:
    f        : função contínua
    a, b     : extremos do intervalo de interesse
    tol      : tolerância para o erro
    max_iter : número máximo de iterações (default 50)

    Retorna:
    A raiz aproximada da função.
    """
    def der1(x: float, dxd1: float = 0.0001) -> float:
        return (f(x + dxd1) - f(x)) / dxd1

    def der2(x: float, dxd2: float = 0.0001) -> float:
        d11 = (f(x) - f(x - dxd2)) / dxd2
        d12 = (f(x + dxd2) - f(x)) / dxd2
        return (d12 - d11) / dxd2

    # Determina os 'flags' de sinal para f e sua segunda derivada
    vfa = 1 if f(a) >= 0 else 0
    vfb = 1 if f(b) >= 0 else 0
    vder2a = 1 if der2(a) >= 0 else 0
    vder2b = 1 if der2(b) >= 0 else 0

    # Seleciona o palpite inicial (xo) e o outro extremo (c)
    if vder2a == vfa:
        xo = a
        c = b
    elif vder2b == vfb:
        xo = b
        c = a
    else:
        # Caso nenhum critério seja atendido, escolhe 'a' como palpite inicial
        xo = a
        c = b

    logging.debug("Método de Newton")
    logging.debug(" n      a        b       xn      f(xn)    erro")
    erro = 10.0
    h = 0
    if vder2a == vfa:
        logging.debug(f"{h:2d} {xo:8.4f} {c:8.4f} {xo:8.4f} {f(xo):8.4f} {erro:8.4f}")
    elif vder2b == vfb:
        logging.debug(f"{h:2d} {c:8.4f} {xo:8.4f} {xo:8.4f} {f(xo):8.4f} {erro:8.4f}")

    # Loop principal do Método de Newton
    for h in range(1, max_iter + 1):
        derivada = der1(xo)
        if derivada == 0:
            raise ZeroDivisionError("Derivada nula encontrada durante iteração.")
        xk = xo - f(xo) / derivada
        erro = abs(xk - xo)
        xo = xk
        if vder2a == vfa:
            logging.debug(f"{h:2d} {xo:8.4f} {c:8.4f} {xo:8.4f} {f(xo):8.4f} {erro:8.4f}")
        elif vder2b == vfb:
            logging.debug(f"{h:2d} {c:8.4f} {xo:8.4f} {xo:8.4f} {f(xo):8.4f} {erro:8.4f}")
        if erro < tol and h > 1:
            break

    logging.debug(f"\nA raiz aproximada é {xo:4.4f}\n")

    # Plot da função para visualização

    if plot:
        xi = np.linspace(-10, 10, 100)
        fig = plt.figure()
        plt.plot(xi, [f(val) for val in xi], '-')
        plt.grid()
        plt.show()

    return xo