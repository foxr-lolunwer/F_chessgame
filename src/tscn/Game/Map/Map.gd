extends Node2D

# --- 内部变量 ---
# 节点缓存
var _move_layer: TileMapLayer
var _map_layer: TileMapLayer
var _ex_layer: TileMapLayer

# 地图数据缓存
var used_cells: Array[Vector2i] = []
var special_tiles: Dictionary = {
	"cannon": [], "speed": [], "cover": [], "heal": [], "capture": []
}
var capture_status: Dictionary = {}
var forbidden_trigger_status: Dictionary = {}
var bomb_trigger_status: Dictionary = {}


func setup(map_tile_path: String):
	_move_layer = $MoveHintLayer
	_map_layer = $TileMapLayer
	_ex_layer = $ExLayer
	var map_tile_set: TileSet = load(map_tile_path)
	_map_layer.set_tile_set(map_tile_set)

	
	used_cells = _map_layer.get_used_cells()
	
	# 初始化特殊地块列表
	special_tiles["cover"] = _map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.COVER, 0)
	special_tiles["heal"] = _map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.HEAL, 0)
	special_tiles["cannon"] = _map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.CANNON, 0)
	special_tiles["speed"] = _map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.SPEED, 0)
	special_tiles["capture"] = _map_layer.get_used_cells_by_id(1, ConstData.MAP_LAYER_ID.CAPTURE, 0)
	
	var count: int = 0
	for p in special_tiles["capture"]:
		var c_meta: Dictionary = { "pname": str(count), "index": -1, "cname": "null" }
		count += 1
		capture_status.get_or_add(p, c_meta)
