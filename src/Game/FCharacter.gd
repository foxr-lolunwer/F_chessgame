class_name FCharacter
extends CharacterBody2D

var ui_link: bool = false
@export var is_player_controlled: bool = false
@export var cname: String = "null"
@export var max_hp: int = 5:
	set(value):
		if value < 0:
			value = 0
			is_alive = false
		if value < current_hp:
			current_hp = value
		max_hp = value
		ui_properties_update()
@export var attack: int = 1:
	set(value):
		if value < 0:
			value = 0
		attack = value
		ui_properties_update()
@export var defense: int = 0:
	set(value):
		if value < 0:
			value = 0
		defense = value
		ui_properties_update()
@export var move_range: int = 1  # 移动长度
@export var is_main_player: bool = true
@export var tp_position_set: bool = false
@export var tp_position: Vector2i = Vector2i(0, 0)
@export var tp_range: int = 3  # 传送矩形的1/2边长
@export var move_speed: float = 6.0  # 每秒移动几格（越大越快）
@export var damage_range: int = 2  # 攻击范围
@export var health_val: int = 1:
	set(value):
		if value < 0:
			value = 0
		health_val = value

@export var flip_h: bool = true
@export var current_hp: int = max_hp:
	set(value):
		if value < 0:
			value = 0
			is_alive = false
		if value > max_hp:
			value = max_hp
		current_hp = value
		ui_properties_update()
@export var is_alive: bool = true
@export var temp_attack_bonus: int= 0:
	set(value):
		if -value > attack:
			value = 0
		temp_attack_bonus = value
		ui_properties_update()
@export var temp_defense_bonus: int= 0:
	set(value):
		if -value > defense:
			value = 0
		temp_defense_bonus = value
		ui_properties_update()

@export var grid_position: Vector2i = Vector2i(0, 0)
var target_grid: Vector2i
var tilemap: TileMapLayer
var is_moving: bool = false
var tile_size: Vector2

@onready var sprite: Sprite2D = $Sprite2D

@export var ui_properties: CharacterUiProperties

signal move_finished

func _ready():
	tilemap = $"../TileMapLayer"
	tile_size = tilemap.tile_set.tile_size
	current_hp = max_hp
	## 初始化位置到瓦片中心
	global_position = tilemap.map_to_local(grid_position)
	ui_link = true
	ui_properties_update()

func _process(delta):
	if is_moving:
		_move_towards_target(delta)

func apply_damage(damage: int):
	current_hp -= damage

# --- 外部控制角色移动 ---
func move_to(target: Vector2i):
	if not _can_move_to(target):
		return
	target_grid = target
	is_moving = true

	if target.x < grid_position.x:
		sprite.flip_h = not flip_h
	elif target.x > grid_position.x:
		sprite.flip_h = flip_h

# --- 移动动画 ---
func _move_towards_target(delta):
	var target_pos = tilemap.map_to_local(target_grid)
	var move_step = move_speed * tile_size.x * delta
	var diff = target_pos - global_position

	if diff.length() <= move_step:
		global_position = target_pos
		is_moving = false
		grid_position = target_grid
		emit_signal("move_finished")
	else:
		global_position += diff.normalized() * move_step

# --- 判断是否可到达 ---
func _can_move_to(target: Vector2i) -> bool:
	var tile_data = tilemap.get_cell_tile_data(target)
	return tile_data != null

func remove_tile_effect():
	temp_attack_bonus = 0
	temp_defense_bonus = 0
	
func ui_properties_update():
	if ui_link:
		ui_properties.update_properties(self)
	
