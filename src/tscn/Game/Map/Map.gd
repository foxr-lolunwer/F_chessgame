extends Node2D

func setup():
	TurnManager.map_layer = $MapLayer
	TurnManager.select_layer = $SeletLayer
	TurnManager.ex_layer = $ExLayer
	var tile_set: TileSet = load(TurnManager.map_data["folderpath"] + "/map_tile.tres")
	TurnManager.map_layer.set_tile_set(tile_set)
	TurnManager.tile_size = tile_set.tile_size
	tile_set = load(TurnManager.map_data["folderpath"] + "/select_tile.tres")
	TurnManager.select_layer.set_tile_set(tile_set)
	
	TurnManager.init_map_data()
