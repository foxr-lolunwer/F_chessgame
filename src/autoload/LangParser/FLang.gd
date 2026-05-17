extends Node

## 全局本地化缓存（简化为 key -> value 的直接映射）
var _loc_cache: Dictionary = {}

var current_lang: String = ""

## 外部调用：初始化加载
func load_language(lang_code: String) -> void:
	if current_lang == lang_code:
		return
	var root = "res://loc/%s/" % lang_code
	_loc_cache.clear()
	# 读取所有文件
	var loc_dict = JsonxDataParser.parse_path_to_dict(root, Callable(self, "_flatten_loc_data"))
	if len(loc_dict) == 0:
		FLogger.error("No data for this language | Lang Code: " + lang_code)
		return
	# 解析引用
	var load_order = _resolve_all(loc_dict)
	if load_order:
		loc_dict = _resolve_in_order(load_order, loc_dict)
	# 编译到内存结构
	_compile_to_cache(loc_dict)
	current_lang = lang_code
	FLogger.info("LangParser: Language: %s, Number of loaded entries: %d" % [lang_code, _loc_cache.size()])

# 递归扁平化字典：将所有嵌套结构扁平化为单层 key->value
func _flatten_loc_data(raw: Dictionary) -> Dictionary:
	var result = {}
	for top_key in raw:
		var top_value = raw[top_key]
		
		if top_value is Dictionary:
			# 递归扁平化内部内容，使用 top_key 作为前缀
			var sub_flattened = _recursive_flatten(top_key, top_value)
			result.merge(sub_flattened)
		else:
			result[top_key] = top_value
	return result

# 内部递归辅助函数
func _recursive_flatten(prefix: String, current_dict: Dictionary) -> Dictionary:
	var flat_map = {}
	for key in current_dict:
		var value = current_dict[key]
		# 构造新的键名：prefix.key
		var new_key = prefix + "." + str(key)
		
		if value is Dictionary:
			# 如果值还是字典，继续向深层递归
			var deep_flat = _recursive_flatten(new_key, value)
			flat_map.merge(deep_flat)
		else:
			# 到达叶子节点，存入最终键值对
			flat_map[new_key] = value
	return flat_map

func _merge_raw_data(list: Array) -> Dictionary:
	var merged: Dictionary = {}

	for data in list:
		for key in data:
			if merged.has(key):
				print("[I18n] Overwrite: %s" % key)
			merged[key] = data[key]

	return merged

# 解析引用-开始
func _resolve_all(merged_data: Dictionary) -> Array:
	var deps := {}
	
	for key in merged_data:
		var value = merged_data[key]
		if value is String:
			_collect_deps_recursive(value, key, deps)
	if not deps:
		return []
	var active_deps = _collect_active_nodes(deps)
	
	var order = _topo_sort(active_deps)
	if order.is_empty():
		var cyclic_nodes = _find_cyclic_nodes(deps)
		FLogger.error("CIRCULAR REFERENCE DETECTED IN: ", ", ".join(cyclic_nodes))
		return []
		
	return order

func _find_cyclic_nodes(deps: Dictionary) -> Array:
	var cyclic_nodes = []
	var visited = {}
	var recursion_stack = {}
	
	for node in deps.keys():
		if _has_cycle(node, deps, visited, recursion_stack):
			cyclic_nodes.append(node)
	
	return cyclic_nodes

func _has_cycle(node, deps, visited, recursion_stack) -> bool:
	if visited.get(node, false):
		return false
	
	if recursion_stack.get(node, false):
		return true
	
	recursion_stack[node] = true
	
	if deps.has(node):
		for neighbor in deps[node]:
			if _has_cycle(neighbor, deps, visited, recursion_stack):
				return true
	
	recursion_stack[node] = false
	visited[node] = true
	return false

# 解析引用-辅助方法
func _collect_deps_recursive(value: String, current_key: String, deps: Dictionary) -> void:
	var stripped = _strip_brackets(value)
	var refs = _extract_refs(stripped)
	
	if refs.is_empty():
		return
	
	var base_prefix = current_key.rsplit(".", true, 1)[0]
	var dep_list := []
	
	for ref in refs:
		var resolved = ref
		
		if ref.begins_with("."):
			resolved = base_prefix + ref
		
		elif not ref.contains("."):
			continue
		
		dep_list.append(resolved)
	
	if dep_list.size() > 0:
		deps[current_key] = dep_list

func _collect_active_nodes(deps: Dictionary) -> Dictionary:
	var active := {}
	var stack := []
	
	# 起点：有依赖的节点（即包含引用的键）
	for k in deps:
		if deps[k].size() > 0:
			active[k] = true
			stack.append(k)
	
	# 向下扩展：把它们依赖的节点也纳入（闭包）
	while stack.size() > 0:
		var cur = stack.pop_back()
		
		for d in deps.get(cur, []):
			if not active.has(d) and deps.has(d):
				active[d] = true
				stack.append(d)
	
	# 生成子图
	var sub := {}
	for k in active:
		var list := []
		for d in deps.get(k, []):
			if active.has(d):
				list.append(d)
		sub[k] = list
	
	return sub

func _extract_refs(text: String) -> Array:
	var result := []
	var i = 0
	
	while i < text.length():
		if text[i] == "{":
			var j = i + 1
			while j < text.length() and text[j] != "}":
				j += 1
			
			if j < text.length():
				var inner = text.substr(i + 1, j - i - 1)
				
				# 排除 {$...}
				if not inner.begins_with("$"):
					result.append(inner)
				
				i = j
		i += 1
	
	return result

func _strip_brackets(text: String) -> String:
	var result := ""
	var depth := 0
	
	for i in text.length():
		var c = text[i]
		
		if c == "[":
			depth += 1
			continue
		
		if c == "]":
			if depth > 0:
				depth -= 1
			continue
		
		if depth == 0:
			result += c
	
	return result

func _topo_sort(deps: Dictionary) -> Array:
	var indegree := {}
	var graph := {}
	
	for k in deps.keys():
		indegree[k] = 0
		graph[k] = []
	
	for k in deps:
		for d in deps[k]:
			if not deps.has(d):
				continue
			
			graph[d].append(k)
			indegree[k] += 1
	
	var queue := []
	for k in indegree:
		if indegree[k] == 0:
			queue.append(k)
	
	var result := []
	
	while queue.size() > 0:
		var cur = queue.pop_front()
		result.append(cur)
		
		for nxt in graph[cur]:
			indegree[nxt] -= 1
			if indegree[nxt] == 0:
				queue.append(nxt)
	
	if result.size() != deps.size():
		return []  # 环
	
	return result

# 解析引用-应用解析
func _resolve_in_order(order: Array, data: Dictionary) -> Dictionary:
	var result_data = data.duplicate(true)
	
	for full_key in order:
		var raw = result_data.get(full_key)
		if not raw is String:
			continue
		
		var resolved = _resolve_one_layer(raw, full_key, result_data)
		result_data[full_key] = resolved
		
	return result_data

func _resolve_one_layer(text: String, current_key: String, data: Dictionary) -> String:
	var stripped = _strip_brackets(text)
	var refs = _extract_refs(stripped)
	
	if refs.is_empty():
		return text
	
	var base_prefix = current_key.rsplit(".", true, 1)[0]
	var result = text
	
	for ref in refs:
		var replacement = _parse_ref(ref, base_prefix, data)
		result = result.replace("{" + ref + "}", replacement)
	
	return result

func _parse_ref(ref: String, base_prefix: String, data: Dictionary) -> String:
	var path = ref
	var args := {}
	
	# 拆参数
	var p = ref.find("(")
	if p != -1 and ref.ends_with(")"):
		path = ref.substr(0, p)
		var arg_str = ref.substr(p + 1, ref.length() - p - 2)
		args = _parse_args(arg_str)
	
	# 相对路径
	if path.begins_with("."):
		path = base_prefix + path
	
	var value = data.get(path)
	if not value is String:
		return ""
	
	# 参数替换 {$x}
	for k in args:
		value = value.replace("{$%s}" % k, str(args[k]))
	
	return value

func _parse_args(s: String) -> Dictionary:
	var d := {}
	if s.strip_edges() == "":
		return d
	
	for part in s.split(","):
		var kv = part.split("=")
		if kv.size() != 2:
			continue
		
		var k = kv[0].strip_edges()
		var v = kv[1].strip_edges()
		
		if (v.begins_with("'") and v.ends_with("'")) or (v.begins_with("\"") and v.ends_with("\"")):
			v = v.substr(1, v.length() - 2)
		
		d[k] = v
	
	return d

# 转换为易索引格式（简化版）
func _compile_to_cache(raw: Dictionary) -> void:
	for key in raw:
		_loc_cache[key] = str(raw[key])

# 获取文本（简化版）
func get_text(key: String) -> String:
	if _loc_cache.has(key):
		return _loc_cache[key]
	
	FLogger.warn("get_text: not find loc key: %s" % key)
	return key

# 获取格式化文本（简化版）
func get_text_format(key: String, params: Dictionary) -> String:
	var text = get_text(key)
	
	if text == key:
		return key
	
	var regex = RegEx.new()
	regex.compile(r"\{\$(\w+)\}")
	
	var matches = regex.search_all(text)
	
	for match in matches:
		var param_name = match.get_string(1)
		
		if params.has(param_name):
			text = text.replace(
				match.get_string(0),
				str(params[param_name])
			)
		else:
			FLogger.warn(
				"get_text_format: missing param \"%s\" in key \"%s\""
				% [param_name, key]
			)
	
	return text
