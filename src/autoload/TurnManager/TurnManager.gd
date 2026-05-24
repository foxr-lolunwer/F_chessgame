extends Node

# --- 内部变量 ---
## 各种移动类型的机率
var move_type_roll: Array[Array] = [
	[ConstData.MOVE_OPERATION.CROSS, 2],
	[ConstData.MOVE_OPERATION.DIAGONAL, 2],
	[ConstData.MOVE_OPERATION.DOUBLE_CROSS, 1],
	[ConstData.MOVE_OPERATION.TELEPORT, 0]
]
## 各种战斗类型的机率
var fight_type_roll: Array[Array] = [
	[ConstData.FIGHT_OPERATION.NORMAL_SHOT, 2],
	[ConstData.FIGHT_OPERATION.X_RAY, 1],
	[ConstData.FIGHT_OPERATION.POWER_SHOT, 1],
	[ConstData.FIGHT_OPERATION.BOMB, 0],
	[ConstData.FIGHT_OPERATION.HEALTH, 1]
]
# 地图信息
var select_map_id: String = ""  ## 选择的地图id
var map_data: Dictionary = {}  ## 地图信息
var player_count: String = "2"  ## 玩家数量
# 游戏状态
# --- 状态变量 ---
var current_phase: ConstData.GAME_PHASE = ConstData.GAME_PHASE.NONE ## 全局状态
var turn_count: int = 0  ## 回合计数
var current_active_char: FCharacter ## 当前行动的角色实例
var win_index: int = -1  ## 获胜玩家index
var is_game_over: bool = false  ## 游戏是否已结束
var player_nodes: Array[FCharacter] = []  ## 玩家node列表
var action_queue: Array[FCharacter] = []  ## 当前阶段“剩余待行动”的角色队列
# 当前回合临时数据
var valid_attack_targets: Array[FCharacter] = [] ## 可攻击的目标FCharacter列表
# 节点缓存
var map_layer: TileMapLayer  ## 地图节点下的map_layer
var select_layer: TileMapLayer  ## 地图节点下的select_layer
var ex_layer: TileMapLayer  ## 地图节点下的ex_layer
var node_map: Node2D  ## 地图节点
var node_players: Node2D  ## 玩家节点根
var node_ui_layer: CanvasLayer  ## UI节点
# 地图数据缓存
var used_cells: Array[Vector2i] = []  ## 可用的位置集
var special_tiles: Dictionary = {  ## 特殊位置集
	"cannon": [], "speed": [], "cover": [], "heal": [], "capture": []
}
var capture_status: Dictionary = {}  ## 点位占领状态
var forbidden_trigger_status: Dictionary = {}  ##
var bomb_trigger_status: Dictionary = {}
var tile_size  ## 地图瓦片大小
# --- 信号（用于通知UI或相机聚焦） ---
#signal phase_changed(new_phase: int)
#signal active_char_changed(character: FCharacter)
#signal turn_ended(count: int)

func init_map_data() -> void: # 由Map节点调用
	used_cells = map_layer.get_used_cells()
	
	# 初始化特殊地块列表
	special_tiles["cover"] = map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.COVER, 0)
	special_tiles["heal"] = map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.HEAL, 0)
	special_tiles["cannon"] = map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.CANNON, 0)
	special_tiles["speed"] = map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.SPEED, 0)
	special_tiles["capture"] = map_layer.get_used_cells_by_id(0, ConstData.MAP_LAYER_ID.CAPTURE, 0)
	
	var count: int = 0
	for p in special_tiles["capture"]:
		var c_meta: Dictionary = { "pname": str(count), "index": -1, "cname": "null" }
		count += 1
		capture_status.get_or_add(p, c_meta)

## 开始一场全新的游戏
func start_game() -> void:
	turn_count = 1
	is_game_over = false
	# 不写 while 循环！直接触发第一步，后续全部交给事件链条驱动
	enter_phase(ConstData.GAME_PHASE.MOVE_STAGE)

## 切换全局阶段
func enter_phase(new_phase: ConstData.GAME_PHASE) -> void:
	current_phase = new_phase
	_prepare_action_queue()
	_run_next_player() # 驱动第一个人

## 准备当前阶段的轮流队列
func _prepare_action_queue() -> bool:
	action_queue.clear()
	if player_nodes.is_empty():
		_back_to_main_menu()
		return false
	for player in player_nodes:
		if player.is_alive: # 确保角色还活着（如果有死亡机制）
			action_queue.append(player)
	return true

## 驱动队列：没有 while 循环，一次只处理一个人！
func _run_next_player() -> void:
	if action_queue.is_empty():
		# 队列空了，代表全员该阶段做完了
		_on_phase_complete()
		return
		
	# 一次只弹出一个玩家
	current_active_char = action_queue.pop_front()
	current_active_char.start_turn_phase(current_phase)
	# 此时函数直接安全结束，完全不会锁死程序。
	# 游戏引擎会继续正常渲染、处理输入、播放玩家的移动动画。

## 供玩家节点在“所有动画和逻辑都完毕后”主动调用
func mint_player_action_finished() -> void:
	current_active_char = null
	
	# 核心：老玩家彻底结算完了，我们手动触发下一次点名
	_run_next_player()

## 当全员都完成了当前阶段
func _on_phase_complete() -> void:
	match current_phase:
		ConstData.GAME_PHASE.MOVE_STAGE:
			# 全员移动完 -> 进入全员战斗
			enter_phase(ConstData.GAME_PHASE.FIGHT_STAGE)
		ConstData.GAME_PHASE.FIGHT_STAGE:
			# 全员战斗完 -> 回合数递增，重新开始移动阶段
			turn_count += 1
			# 处理毒圈/Buff结算...
			enter_phase(ConstData.GAME_PHASE.MOVE_STAGE)


































































































func clear_hints():
	select_layer.clear()
	ex_layer.clear()

func _back_to_main_menu() -> void:
	current_phase = ConstData.GAME_PHASE.TURN_END
	get_tree().change_scene_to_file("res://src/tscn/MainMenu/MainMenu.tscn")

func set_select_map_id(m_id) -> void:
	TurnManager.reset_data()
	select_map_id = m_id
	map_data = GameData.map_data[select_map_id].duplicate(true)

func get_game_time() -> String:
	return "Turn %d: " % turn_count if turn_count else "Unknown"

func reset_data(data_id: String = "") -> void:
	match data_id:
		"map_info":
			_reset_map_info()
		"game_state":
			_reset_game_state()
		"turn_temp":
			_reset_turn_temp_data()
		"node_cache":
			_reset_node_cache()
		"map_cache":
			_reset_map_cache()
		"": # data_id 为空时，重置所有数据
			_reset_map_info()
			_reset_game_state()
			_reset_turn_temp_data()
			_reset_node_cache()
			_reset_map_cache()
		_:
			FLogger.warn("PlayingData reset fail, unknown data_id: " + data_id)

func _reset_map_info() -> void:
	select_map_id = ""
	map_data.clear()
	player_count = "2"

func _reset_game_state() -> void:
	current_phase = ConstData.GAME_PHASE.NONE
	turn_count = 0
	current_active_char = null
	win_index = -1
	is_game_over = false
	player_nodes.clear()
	action_queue.clear()

func _reset_turn_temp_data() -> void:
	valid_attack_targets.clear()

func _reset_node_cache() -> void:
	map_layer = null
	select_layer = null
	ex_layer = null
	node_map = null
	node_players = null
	node_ui_layer = null

func _reset_map_cache() -> void:
	used_cells.clear()
	
	# 重置特殊点位字典，保持键的存在
	for key in special_tiles.keys():
		special_tiles[key] = []
		
	capture_status.clear()
	forbidden_trigger_status.clear()
	bomb_trigger_status.clear()
	tile_size = null # 或者设置为默认的 Vector2i(0, 0) / null
