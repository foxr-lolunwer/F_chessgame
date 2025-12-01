extends Node

@export var characters: Array[NodePath]
@export var move_hint_layer: NodePath  # 指向 MoveHintLayer
@export var tile_map_layer: NodePath
@export var ex_map_layer: NodePath
var move_layer: TileMapLayer
var forbidden_trigger_status: Dictionary = {}
var bomb_trigger_status: Dictionary = {}
var map_layer: TileMapLayer
var active_character: Player
var current_index := 0
var waiting_for_click := false
var ex_layer: TileMapLayer
var switch_character: bool = true

var can_attack_targets: Array[FCharacter]
var move_type: int
@export var keep_move_type: bool = false
var fight_type: int
@export var keep_fight_type: bool = false

var tile_cannon_list: Array[Vector2i] = []
var tile_speed_list: Array[Vector2i] = []
var tile_cover_list: Array[Vector2i] = []
var tile_heal_list: Array[Vector2i] = []
var tile_capture_list: Array[Vector2i] = []
var capture_status: Dictionary = {}
var capture_ui_name_container: VBoxContainer
var capture_ui_info_container: VBoxContainer
var used_cells: Array[Vector2i]

var win_index:int = -1

enum MOVE_OPERATION {
	CROSS,        # 十字移动(上下左右)
	DIAGONAL,     # 斜线移动(对角线*行动力)
	DOUBLE_CROSS, # 十字移动*2(行动力翻倍)
	TELEPORT      # 传送(第一次先设置传送点,第二次直接传送,传送点作废)
}
@export var move_type_roll: Array[Array] = [
	[MOVE_OPERATION.CROSS, 2],
	[MOVE_OPERATION.DIAGONAL, 2],
	[MOVE_OPERATION.DOUBLE_CROSS, 1],
	[MOVE_OPERATION.TELEPORT, 1]
]
enum FIGHT_OPERATION {
	NORMAL_SHOT,   # 普通射击
	X_RAY,         # X射线攻击
	POWER_SHOT,    # 强力射击
	BOMB,          # 炸弹
	HEALTH         # 治疗
}
@export var fight_type_roll: Array[Array] = [
	[FIGHT_OPERATION.NORMAL_SHOT, 2],
	[FIGHT_OPERATION.X_RAY, 0],
	[FIGHT_OPERATION.POWER_SHOT, 0],
	[FIGHT_OPERATION.BOMB, 0],
	[FIGHT_OPERATION.HEALTH, 0]
]

enum GAME_TURN_TYPE {
	MOVE,
	FIGHT
}
var move_turn_count: int = 0
var fight_turn_count: int = 0
var turn_type: int = GAME_TURN_TYPE.MOVE

func _ready():
	move_layer = get_node(move_hint_layer)
	map_layer = get_node(tile_map_layer)
	ex_layer = get_node(ex_map_layer)
	_map_init()
	_capture_ui_init()
	_start_turn()
func _map_init():
	tile_cover_list = map_layer.get_used_cells_by_id(0, Vector2i(1, 0), 0)
	tile_heal_list = map_layer.get_used_cells_by_id(0, Vector2i(2, 0), 0)
	tile_cannon_list = map_layer.get_used_cells_by_id(0, Vector2i(3, 0), 0)
	tile_speed_list = map_layer.get_used_cells_by_id(0, Vector2i(4, 0), 0)
	tile_capture_list = map_layer.get_used_cells_by_id(1, Vector2i(-1, -1), 0)
	used_cells = map_layer.get_used_cells()
	var count: int = 0
	for p in tile_capture_list:
		var c_meta: Dictionary = { "pname": str(count), "index": -1, "cname": "null" }
		count += 1
		capture_status.get_or_add(p, c_meta)
func _capture_ui_init():
	capture_ui_name_container = $"../UiTab/HBoxContainer/HBoxContainer/VBoxContainer1"
	capture_ui_info_container = $"../UiTab/HBoxContainer/HBoxContainer/VBoxContainer2"
	_update_capture_ui()
func _start_turn():
	if win_index > -1:
		print("%s win!" % get_node(characters[win_index]).cname)
	match turn_type:
		0:
			_start_move_turn()
		1:
			_start_fight_turn()
	_check_forbidden_trigger_status()
func _start_move_turn():
	active_character = get_node(characters[current_index])
	waiting_for_click = true
	_clear_move_hints()
	var origin = active_character.grid_position
	var grid_positions: Array[Vector2i] = []
	var forbidden_trigger_list: Array = forbidden_trigger_status.keys() if not forbidden_trigger_status.is_empty() else []
	for path in characters:
		grid_positions.append(get_node(path).grid_position)
	# 抽取移动类型
	var key_list = MOVE_OPERATION.keys()
	if not keep_move_type:
		move_type = MOVE_OPERATION[key_list[weighted_random(move_type_roll)]]
	else:
		keep_move_type = false
	var m_move_range = active_character.move_range
	match move_type:
		MOVE_OPERATION.CROSS, MOVE_OPERATION.DOUBLE_CROSS, MOVE_OPERATION.DIAGONAL:
			# 如果是 DOUBLE_CROSS，移动范围加倍
			if move_type == MOVE_OPERATION.DOUBLE_CROSS:
				m_move_range *= 2
			var dirs: Array 
			if move_type == MOVE_OPERATION.DIAGONAL:
				dirs = [Vector2i(1, 1),Vector2i(1, -1),Vector2i(-1, 1),Vector2i(-1, -1)]
			else:
				dirs = [Vector2i(1, 0),Vector2i(-1, 0),Vector2i(0, 1),Vector2i(0, -1)]
			for dir in dirs:
				for step in range(1, m_move_range + 1):
					var p = origin + dir * step
					# 如果超出地图使用格、或该格不能走，终止本方向的延伸
					if not (p in used_cells) or not active_character._can_move_to(p):
						break
					# 可走则设置提示格：优先判断是否为禁用效果点位
					if forbidden_trigger_list and p in forbidden_trigger_list:
						move_layer.set_cell(p, 2, Vector2i(2, 0))  # 禁用效果的提示（灰）
					else:
						move_layer.set_cell(p, 2, Vector2i(0, 0))  # 可移动：蓝色格
		MOVE_OPERATION.TELEPORT:
			if active_character.tp_position_set:
				var tp_pos = active_character.tp_position
				# 第二次触发：执行传送
				if tp_pos != null and tp_pos in used_cells:
					move_layer.set_cell(tp_pos, 2, Vector2i(0, 0))
				move_layer.set_cell(origin, 2, Vector2i(0, 0))
				# 清除标记与提示
				active_character.tp_position_set = false
			else:
				# 第一次触发：设置传送点选择范围
				var tp_range = active_character.tp_range
				var tp_allow_positions: Array = map_layer.get_used_cells_by_id(0, Vector2i(0, 0), 0)
				for x in range(-tp_range, tp_range + 1):
					for y in range(-tp_range, tp_range + 1):
						var p = Vector2i(origin.x + x, origin.y + y)
						if not (p in tp_allow_positions):
							continue
						if active_character._can_move_to(p):
							move_layer.set_cell(p, 2, Vector2i(3, 0))  # 紫色：传送目标范围
	# 排除玩家坐标
	for p in grid_positions:
		if origin != p: # 排除自身
			move_layer.set_cell(p, 2, Vector2i(1, 0))
	# 填充其余空间
	for p in used_cells:
		if move_layer.get_cell_source_id(p) == -1:
			move_layer.set_cell(p, 2, Vector2i(1, 0))
func _start_fight_turn():
	active_character = get_node(characters[current_index])
	var key_list = FIGHT_OPERATION.keys()
	if not keep_fight_type:
		fight_type = FIGHT_OPERATION[key_list[weighted_random(fight_type_roll)]]
	else:
		keep_fight_type = false
	var origin = active_character.grid_position
	var damage_range: int = active_character.damage_range
	match fight_type:
		FIGHT_OPERATION.NORMAL_SHOT, FIGHT_OPERATION.POWER_SHOT:
			can_attack_targets.clear()
			for x in range(-damage_range, damage_range + 1):
				for y in range(-damage_range, damage_range + 1):
					var p = Vector2i(origin.x + x, origin.y + y)
					# 攻击范围
					if abs(x) + abs(y) <= damage_range:
						for target_path in characters:
							var target: FCharacter = get_node(target_path)
							if target == active_character:
								continue
							if target.grid_position == p:
								can_attack_targets.append(target)
								ex_layer.set_cell(p, 2, Vector2i(1, 0)) # 显示可攻击
								break
			# 没有可攻击目标 → 直接切换角色
			if can_attack_targets.is_empty():
				print(active_character.cname, "没有目标可攻击")
				_next_turn()
			else:
				waiting_for_click = true
				print("请选择攻击目标")
			return
		FIGHT_OPERATION.HEALTH:
			active_character.current_hp += active_character.health_val
			print(active_character.cname, "生命恢复")
			_next_turn()
		FIGHT_OPERATION.X_RAY:
			var dirs: Array = [Vector2i(1, 1),Vector2i(1, -1),Vector2i(-1, 1),Vector2i(-1, -1)]
			var m_damage_range = damage_range * 3
			for dir in dirs:
				for step in range(1, m_damage_range + 1):
					var p = origin + dir * step
					# 如果超出地图使用格、或该格不能走，终止本方向的延伸
					if not (p in used_cells) or not active_character._can_move_to(p):
						break
					# 可走则设置提示格：优先判断是否为禁用效果点位
					for character_path in characters:
						var target_character: FCharacter = get_node(character_path)
						if p == target_character.grid_position:
							_apply_damage(active_character, target_character)
			return
	

	

# 检查临时禁用的点位回合数 
func _check_forbidden_trigger_status():
	if forbidden_trigger_status.is_empty():
		return
	var to_remove: Array[Vector2i] = []
	for p in forbidden_trigger_status.keys():
		var c_meta: Dictionary = forbidden_trigger_status[p]
		var c_turn_type = c_meta.get("turn_type", -1)
		var c_turn_count = c_meta.get("turn_count", 0)
		# 判断当前是哪种统计方式
		var current_count = 0
		if c_turn_type == GAME_TURN_TYPE.MOVE:
			current_count = move_turn_count
		elif c_turn_type == GAME_TURN_TYPE.FIGHT:
			current_count = fight_turn_count
		else: # c_turn_type == -1
			current_count = move_turn_count + fight_turn_count  # 双计数模式
		# 若已过期则标记删除
		if current_count >= c_turn_count:
			to_remove.append(p)
	# 移除已过期项
	for pos in to_remove:
		forbidden_trigger_status.erase(pos)
	if not to_remove.is_empty():
		print("已解除禁用点位：", to_remove)
# 检查炸弹是否应引爆
func _check_bombs():
	if bomb_trigger_status.is_empty():
		return
	var to_explode: Array[Vector2i] = []
	for p in bomb_trigger_status.keys():
		var meta = bomb_trigger_status[p]
		var idx = meta["character_index"]
		var turn = meta["explode_turn"]
		if current_index == idx and fight_turn_count >= turn:
			to_explode.append(p)
	for p in to_explode:
		pass
		#_explode_bomb(p, get_node(characters[bomb_status[p]["character_index"]]))
		#bomb_status.erase(p)
# 玩家点击处理
func _process(_delta):
	if not waiting_for_click:
		return
	if Input.is_action_just_pressed("click"):
		var mouse_pos = get_viewport().get_mouse_position()
		var grid = map_layer.local_to_map(mouse_pos)
		var cell = move_layer.get_cell_atlas_coords(grid)
		# 如果点击在可移动区域(绿框)内
		if turn_type == GAME_TURN_TYPE.MOVE:	
			# 设置传送点位
			if cell == Vector2i(3, 0):
				_clear_move_hints()
				waiting_for_click = false
				active_character.tp_position_set = true
				active_character.tp_position = grid
				_next_turn()
				return
			if cell in [Vector2i(0, 0), Vector2i(2, 0)]:
				_clear_move_hints()
				waiting_for_click = false
				active_character.move_to(grid)
				active_character.connect("move_finished", Callable(self, "_on_move_finished"))
		else:
			cell = ex_layer.get_cell_atlas_coords(grid)
		if turn_type == GAME_TURN_TYPE.FIGHT:
			# 找到对应目标
			if cell == Vector2i(1, 0):
				for character in can_attack_targets:
					var target: FCharacter = character
					if target.grid_position == grid:
						_clear_move_hints()
						waiting_for_click = false
						_apply_damage(active_character, target)
						break
					
func _apply_damage(attacker:FCharacter, target:FCharacter):
	var attack_val = attacker.attack + attacker.temp_attack_bonus
	var defense_val = target.defense + target.temp_defense_bonus
	var damage = max(attack_val - defense_val, 0)
	if fight_type in [FIGHT_OPERATION.POWER_SHOT, FIGHT_OPERATION.X_RAY]:
		damage *= 2
	target.apply_damage(damage)
	print(attacker.cname, "攻击", target.cname, "造成", damage, "伤害")
	if target.current_hp <= 0:
		target.is_alive = false
		print(target.cname, "被击败")
	_next_turn()
	
# 清空提示层 - move
func _clear_move_hints():
	move_layer.clear()
	ex_layer.clear()
# 移动完成 → 占位判断+切换角色 - move
func _on_move_finished():
	active_character.remove_tile_effect()
	var p = active_character.grid_position
	if tile_cannon_list and p in tile_cannon_list:
		active_character.temp_attack_bonus = active_character.attack
	elif tile_cover_list and p in tile_cover_list:
		active_character.temp_defense_bonus = 1
	elif tile_heal_list and p in tile_heal_list:
		active_character.current_hp += 1
	elif tile_capture_list and p in tile_capture_list:
		capture_status[p]["index"] = current_index
		capture_status[p]["cname"] = active_character.cname
		_update_capture_ui()
	else:
		pass
	if tile_speed_list and p in tile_speed_list:
		var forbidden_trigger_list: Array = forbidden_trigger_status.keys() if not forbidden_trigger_status.is_empty() else []
		if not(forbidden_trigger_list and p in forbidden_trigger_list):
			var c_meta: Dictionary = { "turn_type": GAME_TURN_TYPE.MOVE, "turn_count": move_turn_count + 3 }
			forbidden_trigger_status.get_or_add(p, c_meta)
			keep_move_type = true
			switch_character = false
	_next_turn()

# 更新占领UI
func _update_capture_ui():
	for child in capture_ui_name_container.get_children():
		child.queue_free()
	for child in capture_ui_info_container.get_children():
		child.queue_free()

	for key in capture_status.keys():
		var point_label = Label.new()
		var owner_label = Label.new()

		point_label.text = "%s 点：" % capture_status[key]["pname"]
		owner_label.text = str(capture_status[key]["cname"])

		capture_ui_name_container.add_child(point_label)
		capture_ui_info_container.add_child(owner_label)
# 加权随机
func weighted_random(items: Array[Array]) -> int:
	# 计算总权重
	var total_weight = 0
	for item_array in items:
		total_weight += item_array[1]
	# 生成随机数（0到总权重之间）
	var random_value = randf() * total_weight  # randf()返回0-1之间的浮点数
	# 遍历权重区间，找到随机数落在的区间
	var current_sum = 0
	for item_array in items:
		current_sum += item_array[1]
		if random_value < current_sum:
			return item_array[0]
	return -1
# 占领胜利判断
func _capture_win():
	if not capture_status:
		return -1
	var a_index: int = -1
	for key in capture_status:
		var b_index:int = capture_status[key]["index"]
		a_index = capture_status[key]["index"]
		if a_index == -1 and b_index != -1:
			a_index = b_index
			return
		if a_index != b_index:
			return
	win_index = a_index
func _kill_win():
	var alive_count = 0
	var winner_index = -1
	# 遍历所有角色，检查哪个角色仍然存活
	for idx in range(characters.size()):
		var character = get_node(characters[idx])
		if character.is_alive:
			alive_count += 1
			if alive_count > 1:
				return
			winner_index = idx
	win_index = winner_index
	
# 下回合 - move
func _next_turn():
	if turn_type == GAME_TURN_TYPE.MOVE:
		_capture_win()
		if active_character.is_connected("move_finished", Callable(self, "_on_move_finished")):
			active_character.disconnect("move_finished", Callable(self, "_on_move_finished"))
	elif turn_type == GAME_TURN_TYPE.FIGHT:
		_kill_win()
	if win_index > -1:
		_start_turn()
		return
	var original_index = current_index
	if switch_character:
		# 跳过所有已死亡的角色，直到找到一个存活的角色
		# 继续循环，直到找到一个存活的角色
		current_index = (current_index + 1) % characters.size()
		while !get_node(characters[current_index]).is_alive:
			current_index = (current_index + 1) % characters.size()
			# 如果绕一圈都没有找到存活的角色，结束游戏或其他处理
			if current_index == original_index:
				print("没有存活角色，游戏结束")
				win_index = original_index
				_start_turn()  # TODO 添加无存活角色异常处理
				return
	if current_index < original_index:
		if turn_type == GAME_TURN_TYPE.MOVE:
			move_turn_count += 1
			turn_type = GAME_TURN_TYPE.FIGHT
		elif turn_type == GAME_TURN_TYPE.FIGHT:
			fight_turn_count += 1
			turn_type = GAME_TURN_TYPE.MOVE
	switch_character = true
	_start_turn()
