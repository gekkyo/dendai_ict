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
    "pad": ((0, 0), (0, 0)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
}

column_right = {
    "size": (320, 1080),
    "pad": ((0, 0), (0, 0)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
}

# グラフ
fig_style_l = {"size": (640, 480), "pad": ((0, 0), (1, 0))}
fig_style_m = {"size": (640, 300), "pad": (0, 0)}
fig_style_s = {"size": (640, 240), "pad": (0, 0)}
fig_style_ss = {"size": (640, 180), "pad": (0, 0)}

column_graph_l = {
    "size": (640, 480 * 2),
    "pad": (0, 0),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

column_graph_m = {
    "size": (640, 300),
    "pad": (0, 0),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

column_graph_s = {
    "size": (640, 240),
    "pad": (0, 0),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

column_graph_ss = {
    "size": (640, 180),
    "pad": (0, 0),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

# セットアップ
port_selection_style = {
    "font": ("Hiragino Kaku Gothic Pro", 8),
    "size": (27, 2),
}
input_button_style_refresh = {
    "font": ("Hiragino Kaku Gothic Pro", 8),
    "size": (7, 1),
    "button_color": ("#ffffff", "#000000"),
    "disabled_button_color": ("#999999", "#cccccc"),
}

column_base = {
    "size": (640, 300),
    "pad": (0, 0),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

column_base_frame = {
    "size": (320, 300),
    "pad": ((0, 0), (10, 0)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center",
    "expand_x": True,
    "expand_y": True,
    "font": ("Hiragino Kaku Gothic Pro", 10),
}

column_values = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
    "expand_x": True,
    "expand_y": True,
}

values_text_title_style = {
    "pad": ((1, 1), (5, 0)),
    "font": ("Hiragino Kaku Gothic Pro", 10),
    "justification": "center",
    "size": (18, 1),
}
values_text_style = {
    "pad": ((1, 1), (0, 5)),
    "font": ("Hiragino Kaku Gothic Pro", 14),
    "justification": "center",
    "size": (14, 1),
}

column_setup = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
    "expand_x": True,
    "expand_y": True,
}

column_save_item = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
    "expand_x": True,
    "expand_y": True,
}

column_save = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
    "expand_x": True,
    "expand_y": True,
}

column_reset = {
    "pad": ((10, 10), (0, 10)),
    "element_justification": "center",
    "vertical_alignment": "center",
    # "justification":"center"
    "expand_x": True,
    "expand_y": True,
}

column_setup_layout = {
    "size": (320, 100),
    "pad": ((0, 0), (0, 0)),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

text_style = {
    "font": (None, 12),
    "justification": "center",
    "vertical_alignment": "center",
}

column_button = {
    "size": (300, 50),
    "pad": ((0, 0), (40, 0)),
    "element_justification": "center",
    "vertical_alignment": "center",
    "justification": "center",
}

horizontal_line = {"pad": (0, 20), "color": "white"}

input_button_style_l = {
    "pad": ((5, 5), (5, 10)),
    "size": (20, 2),
    "button_color": ("#ffffff", "#000000"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": ("Hiragino Kaku Gothic Pro", 11),
}

input_button_style_reset = {
    "pad": ((5, 5), (5, 10)),
    "size": (20, 2),
    "button_color": ("#ffffff", "#444444"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": ("Hiragino Kaku Gothic Pro", 10),
}

input_button_style_m = {
    "pad": ((10, 10), (7, 12)),
    "size": (28, 2),
    "button_color": ("#ffffff", "#000000"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": ("Hiragino Kaku Gothic Pro", 10),
}

input_button_style_s = {
    "pad": (5, 5),
    "size": (8, 1),
    "button_color": ("#ffffff", "#444444"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": ("Hiragino Kaku Gothic Pro", 10),
}

input_button_style_sl = {
    "pad": ((0, 0), (5, 10)),
    "size": (18, 1),
    "button_color": ("#ffffff", "#444444"),
    "disabled_button_color": ("#999999", "#cccccc"),
    "font": ("Hiragino Kaku Gothic Pro", 10),
}
