from CheckmatePattern import CheckmatePattern
import chess, chess.pgn
import io
import berserk
import json

with open('token.json') as f:
    token = json.load(f)

client = berserk.Client(session=berserk.TokenSession(token["token"]))
player = input('Please enter the lichess.org account you want to analyze: ')


print("Fetching " + player + "'s games. This may take a moment on the number of games they have played...\n")
games = list(client.games.export_by_player(player))

gave_checkmate_moves = []
recieved_checkmate_moves = []

gave_checkmate_ids = []
recieved_checkmate_ids = []

for i in range(len(games)):
    try:
        if games[i]['status'] == 'mate' and games[i]['variant'] == 'standard':
            if games[i]['players']['white']['user']['name'] == player and games[i]['winner'] == 'white':
                gave_checkmate_moves.append(games[i]['moves'])
                gave_checkmate_ids.append(games[i]['id'])
            else:
                recieved_checkmate_moves.append(games[i]['moves'])
                recieved_checkmate_ids.append(games[i]['id'])
    except KeyError:
        # If the user played against stockfish it messes up the keys
        pass
print(player, 'has given', len(gave_checkmate_moves), 'checkmates total.')
print(player, 'has recieved', len(recieved_checkmate_moves), 'checkmates total\n')

answer = input("Would you like to see " + player +"'s a. given checkamtes or b. recieved checkmates? (a / b) ")

gave_fens = []
recieved_fens = []

if answer == 'a':
    if len(gave_checkmate_moves) > 0:
        for i in gave_checkmate_moves:
            gave_fens.append(chess.pgn.read_game(io.StringIO(i)).end().board().fen())
        for i in range(len(gave_fens)):
            CheckmatePattern(gave_fens[i]).find_checkmate_pattern()
            print('https://lichess.org/' + gave_checkmate_ids[i])
    else:
        print(player, 'has never given a checkmate!')
else:
    if len(recieved_checkmate_moves) > 0:
        for i in recieved_checkmate_moves:
            recieved_fens.append(chess.pgn.read_game(io.StringIO(i)).end().board().fen())
        for i in range(len(recieved_fens)):
            CheckmatePattern(recieved_fens[i]).find_checkmate_pattern()
            print('https://lichess.org/' + recieved_checkmate_ids[i])
    else:
        print(player, 'has never recieved a checkmate!')
