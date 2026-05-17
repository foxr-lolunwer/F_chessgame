extends Node

enum LEVEL {
	OFF,
	DEBUG,
	INFO,
	WARN,
	ERROR,
	FATAL
}

var current_level: LEVEL = LEVEL.DEBUG

var log_dir := "user://logs/flogger/"
var latest_dir := log_dir + "latest/"
var log_file_path := latest_dir + "game_log.log"
var max_num := 5

var file: FileAccess
var timestamp_regex := RegEx.new()

func _ready():
	timestamp_regex.compile(
		r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$"
	)
	_prepare_dirs()
	_open_log_file()
	
func _prepare_dirs():
	var dir = DirAccess.open("user://")
	if not dir:
		push_error("Unable to access user://")
		return
	
	if not DirAccess.dir_exists_absolute(log_dir):
		DirAccess.make_dir_recursive_absolute(log_dir)
	
	if DirAccess.dir_exists_absolute(latest_dir):
		DirAccess.remove_absolute(latest_dir)  # 清空旧 latest
	
	DirAccess.make_dir_recursive_absolute(latest_dir)
	
func _open_log_file():
	file = FileAccess.open(log_file_path, FileAccess.WRITE)
	if file == null:
		push_error("Unable to create log file")
	
func push(log_level: LEVEL, message: String, game_time: String = "Unknown", control: Variant = null, with_stack: bool = false):
	if log_level < current_level:
		return
	if log_level == LEVEL.OFF:
		print("Use error log level OFF")
		log_level = LEVEL.DEBUG
	
	var time = Time.get_datetime_string_from_system()
	var level_str = _level_to_string(log_level)
	
	var ctrl_str = ""
	if control != null:
		ctrl_str = " [%s]" % str(control)
	
	var text = "[%s][%s][%s]%s %s" % [level_str, game_time, time, ctrl_str, message]
	
	# --- 堆栈 ---
	if with_stack or log_level >= LEVEL.ERROR:
		text += "\n" + _format_stack()
	
	# 输出
	match log_level:
		LEVEL.DEBUG, LEVEL.INFO:
			print(text)
		LEVEL.WARN:
			push_warning(text)
		LEVEL.ERROR, LEVEL.FATAL:
			push_error(text)
	
	if file:
		file.store_line(text)
	
func _format_stack() -> String:
	var stack = get_stack()
	var lines = []
	
	for i in range(stack.size()):
		var s = stack[i]
		lines.append("  at %s (%s:%d)" % [
			s.function,
			s.source,
			s.line
		])
	
	return "\n".join(lines)
	
func debug(message: String, game_time: String = "Unknown", control: Variant = null):
	push(LEVEL.DEBUG, message, game_time, control)

func info(message: String, game_time: String = "Unknown", control: Variant = null):
	push(LEVEL.INFO, message, game_time, control)

func warn(message: String, game_time: String = "Unknown", control: Variant = null):
	push(LEVEL.WARN, message, game_time, control)

func error(message: String, game_time: String = "Unknown", control: Variant = null):
	push(LEVEL.ERROR, message, game_time, control)

func fatal(message: String, game_time: String = "Unknown", control: Variant = null):
	push(LEVEL.FATAL, message, game_time, control)
	
func _level_to_string(l: LEVEL) -> String:
	match l:
		LEVEL.DEBUG: return "DEBUG"
		LEVEL.INFO: return "INFO"
		LEVEL.WARN: return "WARN"
		LEVEL.ERROR: return "ERROR"
		LEVEL.FATAL: return "FATAL"
		_: return "UNKNOWN"
		
func _exit_tree():
	_finalize_log()
	
func _finalize_log():
	if file:
		file.flush()
		file.close()

	var timestamp := Time.get_datetime_string_from_system().replace(":", "-")
	var archive_dir := log_dir.path_join(timestamp)

	DirAccess.make_dir_recursive_absolute(log_dir)

	# latest -> archive
	var err := DirAccess.rename_absolute(latest_dir, archive_dir)

	if err != OK:
		push_error("Log archiving failed")
		return

	_cleanup_old_logs()
	
func _cleanup_old_logs():
	var dir := DirAccess.open(log_dir)

	if not dir:
		push_error("Unable to open log dir: " + log_dir)
		return

	var log_dirs: Array[String] = []

	# 只获取目录
	for folder in dir.get_directories():
		# 跳过 latest
		if folder == "latest":
			continue

		# 校验时间戳格式
		if _is_log_timestamp(folder):
			log_dirs.append(folder)

	# 按字母排序
	# 时间戳格式下，字母序即时间序
	log_dirs.sort()

	# 删除最旧日志
	while log_dirs.size() > max_num:
		var oldest := log_dirs[0]
		var full_path := log_dir.path_join(oldest)

		_delete_dir_recursive(full_path)

		log_dirs.remove_at(0)

func _is_log_timestamp(text) -> bool:

	# 2026-05-04T14-33-21
	# 2026-05-04T22-28-20
	timestamp_regex.compile(
		r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$"
	)

	return timestamp_regex.search(text) != null

func _delete_dir_recursive(path: String):
	var dir := DirAccess.open(path)

	if not dir:
		return

	# 先删文件
	for file_name in dir.get_files():
		DirAccess.remove_absolute(
			path.path_join(file_name)
		)

	# 再删子目录
	for folder in dir.get_directories():
		_delete_dir_recursive(
			path.path_join(folder)
		)

	# 最后删自己
	DirAccess.remove_absolute(path)
