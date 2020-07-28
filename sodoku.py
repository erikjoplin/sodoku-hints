with open('puzzle.csv') as f:
    p = f.readlines()

p = [line.strip().split(',') for line in p]
print(*p, sep = '\n')
print('\n')

def convert_to_boxes(p):
    boxes = list()
    count = 0
    box1 = list()
    box2 = list()
    box3 = list()
    for row in p:
        box1.extend(row[0:3])
        box2.extend(row[3:6])
        box3.extend(row[6:10])
        count += 1
        if count % 3 == 0:
            boxes.append(box1)
            boxes.append(box2)
            boxes.append(box3)
            box1 = list()
            box2 = list()
            box3 = list()
    return boxes

def get_box_number(row_number, col):
    return (row_number//3)*3 + (col//3)

def inverse_box_number(box_number):
    output = list()
    for rows in range(9):
        for cols in range(9) :
            if get_box_number(rows, cols) == box_number:
                output.append((rows, cols))
    return output

def transpose(p):
    p_t = [['' for i in range(9)] for j in range(9)]
    for row_index in range(9):
        for col_index in range(9):
            p_t[col_index][row_index] = p[row_index][col_index]
    return p_t

def inverse_transpose(p_t):
    p = [['' for i in range(9)] for j in range(9)]
    for row_index in range(9):
        for col_index in range(9):
            p[col_index][row_index] = p_t[row_index][col_index]
    return p

def hidden_single_box(p):
    boxes = convert_to_boxes(p)
    for i in range(9):
        box = boxes[i]
        positions = inverse_box_number(i)
        for num in range(1,10):
            if str(num) in box:
                continue
            count = 0
            valid = True
            for cell in positions:
                if not p[cell[0]][cell[1]]:
                    row = p[cell[0]]
                    col = [j[cell[1]] for j in p]
                    if ((str(num) not in row) and (str(num) not in col)):
                        count += 1
                        save = cell
                    if count > 1:
                        valid = False
                        break

            if valid:
                return [num, save]             
    return False

def hidden_single_row(p):
    boxes = convert_to_boxes(p)
    for row_index in range(9):
        row = p[row_index]
        for num in range(1,10):
            if str(num) in row:
                continue
            count = 0
            valid = True
            for col_index in range(9):
                cell = row[col_index]
                if not cell:
                    col = [j[col_index] for j in p]
                    box_number = get_box_number(row_index, col_index)
                    box = boxes[box_number]
                    if ((str(num) not in box) and (str(num) not in col)):
                        count += 1
                        save = (row_index, col_index)
                    if count > 1:
                        valid = False
            if valid:
                return [num, save]
    return False

def naked_single(p):
    boxes = convert_to_boxes(p)
    for row in range(len(p)):
        for cell in range(len(p[row])):
            if p[row][cell]:
                continue
            cell_row = p[row]
            cell_column = [j[cell] for j in p]
            cell_box = boxes[get_box_number(row, cell)]
            rcb = sorted(set(cell_row + cell_column + cell_box))
            rcb.remove('')
            if len(rcb) == 8:
                nums = [str(i) for i in range(1,10)]
                single = sorted(set(nums).difference(rcb))
                return [single[0], (row, cell)]
    return False

def solve_puzzle(p):
    q = p.copy()
    while True:
        hsb = hidden_single_box(q)
        if hsb:
            row = hsb[1][0]
            col = hsb[1][1]
            q[row][col] = str(hsb[0])
            print("hidden single")
            print(str(hsb[0]) +" goes in row: " + str(row) + " and col: " + str(col))
            print(*q, sep = '\n')
        hsr = hidden_single_row(q)
        if hsr:
            row = hsr[1][0]
            col = hsr[1][1]
            q[row][col] = str(hsr[0])
            print("hidden single")
            print(str(hsr[0]) +" goes in row: " + str(row) + " and col: " + str(col))
            print(*q, sep = '\n')
        q_t = transpose(q)
        hsc = hidden_single_row(q_t)
        if hsc:
            row = hsc[1][1]
            col = hsc[1][0]
            q[row][col] = str(hsc[0])
            print("naked single")
            print(str(hsc[0]) +" goes in row: " + str(row) + " and col: " + str(col))
            print(*q, sep = '\n')
        ns = naked_single(q)
        if ns:
            row = ns[1][0]
            col = ns[1][1]
            q[row][col] = str(ns[0])
            print(str(ns[0]) +" goes in row: " + str(row) + " and col: " + str(col))
            print(*q, sep = '\n')
        if (not ns) and (not hsb) and (not hsr) and (not hsc):
            print('------------------')
            return q
        

solve = solve_puzzle(p)
print(*solve, sep = '\n')