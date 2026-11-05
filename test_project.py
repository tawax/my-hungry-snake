from project import (
    next_head, key_to_direction, change_direction, is_collision, place_food, speed_for_score, snake_colors, SNAKE_PALETTE,
    COLS, ROWS, START_DELAY, MIN_DELAY,
)


def test_next_head():
    assert next_head((5, 5), "Up") == (5, 4)
    assert next_head((5, 5), "Down") == (5, 6)
    assert next_head((5, 5), "Left") == (4, 5)
    assert next_head((5, 5), "Right") == (6, 5)


def test_next_head_wraps_around():
    assert next_head((0, 5), "Left") == (COLS - 1, 5)
    assert next_head((COLS - 1, 5), "Right") == (0, 5)
    assert next_head((5, 0), "Up") == (5, ROWS - 1)
    assert next_head((5, ROWS - 1), "Down") == (5, 0)


def test_change_direction():
    assert change_direction("Right", "Up") == "Up"
    assert change_direction("Right", "Left") == "Right"
    assert change_direction("Up", "Down") == "Up"
    assert change_direction("Up", "x") == "Up"


def test_is_collision():
    assert is_collision((3, 3), [(3, 3), (3, 4)])
    assert not is_collision((3, 3), [(4, 3)])


def test_place_food():
    snake = [(x, y) for x in range(COLS) for y in range(ROWS)]
    assert place_food(snake) is None
    snake.remove((7, 7))
    assert place_food(snake) == (7, 7)
    for _ in range(100):
        assert place_food([(0, 0)]) != (0, 0)


def test_speed_for_score():
    assert speed_for_score(0) == START_DELAY
    assert speed_for_score(1000) == MIN_DELAY


def test_key_to_direction():
    assert key_to_direction("w") == "Up"
    assert key_to_direction("S") == "Down"
    assert key_to_direction("a") == "Left"
    assert key_to_direction("D") == "Right"
    assert key_to_direction("Up") == "Up"
    assert key_to_direction("x") is None


def test_snake_colors():
    assert snake_colors(0) == SNAKE_PALETTE[0]
    assert snake_colors(9) == SNAKE_PALETTE[0]
    assert snake_colors(10) == SNAKE_PALETTE[1]
    assert snake_colors(25) == SNAKE_PALETTE[2]
    assert snake_colors(10 * len(SNAKE_PALETTE)) == SNAKE_PALETTE[0]
