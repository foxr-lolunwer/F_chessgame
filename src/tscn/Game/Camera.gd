extends Camera2D

var setuped: bool = false

@onready var display_sprite: TileMapLayer
var map_width_pixels: float # 你的地图像素宽度
var map_height_pixels: float

@export_group("Movement")
@export var speed: float = 1000.0      ## 移动速度
@export var acceleration: float = 10.0 ## 加速度（平滑感）
@export var dragging_acceleration: float = 5.0 ## 加速度（拖动时）

@export_group("Zoom")
@export var zoom_speed: float = 0.1     ## 缩放速度
@export var min_zoom := 0.1            ## 最小缩放
@export var min_zoom_padding: float = 1  ## 基于地图尺寸的最小缩放乘数
@export var max_zoom: float = 2.0      ## 最大缩放
@export var zoom_duration: float = 0.15 ## 缩放平滑时间

var target_zoom: float = 1.0
# 平滑移动
var velocity: Vector2 = Vector2.ZERO
var drag_velocity: Vector2 = Vector2.ZERO
# 中键拖动
var is_dragging := false

func setup():
	display_sprite = TurnManager.map_layer
	var rect: Rect2i = display_sprite.get_used_rect()
	map_width_pixels = rect.size.x * TurnManager.tile_size.x
	map_height_pixels = rect.size.y * TurnManager.tile_size.y
	_update_dynamic_zoom()
	target_zoom = clamp(zoom.x, min_zoom, max_zoom)
	zoom = Vector2.ONE * target_zoom
	setuped = true

func _update_dynamic_zoom():
	var viewport_size = get_viewport_rect().size
	# 希望最小缩放时：
	# 视口尺寸 = 地图尺寸 × 1.25
	var zoom_x = (map_width_pixels * min_zoom_padding) / viewport_size.x
	var zoom_y = (map_height_pixels * min_zoom_padding) / viewport_size.y
	min_zoom = max(max(zoom_x, zoom_y), min_zoom)

func _process(delta):
	if not setuped:
		return
	# 1. 预处理：记录缩放前的鼠标世界位置
	var mouse_pos_before_zoom = get_global_mouse_position()

	# 2. 执行缩放 (仅改变 zoom 值)
	var old_zoom = zoom.x
	zoom.x = lerp(zoom.x, target_zoom, 1.0 - pow(0.01, delta / zoom_duration))
	zoom.y = zoom.x

	# 3. 立即修正缩放造成的“偏移”
	# 注意：这一步要先于 WASD 移动执行，确保相机中心点对准缩放目标
	if abs(zoom.x - old_zoom) > 0.0001:
		var mouse_pos_after_zoom = get_global_mouse_position()
		position += (mouse_pos_before_zoom - mouse_pos_after_zoom)

	# 4. WASD 移动逻辑 (叠加在修正后的位置上)
	var target_vel = Vector2.ZERO
	if is_dragging:
		target_vel = drag_velocity
		# 每一帧都衰减 drag_velocity，防止鼠标不动时相机还疯狂飞
		drag_velocity = drag_velocity.lerp(Vector2.ZERO, 0.2) 
	else:
		var input_dir = Input.get_vector("move_left", "move_right", "move_up", "move_down")
		var current_speed = speed / zoom.x 
		target_vel = input_dir * current_speed
	velocity = velocity.lerp(target_vel, acceleration * delta)
	position += velocity * delta
	if position.x < 0:
		position.x = 0
	if position.x > map_width_pixels:
		position.x = map_width_pixels
	if position.y < 0:
		position.y = 0
	if position.y > map_height_pixels:
		position.y = map_height_pixels

func _unhandled_input(event):
	if not setuped:
		return
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_MIDDLE:
			is_dragging = event.pressed

		if event.is_pressed():
			if event.button_index == MOUSE_BUTTON_WHEEL_UP:
				target_zoom = clamp(target_zoom + target_zoom * zoom_speed, min_zoom, max_zoom)
			elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
				target_zoom = clamp(target_zoom - target_zoom * zoom_speed, min_zoom, max_zoom)

	elif event is InputEventMouseMotion and is_dragging:
		# 计算阻尼 
		drag_velocity = -event.relative / zoom.x / get_process_delta_time()
