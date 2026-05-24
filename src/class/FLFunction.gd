extends Node
class_name FL

static func get_json_data(json: JSON, file_path: String):
	var file_access = FileAccess.open(file_path, FileAccess.READ)
	if file_access:
		var json_text = file_access.get_as_text()
		file_access.close()
		var err = json.parse(json_text)
		if err != OK:
			FLogger.error("JSON Parse Error: " + file_path)
			return null
		return json.data
	return null

static func remove_all_children(node: Node) -> void:
	for child in node.get_children():
		node.remove_child(child)
		child.queue_free()

static func deep_get(data: Variant, keys: Array, default: Variant):
	var current = data
	var path := []

	for key in keys:
		path.append(str(key))

		if current == null:
			FLogger.error(
				"deep_get null at: %s"
				% ".".join(path)
			)
			return default

		if current is Dictionary:
			if not current.has(key):
				FLogger.error(
					"deep_get missing key: %s"
					% ".".join(path)
				)
				return default

			current = current[key]

		elif current is Array:
			if key is not int:
				FLogger.error(
					"deep_get array key must int: %s"
					% ".".join(path)
				)
				return default

			if key < 0 or key >= current.size():
				FLogger.error(
					"deep_get array out of range: %s"
					% ".".join(path)
				)
				return default

			current = current[key]

		else:
			FLogger.error(
				"deep_get invalid type at: %s"
				% ".".join(path)
			)
			return default

	return current

static func set_ui_text(ui: Control, text_str: String, text_key: bool = true) -> void:
	if not _ui_has_func_set_text(ui):
		return
	if text_key:
		ui.set_text(FLang.get_text(text_str))
	else:
		ui.set_text(text_str)

static func set_selector_data(
	selector: OptionButton,
	keys: Array,
	loc_prefix: String = "",
	loc_func: Callable = Callable()
):
	if keys.is_empty():
		FLogger.error(
			"selector:%s keys is null"
			% selector.get_name()
		)
		return

	selector.clear()

	for key in keys:
		var text: String

		if loc_func.is_valid():
			text = loc_func.call(key)
		else:
			text = FLang.get_text("%s.%s" % [loc_prefix, key])

		var idx = selector.get_item_count()

		selector.add_item(text)
		selector.set_item_metadata(idx, key)

static func set_ui_text_with_param(ui: Control, text_str: String, params: Dictionary = {}) -> void:
	if not _ui_has_func_set_text(ui):
		return
	ui.set_text(FLang.get_text_format(text_str, params))

static func _ui_has_func_set_text(ui: Control) -> bool:
	if "set_text" in ui:
		return true
	else:
		FLogger.error("UI:%s, type:%s has not \"set_text\" func"
			% [ui.get_name(), ui.get_class()])
		return false

## 根据权重配置进行可调试的随机抽签
## @param roll_config 传入的权重数组（支持权重为0的项）[[项目, 权重], ...]
## @param rng 传入一个配置好种子的 RandomNumberGenerator 实例
## @return 返回选中的项目
static func roll_with_weight(roll_config: Array[Array], rng: RandomNumberGenerator) -> Variant:
	if roll_config.is_empty():
		FLogger.error("roll_config is empty.")
		return null
		
	# 1. 计算总权重
	var total_weight: int = 0
	for item in roll_config:
		total_weight += item[1]

	if total_weight <= 0:
		FLogger.error("total_weight<=0.")
		return null

	# 2. 使用传入的专属 rng 实例生成 0 到总权重之间的随机数
	# rng.randi_range(min, max) 包含两端，所以上限要 -1 才能精准匹配区间 [0, total_weight - 1]
	var random_value: int = rng.randi_range(0, total_weight - 1)
	
	# 3. 区间扫描判定
	var current_sum: int = 0
	for item in roll_config:
		current_sum += item[1]
		if random_value < current_sum:
			return item[0]

	return roll_config[0][0]
