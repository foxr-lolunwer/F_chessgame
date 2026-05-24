extends Node

func _ready() -> void:
	_load_sub_tscn()
	$Camera2D.setup()
	await get_tree().physics_frame
	TurnManager.start_game()

func _load_sub_tscn():
	TurnManager.node_map = $Map
	TurnManager.node_players = $Players
	TurnManager.node_ui_layer = $CanvasLayer
	TurnManager.node_map.setup()
	TurnManager.node_players.setup()
	

		
#
#func _capture_ui_init():
	#_update_capture_ui()
#
## --- 核心回合流程 ---
#
#func _start_turn():
	#if is_game_over:
		#return
		#
	## 检查胜利条件
	#if win_index > -1:
		#_handle_game_over()
		#return
#
	## 获取当前角色
	#current_active_char = _character_nodes[current_char_index]
	#
	## 如果角色已死亡，直接下一位（防止死循环逻辑在 _next_turn 处理）
	#if not current_active_char.get("is_alive"): 
		#_next_turn()
		#return
	#
	## 执行回合变量初始化
	#_clear_hints()
	#turn_confirm_skip = false
	#
	## 执行特定回合逻辑
	#match turn_type:
		#ConstData.GAME_TURN_TYPE.MOVE:
			#_start_move_turn()
		#ConstData.GAME_TURN_TYPE.FIGHT:
			#_start_fight_turn()
			#
	#_check_forbidden_trigger_status()

#func _start_move_turn():
	#waiting_for_input = true
	#_clear_hints()
	#
	#var origin: Vector2i = current_active_char.grid_position
	#var other_chars_pos: Array[Vector2i] = []
	#
	#for char_node in _character_nodes:
		#other_chars_pos.append(char_node.grid_position)
	#
	## 抽取移动类型
	#if not keep_move_type:
		#var key_list = ConstData.MOVE_OPERATION.keys()
		#current_move_type = ConstData.MOVE_OPERATION[key_list[weighted_random(move_type_roll)]]
	#else:
		#keep_move_type = false
		#
	#var m_move_range = current_active_char.move_range
	#var forbidden_list = forbidden_trigger_status.keys()
	#
	#match current_move_type:
		#ConstData.MOVE_OPERATION.CROSS, ConstData.MOVE_OPERATION.DOUBLE_CROSS, ConstData.MOVE_OPERATION.DIAGONAL:
			#if current_move_type == ConstData.MOVE_OPERATION.DOUBLE_CROSS:
				#m_move_range *= 2
				#
			#var dirs: Array 
			#if current_move_type == ConstData.MOVE_OPERATION.DIAGONAL:
				#dirs = [Vector2i(1, 1), Vector2i(1, -1), Vector2i(-1, 1), Vector2i(-1, -1)]
			#else:
				#dirs = [Vector2i(0, 1), Vector2i(0, -1), Vector2i(1, 0), Vector2i(-1, 0)]
				#
			#for dir in dirs:
				#for step in range(1, m_move_range + 1):
					#var p = origin + dir * step
					## 边界检查与阻挡检查
					#if not (p in used_cells) or not current_active_char._can_move_to(p):
						#break
					#
					#var cell_color = ConstData.ATLAS_COORDS.BLUE_MOVE
					#if p in forbidden_list:
						#cell_color = ConstData.ATLAS_COORDS.GRAY_FORBIDDEN
					#if p in other_chars_pos:
						#cell_color = ConstData.ATLAS_COORDS.RED_ATTACK
						#
					#_move_layer.set_cell(p, 2, cell_color)
					#
		#ConstData.MOVE_OPERATION.TELEPORT:
			#_handle_teleport_logic(origin, other_chars_pos)
#
#func _handle_teleport_logic(origin: Vector2i, other_chars_pos:Array[Vector2i]):
	#var reset_tp_position: bool = true
	#if current_active_char.tp_position_set:
		## 检查传送点上是否有本体或其他人，如果有，重新设置点位
		#if origin != current_active_char.tp_position and current_active_char.tp_position not in other_chars_pos:
			#var tp_pos = current_active_char.tp_position
			#if tp_pos != null and tp_pos in used_cells:
				#_move_layer.set_cell(tp_pos, 2, ConstData.ATLAS_COORDS.BLUE_MOVE)
			#_move_layer.set_cell(origin, 2, ConstData.ATLAS_COORDS.BLUE_MOVE)
			#current_active_char.tp_position_set = false
			#reset_tp_position = false
		#else:
			#print("传送点位已不可用，请重新设置")
			#reset_tp_position = true
	#if reset_tp_position:
		#var tp_range = current_active_char.tp_range
		##var tp_area = _map_layer.get_used_cells() # 简化：所有格子都在范围内？需确认逻辑
		## 这里原本逻辑似乎是全图遍历范围？保持原逻辑
		#for x in range(-tp_range, tp_range + 1):
			#for y in range(-tp_range, tp_range + 1):
				#var p = origin + Vector2i(x, y)
				#if p in used_cells and current_active_char._can_move_to(p):
					#_move_layer.set_cell(p, 2, ConstData.ATLAS_COORDS.PURPLE_TELEPORT)
#
#func _start_fight_turn():
	## 抽取战斗类型
	#if not keep_fight_type:
		#var key_list = FIGHT_OPERATION.keys()
		#current_fight_type = FIGHT_OPERATION[key_list[weighted_random(fight_type_roll)]]
	#else:
		#keep_fight_type = false
		#
	#var origin = current_active_char.grid_position
	#var damage_range = current_active_char.damage_range
	#
	#match current_fight_type:
		#FIGHT_OPERATION.HEALTH:
			#current_active_char.current_hp += current_active_char.health_val
			#print(current_active_char.cname, " 生命恢复")
			#_schedule_next_turn() # 异步切换
			#return
			#
		#FIGHT_OPERATION.NORMAL_SHOT, FIGHT_OPERATION.POWER_SHOT:
			#valid_attack_targets.clear()
			## 简单的范围检测
			#for target in _character_nodes:
				#if target == current_active_char or not target.is_alive:
					#continue
				#
				#var dist = abs(target.grid_position.x - origin.x) + abs(target.grid_position.y - origin.y)
				#if dist <= damage_range:
					#valid_attack_targets.append(target)
					#_ex_layer.set_cell(target.grid_position, 2, ATLAS_COORDS.RED_ATTACK)
			#
			#if valid_attack_targets.is_empty():
				#print(current_active_char.cname, " 没有目标可攻击，跳过")
				#_schedule_next_turn() # 关键：异步切换
			#else:
				#waiting_for_input = true
				#print("请选择攻击目标")
				#
		#FIGHT_OPERATION.X_RAY:
			#_handle_xray_attack(origin, damage_range)
			#_schedule_next_turn() # X射线即时释放不需要选目标
#
#func _handle_xray_attack(origin: Vector2i, base_range: int):
	#var dirs = [Vector2i(1, 1), Vector2i(1, -1), Vector2i(-1, 1), Vector2i(-1, -1)]
	#var xray_range = base_range * 3
	#
	#for dir in dirs:
		#for step in range(1, xray_range + 1):
			#var p = origin + dir * step
			#if not (p in used_cells) or not current_active_char._can_move_to(p):
				#break
			#
			## 检查路径上的敌人
			#for target in _character_nodes:
				#if target.grid_position == p and target.is_alive:
					#_apply_damage(current_active_char, target)
#
## --- 输入处理 (使用 _unhandled_input 替代 _process) ---
#func _unhandled_input(event):
	#if not waiting_for_input or is_game_over:
		#return
		#
	#if event.is_action_pressed("click"):
		#turn_confirm_skip = false
		#_handle_click_input()
	## 不间断点击两次右键跳过回合
	#if event.is_action_pressed("right_click"):
		#if turn_confirm_skip:
			#turn_confirm_skip = false
			#_next_turn()
		#else:
			#print("跳过回合？")
			#turn_confirm_skip = true
#func _handle_click_input():
	#var mouse_pos = get_viewport().get_mouse_position()
	#var grid_pos = _map_layer.local_to_map(mouse_pos)
	#
	#if turn_type == ConstData.GAME_TURN_TYPE.MOVE:
		#var cell_atlas = _move_layer.get_cell_atlas_coords(grid_pos)
		#
		## 传送设置点
		#if cell_atlas == ConstData.ATLAS_COORDS.PURPLE_TELEPORT:
			#_confirm_action()
			#current_active_char.tp_position_set = true
			#current_active_char.tp_position = grid_pos
			#_next_turn()
			#return
			#
		## 普通移动
		#if cell_atlas == ConstData.ATLAS_COORDS.BLUE_MOVE or cell_atlas == ConstData.ATLAS_COORDS.GRAY_FORBIDDEN:
			#_confirm_action()
			#current_active_char.move_to(grid_pos)
			## 使用 await 等待信号，比 connect/disconnect 更干净
			#await current_active_char.move_finished
			#_on_move_finished()
			#
	#elif turn_type == ConstData.GAME_TURN_TYPE.FIGHT:
		#var cell_atlas = _ex_layer.get_cell_atlas_coords(grid_pos)
		#
		#if cell_atlas == ConstData.ATLAS_COORDS.RED_ATTACK:
			#for target in valid_attack_targets:
				#if target.grid_position == grid_pos:
					#_confirm_action()
					#_apply_damage(current_active_char, target)
					#break
#
#func _confirm_action():
	#_clear_hints()
	#waiting_for_input = false
#
## --- 逻辑辅助 ---
#
#func _apply_damage(attacker: FCharacter, target: FCharacter):
	#var attack_val = attacker.attack + attacker.temp_attack_bonus
	#var defense_val = target.defense + target.temp_defense_bonus
	#var damage = max(attack_val - defense_val, 0)
	#
	#if current_fight_type in [FIGHT_OPERATION.POWER_SHOT, FIGHT_OPERATION.X_RAY]:
		#damage *= 2
		#
	#target.apply_damage(damage)
	#print(attacker.cname, " 攻击 ", target.cname, " 造成 ", damage, " 伤害")
	#
	#if target.current_hp <= 0:
		#target.is_alive = false
		#print(target.cname, " 被击败")
		#
	## 攻击后不立即跳过，等待一帧避免逻辑冲突（可选）
	#_schedule_next_turn()
#
#func _on_move_finished():
	#current_active_char.remove_tile_effect()
	#var p = current_active_char.grid_position
	#
	## 地块效果触发
	#if p in special_tiles["cannon"]:
		#current_active_char.temp_attack_bonus = current_active_char.attack
	#elif p in special_tiles["cover"]:
		#current_active_char.temp_defense_bonus = 1
	#elif p in special_tiles["heal"]:
		#current_active_char.current_hp += 1
	#elif p in special_tiles["capture"]:
		#capture_status[p]["index"] = current_char_index
		#capture_status[p]["cname"] = current_active_char.cname
		#_update_capture_ui()
		#
	#if p in special_tiles["speed"]:
		#if not (p in forbidden_trigger_status):
			#var c_meta = { "turn_type": GAME_TURN_TYPE.MOVE, "turn_count": move_turn_count + 3 }
			#forbidden_trigger_status[p] = c_meta
			#keep_move_type = true
			#switch_character_flag = false # 踩到速度格，不切换角色
			#
	#_next_turn()
#
## 使用 call_deferred 或 Timer 防止无限递归
#func _schedule_next_turn():
	## 等待一小段时间，既能防止栈溢出，也能让玩家看清发生了什么（比如“无目标”提示）
	#await get_tree().create_timer(0.3).timeout
	#_next_turn()
#
#func _next_turn():
	#if is_game_over: return
#
	## 1. 检查胜利条件
	#if turn_type == GAME_TURN_TYPE.MOVE:
		#_check_capture_win()
	#else:
		#_check_kill_win()
		#
	#if win_index > -1:
		#_start_turn() # 会触发 _handle_game_over
		#return
#
	#var original_index = current_char_index
#
	## 2. 切换角色逻辑
	#if switch_character_flag:
		## 寻找下一个存活角色
		#var found_alive = false
		#var loop_count = 0
		#var temp_index = current_char_index
		#
		## 最多遍历一圈
		#while loop_count < _character_nodes.size():
			#temp_index = (temp_index + 1) % _character_nodes.size()
			#if _character_nodes[temp_index].is_alive:
				#current_char_index = temp_index
				#found_alive = true
				#break
			#loop_count += 1
			#
		#if not found_alive:
			#print("所有角色死亡，异常结束")
			#return # 或处理平局逻辑
	#
	#switch_character_flag = true # 重置标志位
#
	## 3. 判断是否进入了新的一轮（索引回绕）
	## 注意：这里的逻辑需要根据你游戏的具体回合制规则调整
	## 简单判断：如果当前索引变小了（比如从 3 变成 0），说明一轮结束
	#if current_char_index < original_index:
		#_switch_phase()
	#
	## 4. 开始新回合
	#_start_turn()
#
#func _switch_phase():
	#if turn_type == GAME_TURN_TYPE.MOVE:
		#move_turn_count += 1
		#turn_type = GAME_TURN_TYPE.FIGHT
		#print("--- 进入战斗阶段 ---")
	#else:
		#fight_turn_count += 1
		#turn_type = GAME_TURN_TYPE.MOVE
		#print("--- 进入移动阶段 ---")
#
## --- 辅助功能 ---
#
#func _check_forbidden_trigger_status():
	#var to_remove = []
	#for p in forbidden_trigger_status:
		#var meta = forbidden_trigger_status[p]
		#var c_type = meta.get("turn_type", -1)
		#var target_count = meta.get("turn_count", 0)
		#var current_count = move_turn_count if c_type == GAME_TURN_TYPE.MOVE else fight_turn_count
		#
		#if c_type == -1: current_count = move_turn_count + fight_turn_count
		#
		#if current_count >= target_count:
			#to_remove.append(p)
			#
	#for p in to_remove:
		#forbidden_trigger_status.erase(p)
#
#func _clear_hints():
	#_move_layer.clear()
	#_ex_layer.clear()
#
#func _update_capture_ui():
	## 建议：不要每次都 queue_free 重建，性能较差。
	## 但为保持逻辑兼容，这里暂不修改核心UI逻辑。
	#for child in _ui_name_container.get_children(): child.queue_free()
	#for child in _ui_info_container.get_children(): child.queue_free()
#
	#for key in capture_status:
		#var meta = capture_status[key]
		#var l1 = Label.new()
		#l1.text = "%s 点：" % meta["pname"]
		#var l2 = Label.new()
		#l2.text = str(meta["cname"])
		#_ui_name_container.add_child(l1)
		#_ui_info_container.add_child(l2)
#
#func _check_capture_win():
	#if capture_status.is_empty(): return
	#var first_owner = -2 # -2 表示未初始化
	#
	#for key in capture_status:
		#var idx = capture_status[key]["index"]
		#if idx == -1: return # 还有未被占领的
		#if first_owner == -2:
			#first_owner = idx
		#elif first_owner != idx:
			#return # 存在不同持有者
			#
	#win_index = first_owner
#
#func _check_kill_win():
	#var alive_count = 0
	#var last_alive_index = -1
	#for i in range(_character_nodes.size()):
		#if _character_nodes[i].is_alive:
			#alive_count += 1
			#last_alive_index = i
	#
	#if alive_count == 1:
		#win_index = last_alive_index
#
#func _handle_game_over():
	#is_game_over = true
	#var winner_name = _character_nodes[win_index].cname if win_index < _character_nodes.size() else "Unknown"
	#print("游戏结束！获胜者: ", winner_name)
	## 这里可以弹出结算UI，或者 reload_current_scene
#
#func weighted_random(items: Array[Array]) -> int:
	#var total_weight = 0.0
	#for item in items:
		#total_weight += item[1]
	#
	#var rnd = randf() * total_weight
	#var current = 0.0
	#for item in items:
		#current += item[1]
		#if rnd < current:
			#return item[0]
	#return -1
