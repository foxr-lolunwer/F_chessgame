extends Node

var select_map_id: String = "default"
var lang_code: String = "en_US"
var map_data: Dictionary = {}  # 地图信息
var player_count: String = "2"  # 玩家数量
# --- 内部变量 ---
# 节点缓存
var map_layer: TileMapLayer
var select_layer: TileMapLayer
var ex_layer: TileMapLayer

# 地图数据缓存
var used_cells: Array[Vector2i] = []
var special_tiles: Dictionary = {
	"cannon": [], "speed": [], "cover": [], "heal": [], "capture": []
}
var capture_status: Dictionary = {}
var forbidden_trigger_status: Dictionary = {}
var bomb_trigger_status: Dictionary = {}
var tile_size
