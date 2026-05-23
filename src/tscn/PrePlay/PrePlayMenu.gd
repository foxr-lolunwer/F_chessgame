extends Control

var selected_map_id = "default"

func _ready() -> void:
	set_ui_loc()

func setup(set_map_id) -> void:
	update_select_map(set_map_id)

func set_ui_loc():
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer2/HBoxContainer/LabelAuthor,
		"ui.menu.author"
	)
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer/ButtonPlay,
		"ui.menu.play"
	)
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer/ButtonBack,
		"ui.menu.back"
	)
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer/HBoxContainer/ButtonPre,
		"ui.menu.pre_map"
	)
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer/HBoxContainer/ButtonNext,
		"ui.menu.next_map"
	)

func update_select_map(set_map_id):
	if not set_map_id.is_empty():
		selected_map_id = set_map_id
	else:
		FLogger.fatal("selected_map_id is null!")
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer/LabelNameMap,
		"map.%s.name" % selected_map_id
	)
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer2/LabelDesc,
		"map.%s.desc" % selected_map_id
	)
	FL.set_ui_text(
		$HBoxContainer/VBoxContainer2/HBoxContainer/LabelAuthorName,
		"map.%s.author" % selected_map_id
	)

func _on_button_play_pressed() -> void:
	TurnManager.set_select_map_id(selected_map_id)
	get_tree().change_scene_to_file("res://src/tscn/Game/Game.tscn")


func _on_button_back_pressed() -> void:
	get_tree().change_scene_to_file("res://src/tscn/MainMenu/MainMenu.tscn")
