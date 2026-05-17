extends Node

var json = JSON.new()
var map_data: Dictionary = {}

func _ready() -> void:
	_load_map_data()

func _load_map_data(dir_path: String = "res://asset/map/") -> void:
	var dir = DirAccess.open(dir_path)

	var sub_dirs: Array[String] = []
	dir.list_dir_begin()
	var item = dir.get_next()
	while item != "":
		if item != "." and item != ".." and dir.current_is_dir():
			sub_dirs.append(item)
		item = dir.get_next()
	dir.list_dir_end()

	for sub_dir in sub_dirs:
		var info_path = dir_path + sub_dir + "/info.json"
		var json_data = FL.get_json_data(json, info_path)
		if json_data is Dictionary:
			map_data[json_data.get("id")] = json_data.get("data")
