from enum import Enum
import copy
import numpy as np
import pandas as pd


class Action(Enum):
    TURN_LEFT = 1
    TURN_RIGHT = 2
    TURN_UP = 3
    TURN_DOWN = 4
    MOVE_FORWARD = 5
    GRAB_GOLD = 6
    PERCEIVE_BREEZE = 7
    PERCEIVE_STENCH = 8
    SHOOT = 9
    KILL_WUMPUS = 10
    KILL_NO_WUMPUS = 11
    BE_EATEN_BY_WUMPUS = 12
    FALL_INTO_PIT = 13
    KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD = 14
    CLIMB_OUT_OF_THE_CAVE = 15
    DETECT_PIT = 16
    DETECT_WUMPUS = 17
    DETECT_NO_PIT = 18
    DETECT_NO_WUMPUS = 19
    INFER_PIT = 20
    INFER_NOT_PIT = 21
    INFER_WUMPUS = 22
    INFER_NOT_WUMPUS = 23
    DETECT_SAFE = 24
    INFER_SAFE = 25
    PERCEIVE_GAS = 26
    DETECT_GAS = 27
    DETECT_NO_GAS = 28
    INFER_GAS = 29
    INFER_NOT_GAS = 30
    PERCEIVE_POTION = 31
    GRAB_POTION = 32


class AgentBrain:
    def __init__(self, map_filename, output_filename):
        self.output_filename = output_filename

        self.map_size = None
        self.cell_matrix = None
        self.init_cell_matrix = None

        self.cave_cell = {'pos': (-1, -1), 'value': 'EMPTY'}
        self.agent_cell = None
        self.init_agent_cell = None
        self.KB = pd.DataFrame()
        self.path = []
        self.action_list = []
        self.score = 0

        self.read_map(map_filename)

    def read_map(self, map_filename):
        with open(map_filename, 'r') as file:
            self.map_size = int(file.readline())
            raw_map = [line.split('.') for line in file.read().splitlines()]

        self.cell_matrix = np.empty((self.map_size, self.map_size), dtype=object)
        for ir in range(self.map_size):
            for ic in range(self.map_size):
                self.cell_matrix[ir][ic] = {'pos': (ir, ic), 'value': raw_map[ir][ic]}
                if 'AGENT' in raw_map[ir][ic]:
                    self.agent_cell = self.cell_matrix[ir][ic]
                    self.agent_cell['parent'] = self.cave_cell
                    self.init_agent_cell = copy.deepcopy(self.agent_cell)

        self.init_cell_matrix = copy.deepcopy(self.cell_matrix)

        result, pos = self.is_valid_map()
        if not result:
            if pos is None:
                raise TypeError('Input Error: The map is invalid! There is no Agent!')
            raise TypeError('Input Error: The map is invalid! Please check at row ' + str(pos[0]) + ' and column ' + str(pos[1]) + '.')

    def is_valid_map(self):
        for cell_row in self.cell_matrix:
            for cell in cell_row:
                adj_cell_list = self.get_adj_cell_list(cell)
                if 'PIT' in cell['value']:
                    for adj_cell in adj_cell_list:
                        if 'BREEZE' not in adj_cell['value']:
                            return False, cell['pos']
                if 'WUMPUS' in cell['value']:
                    for adj_cell in adj_cell_list:
                        if 'STENCH' not in adj_cell['value']:
                            return False, cell['pos']
        if self.agent_cell is None:
            return False, None
        return True, None

    def get_adj_cell_list(self, cell):
        adj_cells = []
        row, col = cell['pos']
        for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= r < self.map_size and 0 <= c < self.map_size:
                adj_cells.append(self.cell_matrix[r][c])
        return adj_cells

    def append_event_to_output_file(self, text: str):
        with open(self.output_filename, 'a') as out_file:
            out_file.write(text + '\n')

    def add_action(self, action):
        self.action_list.append(action)
        print(action)
        self.append_event_to_output_file(action.name)

        if action == Action.TURN_LEFT:
            self.score -= 10
        elif action == Action.TURN_RIGHT:
            self.score -= 10
        elif action == Action.TURN_UP:
            self.score -= 10
        elif action == Action.TURN_DOWN:
            self.score -= 10
        elif action == Action.MOVE_FORWARD:
            self.score -= 10
        elif action == Action.GRAB_GOLD:
            self.score += 5000
        elif action == Action.GRAB_POTION:
            self.score += 50
        elif action == Action.SHOOT:
            self.score -= 100
        elif action == Action.BE_EATEN_BY_WUMPUS:
            self.score -= 10000
        elif action == Action.FALL_INTO_PIT:
            self.score -= 10000
        elif action == Action.CLIMB_OUT_OF_THE_CAVE:
            self.score += 10
        # Các hành động khác
        print('Score: ' + str(self.score))
        self.append_event_to_output_file('Score: ' + str(self.score))

    def add_new_percepts_to_KB(self, cell):
        adj_cell_list = self.get_adj_cell_list(cell)

        sign = '-'
        if 'PIT' in cell['value']:
            sign = '+'
            self.KB = self.KB.append({'literal': cell['pos'], 'type': 'WUMPUS', 'sign': '-'}, ignore_index=True)
        self.KB = self.KB.append({'literal': cell['pos'], 'type': 'PIT', 'sign': sign}, ignore_index=True)
        sign_pit = sign

        sign = '-'
        if 'WUMPUS' in cell['value']:
            sign = '+'
            self.KB = self.KB.append({'literal': cell['pos'], 'type': 'PIT', 'sign': '-'}, ignore_index=True)
        self.KB = self.KB.append({'literal': cell['pos'], 'type': 'WUMPUS', 'sign': sign}, ignore_index=True)
        sign_wumpus = sign

        if sign_pit == sign_wumpus == '+':
            raise TypeError('Logic Error: Pit và Wumpus không thể xuất hiện cùng một ô.')

        sign = '-'
        if 'BREEZE' in cell['value']:
            sign = '+'
        self.KB = self.KB.append({'literal': cell['pos'], 'type': 'BREEZE', 'sign': sign}, ignore_index=True)

        sign = '-'
        if 'STENCH' in cell['value']:
            sign = '+'
        self.KB = self.KB.append({'literal': cell['pos'], 'type': 'STENCH', 'sign': sign}, ignore_index=True)

        sign = '-'
        if 'GAS' in cell['value']:
            sign = '+'
        self.KB = self.KB.append({'literal': cell['pos'], 'type': 'GAS', 'sign': sign}, ignore_index=True)

        sign = '-'
        if 'POTION' in cell['value']:
            sign = '+'
        self.KB = self.KB.append({'literal': cell['pos'], 'type': 'POTION', 'sign': sign}, ignore_index=True)

        if 'BREEZE' in cell['value']:
            clause = [{'literal': cell['pos'], 'type': 'BREEZE', 'sign': '-'}]
            for adj_cell in adj_cell_list:
                clause.append({'literal': adj_cell['pos'], 'type': 'PIT', 'sign': '+'})
            self.KB = self.KB.append(clause, ignore_index=True)

            for adj_cell in adj_cell_list:
                clause = [{'literal': cell['pos'], 'type': 'BREEZE', 'sign': '+'}, {'literal': adj_cell['pos'], 'type': 'PIT', 'sign': '-'}]
                self.KB = self.KB.append(clause, ignore_index=True)
        else:
            for adj_cell in adj_cell_list:
                clause = [{'literal': adj_cell['pos'], 'type': 'PIT', 'sign': '-'}]
                self.KB = self.KB.append(clause, ignore_index=True)

        if 'STENCH' in cell['value']:
            clause = [{'literal': cell['pos'], 'type': 'STENCH', 'sign': '-'}]
            for adj_cell in adj_cell_list:
                clause.append({'literal': adj_cell['pos'], 'type': 'WUMPUS', 'sign': '+'})
            self.KB = self.KB.append(clause, ignore_index=True)

            for adj_cell in adj_cell_list:
                clause = [{'literal': cell['pos'], 'type': 'STENCH', 'sign': '+'}, {'literal': adj_cell['pos'], 'type': 'WUMPUS', 'sign': '-'}]
                self.KB = self.KB.append(clause, ignore_index=True)
        else:
            for adj_cell in adj_cell_list:
                clause = [{'literal': adj_cell['pos'], 'type': 'WUMPUS', 'sign': '-'}]
                self.KB = self.KB.append(clause, ignore_index=True)

        if 'GAS' in cell['value']:
            clause = [{'literal': cell['pos'], 'type': 'GAS', 'sign': '-'}]
            for adj_cell in adj_cell_list:
                clause.append({'literal': adj_cell['pos'], 'type': 'GAS_SOURCE', 'sign': '+'})
            self.KB = self.KB.append(clause, ignore_index=True)

            for adj_cell in adj_cell_list:
                clause = [{'literal': cell['pos'], 'type': 'GAS', 'sign': '+'}, {'literal': adj_cell['pos'], 'type': 'GAS_SOURCE', 'sign': '-'}]
                self.KB = self.KB.append(clause, ignore_index=True)
        else:
            for adj_cell in adj_cell_list:
                clause = [{'literal': adj_cell['pos'], 'type': 'GAS_SOURCE', 'sign': '-'}]
                self.KB = self.KB.append(clause, ignore_index=True)

        print(self.KB)
        self.append_event_to_output_file(str(self.KB))

    def backtracking_search(self):
        if 'PIT' in self.agent_cell['value']:
            self.add_action(Action.FALL_INTO_PIT)
            return False

        if 'WUMPUS' in self.agent_cell['value']:
            self.add_action(Action.BE_EATEN_BY_WUMPUS)
            return False

        if 'GOLD' in self.agent_cell['value']:
            self.add_action(Action.GRAB_GOLD)
            self.agent_cell['value'].remove('GOLD')

        if 'BREEZE' in self.agent_cell['value']:
            self.add_action(Action.PERCEIVE_BREEZE)

        if 'STENCH' in self.agent_cell['value']:
            self.add_action(Action.PERCEIVE_STENCH)

        if 'GAS' in self.agent_cell['value']:
            self.add_action(Action.PERCEIVE_GAS)

        if 'POTION' in self.agent_cell['value']:
            self.add_action(Action.GRAB_POTION)
            self.agent_cell['value'].remove('POTION')

        if not self.agent_cell.get('explored', False):
            self.agent_cell['explored'] = True
            self.add_new_percepts_to_KB(self.agent_cell)

        valid_adj_cell_list = self.get_adj_cell_list(self.agent_cell)

        if self.agent_cell.get('parent') in valid_adj_cell_list:
            valid_adj_cell_list.remove(self.agent_cell.get('parent'))

        pre_agent_cell = self.agent_cell

        if not self.agent_cell.get('is_OK', True):
            temp_adj_cell_list = []
            for valid_adj_cell in valid_adj_cell_list:
                if valid_adj_cell.get('explored') and 'PIT' in valid_adj_cell['value']:
                    temp_adj_cell_list.append(valid_adj_cell)
            for adj_cell in temp_adj_cell_list:
                valid_adj_cell_list.remove(adj_cell)

            temp_adj_cell_list = []

            if 'STENCH' in self.agent_cell['value']:
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell['pos'])
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell['pos']))
                    self.turn_to(valid_adj_cell)

                    self.add_action(Action.INFER_WUMPUS)
                    not_alpha = [[valid_adj_cell['pos'], 'WUMPUS', '-']]
                    have_wumpus = self.KB.query('WUMPUS == "+"').empty

                    if have_wumpus:
                        self.add_action(Action.DETECT_WUMPUS)
                        self.add_action(Action.SHOOT)
                        self.add_action(Action.KILL_WUMPUS)
                        valid_adj_cell['value'].remove('WUMPUS')
                        self.append_event_to_output_file('KB: ' + str(self.KB))
                    else:
                        self.add_action(Action.INFER_NOT_WUMPUS)
                        not_alpha = [[valid_adj_cell['pos'], 'WUMPUS', '+']]
                        have_no_wumpus = self.KB.query('WUMPUS == "-"').empty

                        if have_no_wumpus:
                            self.add_action(Action.DETECT_NO_WUMPUS)
                        else:
                            temp_adj_cell_list.append(valid_adj_cell)

            if 'STENCH' in self.agent_cell['value']:
                adj_cell_list = self.get_adj_cell_list(self.agent_cell)
                if self.agent_cell.get('parent') in adj_cell_list:
                    adj_cell_list.remove(self.agent_cell.get('parent'))

                explored_cell_list = [adj_cell for adj_cell in adj_cell_list if adj_cell.get('explored')]
                for explored_cell in explored_cell_list:
                    adj_cell_list.remove(explored_cell)

                for adj_cell in adj_cell_list:
                    print("Try: ", end='')
                    print(adj_cell['pos'])
                    self.append_event_to_output_file('Try: ' + str(adj_cell['pos']))
                    self.turn_to(adj_cell)

                    self.add_action(Action.SHOOT)
                    if 'WUMPUS' in adj_cell['value']:
                        self.add_action(Action.KILL_WUMPUS)
                        adj_cell['value'].remove('WUMPUS')
                        self.append_event_to_output_file('KB: ' + str(self.KB))

                    if 'STENCH' not in self.agent_cell['value']:
                        self.agent_cell['child_list'] = [adj_cell]
                        break

            if 'BREEZE' in self.agent_cell['value']:
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell['pos'])
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell['pos']))
                    self.turn_to(valid_adj_cell)

                    self.add_action(Action.INFER_PIT)
                    not_alpha = [[valid_adj_cell['pos'], 'PIT', '-']]
                    have_pit = self.KB.query('PIT == "+"').empty

                    if have_pit:
                        self.add_action(Action.DETECT_PIT)
                        valid_adj_cell['explored'] = True
                        self.add_new_percepts_to_KB(valid_adj_cell)
                        valid_adj_cell['parent'] = valid_adj_cell
                        temp_adj_cell_list.append(valid_adj_cell)
                    else:
                        self.add_action(Action.INFER_NOT_PIT)
                        not_alpha = [[valid_adj_cell['pos'], 'PIT', '+']]
                        have_no_pit = self.KB.query('PIT == "-"').empty

                        if have_no_pit:
                            self.add_action(Action.DETECT_NO_PIT)
                        else:
                            temp_adj_cell_list.append(valid_adj_cell)

            if 'GAS' in self.agent_cell['value']:
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell['pos'])
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell['pos']))
                    self.turn_to(valid_adj_cell)

                    self.add_action(Action.INFER_GAS)
                    not_alpha = [[valid_adj_cell['pos'], 'GAS_SOURCE', '-']]
                    have_gas = self.KB.query('GAS_SOURCE == "+"').empty

                    if have_gas:
                        self.add_action(Action.DETECT_GAS)
                        valid_adj_cell['value'].append('GAS_SOURCE')
                        self.append_event_to_output_file('KB: ' + str(self.KB))
                    else:
                        self.add_action(Action.INFER_NOT_GAS)
                        not_alpha = [[valid_adj_cell['pos'], 'GAS_SOURCE', '+']]
                        have_no_gas = self.KB.query('GAS_SOURCE == "-"').empty

                        if have_no_gas:
                            self.add_action(Action.DETECT_NO_GAS)
                        else:
                            temp_adj_cell_list.append(valid_adj_cell)

        temp_adj_cell_list = list(set(temp_adj_cell_list))

        for adj_cell in temp_adj_cell_list:
            valid_adj_cell_list.remove(adj_cell)
        self.agent_cell['child_list'] = valid_adj_cell_list

        for next_cell in self.agent_cell['child_list']:
            self.move_to(next_cell)
            print("Move to: ", end='')
            print(self.agent_cell['pos'])
            self.append_event_to_output_file('Move to: ' + str(self.agent_cell['pos']))

            if not self.backtracking_search():
                return False

            self.move_to(pre_agent_cell)
            print("Backtrack: ", end='')
            print(pre_agent_cell['pos'])
            self.append_event_to_output_file('Backtrack: ' + str(pre_agent_cell['pos']))

        return True

    def solve_wumpus_world(self):
        with open(self.output_filename, 'w'):
            pass

        self.backtracking_search()

        victory_flag = True
        for cell_row in self.cell_matrix:
            for cell in cell_row:
                if 'GOLD' in cell['value'] or 'WUMPUS' in cell['value']:
                    victory_flag = False
                    break
        if victory_flag:
            self.add_action(Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)

        if self.agent_cell.get('parent') == self.cave_cell:
            self.add_action(Action.CLIMB_OUT_OF_THE_CAVE)

        return self.action_list, self.init_agent_cell, self.init_cell_matrix
    
def get_path(self):
    # Khởi tạo lại tệp đầu ra
    with open(self.output_filename, 'w'):
        pass

    # Khởi chạy tìm kiếm bằng phương pháp backtracking
    self.backtracking_search()

    # Kiểm tra xem tác nhân có chiến thắng hay không
    victory_flag = True
    for cell_row in self.cell_matrix:
        for cell in cell_row:
            if 'GOLD' in cell['value'] or 'WUMPUS' in cell['value']:
                victory_flag = False
                break
    if victory_flag:
        self.add_action(Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)

    # Nếu tác nhân đã về lại vị trí ban đầu
    if self.agent_cell.get('parent') == self.cave_cell:
        self.add_action(Action.CLIMB_OUT_OF_THE_CAVE)

    # Tạo ra danh sách các vị trí mà tác nhân đã đi qua
    path = [self.init_agent_cell['pos']]
    for action in self.action_list:
        if action in [Action.MOVE_FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT, Action.TURN_UP, Action.TURN_DOWN]:
            path.append(self.agent_cell['pos'])

    return path
