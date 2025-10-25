extends Node2D

# 在主控制器脚本（Node2D）中
var characters: Array[FCharacter]
var current_index := 0

func _ready():
	characters = [
		$FCharacter1,
		$FCharacter2
	]
	_set_active_character(0)

func _input(event):
	if event.is_action_pressed("switch_character"):
		current_index = (current_index + 1) % characters.size()
		_set_active_character(current_index)

func _set_active_character(index: int):
	for i in range(characters.size()):
		characters[i].is_player_controlled = (i == index)
