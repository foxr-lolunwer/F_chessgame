extends FCharacter

@export var ui_properties: VBoxContainer

func _ready():
	tilemap = $"../TileMapLayer"
	tile_size = tilemap.tile_set.tile_size
	current_hp = max_hp
	# 初始化位置到瓦片中心
	global_position = tilemap.map_to_local(grid_position)
	ui_properties.update_properties(self)

func _process(delta):
	if is_moving:
		_move_towards_target(delta)
	elif is_player_controlled:
		_handle_input()

func _handle_input():
	var direction := Vector2i.ZERO

	if Input.is_action_just_pressed("move_up"):
		direction = Vector2i(0, -1)
	elif Input.is_action_just_pressed("move_down"):
		direction = Vector2i(0, 1)
	elif Input.is_action_just_pressed("move_left"):
		direction = Vector2i(-1, 0)
	elif Input.is_action_just_pressed("move_right"):
		direction = Vector2i(1, 0)
	else:
		return

	if direction != Vector2i.ZERO:
		var target_grid = grid_position + direction

		# 判断该格子是否存在
		if _can_move_to(target_grid):
			grid_position = target_grid
			is_moving = true

			if direction.x != 0:
				sprite.flip_h = (direction.x < 0) == flip_h

func _move_towards_target(delta):
	var target_pos = tilemap.map_to_local(grid_position)
	var move_step = move_speed * tile_size.x * delta
	var diff = target_pos - global_position

	if diff.length() <= move_step:
		global_position = target_pos
		is_moving = false
	else:
		global_position += diff.normalized() * move_step

func _can_move_to(target_grid: Vector2i) -> bool:
	var tile_data = tilemap.get_cell_tile_data(target_grid)
	return tile_data != null
