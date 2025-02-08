#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
В системе управления складом товары упорядочены в структуре,
похожей на двоичное дерево. Каждый узел дерева представляет
место хранения, которое может вести к другим местам хранения
(левому и правому подразделу). Необходимо найти наименее
затратный путь к товару, ограничив поиск заданной глубиной,
чтобы гарантировать, что поиск займет приемлемое время.
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
        Проверяем, достигли ли мы узла с нужным value = self.goal.
        state: объект BinaryTreeNode.
        """
        return state.value == self.goal

    def action_cost(self, s, a, s1):
        """По умолчанию = 1 (не используется в глубинном поиске)."""
        return 1


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
        """Глубина узла — расстояние от корня."""
        if self.parent is None:
            return 0
        return self.parent.depth() + 1


# Специальные «сигнальные» узлы
failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


def expand(problem, node):
    """
    Функция раскрытия узлов.
    """
    for action in problem.actions(node.state):
        s_next = problem.result(node.state, action)
        yield Node(
            state=s_next,
            parent=node,
            action=action,
            path_cost=node.path_cost + 1,
        )


def depth_limited_search(problem, limit):
    """
    Проверяет существование пути к цели, не превышая глубину 'limit'.
    """

    frontier = [Node(problem.initial)]
    result = failure

    while frontier:
        node = frontier.pop()

        # Проверяем, не цель ли это
        if problem.is_goal(node.state):
            return node

        # Если достигли предельной глубины, то cutoff
        if node.depth() >= limit:
            result = cutoff
        else:
            # Расширение узла
            for child in expand(problem, node):
                frontier.append(child)

    return result


class WarehouseProblem(Problem):
    """
    Описание задачи системы управления складом в двоичном дереве товаров.
    """

    def actions(self, state):
        """
        Список "действий" — это переходы к left или right.
        """
        children = []
        if state.left is not None:
            children.append(state.left)
        if state.right is not None:
            children.append(state.right)
        return children

    def result(self, state, action):
        """
        Переход в узел 'action'.
        """
        return action


def main():
    """
    Главная функция программы.
    """

    root = BinaryTreeNode(
        1,
        left=BinaryTreeNode(2, None, BinaryTreeNode(4)),
        right=BinaryTreeNode(3, BinaryTreeNode(5), None),
    )

    goal = 4
    limit = 2

    # Создаём задачу
    problem = WarehouseProblem(initial=root, goal=goal)

    # Ищем узел со значением 4, глубина не более limit=2
    solution_node = depth_limited_search(problem, limit=limit)

    if solution_node is failure:
        print("Цель не найдена!")
    elif solution_node is cutoff:
        print(f"Глубина поиска достигла лимита={limit}, решение не найдено на этой глубине.")
    else:
        # Решение найдено
        print("Цель найдена:", solution_node.state)


if __name__ == "__main__":
    main()
