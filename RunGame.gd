extends Node

func _ready() -> void:
	FLang.load_language("zh_CN")
	await get_tree().physics_frame
	get_tree().change_scene_to_file("res://src/tscn/MainMenu/MainMenu.tscn")
