import networkx as nx
import fib_heap_mod
import copy, random


def charikarHeap(G):
         
    E = G.number_of_edges()
    N = G.number_of_nodes()
    fib_heap = fib_heap_mod.FibonacciHeap()
    entries = {}
    order = []
    S = copy.deepcopy(G)
    
    for node, deg in list(G.degree()):
        entries[node] = fib_heap.insert(deg, node)
    
    best_avg = 0.0    
    best_iter = iter = 0
    
    while fib_heap:
        avg_degree = (2.0 * E)/N
        if best_avg <= avg_degree:
            best_avg = avg_degree
            best_iter = iter
            
        min_deg_obj = fib_heap.extract_min()
        min_deg_node = min_deg_obj.get_value()
        order.append(min_deg_node)
        for n in list(S.neighbors(min_deg_node)):
            new_key = entries[n].get_key() - 1
            fib_heap.decrease_key(entries[n], new_key)
        
        
        S.remove_node(min_deg_node)
        E -= min_deg_obj.get_key()
        N -= 1
        iter += 1
        
        
    S = copy.deepcopy(G)       
    for i in range(best_iter):
        S.remove_node(order[i])
    return S, best_avg #len(S.edges())/len(S.nodes())
