font = "Hiragino Kaku Gothic Pro"

# -------------Window--------------
window_style = {
    "auto_size_text": True,
    "auto_size_buttons": False,
    "default_element_size": (20, 1),
    "finalize": True,
    "grab_anywhere": True,
    "element_justification": "center",
    "text_justification": "center",
    "location": (200, 200),
}

# 外枠
column_left = {
    "size": (1280, 1080),
    "pad": 0,
}

column_right = {
    "size": (320, 1080),
    "pad": 0,
}

column_values = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "expand_x": True,
    "expand_y": True,
}

column_setup = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "expand_x": True,
    "expand_y": True,
}

column_save_item = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "expand_x": True,
    "expand_y": True,
}

column_save = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "expand_x": True,
    "expand_y": True,
}

column_reset = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "expand_x": True,
    "expand_y": True,
}

column_base_frame = {
    "size": (320, 300),
    "pad": ((0, 0), (10, 0)),
    "element_justification": "center",
    "expand_x": True,
    "expand_y": True,
    "font": (font, 10),
}

column_graph_l = {
    "size": (640, 480 * 2),
    "pad": 0,
    "element_justification": "center",
}

column_base = {
    "size": (640, 300),
    "pad": 0,
    "element_justification": "center",
}

# グラフ
fig_style_l = {"size": (640, 480), "pad": ((0, 0), (1, 0))}

# テキスト
values_text_title_style = {
    "pad": ((1, 1), (5, 0)),
    "font": (font, 10),
    "justification": "center",
    "size": (18, 1),
}
values_text_style = {
    "pad": ((1, 1), (0, 5)),
    "font": (font, 14),
    "justification": "center",
    "size": (14, 1),
}

# コネクト
port_selection_style = {
    "font": (font, 8),
    "size": (27, 2),
}
input_button_style_refresh = {
    "font": (font, 8),
    "size": (7, 1),
    "button_color": ("#ffffff", "#000000"),
    "disabled_button_color": ("#999999", "#cccccc"),
}

# ボタン類
input_button_style_l = {
    "pad": ((5, 5), (5, 10)),
    "size": (20, 2),
    "button_color": ("#ffffff", "#000000"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": (font, 11),
}

input_button_style_m = {
    "pad": ((10, 10), (7, 12)),
    "size": (28, 2),
    "button_color": ("#ffffff", "#000000"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": (font, 10),
}

input_button_style_s = {
    "pad": (5, 5),
    "size": (8, 1),
    "button_color": ("#ffffff", "#444444"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": (font, 10),
}

input_button_style_sl = {
    "pad": ((0, 0), (5, 10)),
    "size": (18, 1),
    "button_color": ("#ffffff", "#444444"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": (font, 10),
}

input_button_style_reset = {
    "pad": ((5, 5), (5, 10)),
    "size": (20, 2),
    "button_color": ("#ffffff", "#444444"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": (font, 10),
}
