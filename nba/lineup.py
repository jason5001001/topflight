import operator as op
from ortools.linear_solver import pywraplp
from nba.models import *

import pdb
class Roster:
    POSITION_ORDER = {
        "PG": 0,
        "SG": 1,
        "SF": 2,
        "PF": 3,
        "C": 4
    }

    def __init__(self, ds):
        self.players = []
        self.ds = ds

    def add_player(self, player):
        self.players.append(player)

    def get_num_teams(self):
        teams = set([ii.team for ii in self.players])
        return len(teams)

    def is_member(self, player):
        return player.id in [ii.id for ii in self.players]

    def spent(self):
        return sum(map(lambda x: getattr(x, ATTR[self.ds]['salary']), self.players))

    def projected(self):
        return sum(map(lambda x: getattr(x, ATTR[self.ds]['projection']), self.players))

    def position_order(self, player):
        return self.POSITION_ORDER[player.position]

    def sorted_players(self):
        return sorted(self.players, key=self.position_order)

    def get_players(self):
        if self.ds == 'FanDuel': 
            return self.sorted_players()
        else:
            pos = ['PG', 'SG', 'SF', 'PF', 'C', 'PG,SG', 'SF,PF']
            players = list(self.players)
            players_ = []

            for ii in pos:
                for jj in players:
                    if jj.position in ii:
                        players_.append(jj)
                        players.remove(jj)
                        break
            return players_ + players

    def __repr__(self):
        s = '\n'.join(str(x) for x in self.sorted_players())
        s += "\n\nProjected Score: %s" % self.projected()
        s += "\tCost: $%s" % self.spent()
        return s


POSITION_LIMITS = {
    'FanDuel': [
        ["PG", 2, 2],
        ["SG", 2, 2],
        ["SF", 2, 2],
        ["PF", 2, 2],
        ["C", 1, 1]
    ],
    'DraftKings': [
        ["PG", 1, 3],
        ["SG", 1, 3],
        ["SF", 1, 3],
        ["PF", 1, 3],
        ["C", 1, 2],
        ["PG,SG", 3, 4],
        ["SF,PF", 3, 4]
    ]
}

ROSTER_SIZE = {
    'FanDuel': 9,
    'DraftKings': 8,
}

TEAM_LIMIT = {
    'FanDuel': 3,
    'DraftKings': 2
}

def get_lineup(ds, players, teams, locked, ban, max_point, con_mul, min_salary, max_salary, min_team_member, max_team_member):
    solver = pywraplp.Solver('nba-lineup', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    variables = []

    for i, player in enumerate(players):
        if player.id in locked and ds != 'DraftKings':
            variables.append(solver.IntVar(1, 1, str(player)+str(i)))
        elif player.id in ban:
            variables.append(solver.IntVar(0, 0, str(player)+str(i)))
        else:
            variables.append(solver.IntVar(0, 1, str(player)+str(i)))

    objective = solver.Objective()
    objective.SetMaximization()

    # pdb.set_trace()
    for i, player in enumerate(players):
        objective.SetCoefficient(variables[i], float(getattr(player, ATTR[ds]['projection'])))

    salary_cap = solver.Constraint(min_salary, max_salary)
    for i, player in enumerate(players):
        salary_cap.SetCoefficient(variables[i], getattr(player, ATTR[ds]['salary']))

    point_cap = solver.Constraint(0, max_point)
    for i, player in enumerate(players):
        point_cap.SetCoefficient(variables[i], float(getattr(player, ATTR[ds]['projection'])))

    position_limits = POSITION_LIMITS[ds]
    for position, min_limit, max_limit in position_limits:
        position_cap = solver.Constraint(min_limit, max_limit)

        for i, player in enumerate(players):
            if player.position in position:
                position_cap.SetCoefficient(variables[i], 1)

    # no more than n players from one team (fanduel)
    if max_team_member != ROSTER_SIZE[ds]:
        for team in teams:
            team_cap = solver.Constraint(min_team_member, max_team_member)
            for i, player in enumerate(players):
                if team == player.team:
                    team_cap.SetCoefficient(variables[i], 1)

    if ds == 'DraftKings':    # multi positional constraints
        for ii in con_mul:
            if players[ii[0]].id in locked:
                mul_pos_cap = solver.Constraint(1, 1)
            else:
                mul_pos_cap = solver.Constraint(0, 1)

            for jj in ii:
                mul_pos_cap.SetCoefficient(variables[jj], 1)

    size_cap = solver.Constraint(ROSTER_SIZE[ds], ROSTER_SIZE[ds])
    for variable in variables:
        size_cap.SetCoefficient(variable, 1)

    solution = solver.Solve()

    if solution == solver.OPTIMAL:
        roster = Roster(ds)

        for i, player in enumerate(players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        return roster


def get_num_lineups(player, lineups):
    num = 0
    for ii in lineups:
        if ii.is_member(player):
            num = num + 1
    return num

def get_exposure(players, lineups):
    result = {}
    for ii in players:
        result[ii.id] = get_num_lineups(ii, lineups)
    return result


def calc_lineups(players, num_lineups, locked, ds, min_salary, max_salary, min_team_member, max_team_member, exposure):
    result = []

    max_point = 10000
    teams = set([ii.team for ii in players])

    # pdb.set_trace()

    con_mul = []
    if ds == 'DraftKings':      # multi positional in DraftKings
        players_ = []
        idx = 0
        for ii in players:
            if ii.draftkings_position:
                p = vars(ii)
                p.pop('_state')
                ci_ = []
                for jj in ii.draftkings_position.split('/'):
                    ci_.append(idx)
                    p['position'] = jj
                    players_.append(Player(**p))
                    idx += 1
                con_mul.append(ci_)
        players = players_

    # for min exposure
    for id, val in exposure.items():
        if val['min']:
            while True:
                cur_exps = get_exposure(players, result)
                _ban = []
                for pid, exp in cur_exps.items():
                    if exp == exposure[pid]['max'] and pid not in ban:
                        ban.append(pid)
                    elif exp >= exposure[pid]['min']:
                        _ban = [pid]

                if cur_exps[id] >= val['min']:
                    break
                    
                _locked = [id]
                roster = get_lineup(ds, players, teams, locked+_locked, ban+_ban, max_point, con_mul, min_salary, max_salary, min_team_member, max_team_member)

                if not roster:
                    return result

                max_point = float(roster.projected()) - 0.001
                if roster.get_num_teams() >= TEAM_LIMIT[ds]:
                    result.append(roster)
                    if len(result) == num_lineups:
                        return result

    for id, val in exposure.items():
        while True:
            cur_exps = get_exposure(players, result)
            for pid, exp in cur_exps.items():
                if exp == exposure[pid]['max'] and pid not in ban:
                    ban.append(pid)

            if cur_exps[id] == val['max']:
                break

            _locked = [id]
            roster = get_lineup(ds, players, teams, locked+_locked, ban, max_point, con_mul, min_salary, max_salary, min_team_member, max_team_member)

            if not roster:
                return result

            max_point = float(roster.projected()) - 0.001
            if roster.get_num_teams() >= TEAM_LIMIT[ds]:
                result.append(roster)
                if len(result) == num_lineups:
                    return result

    return result
