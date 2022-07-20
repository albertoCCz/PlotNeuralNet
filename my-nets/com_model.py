import sys
sys.path.append("../")
from pycore.tikzeng import *
from pycore.blocks import alt_colors_block

# generate nodes
n_blocks = 5
nodes_plus = gen_nodes(4, zoffset=28)
nodes_spec = gen_nodes(n_blocks, xspace=[0,4,5.5,2,3], zoffset=13)
nodes_liti = gen_nodes(n_blocks, xspace=[0,4,5.5,2,3], zoffset=0)
nodes_mixg = gen_nodes(1, zoffset=13)

# right align nodes
width_plus = float(list(nodes_plus.values())[-1].split(",")[0].lstrip('("')) + 2 * 4
width_spec = float(list(nodes_spec.values())[-1].split(",")[0].lstrip('("')) + 2 * 4
width_liti = float(list(nodes_liti.values())[-1].split(",")[0].lstrip('("')) + 2 * 4
widths = [width_plus, width_spec, width_liti]

xoffset_plus = min(widths) - width_plus
xoffset_spec = min(widths) - width_spec
xoffset_liti = min(widths) - width_liti

nodes_plus = apply_offset(xoffset_plus, 'x', nodes_plus)
nodes_spec = apply_offset(xoffset_spec, 'x', nodes_spec)
nodes_liti = apply_offset(xoffset_liti, 'x', nodes_liti)
nodes_mixg = apply_offset(float(list(nodes_spec.values())[-1].replace('+\skipshift','').strip('()').split(',')[0]) + 4, 'x', nodes_mixg)

# print(f"plus: {nodes_plus}")
# print(f"spec: {nodes_spec}")
# print(f"liti: {nodes_liti}")
# print(f"mixg: {nodes_mixg}")

# define the input images
input_offset = -2.5
width  = 7
height = 3.5
inputs = [
    insert_canvas_image("images/lifetime_mirror.jpg",              list(apply_offset(input_offset, 'x', get_node(nodes_liti, 0)).values())[0], width=width, height=height),
    insert_canvas_image("images/fluorescence_spectrum_mirror.jpg", list(apply_offset(input_offset, 'x', get_node(nodes_spec, 0)).values())[0], width=width, height=height),
    insert_canvas_image("images/plus_features_mirror.jpg",         list(apply_offset(input_offset, 'x', get_node(nodes_plus, 0)).values())[0], width=width, height=height),
]

# define each submodel architecture
liti = [
    # conv1
    to_Conv("conv1d_10", caption="Conv stack 1", s_filter=5, n_filter=8, size="", to=nodes_liti["a"], width=6, height=2, depth=24, color="conv_color"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_10", size="", to="(conv1d_10-east)",     depth=24, caption=""),
            to_Dense(name="relu_10",       size="", to="(batch_norm_10-east)", depth=24, caption=""),
            to_Dense(name="dropout_10",    size=24, to="(relu_10-east)",       depth=24, caption=""),
        ]
    ),
    to_Pool(name="maxpool_10", s_pool=4, size=6, to="(dropout_10-east)", width=2, height=2, depth=6, color="color_pool"),

    to_connection_node("maxpool_10", nodes_liti["b"]),

    # conv2
    to_Conv("conv1d_11", caption="Conv stack 2", s_filter=10, n_filter=16, size="", to=nodes_liti["b"], width=12, height=2, depth=6, color="conv_color"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_11", size="", to="(conv1d_11-east)",     depth=6, caption=""),
            to_Dense(name="relu_11",       size=16, to="(batch_norm_11-east)", depth=6, caption=""),
            to_Dense(name="dropout_11",    size="", to="(relu_11-east)",       depth=6, caption=""),
        ]
    ),
    to_Pool(name="maxpool_11", s_pool=4, size=1, to="(dropout_11-east)", width=2, height=2, depth=2, color="color_pool"),

    to_connection_node("maxpool_11", nodes_liti["c"]),

    # flatten
    to_Dense("flatten_12", size=16, to=nodes_liti["c"], depth=16, color="flatten", caption="Flatten 1"),

    to_connection_node("flatten_12", nodes_liti["d"]),

    # dense1
    to_Dense(name="dense_13", size="", to=nodes_liti["d"], depth=32, caption="", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_13", size="", to="(dense_13-east)",        depth=32, caption="Dense stack 1"),
            to_Dense(name="relu_13",       size="", to="(batch_norm_13-east)", depth=32, caption=""),
            to_Dense(name="dropout_13",    size=32, to="(relu_13-east)",       depth=32, caption=""),
        ]
    ),

    to_connection_node("dropout_13", nodes_liti["e"]),

    # dense2
    to_Dense(name="dense_14", size="", to=nodes_liti["e"], depth=8, caption="Dense stack 2", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_14", size="", to="(dense_14-east)",      depth=8, caption=""),
            to_Dense(name="relu_14",       size="", to="(batch_norm_14-east)", depth=8, caption=""),
            to_Dense(name="dropout_14",    size=8, to="(relu_14-east)",       depth=8, caption=""),
        ]
    ),
]

spec = [
    # conv1
    to_Conv("conv1d_5", caption="Conv stack 3", s_filter=5, n_filter=8, size="", to=nodes_spec["a"], width=6, height=2, depth=32, color="conv_color"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_5", size="", to="(conv1d_5-east)",     depth=32, caption=""),
            to_Dense(name="relu_5",       size="", to="(batch_norm_5-east)", depth=32, caption=""),
            to_Dense(name="dropout_5",    size=32, to="(relu_5-east)",       depth=32, caption=""),
        ]
    ),
    to_Pool(name="maxpool_5", s_pool=2, size=16, to="(dropout_5-east)", width=2, height=2, depth=16, color="color_pool"),

    to_connection_node("maxpool_5", nodes_spec["b"]),

    # conv2
    to_Conv("conv1d_6", caption="Conv stack 4", s_filter=10, n_filter=16, size="", to=nodes_spec["b"], width=12, height=2, depth=16, color="conv_color"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_6", size="", to="(conv1d_6-east)",     depth=16, caption=""),
            to_Dense(name="relu_6",       size="", to="(batch_norm_6-east)", depth=16, caption=""),
            to_Dense(name="dropout_6",    size=16, to="(relu_6-east)",       depth=16, caption=""),
        ]
    ),
    to_Pool(name="maxpool_6", s_pool=2, size=8, to="(dropout_6-east)", width=2, height=2, depth=8, color="color_pool"),

    to_connection_node("maxpool_6", nodes_spec["c"]),

    # flatten
    to_Dense("flatten_7", size=128, to=nodes_spec["c"], depth=48, color="flatten", caption="Flatten 2"),

    to_connection_node("flatten_7", nodes_spec["d"]),

    # dense1
    to_Dense(name="dense_8", size="", to=nodes_spec["d"], depth=32, caption="", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_8", size="", to="(dense_8-east)",        depth=32, caption="Dense stack 3"),
            to_Dense(name="relu_8",       size="", to="(batch_norm_8-east)", depth=32, caption=""),
            to_Dense(name="dropout_8",    size=32, to="(relu_8-east)",       depth=32, caption=""),
        ]
    ),

    to_connection_node("dropout_8", nodes_spec["e"]),

    # dense2
    to_Dense(name="dense_9", size="", to=nodes_spec["e"], depth=8, caption="Dense stack 4", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_9", size="", to="(dense_9-east)",      depth=8, caption=""),
            to_Dense(name="relu_9",       size="", to="(batch_norm_9-east)", depth=8, caption=""),
            to_Dense(name="dropout_9",    size=8, to="(relu_9-east)",       depth=8, caption=""),
        ]
    ),
]

plus = [
    to_Dense(name="dense_1", size="", to=nodes_plus["a"],  depth=34, caption="", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_1", size="", to="(dense_1-east)",      depth=34, caption="Dense stack 5"),
            to_Dense(name="relu_1",       size="", to="(batch_norm_1-east)", depth=34, caption=""),
            to_Dense(name="dropout_1",    size=34, to="(relu_1-east)",       depth=34, caption=""),
        ]
    ),

    to_connection_node("dropout_1", nodes_plus["b"]),

    to_Dense(name="dense_2", size="", to=nodes_plus["b"], depth=38, caption="", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_2", size="", to="(dense_2-east)",      depth=38, caption="Dense stack 6"),
            to_Dense(name="relu_2",       size="", to="(batch_norm_2-east)", depth=38, caption=""),
            to_Dense(name="dropout_2",    size=38, to="(relu_2-east)",       depth=38, caption=""),
        ]
    ),

    to_connection_node( "dropout_2", nodes_plus["c"]),

    to_Dense(name="dense_3", size="", to=nodes_plus["c"], depth=38, caption="", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_3", size="", to="(dense_3-east)",      depth=38, caption="Dense stack 7"),
            to_Dense(name="relu_3",       size="", to="(batch_norm_3-east)", depth=38, caption=""),
            to_Dense(name="dropout_3",    size=38, to="(relu_3-east)",       depth=38, caption=""),
        ]
    ),

    to_connection_node( "dropout_3", nodes_plus["d"]),

    to_Dense(name="dense_4", size="", to=nodes_plus["d"], depth=8, caption="", color="superdarkgreen"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_4", size="", to="(dense_4-east)",      depth=8, caption="Dense stack 8"),
            to_Dense(name="relu_4",       size="", to="(batch_norm_4-east)", depth=8, caption=""),
            to_Dense(name="dropout_4",    size=8, to="(relu_4-east)",        depth=8, caption=""),
        ]
    ),
]

conn = [
    new_node_obj("right plus", list(apply_offset(2.5, 'x', (get_node(nodes_plus, len(nodes_plus)-1))).values())[0]),
    new_node_obj("right spec", list(apply_offset(2.5, 'x', (get_node(nodes_spec, len(nodes_spec)-1))).values())[0]),
    new_node_obj("right liti", list(apply_offset(2.5, 'x', (get_node(nodes_liti, len(nodes_liti)-1))).values())[0]),
]

lines = [
    to_connection_nodes(["dropout_14-east", "right liti", "right spec"]),
    to_connection_nodes(["dropout_9-east",  "right spec", str(list(get_node(nodes_mixg, 0).values())[0].strip('()'))]),
    to_connection_nodes(["dropout_4-east",  "right plus", "right spec"]),
]

mixg = [
    to_Dense(name="dense_9",      size="",  to=nodes_mixg["a"],       depth=8, color="superdarkgreen"),
    to_Dense(name="dense_10",     size="",  to="(dense_9-east)",      depth=8, caption="Mixing stack", color="superdarkgreen"),
    to_Dense(name="batch_norm_9", size="",  to="(dense_10-east)",     depth=8, color="color1"),
    to_Dense(name="softmax_1",    size="8", to="(batch_norm_9-east)", depth=8),
]

# define the global architecture
arch = [
    to_head( '.' ),
    to_cor(),
    new_color("color1", "A2C7EA"),
    new_color("color2", "357ABB"),
    new_color("color_pool", "F44724"),
    new_color("flatten", "D079F9"),
    new_color("conv_color", "F1941D"),
    new_color("dark_yellow", "F9D046"),
    new_color("forestgreen", "24BB09"),
    new_color("superdarkgreen", "14A616"),
    to_begin(),

    *inputs,

    *liti,
    *spec,
    *plus,

    *conn,
    *lines,
    *mixg,

    to_end()
]


def main():
    file_name = str(sys.argv[0]).split('.')[0]
    verb      = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    to_generate(arch, file_name + '.tex', verbosity=verb)

if __name__ == '__main__':
    main()
