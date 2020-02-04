# API Reference

## Base URL

This API runs on [Heroku](https://www.heroku.com/) using the following URL:
```
https://gaming-tournaments.herokuapp.com
```

## Error Handling

### Response Codes

All the errors are returned in JSON format with the following structure:
```
{
	'success': False,
	'error': 422,
	'message': 'Unprocessable Entity'
}
```

### Error types

The API handles the following error codes:
  
- 400: Bad Request
- 401: Unathorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable entity
- 500: Internal server error

### Authentication - Roles

Each endpoint of the API needs different persmissions to be accessed, some are public and some need an authentication, the different authentication roles for the API are the following:

- Players manager: This person is in charge of make the first contact with the current or aspiring players and has the permissions to everything related of giving the players the services they need from the API.

- Tourneys administrator: This person has a total access for every endpoint as it's a person who can handle players requests if needed, but also he's in charge of supervise everything related to the tourneys.

For authentication we use an Authorization header with a Bearer Token as value.

## Endpoints

- GET '/players'
- GET '/players/id'
- GET '/tourneys'
- GET '/tourneys/id'
- GET '/tourneys/id/players'
- GET '/games'
- POST '/players'
- POST '/tourneys'
- POST '/games'
- POST '/inscriptions'
- DELETE '/players/id'
- DELETE '/tourneys/id'
- DELETE '/games/id'
- DELETE '/inscriptions'
- PATCH '/players/id'
- PATCH '/tourneys/id'

### GET /players

- This is a public endpoint, anyone can access even without login a session. 
- Returns a dictionary with an array of all the players and a success argument.
- Request Arguments: None.

Response example:
```
{
    "players": [
        {
            "id": 1,
            "name": "Kevin Cruz",
            "nationality": "Mexican",
            "nickname": "KGM20"
        },
        {
            "id": 2,
            "name": "Person 1",
            "nationality": "Korean",
            "nickname": "Faker"
        },
        {
            "id": 3,
            "name": "Person 2",
            "nationality": "Chilean",
            "nickname": "ZeRo"
        }
    ],
    "success": true
}
```

### GET /players/integer:id

- This is a public endpoint, anyone can access even without login a session. 
- Returns a dictionary with the player object that corresponds the id and a success argument.
- Request Arguments: None.

Response example:
```
{
    "player": {
        "id": 1,
        "name": "Kevin Cruz",
        "nationality": "Mexican",
        "nickname": "KGM20"
    },
    "success": true
}
```

### GET /tourneys

- This is a public endpoint, anyone can access even without login a session. 
- Returns a dictionary with an array of all the tourneys and a success argument.
- Request Arguments: None.

Response example:
```
{
    "success": true,
    "tourneys": [
        {
            "date": "2020-01-24 10:00:00",
            "game": "Super Smash Bros. Ultimate",
            "id": 1,
            "location": "Oakland, CA",
            "name": "Genesis",
            "winner": null
        },
        {
            "date": "2020-10-28 15:00:00",
            "game": "League of Legends",
            "id": 2,
            "location": "Mexico City, MX",
            "name": "Worlds 2020",
            "winner": null
        }
    ]
}
```

### GET /tourneys/integer:id

- This is a public endpoint, anyone can access even without login a session. 
- Returns a dictionary with the player object that corresponds the id and a success argument.
- Request Arguments: None.

Response example:
```
{
    "success": true,
    "tourney": {
        "date": "2020-10-28 15:00:00",
        "game": "League of Legends",
        "id": 2,
        "location": "Mexico City, MX",
        "name": "Worlds 2020",
        "winner": null
    }
}
```

### GET /tourneys/integer:id/players

- This is a public endpoint, anyone can access even without login a session. 
- Returns a dictionary with the tourney object that corresponds the id, an array with all the players that are inscribed to that tourney and a success argument.
- Request Arguments: None.

Response example:
```
{
    "players": [
        {
            "id": 1,
            "name": "Kevin Cruz",
            "nationality": "Mexican",
            "nickname": "KGM20"
        },
        {
            "id": 6,
            "name": "Person 4",
            "nationality": "Argentinian",
            "nickname": "Whitelotus"
        }
    ],
    "success": true,
    "tourney": {
        "date": "2020-10-28 15:00:00",
        "game": "League of Legends",
        "id": 2,
        "location": "Mexico City, MX",
        "name": "Worlds 2020",
        "winner": null
    }
}
```

### GET /games

- This is a public endpoint, anyone can access even without login a session. 
- Returns a dictionary with an array of all the games and a success argument.
- Request Arguments: None.

Response example:
```
{
    "games": [
        {
            "id": 1,
            "title": "Super Smash Bros. Melee"
        },
        {
            "id": 2,
            "title": "Super Smash Bros. Ultimate"
        },
        {
            "id": 4,
            "title": "League of Legends"
        }
    ],
    "success": true
}
```

### POST /players

- This is a private endpoint, you need Players Manager or Tourneys Administrator access to use it. 
- This endpoint creates a player based on the requested parameters. Returns a success argument if worked fine.
- Request Arguments: A JSON object with the following format (parameters marked with ** are optional):
```
{
    "name": "A real name",
    "nickname": "A cool nickname",
    "nationality": "Some nice country" **
}
```

Response example:
```
{
    "success": true
}
```

### POST /tourneys

- This is a private endpoint, you need Tourneys Administrator access to use it. 
- This endpoint creates a tourney based on the requested parameters. Returns a success argument if worked fine.
- Request Arguments: A JSON object with the following format:
```
{
    "name": "A tourney for cool people",
    "location": "Some awesome city",
    "date": "2020-08-13 9:10",
    "game_id": 2
}
```

Response example:
```
{
    "success": true
}
```

### POST /games

- This is a private endpoint, you need Tourneys Administrator access to use it. 
- This endpoint creates a game based on the requested parameters. Returns a success argument if worked fine.
- Request Arguments: A JSON object with the following format:
```
{
    "title": "A cool game"
}
```

Response example:
```
{
    "success": true
}
```

### POST /inscriptions

- This is a private endpoint, you need Players Manager or Tourneys Administrator access to use it.
- This endpoint registers a player on a tourney based on the requested parameters. Returns a success argument if worked fine.
- You cannot register a player to a tourney that has been held already.
- Request Arguments: A JSON object with the following format:
```
{
    "player_id": 1,
    "tourney_id": 2
}
```

Response example:
```
{
    "success": true
}
```

### DELETE /players/integer:id

- This is a private endpoint, you need Players Manager or Tourneys Administrator access to use it.
- This endpoint deletes the player that corresponds the id on the URL. Returns a success argument if worked fine.
- Request Arguments: None.

Response example:
```
{
    "success": true
}
```

### DELETE /tourneys/integer:id

- This is a private endpoint, you need Tourneys Administrator access to use it.
- This endpoint deletes the tourney that corresponds the id on the URL. Returns a success argument if worked fine.
- Request Arguments: None.

Response example:
```
{
    "success": true
}
```

### DELETE /games/integer:id

- This is a private endpoint, you need Tourneys Administrator access to use it.
- This endpoint deletes the game that corresponds the id on the URL. Returns a success argument if worked fine.
- Request Arguments: None.

Response example:
```
{
    "success": true
}
```

### DELETE /inscriptions

- This is a private endpoint, you need Players Manager or Tourneys Administrator access to use it.
- This endpoint unsuscribes a player from a tourney based on the requested parameters. Returns a success argument if worked fine.
- Request Arguments: A JSON object with the following format:
```
{
    "player_id": 1,
    "tourney_id": 2
}
```

Response example:
```
{
    "success": true
}
```

### PATCH /players/integer:id

- This is a private endpoint, you need Players Manager or Tourneys Administrator access to use it. 
- This endpoint updates the player that matches the id on the URL based on the requested parameters. Returns a success argument if worked fine.
- Request Arguments: A JSON object with the following format (parameters marked with ** are optional):
```
{
    "name": "An unreal name",
    "nickname": "A not cool nickname",
    "nationality": "A not nice country" **
}
```

Response example:
```
{
    "success": true
}
```

### PATCH /tourneys/integer:id

- This is a private endpoint, you need Players Manager or Tourneys Administrator access to use it. 
- This endpoint updates the tourney that matches the id on the URL based on the requested parameters. Returns a success argument if worked fine.
- You cannot set a winner to a tourney that has not been held yet.
- Request Arguments: A JSON object with the following format (parameters marked with ** are optional):
```
{
    "name": "A tourney for cool people",
    "location": "Some awesome city",
    "date": "2019-08-13 9:10",
    "winner": 1, **
    "game_id": 2
}
```

Response example:
```
{
    "success": true
}
```