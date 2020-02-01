import os
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, db, Player, Game, Tourney

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request  # CORS headers
    def after_request(response):
	    response.headers.add('Access-Control-Allow-Headers',
	                         'Content-Type,Authorization,true')
	    response.headers.add('Access-Control-Allow-Methods',
	                         'GET, PATCH, POST, DELETE, OPTIONS')
	    return response


    @app.route('/players', methods=['GET'])
    def retrieve_players():

	    players = db.session.query(Player).all()
	    format_players = [player.format() for player in players]

	    return jsonify({
	        'success': True,
	        'players': format_players
	    }), 200


    @app.route('/players', methods=['POST'])
    def create_player():
	    body = request.get_json()

	    name = body.get('name', None)
	    nickname = body.get('nickname', None)
	    nationality = body.get('nationality', None)

	    player = Player(name=name, nickname=nickname, nationality=nationality)

	    try:
	        player.insert()

	        return jsonify({
                'success': True,
            })

	    except:
	    	db.session.rollback()
	    	abort(422)


    @app.route('/players/<int:player_id>', methods=['DELETE'])
    def delete_a_player(player_id):
        player = db.session.query(Player).get(player_id)

        if player is None:
            abort(404)

        try:
            player.delete()

            return jsonify({
                'success': True,
            })

        except:
        	db.session.rollback()
        	abort(422)


    @app.route('/players/<int:player_id>', methods=['PATCH'])
    def update_drink(player_id):
	    body = request.get_json()

	    name = body.get('name', None)
	    nickname = body.get('nickname', None)
	    nationality = body.get('nationality', None)

	    if name is None or nickname is None:
	    	abort(422)

	    player = db.session.query(Player).get(player_id)

	    if player is None:
	        abort(404)

	    try:
	        player.name = name
	        player.nickname = nickname
	        player.nationality = nationality

	        player.update()

	        return jsonify({
	            'success': True
	        }), 200

	    except:
	    	db.session.rollback()
    		abort(422)


    @app.route('/games', methods=['GET'])
    def retrieve_games():

	    games = db.session.query(Game).all()
	    format_games = [game.format() for game in games]

	    return jsonify({
	        'success': True,
	        'games': format_games
	    }), 200


    @app.route('/games', methods=['POST'])
    def create_game():
	    body = request.get_json()

	    title = body.get('title', None)

	    game = Game(title=title)

	    try:
	        game.insert()

	        return jsonify({
                'success': True,
            })

	    except:
	    	db.session.rollback()
	    	abort(422)


    @app.route('/games/<int:game_id>', methods=['DELETE'])
    def delete_a_game(game_id):
        game = db.session.query(Game).get(game_id)

        if game is None:
            abort(404)

        try:
            game.delete()

            return jsonify({
                'success': True,
            })

        except:
        	db.session.rollback()
        	abort(422)


    @app.route('/tourneys', methods=['GET'])
    def retrieve_tourneys():

	    tourneys = db.session.query(Tourney).all()
	    format_tourneys = [tourney.format() for tourney in tourneys]

	    return jsonify({
	        'success': True,
	        'tourneys': format_tourneys
	    }), 200


    @app.route('/tourneys', methods=['POST'])
    def create_tourney():
	    body = request.get_json()

	    name = body.get('name', None)
	    location = body.get('location', None)
	    game_id = body.get('game_id', None)

	    # This try-except is to validate date has a real date format
	    try:
	    	date = datetime.strptime(body.get('date', None), "%Y-%m-%d %H:%M")

	    except:
	    	abort(422)

	    tourney = Tourney(name=name, location=location, date=date, game_id=game_id)

	    try:
	        tourney.insert()

	        return jsonify({
                'success': True,
            })

	    except:
	    	db.session.rollback()
	    	abort(422)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

      
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

      
    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

      
    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()