from __future__ import unicode_literals

from django.db import models

ATTR = {
    'FanDuel': {
        'projection': 'avg_projection_fd',
        'salary': 'salary',
        'position': 'position'
    },
    'DraftKings': {
        'projection': 'avg_projection_dk',
        'salary': 'dk_salary',
        'position': 'draftkings_position'
    }
}


class Player(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=12)
    position = models.CharField(db_column='Position', max_length=5, blank=True, null=True)
    first_name = models.CharField(db_column='First_Name', max_length=12, blank=True, null=True)
    nickname = models.CharField(db_column='Nickname', max_length=25, blank=True, null=True)
    last_name = models.CharField(db_column='Last_Name', max_length=25, blank=True, null=True)
    fppg = models.DecimalField(db_column='FPPG', max_digits=12, decimal_places=2, blank=True, null=True)
    played = models.IntegerField(db_column='Played', blank=True, null=True)
    salary = models.IntegerField(db_column='Salary', blank=True, null=True)
    game = models.CharField(db_column='Game', max_length=12, blank=True, null=True)
    team = models.CharField(db_column='Team', max_length=5, blank=True, null=True)
    opponent = models.CharField(db_column='Opponent', max_length=5, blank=True, null=True)
    dk_salary = models.IntegerField(db_column='DK_Salary', blank=True, null=True)
    rotogrinders_fd = models.DecimalField(db_column='Rotogrinders_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    rotogrinders_dk = models.DecimalField(db_column='RotoGrinders_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    numberfire_fd = models.DecimalField(db_column='NumberFire_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    numberfire_dk = models.DecimalField(db_column='NumberFire_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    linestar_fd = models.DecimalField(db_column='LineStar_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    linestar_dk = models.IntegerField(db_column='LineStar_DK', blank=True, null=True)
    fantasy_cruncher_fanduel = models.DecimalField(db_column='Fantasy_Cruncher_FanDuel', max_digits=12, decimal_places=2, blank=True, null=True)
    fantasy_cruncher_dk = models.DecimalField(db_column='Fantasy_Cruncher_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    avg_projection_fd = models.DecimalField(db_column='Avg._Projection_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    avg_projection_dk = models.DecimalField(db_column='Avg._Projection_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    vegas_implied = models.DecimalField(db_column='Vegas_Implied', max_digits=12, decimal_places=2, blank=True, null=True)
    rotogrinders_name = models.CharField(db_column='RotoGrinders_Name', max_length=25, blank=True, null=True)
    number_fire_name = models.CharField(db_column='Number_Fire_Name', max_length=25, blank=True, null=True)
    fsc_name = models.CharField(db_column='FSC_Name', max_length=25, blank=True, null=True)
    fantasy_cruncher_name = models.CharField(db_column='Fantasy_Cruncher_Name', max_length=25, blank=True, null=True)
    reference_name = models.CharField(db_column='Reference_Name', max_length=25, blank=True, null=True)
    nf_minutes = models.DecimalField(db_column='NF_Minutes', max_digits=12, decimal_places=2, blank=True, null=True)
    fc_minutes = models.DecimalField(db_column='FC_Minutes', max_digits=12, decimal_places=2, blank=True, null=True)
    minute_projection = models.DecimalField(db_column='Minute_Projection', max_digits=12, decimal_places=2, blank=True, null=True)
    fd_value = models.FloatField(db_column='FD_Value', blank=True, null=True)
    dk_value = models.FloatField(db_column='DK_Value', blank=True, null=True)
    vegas_opp_implied = models.FloatField(db_column='Vegas_Opp._Implied', blank=True, null=True)
    over_under = models.FloatField(db_column='Over/Under', blank=True, null=True)
    dvp = models.IntegerField(db_column='DVP', blank=True, null=True)
    consistency = models.IntegerField(db_column='Consistency', blank=True, null=True)
    fast_break_points = models.FloatField(db_column='Fast_Break_Points', blank=True, null=True)
    fast_break_points_team_rank = models.IntegerField(db_column='Fast_Break_Points_Team_Rank', blank=True, null=True)
    points_in_the_paint = models.FloatField(db_column='Points_in_the_Paint', blank=True, null=True)
    points_in_the_paint_team_rank = models.IntegerField(db_column='Points_in_the_Paint_Team_Rank', blank=True, null=True)
    points_off_turnovers = models.FloatField(db_column='Points_off_Turnovers', blank=True, null=True)
    points_off_turnovers_team_rank = models.IntegerField(db_column='Points_off_Turnovers_Team_Rank', blank=True, null=True)
    number_2nd_chance_points = models.FloatField(db_column='2nd_Chance_Points', blank=True, null=True)
    number_2nd_chance_points_team_rank = models.IntegerField(db_column='2nd_Chance_Points_Team_Rank', blank=True, null=True)
    number_3_pt_shooting_percentage = models.FloatField(db_column='3_Pt_Shooting_Percentage', blank=True, null=True)
    number_3_pt_shooting_percentage_team_rank = models.IntegerField(db_column='3_Pt_Shooting_Percentage_Team_Rank', blank=True, null=True)
    player_pace = models.FloatField(db_column='Player_Pace', blank=True, null=True)
    player_pace_team_rank = models.IntegerField(db_column='Player_Pace_Team_Rank', blank=True, null=True)
    player_offensive_rating = models.FloatField(db_column='Player_Offensive_Rating', blank=True, null=True)
    player_offensive_rating_team_rank = models.IntegerField(db_column='Player_Offensive_Rating_Team_Rank', blank=True, null=True)
    personal_fouls_drawn = models.FloatField(db_column='Personal_Fouls_Drawn', blank=True, null=True)
    personal_fouls_drawn_team_rank = models.IntegerField(db_column='Personal_Fouls_Drawn_Team_Rank', blank=True, null=True)
    draftkings_position = models.CharField(db_column='DraftKings_Position', max_length=45, blank=True, null=True)
    draftkings_name_id = models.CharField(db_column='DraftKings_NameID', max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_topflight'

    def __str__(self):
    	return self.id
 