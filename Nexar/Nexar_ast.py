# ------------------- AST Node -------------------
class ASTNode:
    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print(self, indent=0):
        print("  " * indent + f"{self.node_type}: {self.value}")
        for c in self.children:
            c.print(indent + 1)

# ------------------- Example AST -------------------
if __name__ == "__main__":
    # Root node: Screen
    screen = ASTNode("Screen", "MainScreen")

    # Add a button
    button = ASTNode("Widget", "Button")
    button.add_child(ASTNode("Text", "Play"))
    button.add_child(ASTNode("Event", "onClick -> startGame"))
    screen.add_child(button)

    # Add a layout with icon and label
    layout = ASTNode("Layout", "Row")
    layout.add_child(ASTNode("Widget", "Icon: coin"))
    layout.add_child(ASTNode("Widget", "Label: 100"))
    screen.add_child(layout)

    # Print AST
    screen.print()
