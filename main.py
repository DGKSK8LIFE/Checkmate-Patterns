from CheckmatePattern import CheckmatePattern
import chess, chess.pgn
import io
import berserk
import json

with open('token.json') as f:
    token = json.load(f)

client = berserk.Client(session=berserk.TokenSession(token["token"]))
player = input('Please enter the lichess.org acocunt you want to analyze: ')


print("Fetching " + player + "'s games. This may take a moment on the number of games they have played...")
games = list(client.games.export_by_player(player))

checkmate_counter = 0
checkmate_moves = []
game_ids = []

for i in range(len(games)):
    if games[i]['status'] == 'mate' and games[i]['variant'] == 'standard':
        checkmate_counter += 1
        checkmate_moves.append(games[i]['moves'])
        game_ids.append(games[i]['id'])

print('The user has given and recieved', checkmate_counter, 'checkmates total.')

fens = []

for i in checkmate_moves:
    fens.append(chess.pgn.read_game(io.StringIO(i)).end().board().fen())

for i in range(len(fens)):
    CheckmatePattern(fens[i]).find_checkmate_pattern()
    print('https://lichess.org/' + game_ids[i])
