extends Node2D

func setup():
	var players_pos: Array = TurnManager.map_data["player_num"].get(TurnManager.player_count, [])
	if not players_pos:
		FLogger.fatal("player pos data is null")
	var player_node = preload("res://src/tscn/Game/Character/Player.tscn")
	for player_pos in players_pos:
		var player = player_node.instantiate()
		player.setup(Vector2i(player_pos[0], player_pos[1]))
		add_child(player)
		TurnManager.player_nodes.append(player)
