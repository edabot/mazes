import binary_tree
import grid

grid = grid.Grid(15,15)
binary_tree.BinaryTree.mutate(grid, True)

grid.to_string()
grid.to_svg()
