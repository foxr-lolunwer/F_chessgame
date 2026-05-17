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

static func set_ui_text(ui: Control, text_key: String,):
	if "set_text" in ui:
		ui.set_text(FLang.get_text(text_key))
	else:
		FLogger.error("UI:%s, type:%s has not \"set_text\" func"
			% [ui.get_name(), ui.get_class()])

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
		
static func set_ui_text_xslashx(ui: Control, a, b, rf: float = 0.1) -> void:
	if not ui.has_method("set_text"):
		FLogger.error("UI:%s, type:%s has not \"set_text\" func"
			% [ui.get_name(), ui.get_class()])
		return

	var value_a: String
	var value_b: String

	if a is float:
		value_a = str(snapped(a, -rf))
	else:
		value_a = str(a)

	if b is float:
		value_b = str(snapped(b, -rf))
	else:
		value_b = str(b)

	ui.set_text(
		FLang.get_text_format(
			"ui_core.xslashx",
			{
				"0": value_a,
				"1": value_b
			}
		)
	)
