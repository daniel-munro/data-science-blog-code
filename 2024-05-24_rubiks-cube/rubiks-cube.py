from queue import Queue
import numpy as np

#     www
#     w0w
#     www
# ggg rrr bbb ooo            012
# g1g r2r b3b o4o            3 4
# ggg rrr bbb ooo            567
#     yyy
#     y5y
#     yyy

class Cube:
    def __init__(self):
        self.state = 'w' * 8 + 'g' * 8 + 'r' * 8 + 'b' * 8 + 'o' * 8 + 'y' * 8

    def __repr__(self):
        x = ''
        faces = [[' ', 0, ' ', ' '], [1, 2, 3, 4], [' ', 5, ' ', ' ']]
        cells = [[0, 1, 2], [3, -1, 4], [5, 6, 7]]
        for face_row in faces:
            for cell_row in cells:
                for face in face_row:
                    for cell in cell_row:
                        if face == ' ':
                            x += ' '
                        elif cell == -1:
                            x += 'wgrboy'[face]
                        else:
                            i = face * 8 + cell
                            x += self.state[i]
                    x += ' '
                x += '\n'
        return x
    
    def twist(self, face, dir):
        self.state = twisted(self.state, face, dir)

def twisted(state, face, dir):
    # For this face, give 20 pairs of positions. The color at the first position of each pair
    # moves to the second position in a clockwise turn (and vice versa for counter-clockwise).
    pairs = []
    # First, rotate the 8 positions on the face itself:
    for p1, p2 in [(0, 2), (1, 4), (2, 7), (4, 6), (7, 5), (6, 3), (5, 0), (3, 1)]:
        pairs.append(((face, p1), (face, p2)))
    # Then, add all 4-position cycles for adjacent faces
    cycles = [
        [
            ((1, 0), (4, 0), (3, 0), (2, 0)),
            ((1, 1), (4, 1), (3, 1), (2, 1)),
            ((1, 2), (4, 2), (3, 2), (2, 2)),
        ],
        [
            ((0, 0), (2, 0), (5, 0), (4, 7)),
            ((0, 3), (2, 3), (5, 3), (4, 4)),
            ((0, 5), (2, 5), (5, 5), (4, 2)),
        ],
        [
            ((0, 5), (3, 0), (5, 2), (1, 7)),
            ((0, 6), (3, 3), (5, 1), (1, 4)),
            ((0, 7), (3, 5), (5, 0), (1, 2)),
        ],
        [
            ((0, 2), (4, 5), (5, 2), (2, 2)),
            ((0, 4), (4, 3), (5, 4), (2, 4)),
            ((0, 7), (4, 0), (5, 7), (2, 7)),
        ],
        [
            ((0, 0), (1, 5), (5, 7), (3, 2)),
            ((0, 1), (1, 3), (5, 6), (3, 4)),
            ((0, 2), (1, 0), (5, 5), (3, 7)),
        ],
        [
            ((1, 5), (2, 5), (3, 5), (4, 5)),
            ((1, 6), (2, 6), (3, 6), (4, 6)),
            ((1, 7), (2, 7), (3, 7), (4, 7)),
        ],
    ][face]
    for cycle in cycles:
        for j in range(len(cycle)):
            k = (j + 1) % len(cycle)
            pairs.append((cycle[j], cycle[k]))
    new_state = list(state)
    assert dir in [-1, 1]
    for pair in pairs:
        pos_from = pair[0] if dir == 1 else pair[1]
        pos_to = pair[1] if dir == 1 else pair[0]
        i_from = pos_from[0] * 8 + pos_from[1]
        i_to = pos_to[0] * 8 + pos_to[1]
        new_state[i_from] = state[i_to]
    return ''.join(new_state)


# One 50-twist shuffle

cube = Cube()
# print(cube)
with open('states_shuffle.txt', 'w') as out:
    out.write(cube.state + '\n')
    for _ in range(50):
        face = np.random.randint(0, 6)
        dir = np.random.choice([-1, 1])
        cube.twist(face, dir)
        out.write(cube.state + '\n')
# print(cube)

## 100 50-twist shuffles

with open('states_shuffle_1000.txt', 'w') as out:
    out.write('trial\tstate\n')
    for trial in range(1000):
        cube = Cube()
        out.write(f'{trial}\t{cube.state}\n')
        for _ in range(50):
            face = np.random.randint(0, 6)
            dir = np.random.choice([-1, 1])
            cube.twist(face, dir)
            out.write(f'{trial}\t{cube.state}\n')

## Solver

max_level = 5
init = Cube().state
moves = {init: (0, -1, 0, "")}
Q = Queue()
Q.put(init)
# for _ in range(1000):
while not Q.empty():
    state = Q.get()
    moves_to_solve = moves[state][0]
    if moves_to_solve == max_level:
        break
    for face in range(6):
        for dir in [-1, 1]:
            state2 = twisted(state, face, dir)
            if state2 not in moves:
                moves[state2] = (moves_to_solve + 1, face, -1 * dir, state)
                Q.put(state2)
with open('solver.txt', 'w') as out:
    out.write('state\tlevel\tface\tdir\tresult\n')
    for state, (level, face, dir, result) in moves.items():
        out.write(f'{state}\t{level}\t{face}\t{dir}\t{result}\n')
