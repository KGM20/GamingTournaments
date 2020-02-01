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

    def test_create_new_player(self):
        res = self.client().post('/players', json=self.new_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_player_with_wrong_datatype(self):
        res = self.client().post('/players',
                                 json=self.wrong_format_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_player(self):
        res = self.client().delete('/players/6')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_player(self):
        res = self.client().delete('/players/1234567890')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_update_player(self):
        res = self.client().patch('/players/5', json=self.patch_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_player_with_wrong_format(self):
        res = self.client().patch('/players/5',
                                 json=self.wrong_patch_format)
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
        res = self.client().post('/games', json=self.new_game)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_game_with_wrong_format(self):
        res = self.client().post('/games',
                                 json=self.wrong_format_game)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_game(self):
        res = self.client().delete('/games/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_a_non_existing_game(self):
        res = self.client().delete('/games/1234567890')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
