extends Node

var Json5Parser: JSON5 = JSON5.new()
var json: JSON = JSON.new()

func parse_path_to_dict(path: String, transform: Callable = Callable(), merge_max_depth: int = 30, sub: bool = true) -> Dictionary:
	var list = parse_path_to_json_str(path, sub)
	var result := {}
	
	for text in list:
		var data = parse_file_to_dict_from_text(text, path)
		if data is Dictionary:
			if transform.is_valid():
				data = transform.call(data)
			_deep_merge_into(result, data, merge_max_depth)  # 后加载覆盖前面
	
	return result

func parse_path_to_json_str(path: String, sub: bool = true) -> Array:
	var result := []
	
	var dir = DirAccess.open(path)
	if dir == null:
		FLogger.warn("file path not find: %s" % path)
		return result
	
	# --- 先处理文件（按字母序）---
	var files = dir.get_files()
	for file_name in files:
		var full = path.path_join(file_name)
		
		var text = parse_file_to_json_str(full)
		if text != "":
			result.append(text)
	
	# --- 再处理子目录（按字母序递归）---
	if sub:
		var dirs = dir.get_directories()
		for sub_dir in dirs:
			var full = path.path_join(sub_dir)
			result.append_array(parse_path_to_json_str(full))
	
	return result
	
func parse_file_to_dict(path: String) -> Variant:
	var text = parse_file_to_json_str(path)
	if text == "":
		return {}
	
	return parse_file_to_dict_from_text(text, path)
	
func parse_file_to_dict_from_text(text: String, path: String) -> Variant:
	var err = json.parse(text)
	
	if err != OK:
		FLogger.error("fail to parse: %s (%s)\n%s" % [path, json.get_error_message(), text])
		return {}
	
	return json.data

func parse_file_to_json_str(path: String) -> String:
	var lower = path.to_lower()
	
	if not (lower.ends_with(".json") or lower.ends_with(".json5")):
		return ""
	
	var file = FileAccess.open(path, FileAccess.READ)
	if file == null:
		FLogger.error("fail to open file: " + path)
		return ""
	
	var text: String = file.get_as_text()
	if text == "":
		return ""
	
	if lower.ends_with(".json5"):
		var err = Json5Parser.json5_to_json(text)
		if err != OK:
			FLogger.error("JSON5 Parse Error: " + Json5Parser.err_msg)
			return ""
		text = Json5Parser.data
	return text

func resolve_inherit(data: Dictionary, inherit_depth: int = 0) -> Dictionary:
	var order = _topo_sort(data)
	
	var result := {}
	
	for id in order:
		var node = data[id]
		
		if node.has("inherit"):
			var parent_id = node["inherit"]
			
			if not result.has(parent_id):
				FLogger.error("inherit parent node not find: %s <- %s" % [id, parent_id])
				continue
			
			var merged = result[parent_id].duplicate(true)
			
			var self_data = node.duplicate(true)
			self_data.erase("inherit")

			_deep_merge_into(merged, self_data, inherit_depth)
			result[id] = merged
		else:
			result[id] = node.duplicate(true)
	
	return result

func _topo_sort(data: Dictionary) -> Array:
	var visited := {}
	var visiting := {}
	var result := []
	
	for id in data.keys():
		_dfs(id, data, visited, visiting, result)
	
	return result

func _dfs(id: String, data: Dictionary, visited: Dictionary, visiting: Dictionary, result: Array) -> void:
	if visited.has(id):
		return
	
	if visiting.has(id):
		FLogger.error("circular inheritance detected: " + id)
		return
	
	visiting[id] = true
	
	var node = data[id]
	if node.has("inherit"):
		var parent_id = node["inherit"]
		
		if not data.has(parent_id):
			FLogger.error("inherit target does not exist: %s -> %s" % [id, parent_id])
		else:
			_dfs(parent_id, data, visited, visiting, result)
	
	visiting.erase(id)
	visited[id] = true
	result.append(id)
	
# 按最大深度进行深合并
func _deep_merge_into(dst: Dictionary, src: Dictionary, max_depth: int, depth: int = 0) -> void:
	if depth > max_depth:
		return
	
	for k in src.keys():
		if depth == max_depth:
			dst[k] = src[k]
			continue
		if dst.has(k) and dst[k] is Dictionary and src[k] is Dictionary:
			_deep_merge_into(dst[k], src[k], max_depth, depth + 1)
		else:
			dst[k] = src[k]
