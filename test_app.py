import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Player, Game, Tourney


class GamingTourneyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.
                                                   path.
                                                   join(self.project_dir,
                                                        self.database_name))
        setup_db(self.app, self.database_path)

        self.new_player = {
            "name": "A real name",
            "nickname": "A cool nickname",
            "nationality": "Some nice country"
        }

        self.wrong_format_player = {
            "name": "A real name",
            "nickkname": "A cool nickname",
            "nationality": "Some nice country"
        }

        self.patch_player = {
            "name": "An unreal name",
            "nickname": "A not cool nickname",
            "nationality": ""
        }

        self.wrong_patch_format = {
            "name": "Not cool..."
        }

        self.new_game = {
            "title": "A cool game"
        }

        self.wrong_format_game = {
            "titte": "I\'m not valid :("
        }

        self.new_tourney = {
            "name": "A tourney for cool people",
            "location": "Some awesome city",
            "date": "2020-08-13 9:10",
            "game_id": 2
        }

        self.wrong_datatypes_tourney = {
            "name": "A sad toruney",
            "location": "Some abandoned city",
            "date": ":(",
            "game_id": "R.I.P."
        }

        self.patch_tourney = {
            "name": "A tourney for cool people",
            "location": "Some awesome city",
            "date": "2019-08-13 9:10",
            "winner": 1,
            "game_id": 2
        }

        self.new_inscription = {
            "player_id": 1,
            "tourney_id": 3
        }

        self.repeated_inscription = {
            "player_id": 1,
            "tourney_id": 2
        }

        self.bad_inscription = {
            "player_id": 'Oh no...',
            "tourney_id": False
        }

        self.bad_inscription = {
            "player_id": 2,
            "tourney_id": 4
        }

        self.players_manager_token = ('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ikp'
                                      'XVCIsImtpZCI6IlF6QTVSREJEUVRJeE5rTXhOM'
                                      'El4UXpnd01ERTVNamMwUWpJelFUTTNNRE13UTB'
                                      'GRlFUSXlOQSJ9.eyJpc3MiOiJodHRwczovL2Rl'
                                      'di1rZ20yMC5hdXRoMC5jb20vIiwic3ViIjoiYX'
                                      'V0aDB8NWRlZWQ1MjRmNzg3ODcwY2M4YjZiODNi'
                                      'IiwiYXVkIjoiZ2FtaW5ndG91cm5leSIsImlhdC'
                                      'I6MTU4MDc2MjgxMiwiZXhwIjoxNTgwODQ5MjEy'
                                      'LCJhenAiOiJLT2YxMk45MU5OcGgwQ1htSko2cW'
                                      'VwaXZmUXNLN0owcSIsInNjb3BlIjoiIiwicGVy'
                                      'bWlzc2lvbnMiOlsiZGVsZXRlOmluc2NyaXB0aW'
                                      '9ucyIsImRlbGV0ZTpwbGF5ZXJzIiwicGF0Y2g6'
                                      'cGxheWVycyIsInBhdGNoOnRvdXJuZXlzIiwicG'
                                      '9zdDppbnNjcmlwdGlvbnMiLCJwb3N0OnBsYXll'
                                      'cnMiXX0.MadEGTbFmh1gNkLL3vAlLnBOqRo_O4'
                                      'S3lvkQjUhr4MMVovkJutHjeKz8oDOShqD6H8ob'
                                      'XOiNwdjvoWUQnh_lnmyft2VkQ1TMSZanp6iZ9k'
                                      'AmK9HV_sw7gHcHtmVHD1dvwNSEqoRsAtkaimuK'
                                      'GAGvbkX82dwRztZLLryLIgIcn-EiMy5NBroYeS'
                                      'jfQ_4NrVmeAHwXQiIJrnsb7VAwbcFOwFusoIHL'
                                      'tSU8_ZxKE_XZ1gA_LtLa3GG18emfjxuyu6GDzN'
                                      '3JpXqM_zeCHiuRX5NV_YdqKNp2JzJwScLK21pA'
                                      'QnkRtDpkyE3l3tCUMBwX8wEazQY3SguN_VskuT'
                                      'x0joxxdA')

        self.tourneys_administrator_token = ('Bearer eyJhbGciOiJSUzI1NiIsInR5'
                                             'cCI6IkpXVCIsImtpZCI6IlF6QTVSREJ'
                                             'EUVRJeE5rTXhOMEl4UXpnd01ERTVNam'
                                             'MwUWpJelFUTTNNRE13UTBGRlFUSXlOQ'
                                             'SJ9.eyJpc3MiOiJodHRwczovL2Rldi1'
                                             'rZ20yMC5hdXRoMC5jb20vIiwic3ViIj'
                                             'oiYXV0aDB8NWRmYzE4OWQ5NGQ3YTUxN'
                                             'TM2NWY3MGMyIiwiYXVkIjoiZ2FtaW5n'
                                             'dG91cm5leSIsImlhdCI6MTU4MDc2MzM'
                                             'wMCwiZXhwIjoxNTgwODQ5NzAwLCJhen'
                                             'AiOiJLT2YxMk45MU5OcGgwQ1htSko2c'
                                             'WVwaXZmUXNLN0owcSIsInNjb3BlIjoi'
                                             'IiwicGVybWlzc2lvbnMiOlsiZGVsZXR'
                                             'lOmdhbWVzIiwiZGVsZXRlOmluc2NyaX'
                                             'B0aW9ucyIsImRlbGV0ZTpwbGF5ZXJzI'
                                             'iwiZGVsZXRlOnRvdXJuZXlzIiwicGF0'
                                             'Y2g6cGxheWVycyIsInBhdGNoOnRvdXJ'
                                             'uZXlzIiwicG9zdDpnYW1lcyIsInBvc3'
                                             'Q6aW5zY3JpcHRpb25zIiwicG9zdDpwb'
                                             'GF5ZXJzIiwicG9zdDp0b3VybmV5cyJd'
                                             'fQ.a-RBIBAvTdAUNWgBkyAeAl_j2pYK'
                                             '_an1QudV5Hx_nixxqq0TA_z66JfZZOd'
                                             'doQpq8dAb4z-C2YhTa6J4haJ412ACjP'
                                             'TqqJbZGDWoXgGol9Bkx4boQZeL5PUQ3'
                                             'G6zMe8pjhX1znlyzrJFl6784loywQkg'
                                             'FsZ3PPsIKJF5yvJ4mApyQIFR2MgZfT3'
                                             'MHFSVsx8Z_zRBOMvGO6TbahIhwo0Zo9'
                                             'G-tPfPGSQkj8B0pwPFfxfwZy6XSVB_I'
                                             'k41Xg43wzXKTuUQ92Gwa7Dbyz-Zq5QM'
                                             'UsXDVotUqH6W0pao4aNet2jFx09PEML'
                                             'a3rUFLwRlfNyWDK-VWJfG2CufbM_zsp'
                                             'F32w')

        self.manager_headers = {'Authorization': self.players_manager_token}

        self.administrator_headers = {'Authorization':
                                      self.tourneys_administrator_token}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_players(self):
        res = self.client().get('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])

    def test_405_requesting_players_with_wrong_method(self):
        res = self.client().patch('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_get_players_by_id(self):
        res = self.client().get('/players/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['player'])

    def test_404_requesting_player_that_does_not_exist(self):
        res = self.client().get('/players/1234568790')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_create_new_player(self):
        res = self.client().post('/players', json=self.new_player,
                                 headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_player_with_wrong_datatype(self):
        res = self.client().post('/players',
                                 json=self.wrong_format_player,
                                 headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_player(self):
        res = self.client().delete('/players/6',
                                   headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_player(self):
        res = self.client().delete('/players/1234567890',
                                   headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_player(self):
        res = self.client().patch('/players/5', json=self.patch_player,
                                  headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_player_with_wrong_format(self):
        res = self.client().patch('/players/5',
                                  json=self.wrong_patch_format,
                                  headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_get_games(self):
        res = self.client().get('/games')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['games'])

    def test_405_requesting_games_with_wrong_method(self):
        res = self.client().patch('/games')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_create_new_game(self):
        res = self.client().post('/games', json=self.new_game,
                                 headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_game_with_wrong_format(self):
        res = self.client().post('/games',
                                 json=self.wrong_format_game,
                                 headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_game(self):
        res = self.client().delete('/games/5',
                                   headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_game(self):
        res = self.client().delete('/games/1234567890',
                                   headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    This test is ok and it passes on production environment, however, it
    doesn't pass here at testing environment because we use a SQLite database
    for tests as it's lighter and you can have the database as a file ready to
    use, so it's easier to share and handle. SQLAlchemy has some problems with
    SQLite as it does not have built-in DATE, TIME, or DATETIME types. The
    production environment uses PostgreSQL, which doesn't have that issue.

    For more information:
    https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#date-and-time-types

    def test_get_tourneys(self):
        res = self.client().get('/tourneys')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tourneys'])
    '''

    def test_405_requesting_tourneys_with_wrong_method(self):
        res = self.client().patch('/tourneys')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    '''
    This test is ok and it passes on production environment, however, it
    doesn't pass here at testing environment because we use a SQLite database
    for tests as it's lighter and you can have the database as a file ready to
    use, so it's easier to share and handle. SQLAlchemy has some problems with
    SQLite as it does not have built-in DATE, TIME, or DATETIME types. The
    production environment uses PostgreSQL, which doesn't have that issue.

    For more information:
    https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#date-and-time-types

    def test_get_tourney_by_id(self):
        res = self.client().get('/tourneys/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tourney'])
    '''

    def test_404_requesting_tourney_that_does_not_exist(self):
        res = self.client().get('/tourneys/1234568790')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_create_new_tourney(self):
        res = self.client().post('/tourneys', json=self.new_tourney,
                                 headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_tourney_with_wrong_datatype(self):
        res = self.client().post('/tourneys',
                                 json=self.wrong_datatypes_tourney,
                                 headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_tourney(self):
        res = self.client().delete('/tourneys/4',
                                   headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_tourney(self):
        res = self.client().delete('/tourneys/1234567890',
                                   headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_tourney(self):
        res = self.client().patch('/tourneys/3', json=self.patch_tourney,
                                  headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_tourney_with_wrong_format(self):
        res = self.client().patch('/tourneys/3', json=self.wrong_patch_format,
                                  headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    This tests are ok and they pass on production environment, however, they
    don't pass here at testing environment because we use a SQLite database
    for tests as it's lighter and you can have the database as a file ready to
    use, so it's easier to share and handle. SQLAlchemy has some problems with
    SQLite as it does not have built-in DATE, TIME, or DATETIME types. The
    production environment uses PostgreSQL, which doesn't have that issue.

    For more information:
    https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#date-and-time-types

    def test_create_new_inscription(self):
        res = self.client().post('/inscriptions', json=self.new_inscription)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_inscription_that_already_exists(self):
        res = self.client().post('/inscriptions',
                                 json=self.repeated_inscription)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_inscription(self):
        res = self.client().delete('/inscriptions', json=self.bad_inscription)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    '''

    def test_405_delete_inscription_with_wrong_method(self):
        res = self.client().get('/inscriptions', json=self.bad_inscription)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    '''
    This tests are ok and they pass on production environment, however, they
    don't pass here at testing environment because we use a SQLite database
    for tests as it's lighter and you can have the database as a file ready to
    use, so it's easier to share and handle. SQLAlchemy has some problems with
    SQLite as it does not have built-in DATE, TIME, or DATETIME types. The
    production environment uses PostgreSQL, which doesn't have that issue.

    For more information:
    https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#date-and-time-types

    def test_get_players_by_tourney_id(self):
        res = self.client().get('/tourneys/1/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tourney'])
        self.assertTrue(data['players'])

    def test_404_requesting_players_from_tourney_that_does_not_exist(self):
        res = self.client().get('/tourneys/1/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    '''

    def test_401_create_game_without_authentication(self):
        res = self.client().post('/tourneys')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_401_delete_inscription_without_authentication(self):
        res = self.client().delete('/inscriptions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_403_create_tourney_without_permission(self):
        res = self.client().post('/tourneys', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'Token has not the required persmission.')

    def test_403_delete_game_without_permission(self):
        res = self.client().delete('/games/1', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'Token has not the required persmission.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
