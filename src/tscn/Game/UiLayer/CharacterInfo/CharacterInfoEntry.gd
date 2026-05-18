class_name CharacterUiProperties
extends VBoxContainer

# 引用 UI 组件
@onready var name_label: Label = $MarginContainer/VBoxContainer/LabelName
@onready var hp_label: Label = $MarginContainer/VBoxContainer/Line1/LabelHPVal
@onready var attack_label: Label = $MarginContainer/VBoxContainer/Line2/LabelAttackVal
@onready var defense_label: Label = $MarginContainer/VBoxContainer/Line3/LabelDEFVal

func setup(player: FCharacter):
	set_ui_loc()
	

func set_ui_loc():
	FL.set_ui_text(
		$MarginContainer/VBoxContainer/LabelName,
		""
	)

func update_properties(character: FCharacter):
	"""根据角色数据更新 UI 显示"""
	# 显示名称
	name_label.text = character.cname  # 对应角色的 cname 属性
	# 显示生命值（进度条 + 文本）
	hp_label.text = "%d / %d" % [character.current_hp, character.max_hp]
	# 显示攻击力
	attack_label.text = "%d" % character.attack if not character.temp_attack_bonus else "%d + %d" % [character.attack, character.temp_attack_bonus]
	# 显示防御力
	defense_label.text = "%d" % character.defense if not character.temp_defense_bonus else "%d + %d" % [character.defense, character.temp_defense_bonus]
