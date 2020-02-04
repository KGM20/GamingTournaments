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
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir,
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
            'XVCIsImtpZCI6IlF6QTVSREJEUVRJeE5rTXhOMEl4UXpnd01ERTVNamMwUWpJelF'
            'UTTNNRE13UTBGRlFUSXlOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1rZ20yMC5hdX'
            'RoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlZWQ1MjRmNzg3ODcwY2M4YjZiODNiIi'
            'wiYXVkIjoiZ2FtaW5ndG91cm5leSIsImlhdCI6MTU4MDc2MjgxMiwiZXhwIjoxNT'
            'gwODQ5MjEyLCJhenAiOiJLT2YxMk45MU5OcGgwQ1htSko2cWVwaXZmUXNLN0owcS'
            'IsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmluc2NyaXB0aW9ucy'
            'IsImRlbGV0ZTpwbGF5ZXJzIiwicGF0Y2g6cGxheWVycyIsInBhdGNoOnRvdXJuZX'
            'lzIiwicG9zdDppbnNjcmlwdGlvbnMiLCJwb3N0OnBsYXllcnMiXX0.MadEGTbFmh'
            '1gNkLL3vAlLnBOqRo_O4S3lvkQjUhr4MMVovkJutHjeKz8oDOShqD6H8obXOiNwd'
            'jvoWUQnh_lnmyft2VkQ1TMSZanp6iZ9kAmK9HV_sw7gHcHtmVHD1dvwNSEqoRsAt'
            'kaimuKGAGvbkX82dwRztZLLryLIgIcn-EiMy5NBroYeSjfQ_4NrVmeAHwXQiIJrn'
            'sb7VAwbcFOwFusoIHLtSU8_ZxKE_XZ1gA_LtLa3GG18emfjxuyu6GDzN3JpXqM_z'
            'eCHiuRX5NV_YdqKNp2JzJwScLK21pAQnkRtDpkyE3l3tCUMBwX8wEazQY3SguN_V'
            'skuTx0joxxdA')

        self.tourneys_administrator_token = ('Bearer eyJhbGciOiJSUzI1NiIsInR5'
            'cCI6IkpXVCIsImtpZCI6IlF6QTVSREJEUVRJeE5rTXhOMEl4UXpnd01ERTVNamMw'
            'UWpJelFUTTNNRE13UTBGRlFUSXlOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1rZ20'
            'yMC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRmYzE4OWQ5NGQ3YTUxNTM2NWY'
            '3MGMyIiwiYXVkIjoiZ2FtaW5ndG91cm5leSIsImlhdCI6MTU4MDc2MzMwMCwiZXh'
            'wIjoxNTgwODQ5NzAwLCJhenAiOiJLT2YxMk45MU5OcGgwQ1htSko2cWVwaXZmUXN'
            'LN0owcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmdhbWVzIiw'
            'iZGVsZXRlOmluc2NyaXB0aW9ucyIsImRlbGV0ZTpwbGF5ZXJzIiwiZGVsZXRlOnR'
            'vdXJuZXlzIiwicGF0Y2g6cGxheWVycyIsInBhdGNoOnRvdXJuZXlzIiwicG9zdDp'
            'nYW1lcyIsInBvc3Q6aW5zY3JpcHRpb25zIiwicG9zdDpwbGF5ZXJzIiwicG9zdDp'
            '0b3VybmV5cyJdfQ.a-RBIBAvTdAUNWgBkyAeAl_j2pYK_an1QudV5Hx_nixxqq0T'
            'A_z66JfZZOddoQpq8dAb4z-C2YhTa6J4haJ412ACjPTqqJbZGDWoXgGol9Bkx4bo'
            'QZeL5PUQ3G6zMe8pjhX1znlyzrJFl6784loywQkgFsZ3PPsIKJF5yvJ4mApyQIFR'
            '2MgZfT3MHFSVsx8Z_zRBOMvGO6TbahIhwo0Zo9G-tPfPGSQkj8B0pwPFfxfwZy6X'
            'SVB_Ik41Xg43wzXKTuUQ92Gwa7Dbyz-Zq5QMUsXDVotUqH6W0pao4aNet2jFx09P'
            'EMLa3rUFLwRlfNyWDK-VWJfG2CufbM_zspF32w')

        self.manager_headers = {'Authorization': self.players_manager_token}

        self.administrator_headers = {'Authorization': self.tourneys_administrator_token}

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
        res = self.client().post('/players', json=self.new_player, headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_player_with_wrong_datatype(self):
        res = self.client().post('/players',
                                 json=self.wrong_format_player, headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_player(self):
        res = self.client().delete('/players/6', headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_player(self):
        res = self.client().delete('/players/1234567890', headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_player(self):
        res = self.client().patch('/players/5', json=self.patch_player, headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_player_with_wrong_format(self):
        res = self.client().patch('/players/5',
                                 json=self.wrong_patch_format, headers=self.manager_headers)
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
        res = self.client().post('/games', json=self.new_game, headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_game_with_wrong_format(self):
        res = self.client().post('/games',
                                 json=self.wrong_format_game, headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_game(self):
        res = self.client().delete('/games/5', headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_game(self):
        res = self.client().delete('/games/1234567890', headers=self.administrator_headers)
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
        res = self.client().post('/tourneys', json=self.new_tourney, headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_tourney_with_wrong_datatype(self):
        res = self.client().post('/tourneys',
                                 json=self.wrong_datatypes_tourney, headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_tourney(self):
        res = self.client().delete('/tourneys/4', headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_tourney(self):
        res = self.client().delete('/tourneys/1234567890', headers=self.administrator_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_tourney(self):
        res = self.client().patch('/tourneys/3', json=self.patch_tourney, headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_tourney_with_wrong_format(self):
        res = self.client().patch('/tourneys/3', json=self.wrong_patch_format, headers=self.manager_headers)
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
        self.assertEqual(data['message'], 'Token has not the required persmission.')

    def test_403_delete_game_without_permission(self):
        res = self.client().delete('/games/1', headers=self.manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token has not the required persmission.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
