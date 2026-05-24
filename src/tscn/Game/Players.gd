extends Node2D

func setup():
	var players_pos: Array = TurnManager.map_data["player_num"].get(TurnManager.player_count, [])
	if not players_pos:
		FLogger.fatal("player pos data is null")
	var player_node = preload("res://src/tscn/Game/Character/Player.tscn")
	for i in len(players_pos):
		var player_pos = players_pos[i]
		var player: FCharacter = player_node.instantiate()
		player.setup(Vector2i(player_pos[0], player_pos[1]), "player %d" % i, GameData.players_color[i%len(GameData.players_color)])
		add_child(player)
		TurnManager.player_nodes.append(player)
