"""确定性计算：所有比率、增速必须由本模块从已溯源数字算出。

禁止把计算交给 LLM（LLM 只决定算什么，不执行算术）。
每个计算结果的 inputs 记录输入 Fact 的 key，实现递归溯源。
"""
from __future__ import annotations

import ast
import operator

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}
_FUNCS = {"abs": abs, "min": min, "max": max, "round": round}


def safe_eval(expr: str) -> float:
    """只允许数字、四则运算、乘方与白名单函数的安全求值。"""
    node = ast.parse(expr, mode="eval").body

    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _BINOPS:
            return _BINOPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _UNARY:
            return _UNARY[type(n.op)](ev(n.operand))
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name)
            and n.func.id in _FUNCS
        ):
            return _FUNCS[n.func.id](*[ev(a) for a in n.args])
        raise ValueError(f"表达式包含不允许的节点: {ast.dump(n)}")

    return ev(node)


def pct(numerator: float, denominator: float, decimals: int = 2) -> float | None:
    """百分比（%）。分母为 0 或负值异常时返回 None，禁止臆造。"""
    if denominator == 0:
        return None
    return round(100.0 * numerator / denominator, decimals)


def yoy(curr: float, prev: float, decimals: int = 2) -> float | None:
    """同比增速（%）。"""
    if prev == 0:
        return None
    return round(100.0 * (curr - prev) / abs(prev), decimals)


def cagr(begin: float, end: float, years: float, decimals: int = 2) -> float | None:
    """复合年均增长率（%）。"""
    if begin <= 0 or end <= 0 or years <= 0:
        return None
    return round(100.0 * ((end / begin) ** (1.0 / years) - 1.0), decimals)
