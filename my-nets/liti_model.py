import sys
sys.path.append("../")
from pycore.tikzeng import *
from pycore.blocks import alt_colors_block


n_blocks = 5
nodes = gen_nodes(n_blocks, xspace=[0,4,5.5,2,3])

arch = [
    to_head( '.' ),
    to_cor(),
    new_color("color1", "A2C7EA"),
    new_color("color2", "357ABB"),
    to_begin(),

    # conv1
    to_Conv("conv1d", caption="Conv stack 1", s_filter=5, n_filter=8, size="", to=nodes["a"], width=6, height=2, depth=24),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm", size="", to="(conv1d-east)",     depth=24, caption=""),
            to_Dense(name="relu",       size="", to="(batch_norm-east)", depth=24, caption=""),
            to_Dense(name="dropout",    size=24, to="(relu-east)",       depth=24, caption=""),
        ]
    ),
    to_Pool(name="maxpool", s_pool=4, size=6, to="(dropout-east)", width=2, height=2, depth=6),

    to_connection_node("maxpool", nodes["b"]),

    # conv2
    to_Conv("conv1d_1", caption="Conv stack 2", s_filter=10, n_filter=16, size="", to=nodes["b"], width=12, height=2, depth=6),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_1", size="", to="(conv1d_1-east)",     depth=6, caption=""),
            to_Dense(name="relu_1",       size=16, to="(batch_norm_1-east)", depth=6, caption=""),
            to_Dense(name="dropout_1",    size="", to="(relu_1-east)",       depth=6, caption=""),
        ]
    ),
    to_Pool(name="maxpool", s_pool=4, size=1, to="(dropout_1-east)", width=2, height=2, depth=2),

    to_connection_node("maxpool", nodes["c"]),

    # flatten
    to_Dense("flatten", size=16, to=nodes["c"], depth=16, caption="Flatten"),

    to_connection_node("flatten", nodes["d"]),

    # dense1
    to_Dense(name="dense", size="", to=nodes["d"], depth=32, caption="Dense stack 1"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_2", size="", to="(dense-east)",        depth=32, caption=""),
            to_Dense(name="relu_2",       size="", to="(batch_norm_2-east)", depth=32, caption=""),
            to_Dense(name="dropout_2",    size=32, to="(relu_2-east)",       depth=32, caption=""),
        ]
    ),

    to_connection_node("dropout_2", nodes["e"]),

    # dense2
    to_Dense(name="dense_1", size="", to=nodes["e"], depth=8, caption="Dense stack 2"),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_3", size="", to="(dense_1-east)",      depth=8, caption=""),
            to_Dense(name="relu_3",       size="", to="(batch_norm_3-east)", depth=8, caption=""),
            to_Dense(name="dropout_3",    size=8, to="(relu_3-east)",       depth=8, caption=""),
        ]
    ),


    to_end()
]


def main():
    file_name = str(sys.argv[0]).split('.')[0]
    verb      = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    to_generate(arch, file_name + '.tex', verbosity=verb)

if __name__ == '__main__':
    main()
