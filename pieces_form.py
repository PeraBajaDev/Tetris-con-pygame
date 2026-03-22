pieces_form: dict[str, list[list[str]]] = {
    "T": [
        ["x", "x", "x"],
        ["O", "x", "O"],
    ],
    "O": [
        ["x", "x"],
        ["x", "x"],
    ],
    "I": [["x"] for _ in range(4)],
    "L": [*[["x", "O"] for _ in range(2)], ["x", "x"]],
    "J": [*[["O", "x"] for _ in range(2)], ["x", "x"]],
    "S": [
        ["O", "x", "x"],
        ["x", "x", "O"],
    ],
    "Z": [
        ["x", "x", "O"],
        ["O", "x", "x"],
    ],
}
