extends Node

@export var characters: Array[NodePath]
@export var move_hint_layer: NodePath  # 指向 MoveHintLayer
@export var tile_map_layer: NodePath
var move_layer: TileMapLayer
var forbidden_trigger_status: Dictionary = {}
var map_layer: TileMapLayer
var active_character: FCharacter
var current_index := 0
var waiting_for_click := false

var tile_cannon_list: Array[Vector2i] = []
var tile_speed_list: Array[Vector2i] = []
var tile_cover_list: Array[Vector2i] = []
var tile_heal_list: Array[Vector2i] = []
var tile_capture_list: Array[Vector2i] = []
var capture_status: Dictionary = {}

func _ready():
	move_layer = get_node(move_hint_layer)
	map_layer = get_node(tile_map_layer)
	_map_init()
	_update_capture_ui()
	_start_turn()

# 开始当前角色的回合
func _start_turn():
	active_character = get_node(characters[current_index])
	waiting_for_click = true
	_change_forbidden_trigger_status()
	_show_movable_tiles(active_character)
	
func _map_init():
	tile_cover_list = map_layer.get_used_cells_by_id(0, Vector2i(1, 0), 0)
	tile_heal_list = map_layer.get_used_cells_by_id(0, Vector2i(2, 0), 0)
	tile_cannon_list = map_layer.get_used_cells_by_id(0, Vector2i(3, 0), 0)
	tile_speed_list = map_layer.get_used_cells_by_id(0, Vector2i(4, 0), 0)
	tile_capture_list = map_layer.get_used_cells_by_id(1, Vector2i(-1, -1), 0)
	for p in tile_capture_list:
		capture_status.get_or_add(p, "null")
		
func _change_forbidden_trigger_status():
	# 如果没有被禁用的点位，直接跳过
	if forbidden_trigger_status.is_empty():
		return
	# 临时列表，用于存储要删除的点位
	var to_remove: Array[Vector2i] = []
	# 遍历所有禁用点位
	for p in forbidden_trigger_status.keys():
		forbidden_trigger_status[p] -= 1
		if forbidden_trigger_status[p] < 1:
			to_remove.append(p)
	# 删除所有过期的禁用点位
	for pos in to_remove:
		forbidden_trigger_status.erase(pos)

# 玩家点击处理
func _process(_delta):
	if not waiting_for_click:
		return

	if Input.is_action_just_pressed("click"):
		var mouse_pos = get_viewport().get_mouse_position()
		var grid = map_layer.local_to_map(mouse_pos)
		# 如果点击在可移动区域内
		var cell = move_layer.get_cell_atlas_coords(grid)
		if cell != Vector2i(1, 0):
			waiting_for_click = false
			_clear_move_hints()
			active_character.move_to(grid)
			active_character.connect("move_finished", Callable(self, "_on_move_finished"))

# 计算并显示可移动格
func _show_movable_tiles(character: FCharacter):
	_clear_move_hints()
	var origin = character.grid_position
	var used_cells: Array[Vector2i] = map_layer.get_used_cells()
	var grid_positions: Array[Vector2i] = []
	var forbidden_trigger_list: Array = forbidden_trigger_status.keys() if not forbidden_trigger_status.is_empty() else []
	for path in characters:
		grid_positions.append(get_node(path).grid_position)
	# 移动范围
	for x in range(-character.move_range, character.move_range + 1):
		for y in range(-character.move_range, character.move_range + 1):
			var p = Vector2i(origin.x + x, origin.y + y)
			if abs(x) + abs(y) <= character.move_range:
				if character._can_move_to(p) and p in used_cells:
					move_layer.set_cell(p, 2, Vector2i(0, 0))  # 可移动：蓝色格
					if forbidden_trigger_list and p in forbidden_trigger_list:
						move_layer.set_cell(p, 2, Vector2i(2, 0))  # 可移动，但点位效果不可用
	# 排除玩家坐标
	for p in grid_positions:
		if origin != p: # 排除自身
			move_layer.set_cell(p, 2, Vector2i(1, 0))
	# 填充其余空间
	for p in used_cells:
		if move_layer.get_cell_source_id(p) == -1:
			move_layer.set_cell(p, 2, Vector2i(1, 0))

# 清空提示层
func _clear_move_hints():
	move_layer.clear()

# 移动完成 → 占位判断+切换角色
func _on_move_finished(character: FCharacter):
	character.remove_tile_effect()
	var p = character.grid_position
	if tile_cannon_list and p in tile_cannon_list:
		character.temp_attack_bonus = character.attack
	elif tile_cover_list and p in tile_cover_list:
		character.temp_defense_bonus = 1
	elif tile_heal_list and p in tile_heal_list:
		character.current_hp += 1
	elif tile_capture_list and p in tile_capture_list:
		capture_status[p] = current_index
	else:
		pass
	if tile_speed_list and p in tile_speed_list:
		var forbidden_trigger_list: Array = forbidden_trigger_status.keys() if not forbidden_trigger_status.is_empty() else []
		if not(forbidden_trigger_list and p in forbidden_trigger_list):
			forbidden_trigger_status.get_or_add(p, 3)
			_next_turn(character, false)
			return
	_next_turn(character)

func _next_turn(character: FCharacter, switch_character: bool=true):
	character.disconnect("move_finished", Callable(self, "_on_move_finished"))
	if switch_character:
		current_index = (current_index + 1) % characters.size()
	_start_turn()

func _update_capture_ui():
	var name_container = $"../UiTab/HBoxContainer/HBoxContainer/VBoxContainer1"
	var info_container = $"../UiTab/HBoxContainer/HBoxContainer/VBoxContainer2"
	for child in name_container.get_children():
		child.queue_free()
	for child in info_container.get_children():
		child.queue_free()

	for key in capture_status.keys():
		var point_label = Label.new()
		var owner_label = Label.new()

		point_label.text = "%s 点：" % key
		owner_label.text = str(capture_status[key])

		name_container.add_child(point_label)
		info_container.add_child(owner_label)
