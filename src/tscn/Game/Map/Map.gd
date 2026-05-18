extends Node2D

func setup():
	PD.map_layer = $MapLayer
	PD.select_layer = $SeletLayer
	PD.ex_layer = $ExLayer
	var tile_set: TileSet = load(PD.map_data["folderpath"] + "/map_tile.tres")
	PD.map_layer.set_tile_set(tile_set)
	PD.tile_size = tile_set.tile_size
	tile_set = load(PD.map_data["folderpath"] + "/select_tile.tres")
	PD.select_layer.set_tile_set(tile_set)

	PD.used_cells = PD.map_layer.get_used_cells()
	
	# 初始化特殊地块列表
	PD.special_tiles["cover"] = PD.map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.COVER, 0)
	PD.special_tiles["heal"] = PD.map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.HEAL, 0)
	PD.special_tiles["cannon"] = PD.map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.CANNON, 0)
	PD.special_tiles["speed"] = PD.map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.SPEED, 0)
	PD.special_tiles["capture"] = PD.map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.CAPTURE, 0)
	
	var count: int = 0
	for p in PD.special_tiles["capture"]:
		var c_meta: Dictionary = { "pname": str(count), "index": -1, "cname": "null" }
		count += 1
		PD.capture_status.get_or_add(p, c_meta)
