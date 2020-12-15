import re
from typing import List


def clean_text(x: str):
    x = x.lower().strip()
    # remove periods from abbreviations first to collapse acronyms together
    x = x.replace(".", "")
    cleanString = re.sub(r"\W+", " ", x)
    return cleanString


def minimum_edit_distance(s1: str, s2: str):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(
                    1
                    + min((distances[index1], distances[index1 + 1], newDistances[-1]))
                )
        distances = newDistances
    return distances[-1]


def find_similar(x: str, master_set: List[str]):
    temp = ""
    for el in master_set.keys():
        if (
            (1.0 - (1.0 * minimum_edit_distance(el, x) / max(len(el), len(x)))) >= 0.8
        ) and (
            (1.0 - (1.0 * minimum_edit_distance(el, x) / max(len(el), len(x))))
            > (1.0 - (1.0 * minimum_edit_distance(el, temp) / max(len(el), len(temp))))
        ):
            temp = el
    if temp == "":
        results = []
    else:
        results = [master_set[temp]]

    return results
