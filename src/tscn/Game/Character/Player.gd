extends FCharacter

@export var label_attack: Label
@export var label_defense: Label
@export var progress_bar_hp: TextureProgressBar
@export var color_bg: TextureRect

func _ready():
	pass

func setup(pos: Vector2i, m_cname: String, m_color: Color):
	base_setup(pos, m_cname)
	label_attack = $Container/DataArea/MarginContainer/AttackBg/AttackContainer/LabelAttack
	label_defense = $Container/DataArea/MarginContainer2/DefenseBg/DefenseContainer/LabelDefense
	progress_bar_hp = $Container/HpProgressBar
	color_bg = $Container/PlayerImg
	color_bg.modulate = m_color
	attr_update()
	
func attr_update(attr: String = ""):
	if not attr or attr == "hp":
		var hp_percent_value = float(current_hp) / max_hp * 100
		progress_bar_hp.set_value(hp_percent_value)
		
	if not attr or attr == "attack":
		var ui_text = str(attack) + str(temp_attack) if temp_attack > 0 else str(attack)
		FL.set_ui_text(label_attack, ui_text, false)
			
	if not attr or attr == "defense":
		var ui_text = str(defense) + str(temp_defense) if temp_defense > 0 else str(defense)
		FL.set_ui_text(label_defense, ui_text, false)
	
func _handle_move_operate():
	super._handle_move_operate()
	set_process_unhandled_input(true)

## 捕捉玩家的未处理输入（防止穿透 UI）
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		# 换算为 TileMap 坐标
		var mouse_pos = TurnManager.map_layer.get_local_mouse_position()
		var clicked_tile_pos = TurnManager.map_layer.local_to_map(mouse_pos)
		# 合法性判断
		if TurnManager.select_layer.get_cell_source_id(clicked_tile_pos) == 1:
			if TurnManager.select_layer.get_cell_atlas_coords(clicked_tile_pos) == Vector2i(0, 0):
				t_pos = clicked_tile_pos
				# 关闭输入监听
				set_process_unhandled_input(false)
				move_to()
				
			
