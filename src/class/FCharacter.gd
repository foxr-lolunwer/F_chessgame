class_name FCharacter
extends CharacterBody2D

@export var is_player_controlled: bool = false
@export var cname: String = "null"  ## 角色名称
@export var max_hp: int = 5  ## 最大血量
@export var attack: int = 1  ## 攻击力
@export var defense: int = 0  ## 防御力
@export var move_range: int = 1  ## 移动长度
@export var is_main_player: bool = true
@export var tp_position_set: bool = false
@export var tp_position: Vector2i = Vector2i(0, 0)  ## 存储tp位置
@export var tp_range: int = 3  ## 传送矩形的1/2边长
@export var move_speed: float = 6.0  ## 每秒移动几格（越大越快）
@export var damage_range: int = 2  ## 攻击范围
@export var health_val: int = 1  ## 血量回复量
@export var current_hp: int = max_hp  ## 当前血量
@export var is_alive: bool = true  ## 是否存活
@export var temp_attack: int= 0  ## 临时攻击加成
@export var temp_defense: int= 0 ## 临时防御加成

var my_phase_state: ConstData.GAME_PHASE = ConstData.GAME_PHASE.NONE
var has_acted_this_phase: bool = false
var c_pos: Vector2i = Vector2i(0, 0)
var t_pos: Vector2i
var is_moving: bool = false
var tile_size: Vector2

#@onready var sprite: Sprite2D = $Sprite2D

#@export var info_ui: CharacterUiProperties

signal move_finished

## 初始化节点
func setup(pos: Vector2i, m_cname: String = "null"):
	c_pos = pos
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
func move_to(target: Vector2i):
	if not _can_move_to(target):
		return
	t_pos = target
	is_moving = true

	#if target.x < c_pos.x:
		#sprite.flip_h = not flip_h
	#elif target.x > c_pos.x:
		#sprite.flip_h = flip_h

# --- 移动动画 ---
func _move_towards_target(delta):
	var target_pos = TurnManager.tilemap.map_to_local(t_pos)
	var move_step = move_speed * tile_size.x * delta
	var diff = target_pos - global_position

	if diff.length() <= move_step:
		global_position = target_pos
		is_moving = false
		c_pos = t_pos
		emit_signal("move_finished")
	else:
		global_position += diff.normalized() * move_step

# --- 判断是否可到达 ---
func _can_move_to(target: Vector2i) -> bool:
	var tile_data = TurnManager.tilemap.get_cell_tile_data(target)
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
			# 激活移动UI、高亮移动格子
			print(name, " 请开始你的移动...")
			# 此时等待玩家鼠标点击地图或者键盘操作
			
		ConstData.GAME_PHASE.FIGHT_STAGE:
			# 激活技能/攻击UI、高亮射程
			print(name, " 请开始你的战斗/攻击...")

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
