from __future__ import annotations

class ast_node:
    def __init__(self) -> None:
        self.__parent = None
        self.__next = None
        self.__leftmost_sibling = None
        self.__leftmost_child = None

    def make_siblings(self,y:ast_node)->ast_node:
        x = self
        x_rightmost_sibling = x
        while x_rightmost_sibling.__next != None:
            x_rightmost_sibling  = x_rightmost_sibling.__next
        y_leftmost_sibling = y.__leftmost_sibling
        # concatenação das listas
        x_rightmost_sibling.__next = y_leftmost_sibling
        y_leftmost_sibling.__leftmost_sibling = x.__leftmost_sibling
        y_leftmost_sibling.__parent = x.__parent
        while y_leftmost_sibling.__next != None:
            y_leftmost_sibling = y_leftmost_sibling.__next
            y_leftmost_sibling.__parent = x.__parent
            y_leftmost_sibling.__leftmost_sibling = x.__leftmost_sibling
        return y_leftmost_sibling
    
    def adopt_children(self,y:ast_node):
        x = self
        if x.__leftmost_child != None:
            self.make_siblings(x.__leftmost_child,y)
        else:
            x.__leftmost_child = y_leftmost_sibling
            while y_leftmost_sibling != None:
                y_leftmost_sibling.__parent = x
                y_leftmost_sibling = y_leftmost_sibling.__next
    
    def make_node(self)->ast_node:
        x = ast_node()
        return x
    
    def make_family(self,op,children:list[ast_node])->ast_node:
        parent = self.make_node(op)
        for child in children[1:]:
            children[0].make_siblings(child)
        parent.adopt(children[0])
