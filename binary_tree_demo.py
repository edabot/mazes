import binary_tree
import grid

grid = grid.Grid(20,20)
binary_tree.BinaryTree.mutate(grid)

grid.to_string()
