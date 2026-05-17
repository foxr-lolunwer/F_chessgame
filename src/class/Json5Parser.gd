extends Node
class_name JSON5

var data: Variant

var source: String = ""
var cursor: int = 0
var length: int = 0
var error: Error = OK
var err_msg: String = ""

func json5_to_json(json5_text: String, indent: String = "") -> Error:
	var json_data = parse(json5_text)
	if error:
		data = ""
		return error
	data = JSON.stringify(json_data, indent)
	return OK

func parse(text: String) -> Variant:
	source = text
	cursor = 0
	length = text.length()
	error = OK
	err_msg = ""
	
	_skip_whitespace_and_comments()
	if cursor >= length:
		_set_error("Empty input")
		return null
		
	var result = _parse_value()
	if error: return null
	
	_skip_whitespace_and_comments()
	if cursor < length:
		_set_error("Extra characters after expression")
		return null
		
	return result

func _parse_value() -> Variant:
	_skip_whitespace_and_comments()
	if cursor >= length:
		_set_error("Unexpected end of input")
		return null
		
	var m_char = source[cursor]
	
	if m_char == '{':
		return _parse_object()
	if m_char == '[':
		return _parse_array()
	if m_char == '"' or m_char == "'":
		return _parse_string()
	
	return _parse_literal()

func _parse_object() -> Dictionary:
	var dict = {}
	cursor += 1 # 跳过 '{'
	
	var expect_comma = false
	
	while cursor < length:
		_skip_whitespace_and_comments()
		if cursor >= length: break
		
		if source[cursor] == '}':
			cursor += 1
			return dict
			
		if expect_comma:
			_set_error("Expected ',' or '}' in object")
			return {}
			
		var key = _parse_key()
		if error: return {}
		
		_skip_whitespace_and_comments()
		if cursor >= length or source[cursor] != ':':
			_set_error("Expected ':' after key")
			return {}
		cursor += 1 # 跳过 ':'
		
		var value = _parse_value()
		if error: return {}
		
		dict[key] = value
		
		_skip_whitespace_and_comments()
		if cursor < length and source[cursor] == ',':
			cursor += 1 # 跳过逗号
			# 允许尾随逗号，所以接下来可以直接是 '}'
			_skip_whitespace_and_comments()
			if cursor < length and source[cursor] == '}':
				cursor += 1
				return dict
		else:
			expect_comma = true # 下一轮循环必须是 '}'，否则报错
			
	_set_error("Unterminated object")
	return {}

func _parse_array() -> Array:
	var arr = []
	cursor += 1 # 跳过 '['
	
	var expect_comma = false
	
	while cursor < length:
		_skip_whitespace_and_comments()
		if cursor >= length: break
		
		if source[cursor] == ']':
			cursor += 1
			return arr
			
		if expect_comma:
			_set_error("Expected ',' or ']' in array")
			return []
			
		var value = _parse_value()
		if error: return []
		arr.append(value)
		
		_skip_whitespace_and_comments()
		if cursor < length and source[cursor] == ',':
			cursor += 1 # 跳过逗号
			_skip_whitespace_and_comments()
			if cursor < length and source[cursor] == ']':
				cursor += 1
				return arr
		else:
			expect_comma = true
			
	_set_error("Unterminated array")
	return []

func _parse_key() -> String:
	_skip_whitespace_and_comments()
	if cursor >= length: return ""
	
	var m_char = source[cursor]
	if m_char == '"' or m_char == "'":
		return _parse_string()
		
	var start = cursor
	while cursor < length:
		var c = source[cursor]
		if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9') or c == '_' or c == '$':
			cursor += 1
		else:
			break
			
	if start == cursor:
		_set_error("Expected identifier key")
		return ""
	return source.substr(start, cursor - start)

func _parse_string() -> String:
	var quote = source[cursor]
	cursor += 1
	var result = ""
	
	while cursor < length:
		var m_char = source[cursor]
		if m_char == quote:
			cursor += 1
			return result
		elif m_char == '\\':
			cursor += 1
			if cursor >= length: break
			var escaped = source[cursor]
			match escaped:
				'n': result += "\n"
				'r': result += "\r"
				't': result += "\t"
				'b': result += "\b"
				'f': result += "\f"
				'v': result += "\v"
				'0': result += ""
				#'0': result += "\u0000" # unsupport, skip
				'\n': pass
				'\r':
					if cursor + 1 < length and source[cursor+1] == '\n':
						cursor += 1
				_: result += escaped
			cursor += 1
		else:
			if m_char == '\n' or m_char == '\r':
				_set_error("Unescaped line break in string literal")
				return ""
			result += m_char
			cursor += 1
			
	_set_error("Unterminated string")
	return ""

func _parse_literal() -> Variant:
	var start = cursor
	while cursor < length:
		var c = source[cursor]
		if c == ',' or c == '}' or c == ']' or c == ':' or c == '/' or _is_whitespace(c):
			break
		cursor += 1
		
	var token = source.substr(start, cursor - start)
	if token == "":
		_set_error("Unexpected empty token")
		return null
	
	if token == "true": return true
	if token == "false": return false
	if token == "null": return null
	if token == "Infinity" or token == "+Infinity": return INF
	if token == "-Infinity": return -INF
	if token == "NaN" or token == "+NaN" or token == "-NaN": return NAN
	
	# 十六进制
	if token.to_lower().begins_with("0x") or token.to_lower().begins_with("+0x") or token.to_lower().begins_with("-0x"):
		var is_negative = token.begins_with("-")
		var hex_part = token.substr(token.find("0x") + 2)
		if hex_part == "" or not _is_valid_hex(hex_part):
			_set_error("Invalid hex number: " + token)
			return null
		return -hex_part.hex_to_int() if is_negative else hex_part.hex_to_int()
		
	# 普通数字
	if token.is_valid_float():
		# 排除类似 123foo 的混合错误
		if "." in token or "e" in token.to_lower():
			return token.to_float()
		else:
			return token.to_int()
			
	_set_error("Unexpected token: " + token)
	return null

func _is_valid_hex(hex_str: String) -> bool:
	for i in range(hex_str.length()):
		var c = hex_str[i].to_lower()
		if not ((c >= '0' and c <= '9') or (c >= 'a' and c <= 'f')):
			return false
	return true

func _skip_whitespace_and_comments():
	while cursor < length:
		var m_char = source[cursor]
		if _is_whitespace(m_char):
			cursor += 1
			continue
		if m_char == '/' and cursor + 1 < length:
			var next_char = source[cursor + 1]
			if next_char == '/':
				cursor += 2
				while cursor < length and source[cursor] != '\n' and source[cursor] != '\r':
					cursor += 1
				continue
			elif next_char == '*':
				cursor += 2
				var found_end = false
				while cursor < length:
					if source[cursor] == '*' and cursor + 1 < length and source[cursor + 1] == '/':
						cursor += 2
						found_end = true
						break
					cursor += 1
				if not found_end:
					_set_error("Unterminated multi-line comment")
				continue
		break

func _is_whitespace(m_char: String) -> bool:
	return m_char == ' ' or m_char == '\t' or m_char == '\n' or m_char == '\r' or m_char == '\v' or m_char == '\f' or m_char == '\u00A0'

func _set_error(msg: String, err_type: Error = FAILED):
	error = err_type
	err_msg = msg
