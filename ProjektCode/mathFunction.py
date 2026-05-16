from sympy import lambdify, symbols, pi, E, oo, GoldenRatio, sqrt, log, sin, cos, tan, asin, acos, atan, Abs
from sympy import __dict__ as sympy_dict
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

x = symbols('x')

transformations = (
    standard_transformations +
    (implicit_multiplication_application,)
)

allowed = {
    "x": x,
    "pi": pi,
    "π": pi,
    "E": E,
    "e": E,
    "phi": GoldenRatio,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sqrt": sqrt,
    "log": log,
    "abs": Abs,
}

class MathFunction:
    def __init__(self, expr = None):
        self.__function = None
        self.set_function(expr)
    
    def set_function(self, expr):
        expr = (
            expr
            .replace("^", "**")
            .replace("¹", "**1")
            .replace("²", "**2")
            .replace("³", "**3")
            .replace("⁴", "**4")
            .replace("⁵", "**5")
            .replace("⁶", "**6")
            .replace("⁷", "**7")
            .replace("⁸", "**8")
            .replace("⁹", "**9")
            .replace("⁰", "**0")
            .replace("¼", "(1/4)")
            .replace("½", "(1/2)")
            .replace("⅛", "(1/8)")
            .replace("⅜", "(3/8)")
            .replace("⅝", "(5/8)")
            .replace("⅞", "(7/8)")
        )

        expr = parse_expr(
            expr,
            transformations=transformations,
            local_dict=allowed,
            global_dict=sympy_dict
        )
        self.__function = lambdify(x, expr)
    
    def calc(self, x):
        return self.__function(x)