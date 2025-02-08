#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Представьте, что вы разрабатываете систему для автоматического управления
инвестициями, где дерево решений используется для представления
последовательности инвестиционных решений и их потенциальных исходов.
Цель состоит в том, чтобы найти наилучший исход (максимальную прибыль) на
определённой глубине принятия решений, учитывая ограниченные ресурсы и
время на анализ.
"""

import math
from abc import ABC, abstractmethod


class BinaryTreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<{self.value}>"


class Problem(ABC):
    """
    Абстрактный класс для формальной постановки задачи.
    """

    def __init__(self, initial=None):
        self.initial = initial

    @abstractmethod
    def actions(self, state):
        """
        Вернуть доступные действия (операторы) из данного состояния.
        """
        pass

    @abstractmethod
    def result(self, state, action):
        """
        Вернуть результат применения действия к состоянию.
        """
        pass


class Node:
    """Узел в дереве поиска."""

    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return f"<Node {self.state}>"

    def depth(self):
        """
        Глубина узла — расстояние от корня (считаем по цепочке parent).
        """
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()


failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


def expand(problem, node):
    """
    Генерация дочерних узлов.
    """

    for action in problem.actions(node.state):
        s_next = problem.result(node.state, action)
        yield Node(state=s_next, parent=node, action=action)


def depth_limited_search_max(problem, limit):
    """
    Функция ищет максимум среди значений узлов, не опускаясь глубже limit.
    Возвращает максимальную прибыль число (max_value).
    """

    if problem.initial is None:
        return None

    frontier = [Node(problem.initial)]
    max_value = -math.inf

    while frontier:
        node = frontier.pop()

        # Обновляем максимум
        if node.state.value > max_value:
            max_value = node.state.value

        # Ограничение глубины раскрытия
        if node.depth() < limit:
            # Генерирация дочерних узлов
            for child in expand(problem, node):
                frontier.append(child)

    # Если max_value остался -inf, значит дерево было пустое
    return None if max_value == -math.inf else max_value


class InvestmentProblem(Problem):
    """
    Реализация класса задачи управления складом
    Необходимо найти максимальную прибыль (value), не спускаясь глубже limit.
    """

    def actions(self, state):
        """
        Возвращает список дочерних узлов: left и right, если они есть.
        """
        children = []
        if state.left is not None:
            children.append(state.left)
        if state.right is not None:
            children.append(state.right)
        return children

    def result(self, state, action):
        """
        Переход: из state идём в action (его потомок).
        """
        return action


def main():
    """
    Главная функция программы.
    """

    root = BinaryTreeNode(
        3,
        left=BinaryTreeNode(1, BinaryTreeNode(0), None),
        right=BinaryTreeNode(5, BinaryTreeNode(4), BinaryTreeNode(6)),
    )
    limit = 2

    # Создаём задачу
    problem = InvestmentProblem(initial=root)

    max_val = depth_limited_search_max(problem, limit=limit)

    if max_val is None:
        print("Дерево пустое, нет максимального значения (максимальной прибыли).")
    else:
        print("Максимальное значение на указанной глубине:", max_val)


if __name__ == "__main__":
    main()
