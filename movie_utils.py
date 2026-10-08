"""Utility helpers for movie search and matching."""


def levenshtein_distance(word1: str, word2: str) -> int:
    """Return the Levenshtein distance between two strings."""
    matrix = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    matrix[0] = list(range(len(word2) + 1))

    for j, row in enumerate(matrix):
        row[0] = j

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            if word1[i - 1] == word2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(
                    (matrix[i - 1][j] + 1),  # delete
                    (matrix[i][j - 1] + 1),  # insert
                    (matrix[i - 1][j - 1] + 1),  # replace
                )

    return matrix[-1][-1]
