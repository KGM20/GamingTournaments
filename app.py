import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Player

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