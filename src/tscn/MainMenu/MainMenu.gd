extends Control

func _ready() -> void:
	set_ui_loc()
	
func set_ui_loc():
	FL.set_ui_text(
		$MenuContainer/ButtonStart,
		"ui.menu.start"
	)
	FL.set_ui_text(
		$MenuContainer/ButtonExit,
		"ui.menu.exit"
	)

func _on_button_start_pressed() -> void:
	get_tree().change_scene_to_file("res://src/tscn/PrePlay/PrePlayMenu.tscn")


func _on_button_exit_pressed() -> void:
	get_tree().quit()
