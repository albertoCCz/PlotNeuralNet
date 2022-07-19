import sys
sys.path.append("../")
from pycore.tikzeng import *
from pycore.blocks import alt_colors_block

nodes = gen_nodes(4)

arch = [
    to_head( '.' ),
    to_cor(),
    new_color("color1", "A2C7EA"),
    new_color("color2", "357ABB"),
    to_begin(),

    to_Dense(name="dense", size="", to=nodes["a"],  depth=34, caption=""),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm", size="", to="(dense-east)",      depth=34, caption="Dense stack 1"),
            to_Dense(name="relu",       size="", to="(batch_norm-east)", depth=34, caption=""),
            to_Dense(name="dropout",    size=34, to="(relu-east)",       depth=34, caption=""),
        ]
    ),

    to_connection_node( "dropout", nodes["b"]),

    to_Dense(name="dense_1", size="", to=nodes["b"], depth=38, caption=""),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_1", size="", to="(dense_1-east)",      depth=38, caption="Dense stack 2"),
            to_Dense(name="relu_1",       size="", to="(batch_norm_1-east)", depth=38, caption=""),
            to_Dense(name="dropout_1",    size=38, to="(relu_1-east)",       depth=38, caption=""),
        ]
    ),

    to_connection_node( "dropout_1", nodes["c"]),

    to_Dense(name="dense_2", size="", to=nodes["c"], depth=38, caption=""),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_2", size="", to="(dense_2-east)",      depth=38, caption="Dense stack 3"),
            to_Dense(name="relu_2",       size="", to="(batch_norm_2-east)", depth=38, caption=""),
            to_Dense(name="dropout_2",    size=38, to="(relu_2-east)",       depth=38, caption=""),
        ]
    ),

    to_connection_node( "dropout_2", nodes["d"]),

    to_Dense(name="dense_3", size="", to=nodes["d"], depth=8, caption=""),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_3", size="", to="(dense_3-east)",      depth=8, caption="Dense stack 4"),
            to_Dense(name="relu_3",       size="", to="(batch_norm_3-east)", depth=8, caption=""),
            to_Dense(name="dropout_3",    size=8, to="(relu_3-east)",        depth=8, caption=""),
        ]
    ),

    to_end(),
]

def main():
    file_name = str(sys.argv[0]).split('.')[0]
    verb      = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    to_generate(arch, file_name + '.tex', verbosity=verb)

if __name__ == '__main__':
    main()
