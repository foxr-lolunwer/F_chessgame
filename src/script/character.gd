class_name FCharacter
extends CharacterBody2D

@export var is_player_controlled: bool = true
@export var cname: String = "null"
@export var max_hp: int = 5
@export var attack: int = 1
@export var defense: int = 0
@export var move_range: int = 5
@export var move_speed: float = 6.0  # 每秒移动几格（越大越快）
@export var flip_h: bool = true

var current_hp: int = max_hp
var is_alive: bool = false

@export var grid_position: Vector2i = Vector2i(0, 0)

@onready var sprite: Sprite2D = $Sprite2D
var tilemap: TileMapLayer 
var is_moving: bool = false
var tile_size: Vector2
