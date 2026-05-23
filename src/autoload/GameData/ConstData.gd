extends Node

# --- 常量定义 ---
# tile坐标
const ATLAS_COORDS = {
	"BLUE_MOVE": Vector2i(0, 0),
	"RED_ATTACK": Vector2i(1, 0),
	"GRAY_FORBIDDEN": Vector2i(2, 0),
	"PURPLE_TELEPORT": Vector2i(3, 0),
}
const MAP_LAYER_ID = {
	"COVER": Vector2i(1, 0),
	"HEAL": Vector2i(2, 0),
	"CANNON": Vector2i(3, 0),
	"SPEED": Vector2i(4, 0),
	"CAPTURE": Vector2i(5, 0) # 假设这是capture的特殊标识
}

enum MOVE_OPERATION { CROSS, DIAGONAL, DOUBLE_CROSS, TELEPORT }
enum FIGHT_OPERATION { NORMAL_SHOT, X_RAY, POWER_SHOT, BOMB, HEALTH }
enum GAME_PHASE { NONE, MOVE_STAGE, FIGHT_STAGE, TURN_END }
