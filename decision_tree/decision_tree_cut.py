from copy import deepcopy

class CART_CUT(object):
  
    # input: tree generated by CART algorithm
    # output: child tree list
    
    def __init__(self):
        pass
    
    def compute_gini(self, y_data):
        tmp = y_data.value_counts(normalize=True)
        gini = 1 - tmp.apply(lambda x: x * x).sum()
        return gini

    def tree_compute_gini(self, T):
        leaf_node = 0
        gini = 0
        if T.children == None:
            leaf_node = 1
            gini = self.compute_gini(T.y_data)
            return gini, leaf_node
        else:
            for sub_tree in T.children:
                gini_, leaf_node_ = self.tree_compute_gini(T.children.get(sub_tree))
                gini += gini_
                leaf_node += leaf_node_
        return gini, leaf_node
    
    def BFS(self, tree):
        node = list()
        if tree.children == None:
            return None
        else:
            for child in tree.children:
                node.append(tree.children.get(child))
        return node
                
    def get_node(self, T):
        BFS_node = list()
        BFS_node.append(T)
        i = 0
        while len(BFS_node) > i:
            child_node = self.BFS(BFS_node[i])
            if child_node != None:
                BFS_node += child_node
            i += 1
        return BFS_node
    
    def tree_cut(self, T):
        child_tree_list = list()
        T = deepcopy(T)
        child_tree_list.append(T)
        T = deepcopy(T)
        while True:
            BFS_node = self.get_node(T)
            alpha = float('inf')
            gini_log = [float('inf')] * len(BFS_node) 
            for i in range(1, len(BFS_node)):
                if BFS_node[-i].feature is None or BFS_node[-i].x_data is None or len(BFS_node[-i].x_data) == 0:
                    continue
                else:
                    c_t = self.compute_gini(BFS_node[-i].y_data)
                    c_T, leaf_node = self.tree_compute_gini(BFS_node[-i])
                    g_t = (c_t - c_T) / (leaf_node - 1)
                    gini_log[-i] = g_t
                    alpha = min(alpha, g_t)
            for i in range(1, len(BFS_node)):
                if gini_log[-i] == alpha:
                    BFS_node[-i].children = None
                    BFS_node[-i].category = BFS_node[-i].y_data.value_counts(ascending=False).keys()[0]
                    BFS_node[-i].feature = None
            child_tree_list.append(T)
            T = deepcopy(T)
            T_children = T.children
            keys = list(T_children.keys())
            if T_children[keys[0]].children == None and T_children[keys[1]].children == None:
                break
        return child_tree_list

class Tree_Cut(object):
    # input: tree generated by ID3 or C45, hyper-parameter alpha
    # output: the best tree
    def __init__(self, alpha):
        self.alpha = alpha
        
    def compute_entr(self, y_data):
        tmp = y_data.value_counts(normalize=True)
        label_entr = tmp.apply(lambda x: -1 * x * np.log2(x)).sum()
        return label_entr
    
    def find_leaf_node(self, tree_node):
        children_node = tree_node.children
        leaf_node = list()
        leaf_num = None
        if children_node == None:
            leaf_node.append(tree_node)
            leaf_num = 1
           `return leaf_node, leaf_num
        else:
            keys = list(children_node.keys())
            for key in keys:
                node = children_node.get(key)
                _node, _num = self.find_leaf_node(node)
                leaf_node += _node
                leaf_num += _num
            return leaf_node, leaf_num
        
    def _tree_cut(self, tree_node):
        leaf_node, leaf_num = self.find_leaf_node(tree_node)
        parent_list = list()
        exp_entr = 0
        exp_dict = dict()
        for _node in leaf_node:
            parent = _node.parent
            if parent not in parent_list:
                parent_list.append(parent)
            exp_dict[_node] = self.compute_entr(_node.y_data)
            exp_entr += exp_dict[_node]
        entr_b = exp_entr + self.alpha * leaf_num
        
        for _node in parent_list:
            leaf_num_a = leaf_num + 1
            p_entr = self.compute_entr(_node.y_data)
            for item in exp_dict:
                if item in _node.children:
                    leaf_num_a -= 1
                    continue
                else:
                    p_entr += exp_dict[item]
            entr_a = p_entr + self.alpha * leaf_num_a
            if entr_a <= entr_b:
                _node.children = None
                _node.feature = None
                _node.category = _node.y_data.value_counts(ascending=False).keys()[0]
                self._tree_cut(tree_node)
                break
        
        
                
                
        
