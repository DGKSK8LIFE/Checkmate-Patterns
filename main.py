import CheckmatePattern
import chess.pgn
import io
import berserk

client = berserk.Client()
games = list(client.games.export_by_player('buenossdias'))

checkmate_counter = 0

for i in range(len(games)):
    if games[i]['status'] == 'mate':
        checkmate_counter += 1

print(checkmate_counter)