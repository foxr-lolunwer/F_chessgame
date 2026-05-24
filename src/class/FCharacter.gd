class_name FCharacter
extends CharacterBody2D

@export var is_player_controlled: bool = false
@export var cname: String = "null"  ## 角色名称
@export var max_hp: int = 5  ## 最大血量
@export var attack: int = 1  ## 攻击力
@export var defense: int = 0  ## 防御力
@export var move_range: int = 1  ## 移动长度
@export var is_main_player: bool = true
@export var set_tp_position: bool = false  ## 是否正在设置tp位置
@export var tp_position: Vector2i  ## 存储tp位置
@export var tp_range: int = 3  ## 传送矩形的1/2边长
@export var move_speed: float = 6.0  ## 每秒移动几格（越大越快）
@export var damage_range: int = 2  ## 攻击范围
@export var health_val: int = 1  ## 血量回复量
@export var current_hp: int = max_hp  ## 当前血量
@export var is_alive: bool = true  ## 是否存活
@export var temp_attack: int= 0  ## 临时攻击加成
@export var temp_defense: int= 0 ## 临时防御加成

@export var my_phase_state: ConstData.GAME_PHASE = ConstData.GAME_PHASE.NONE  ## 当前阶段类型
@export var has_acted_this_phase: bool = false  ## 
@export var c_pos: Vector2i = Vector2i(0, 0)  ## 当前位置
@export var t_pos: Vector2i  ## 目标位置
@export var is_moving: bool = false  ## 是否正在移动
@export var c_move_type: ConstData.MOVE_OPERATION  ## 当前移动操作类型
@export var c_fight_type: ConstData.FIGHT_OPERATION  ## 当前战斗操作类型

#@onready var sprite: Sprite2D = $Sprite2D

#@export var info_ui: CharacterUiProperties

## 初始化节点
func base_setup(pos: Vector2i, m_cname: String):
	c_pos = pos
	tp_position = c_pos # 设置起始tp位置
	cname = m_cname
	current_hp = max_hp
	#info_ui = ui
	global_position = TurnManager.map_layer.map_to_local(c_pos)
	#ui_link = true
	#attr_update()

func _process(delta):
	if is_moving:
		_move_towards_target(delta)

func apply_damage(damage: int):
	current_hp -= damage

# --- 外部控制角色移动 ---
func move_to(tp: bool = false):
	if not _can_move_to(t_pos):
		FLogger.error("%s can not move to %s" % [cname, str(t_pos)])
		return
	if tp:
		c_pos = t_pos
	else:
		is_moving = true

	#if target.x < c_pos.x:
		#sprite.flip_h = not flip_h
	#elif target.x > c_pos.x:
		#sprite.flip_h = flip_h

# --- 移动动画 ---
func _move_towards_target(delta):
	var target_pos = TurnManager.map_layer.map_to_local(t_pos)
	var move_step = move_speed * TurnManager.tile_size.x * delta
	var diff = target_pos - global_position

	if diff.length() <= move_step:
		global_position = target_pos
		is_moving = false
		c_pos = t_pos
		TurnManager.mint_player_action_finished()
	else:
		global_position += diff.normalized() * move_step

# --- 判断是否可到达 ---
func _can_move_to(target: Vector2i) -> bool:
	var tile_data = TurnManager.map_layer.get_cell_tile_data(target)
	return tile_data != null

func remove_tile_effect():
	temp_attack = 0
	temp_defense = 0

## 接受管理器指挥：开始当前阶段的行动
func start_turn_phase(phase: ConstData.GAME_PHASE) -> void:
	my_phase_state = phase
	has_acted_this_phase = false
	
	match my_phase_state:
		ConstData.GAME_PHASE.MOVE_STAGE:
			_move_phase()
				# ConstData.MOVE_OPERATION.TELEPORT:
				# 	_handle_teleport_logic(origin, other_chars_pos)
			# 此时等待玩家鼠标点击地图或者键盘操作
		ConstData.GAME_PHASE.FIGHT_STAGE:
			_move_phase()
			# _fight_phase()
## 激活移动UI、高亮移动格子
func _move_phase(roll: bool = true) -> void:
	if c_move_type == ConstData.MOVE_OPERATION.NONE and not roll:
		roll = true
		FLogger.warn("c_move_type is NONE, but roll is false.")
	if roll:
		var rng = RandomNumberGenerator.new()
		rng.randomize()
		c_move_type = FL.roll_with_weight(TurnManager.move_type_roll, rng)
	
	var other_chars_pos: Array[Vector2i] = []
	for char_node: FCharacter in TurnManager.player_nodes:
		other_chars_pos.append(char_node.c_pos)
	
	match c_move_type:
		ConstData.MOVE_OPERATION.CROSS, ConstData.MOVE_OPERATION.DOUBLE_CROSS, ConstData.MOVE_OPERATION.DIAGONAL:
			var cmr = move_range  # 当前移动距离
			if c_move_type == ConstData.MOVE_OPERATION.DOUBLE_CROSS:
				cmr *= 2
			var dirs: Array[Vector2i]
			if c_move_type == ConstData.MOVE_OPERATION.DIAGONAL:
				dirs = [Vector2i(1, 1), Vector2i(1, -1), Vector2i(-1, 1), Vector2i(-1, -1)]
			else:
				dirs = [Vector2i(0, 1), Vector2i(0, -1), Vector2i(1, 0), Vector2i(-1, 0)]
				
			for dir in dirs:
				for step in range(1, cmr + 1):
					var p = c_pos + dir * step
					# 边界检查与阻挡检查
					if not (p in TurnManager.used_cells) or not _can_move_to(p):
						break
					
					var cell_color = ConstData.ATLAS_COORDS.BLUE_MOVE
					# if p in forbidden_list:
					# 	cell_color = ConstData.ATLAS_COORDS.GRAY_FORBIDDEN
					if p in other_chars_pos:
						cell_color = ConstData.ATLAS_COORDS.RED_ATTACK
						
					TurnManager.select_layer.set_cell(p, 1, cell_color)
			_handle_move_operate()

func _handle_move_operate():
	pass
# func _handle_teleport_logic(origin: Vector2i, other_chars_pos:Array[Vector2i]):
# 	var reset_tp_position: bool = true
# 	if current_active_char.tp_position_set:
# 		# 检查传送点上是否有本体或其他人，如果有，重新设置点位
# 		if origin != current_active_char.tp_position and current_active_char.tp_position not in other_chars_pos:
# 			var tp_pos = current_active_char.tp_position
# 			if tp_pos != null and tp_pos in used_cells:
# 				_move_layer.set_cell(tp_pos, 2, ConstData.ATLAS_COORDS.BLUE_MOVE)
# 			_move_layer.set_cell(origin, 2, ConstData.ATLAS_COORDS.BLUE_MOVE)
# 			current_active_char.tp_position_set = false
# 			reset_tp_position = false
# 		else:
# 			print("传送点位已不可用，请重新设置")
# 			reset_tp_position = true
# 	if reset_tp_position:
# 		var tp_range = current_active_char.tp_range
# 		#var tp_area = _map_layer.get_used_cells() # 简化：所有格子都在范围内？需确认逻辑
# 		# 这里原本逻辑似乎是全图遍历范围？保持原逻辑
# 		for x in range(-tp_range, tp_range + 1):
# 			for y in range(-tp_range, tp_range + 1):
# 				var p = origin + Vector2i(x, y)
# 				if p in used_cells and current_active_char._can_move_to(p):
# 					_move_layer.set_cell(p, 2, ConstData.ATLAS_COORDS.PURPLE_TELEPORT)

## 玩家点击了“结束行动”按钮，或者移动/攻击动画播放完毕后调用
func player_finished_input() -> void:
	if has_acted_this_phase: return
	has_acted_this_phase = true
	
	# 向中央汇报：我动完了！
	TurnManager.finish_current_player_action()

## 清理当前状态
func end_turn_phase() -> void:
	my_phase_state = ConstData.GAME_PHASE.NONE
	# 隐藏高亮格子、禁用技能UI等

## 属性更新时调用，默认不执行操作，如果需要在属性更新时执行操作，比如更新UI显示，覆写此方法
func attr_update(attr: String = ""):
	pass
	
func set_max_hp(value):
	if value < 0:
		value = 0
		is_alive = false
	if value < current_hp:
		current_hp = value
	max_hp = value
	attr_update("hp")
	
func set_attack(value):
	if value < 0:
		value = 0
	attack = value
	attr_update("attack")

func set_defense(value):
	if value < 0:
		value = 0
	defense = value
	attr_update("defense")
	
func set_health_val(value):
	if value < 0:
		value = 0
	health_val = value

func set_current_hp(value):
	if value < 0:
		value = 0
		is_alive = false
	if value > max_hp:
		value = max_hp
	current_hp = value
	attr_update("hp")

func set_temp_attack(value):
	if -value > attack:
		value = 0
	temp_attack = value
	attr_update("attack")

func set_temp_defense(value):
	if -value > defense:
		value = 0
	temp_defense = value
	attr_update("defense")
