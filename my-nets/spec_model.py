import sys
sys.path.append("../")
from pycore.tikzeng import *
from pycore.blocks import alt_colors_block


n_blocks = 5
nodes = gen_nodes(n_blocks, xspace=5.5)



arch = [
    to_head( '.' ),
    to_cor(),
    new_color("color1", "A2C7EA"),
    new_color("color2", "357ABB"),
    to_begin(),

    # conv1
    to_Conv("conv1d", s_filter=5, n_filter=8, size="", to=nodes["a"], width=6, height=2, depth=32),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm", size="", to="(conv1d-east)",     depth=32, caption=""),
            to_Dense(name="relu",       size="", to="(batch_norm-east)", depth=32, caption="Conv stack 1"),
            to_Dense(name="dropout",    size=32, to="(relu-east)",       depth=32, caption=""),
        ]
    ),
    to_Pool(name="maxpool", size=16, to="(dropout-east)", width=2, height=2, depth=16),

    # conv2
    to_Conv("conv1d_1", s_filter=10, n_filter=16, size="", to=nodes["b"], width=12, height=2, depth=16),
    *alt_colors_block(
        [
            to_Dense(name="batch_norm_1", size="", to="(conv1d_1-east)",     depth=16, caption=""),
            to_Dense(name="relu_1",       size="", to="(batch_norm_1-east)", depth=16, caption="Conv stack 2"),
            to_Dense(name="dropout_1",    size=16, to="(relu_1-east)",       depth=16, caption=""),
        ]
    ),
    to_Pool(name="maxpool", size=8, to="(dropout_1-east)", width=2, height=2, depth=8),

    # flatten
    to_Dense("flatten", size=128, to=nodes["c"], depth=48, caption="Flatten"),




    to_end()
]


def main():
    file_name = str(sys.argv[0]).split('.')[0]
    verb      = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    to_generate(arch, file_name + '.tex', verbosity=verb)

if __name__ == '__main__':
    main()
