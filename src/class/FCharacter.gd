class_name FCharacter
extends CharacterBody2D

var ui_link: bool = false
@export var is_player_controlled: bool = false
@export var cname: String = "null"
@export var max_hp: int = 5
@export var attack: int = 1
@export var defense: int = 0
@export var move_range: int = 1  # 移动长度
@export var is_main_player: bool = true
@export var tp_position_set: bool = false
@export var tp_position: Vector2i = Vector2i(0, 0)
@export var tp_range: int = 3  # 传送矩形的1/2边长
@export var move_speed: float = 6.0  # 每秒移动几格（越大越快）
@export var damage_range: int = 2  # 攻击范围
@export var health_val: int = 1
@export var flip_h: bool = true
@export var current_hp: int = max_hp
@export var is_alive: bool = true
@export var temp_attack: int= 0
@export var temp_defense: int= 0

var c_pos: Vector2i = Vector2i(0, 0)
var t_pos: Vector2i
var is_moving: bool = false
var tile_size: Vector2

#@onready var sprite: Sprite2D = $Sprite2D

#@export var info_ui: CharacterUiProperties

signal move_finished

func setup(pos: Vector2i, m_cname: String = "null"):
	c_pos = pos
	cname = m_cname
	current_hp = max_hp
	#info_ui = ui
	global_position = PD.map_layer.map_to_local(c_pos)
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
	var target_pos = PD.tilemap.map_to_local(t_pos)
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
	var tile_data = PD.tilemap.get_cell_tile_data(target)
	return tile_data != null

func remove_tile_effect():
	temp_attack = 0
	temp_defense = 0
	
func attr_update(attr: String = ""):
	# 视情况覆写
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
