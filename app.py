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


    @app.route('/players/<int:player_id>', methods=['GET'])
    def retriev_player_by_id(player_id):

	    player = db.session.query(Player).get(player_id)

	    if player is None:
	    	abort(404)

	    return jsonify({
	        'success': True,
	        'player': player.format()
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
    def update_player(player_id):
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


    @app.route('/tourneys/<int:tourney_id>', methods=['DELETE'])
    def delete_a_tourney(tourney_id):
        tourney = db.session.query(Tourney).get(tourney_id)

        if tourney is None:
            abort(404)

        try:
            tourney.delete()

            return jsonify({
                'success': True,
            })

        except:
        	db.session.rollback()
        	abort(422)


    @app.route('/tourneys/<int:tourney_id>', methods=['PATCH'])
    def update_tourney(tourney_id):
	    body = request.get_json()

	    name = body.get('name', None)
	    location = body.get('location', None)
	    game_id = body.get('game_id', None)
	    winner = body.get('winner', None)

	    if name is None or location is None or game_id is None:
	    	abort(422)

	    # This try-except is to validate date has a real date format
	    try:
	    	date = datetime.strptime(body.get('date', None), "%Y-%m-%d %H:%M")
        			
	    except:
	    	abort(422)

	    '''
    	This is because you can't set a winner to a tourney that hasn't been
    	held yet

    	'''
	    if winner is not None:
    		today = datetime.now()

    		if today < date:
    			abort(422)

	    tourney = db.session.query(Tourney).get(tourney_id)

	    if tourney is None:
	        abort(404)

	    try:
	        tourney.name = name
	        tourney.location = location
	        tourney.date = date
	        tourney.winner = winner
	        tourney.game_id = game_id

	        tourney.update()

	        return jsonify({
	            'success': True
	        }), 200

	    except:
	    	db.session.rollback()
    		abort(422)


    @app.route('/inscriptions', methods=['POST'])
    def submit_inscription():
	    body = request.get_json()

	    player_id = body.get('player_id', None)
	    tourney_id = body.get('tourney_id', None)

	    player = db.session.query(Player).get(player_id)
	    tourney = db.session.query(Tourney).get(tourney_id)

	    if player is None or tourney is None:
	    	abort(404)

	    player_tourneys = player.player_tourneys

        # This is to not repeat an inscription
	    if tourney in player_tourneys:
        	abort(422)

	    '''
	    This is to not submit an inscription to a tourney that has been held
	    already
	    '''
	    today = datetime.now()

	    if today > tourney.date:
	    	abort(422)

	    player_tourneys.append(tourney)
	    player.player_tourneys = player_tourneys

	    try:
	        player.update()

	        return jsonify({
                'success': True,
            })

	    except:
	    	db.session.rollback()
	    	abort(422)


    @app.route('/inscriptions', methods=['DELETE'])
    def delete_an_inscription():
	    body = request.get_json()

	    player_id = body.get('player_id', None)
	    tourney_id = body.get('tourney_id', None)

	    player = db.session.query(Player).get(player_id)
	    tourney = db.session.query(Tourney).get(tourney_id)

	    if player is None or tourney is None:
	    	abort(404)

	    player_tourneys = player.player_tourneys

	    if tourney not in player_tourneys:
	    	abort(404)

	    player_tourneys.remove(tourney)
	    player.player_tourneys = player_tourneys

	    try:
    		player.update()

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