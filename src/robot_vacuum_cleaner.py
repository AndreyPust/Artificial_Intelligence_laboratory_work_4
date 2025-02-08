#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дано дерево, где каждый узел представляет собой комнату в доме.
Узлы связаны в соответствии с возможностью перемещения робота
из одной комнаты в другую. Необходимо определить, существует ли
путь от начальной комнаты (корень дерева) к целевой комнате (узел
с заданным значением), так, чтобы робот не превысил лимит по
глубине перемещения.
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

    def __init__(self, initial=None, goal=None):
        self.initial = initial
        self.goal = goal

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

    def is_goal(self, state):
        """
        Проверка, является ли состояние целевым.
        """
        return state.value == self.goal

    def action_cost(self, s, a, s1):
        """
        Стоимость действий, по умолчанию == 1.
        """
        return 1

    def __str__(self):
        return f"{type(self).__name__}(initial={self.initial!r}, goal={self.goal!r})"


class Node:
    """Узел в дереве поиска."""

    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return f"<Node {self.state}>"

    # Глубина узла — длина пути от корня
    def depth(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()


failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


def expand(problem, node):
    """
    Генерируем дочерние узлы, применяя actions к node.state.
    """
    s = node.state
    for action in problem.actions(s):
        s_next = problem.result(s, action)
        yield Node(state=s_next, parent=node, action=action)


def depth_limited_search(problem, limit):
    """
    Функция поиска пути к целевой комнате (узлу), но не глубже, чем limit.
    Если находим цель, возвращаем узел.
    Если все пути исчерпаны и ничего не найдено, возвращаем failure.
    Если достигли глубины limit, то возврат cutoff.
    """

    frontier = [Node(problem.initial)]
    result = failure

    while frontier:
        node = frontier.pop()

        # Проверка цели
        if problem.is_goal(node.state):
            return node

        # Проверка ограничения по глубине
        if node.depth() >= limit:
            result = cutoff
        else:
            # Расширение узла
            for child in expand(problem, node):
                frontier.append(child)

    return result


class RoomNavigationProblem(Problem):
    """
    Имеется дерево (BinaryTreeNode) c начальным узлом root.
    Нужно найти узел, значение которого = goal.
    Движения: можно пойти в left или right.
    """

    def actions(self, state):
        """
        Возвращаем список "дочерних" узлов (left, right), если они есть.
        """

        children = []
        if state.left:
            children.append(state.left)
        if state.right:
            children.append(state.right)
        return children

    def result(self, state, action):
        return action


def main():
    """
    Главная функция программы.
    """

    # Создание бинарного дерева
    root = BinaryTreeNode(
        1,
        left=BinaryTreeNode(2, None, BinaryTreeNode(4)),
        right=BinaryTreeNode(3, BinaryTreeNode(5), None),
    )
    goal = 4
    limit = 2

    problem = RoomNavigationProblem(root, goal)
    solution_node = depth_limited_search(problem, limit)

    if solution_node is failure:
        print("Найден на глубине: False")
    elif solution_node is cutoff:
        print(f"Найден на глубине: False (достигли limit={limit}, нужна большая глубина)")
    else:
        # решение найдено
        print("Найден на глубине: True")


if __name__ == "__main__":
    main()
