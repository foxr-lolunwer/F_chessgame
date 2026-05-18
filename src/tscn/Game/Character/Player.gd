extends FCharacter

var label_attack: Label
var label_defense: Label
var progress_bar_hp: TextureProgressBar

func _ready():
	pass
	
func setup(pos: Vector2i, m_cname: String = "null"):
	super.setup(pos, m_cname)
	label_attack = $Container/DataArea/AttackBg/MarginContainer/AttackContainer/LabelAttack
	label_defense = $Container/DataArea/DefenseBg/MarginContainer/DefenseContainer/LabelDefense
	progress_bar_hp = $Container/HpProgressBar
	attr_update()
	
func attr_update(attr: String = ""):
	if not attr or attr == "hp":
		var hp_percent_value = float(current_hp) / max_hp * 100
		progress_bar_hp.set_value(hp_percent_value)
		
	if not attr or attr == "attack":
		var ui_text = str(attack) + str(temp_attack) if temp_attack > 0 else str(attack)
		FL.set_ui_text(label_attack, ui_text, false)
			
	if not attr or attr == "defense":
		var ui_text = str(defense) + str(temp_defense) if temp_defense > 0 else str(defense)
		FL.set_ui_text(label_defense, ui_text, false)
	
