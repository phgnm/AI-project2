from enum import Enum
import copy
import cells
import knowledge


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
    PERCEIVE_WHIFF = 26
    DETECT_GAS = 27
    DETECT_NO_GAS = 28
    INFER_GAS = 29
    INFER_NOT_GAS = 30
    PERCEIVE_GLOW = 31
    GRAB_POTION = 32
    HEAL = 33
    SNIFF_GAS = 34


class AgentBrain:
    def __init__(self, map_filename, output_filename):
        self.output_filename = output_filename

        self.map_size = None
        self.cell_matrix = None
        self.init_cell_matrix = None

        self.cave_cell = cells.Cell((-1, -1), 10, cells.Object.EMPTY.value)
        self.agent_cell = None
        self.init_agent_cell = None
        self.KB = knowledge.knowledgeBase()
        self.path = []
        self.action_list = []
        self.score = 0

        self.read_map(map_filename)

    def read_map(self, map_filename):
        with open(map_filename, 'r') as file:
            self.map_size = int(file.readline())
            raw_map = [line.split('.') for line in file.read().splitlines()]

        self.cell_matrix = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        for ir in range(self.map_size):
            for ic in range(self.map_size):
                self.cell_matrix[ir][ic] = cells.Cell((ir, ic), self.map_size, raw_map[ir][ic])
                if cells.Object.AGENT.value in raw_map[ir][ic]:
                    self.agent_cell = self.cell_matrix[ir][ic]
                    self.agent_cell.update_parent(self.cave_cell)
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
                adj_cell_list = cell.get_adj_cell_list(self.cell_matrix)
                if cell.exist_pit():
                    for adj_cell in adj_cell_list:
                        if not adj_cell.exist_breeze():
                            return False, cell.matrix_pos
                if cell.exist_wumpus():
                    for adj_cell in adj_cell_list:
                        if not adj_cell.exist_stench():
                            return False, cell.matrix_pos
        if self.agent_cell is None:
            return False, None
        return True, None

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
            self.count_potion += 1 
        elif action == Action.SHOOT:
            self.score -= 100
        elif action == Action.BE_EATEN_BY_WUMPUS:
            self.score -= 10000
        elif action == Action.FALL_INTO_PIT:
            self.score -= 10000
        elif action == Action.CLIMB_OUT_OF_THE_CAVE:
            self.score += 10
            print('Score: ' + str(self.score))
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.HEAL:
            if self.count_potion > 0 & self.health < self.MAX_HP :
                self.potion -= 1
                self.health += 1
                self.score -= 10
            elif self.count_potion == 0 :
                print('Logic Error: Bạn không có bình potion nào.')
            elif self.health == self.MAX_HP :
                print('Logic Error: Bạn đang có 100% HP.')
        # Các hành động khác
        elif action == Action.DETECT_PIT:
            pass
        elif action == Action.DETECT_WUMPUS:
            pass
        elif action == Action.DETECT_NO_PIT:
            pass
        elif action == Action.DETECT_NO_WUMPUS:
            pass
        elif action == Action.INFER_PIT:
            pass
        elif action == Action.INFER_NOT_PIT:
            pass
        elif action == Action.INFER_WUMPUS:
            pass
        elif action == Action.INFER_NOT_WUMPUS:
            pass
        elif action == Action.DETECT_SAFE:
            pass
        elif action == Action.INFER_SAFE:
            pass
        elif action == Action.DETECT_GAS:
            pass
        elif action == Action.INFER_GAS:
            pass
        elif action == Action.INFER_NOT_GAS:
            pass
        elif action == Action.PERCEIVE_BREEZE:
            pass
        elif action == Action.PERCEIVE_STENCH:
            pass
        elif action == Action.KILL_WUMPUS:
            pass
        elif action == Action.KILL_NO_WUMPUS:
            pass
        else:
            raise TypeError("Error: " + self.add_action.__name__)
        
    def add_new_percepts_to_KB(self, cell):
        adj_cell_list = cell.get_adj_cell_list(self.cell_matrix)

        sign = '-'
        if cell.exist_pit():
            sign = '+'
            self.KB.add_clause([cell.get_literal(cells.Object.WUMPUS, '-')])
        self.KB.add_clause([cell.get_literal(cells.Object.PIT, sign)])
        sign_pit = sign

        sign = '-'
        if cell.exist_wumpus():
            sign = '+'
            self.KB.add_clause([cell.get_literal(cells.Object.PIT, '-')])
        self.KB.add_clause([cell.get_literal(cells.Object.WUMPUS, sign)])
        sign_wumpus = sign

        if sign_pit == sign_wumpus == '+':
            raise TypeError('Logic Error: Pit and Wumpus can\'t be at the same cell.')

        sign = '-'
        if cell.exist_poison():
            sign = '+'
        self.KB.add_clause([cell.get_literal(cells.Object.POISON_GAS, sign)])

        sign = '-'
        if cell.exist_health_pot():
            sign = '+'
        self.KB.add_clause([cell.get_literal(cells.Object.HEALTH_POT, sign)])

        sign = '-'
        if cell.exist_breeze():
            sign = '+'
        self.KB.add_clause([cell.get_literal(cells.Object.BREEZE, sign)])

        sign = '-'
        if cell.exist_stench():
            sign = '+'
        self.KB.add_clause([cell.get_literal(cells.Object.STENCH, sign)])

        if cell.exist_breeze():
            # B => Pa v Pb v Pc v Pd
            clause = [cell.get_literal(cells.Object.BREEZE, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(cells.Object.PIT, '+'))
            self.KB.add_clause(clause)

            # Pa v Pb v Pc v Pd => B
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(cells.Object.BREEZE, '+'),
                          adj_cell.get_literal(cells.Object.PIT, '-')]
                self.KB.add_clause(clause)

        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(cells.Object.PIT, '-')]
                self.KB.add_clause(clause)
        
        if cell.exist_stench():
            # S => Wa v Wb v Wc v Wd
            clause = [cell.get_literal(cells.Object.STENCH, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(cells.Object.WUMPUS, '+'))
            self.KB.add_clause(clause)

            # Wa v Wb v Wc v Wd => S
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(cells.Object.STENCH, '+'),
                          adj_cell.get_literal(cells.Object.WUMPUS, '-')]
                self.KB.add_clause(clause)

        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(cells.Object.WUMPUS, '-')]
                self.KB.add_clause(clause)
        
        if cell.exist_whiff():
            # S => Wa v Wb v Wc v Wd
            clause = [cell.get_literal(cells.Object.WHIFF, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(cells.Object.POISON_GAS, '+'))
            self.KB.add_clause(clause)

            # Wa v Wb v Wc v Wd => S
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(cells.Object.WHIFF, '+'),
                          adj_cell.get_literal(cells.Object.POISON_GAS, '-')]
                self.KB.add_clause(clause)

        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(cells.Object.POISON_GAS, '-')]
                self.KB.add_clause(clause)

        print(self.KB.KB)
        self.append_event_to_output_file(str(self.KB.KB))
    def turn_to(self, next_cell):
        if next_cell.map_pos[0] == self.agent_cell.map_pos[0]:
            if next_cell.map_pos[1] - self.agent_cell.map_pos[1] == 1:
                self.add_action(Action.TURN_UP)
            else:
                self.add_action(Action.TURN_DOWN)
        elif next_cell.map_pos[1] == self.agent_cell.map_pos[1]:
            if next_cell.map_pos[0] - self.agent_cell.map_pos[0] == 1:
                self.add_action(Action.TURN_RIGHT)
            else:
                self.add_action(Action.TURN_LEFT)
        else:
            raise TypeError('Error: ' + self.turn_to.__name__)


    def move_to(self, next_cell):
        self.turn_to(next_cell)
        self.add_action(Action.MOVE_FORWARD)
        self.agent_cell = next_cell

    def backtracking_search(self):
        if self.agent_cell.exist_pit():
            self.add_action(Action.FALL_INTO_PIT)
            return False

        if self.agent_cell.exist_wumpus():
            self.add_action(Action.BE_EATEN_BY_WUMPUS)
            return False

        if self.agent_cell.exist_gold():
            self.add_action(Action.GRAB_GOLD)
            self.agent_cell.grab_gold()

        if self.agent_cell.exist_breeze():
            self.add_action(Action.PERCEIVE_BREEZE)

        if self.agent_cell.exist_stench():
            self.add_action(Action.PERCEIVE_STENCH)

        if self.agent_cell.exist_poison():
            self.add_action(Action.SNIFF_GAS)

        if self.agent_cell.exist_whiff():
            self.add_action(Action.PERCEIVE_WHIFF)

        if self.agent_cell.exist_glow():
            self.add_action(Action.PERCEIVE_GLOW)

        if self.agent_cell.exist_health_pot():
            self.add_action(Action.GRAB_POTION)
            self.agent_cell.grab_potion()

        if not self.agent_cell.is_explored():
            self.agent_cell.explore()
            self.add_new_percepts_to_KB(self.agent_cell)

        valid_adj_cell_list = self.agent_cell.get_adj_cell_list(self.cell_matrix)

        temp_adj_cell_list = []
        if self.agent_cell.parent in valid_adj_cell_list:
            valid_adj_cell_list.remove(self.agent_cell.parent)

        pre_agent_cell = self.agent_cell

        if not self.agent_cell.is_OK():
            temp_adj_cell_list = []
            for valid_adj_cell in valid_adj_cell_list:
                if valid_adj_cell.is_explored() and valid_adj_cell.exist_pit():
                    temp_adj_cell_list.append(valid_adj_cell)
            for adj_cell in temp_adj_cell_list:
                valid_adj_cell_list.remove(adj_cell)

            temp_adj_cell_list = []

            if self.agent_cell.exist_stench():
                valid_adj_cell: cells.Cell
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell.map_pos)
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    self.add_action(Action.INFER_WUMPUS)
                    not_alpha = [[valid_adj_cell.get_literal(cells.Object.WUMPUS, '-')]]
                    have_wumpus = self.KB.infer(not_alpha)

                    if have_wumpus:
                        self.add_action(Action.DETECT_WUMPUS)
                        self.add_action(Action.SHOOT)
                        self.add_action(Action.KILL_WUMPUS)
                        valid_adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))
                    else:
                        self.add_action(Action.INFER_NOT_WUMPUS)
                        not_alpha = [[valid_adj_cell.get_literal(cells.Object.WUMPUS, '+')]]
                        have_no_wumpus = self.KB.infer(not_alpha)

                        if have_no_wumpus:
                            self.add_action(Action.DETECT_NO_WUMPUS)
                        else:
                            if valid_adj_cell not in temp_adj_cell_list:
                                temp_adj_cell_list.append(valid_adj_cell)

            if self.agent_cell.exist_stench():
                adj_cell_list = self.agent_cell.get_adj_cell_list(self.cell_matrix)
                if self.agent_cell.parent in adj_cell_list:
                    adj_cell_list.remove(self.agent_cell.parent)

                explored_cell_list = []
                for adj_cell in adj_cell_list:
                    if adj_cell.is_explored():
                        explored_cell_list.append(adj_cell)
                for explored_cell in explored_cell_list:
                    adj_cell_list.remove(explored_cell)

                for adj_cell in adj_cell_list:
                    print("Try: ", end='')
                    print(adj_cell.map_pos)
                    self.append_event_to_output_file('Try: ' + str(adj_cell.map_pos))
                    self.turn_to(adj_cell)

                    self.add_action(Action.SHOOT)
                    if adj_cell.exist_wumpus():
                        self.add_action(Action.KILL_WUMPUS)
                        adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    if not self.agent_cell.exist_stench():
                        self.agent_cell.update_child_list([adj_cell])
                        break

            if self.agent_cell.exist_breeze():
                valid_adj_cell: cells.Cell
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell.map_pos)
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    # Infer Pit.
                    self.add_action(Action.INFER_PIT)
                    not_alpha = [[valid_adj_cell.get_literal(cells.Object.PIT, '-')]]
                    have_pit = self.KB.infer(not_alpha)

                    # If we can infer Pit.
                    if have_pit:
                        # Detect Pit.
                        self.add_action(Action.DETECT_PIT)

                        # Mark these cells as explored.
                        valid_adj_cell.explore()

                        # Add new percepts of these cells to the KB.
                        self.add_new_percepts_to_KB(valid_adj_cell)

                        # Update parent for this cell.
                        valid_adj_cell.update_parent(valid_adj_cell)

                        # Discard these cells from the valid_adj_cell_list.
                        temp_adj_cell_list.append(valid_adj_cell)

                    # If we can not infer Pit.
                    else:
                        # Infer not Pit.
                        self.add_action(Action.INFER_NOT_PIT)
                        not_alpha = [[valid_adj_cell.get_literal(cells.Object.PIT, '+')]]
                        have_no_pit = self.KB.infer(not_alpha)

                        # If we can infer not Pit.
                        if have_no_pit:
                            # Detect no Pit.
                            self.add_action(Action.DETECT_NO_PIT)

                        # If we can not infer not Pit.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            temp_adj_cell_list.append(valid_adj_cell)

            if self.agent_cell.exist_whiff():
                valid_adj_cell: cells.Cell
                for valid_adj_cell in valid_adj_cell_list:
                    print("Infer: ", end='')
                    print(valid_adj_cell.map_pos)
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    self.add_action(Action.INFER_GAS)
                    not_alpha = [[valid_adj_cell.get_literal(cells.Object.POISON_GAS, '-')]]
                    have_gas = self.KB.infer(not_alpha)

                    if have_gas:
                        self.add_action(Action.DETECT_GAS)

                        # Mark these cells as explored.
                        valid_adj_cell.explore()

                        # Add new percepts of these cells to the KB.
                        self.add_new_percepts_to_KB(valid_adj_cell)

                        # Update parent for this cell.
                        valid_adj_cell.update_parent(valid_adj_cell)

                        # Discard these cells from the valid_adj_cell_list.
                        temp_adj_cell_list.append(valid_adj_cell)

                    # If we can not infer Pit.
                    else:
                        # Infer not Pit.
                        self.add_action(Action.INFER_NOT_GAS)
                        not_alpha = [[valid_adj_cell.get_literal(cells.Object.POISON_GAS, '+')]]
                        have_no_gas = self.KB.infer(not_alpha)

                        # If we can infer not Pit.
                        if have_no_gas:
                            # Detect no Pit.
                            self.add_action(Action.DETECT_NO_GAS)

                        # If we can not infer not Pit.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            temp_adj_cell_list.append(valid_adj_cell)

        temp_adj_cell_list = list(set(temp_adj_cell_list))

        for adj_cell in temp_adj_cell_list:
            valid_adj_cell_list.remove(adj_cell)
        self.agent_cell.update_child_list(valid_adj_cell_list)

        for next_cell in self.agent_cell.child_list:
            self.move_to(next_cell)
            print("Move to: ", end='')
            print(self.agent_cell.map_pos)
            self.append_event_to_output_file('Move to: ' + str(self.agent_cell.map_pos))

            if not self.backtracking_search():
                return False

            self.move_to(pre_agent_cell)
            print("Backtrack: ", end='')
            print(pre_agent_cell.map_pos)
            self.append_event_to_output_file('Backtrack: ' + str(pre_agent_cell.map_pos))

        return True

    def solve_wumpus_world(self):
        with open(self.output_filename, 'w'):
            pass

        self.backtracking_search()

        victory_flag = True
        for cell_row in self.cell_matrix:
            for cell in cell_row:
                if cell.exist_gold() or cell.exist_wumpus():
                    victory_flag = False
                    break
        if victory_flag:
            self.add_action(Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)

        if self.agent_cell.parent == self.cave_cell:
            self.add_action(Action.CLIMB_OUT_OF_THE_CAVE)

        return self.action_list, self.init_agent_cell, self.init_cell_matrix

