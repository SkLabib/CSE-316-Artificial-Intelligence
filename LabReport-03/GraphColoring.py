import os

def is_valid(graph, colors, vertex, color):
    """ Check if it is safe to color vertex with the given color. """
    for neighbor in graph[vertex]:
        if colors[neighbor] == color:
            return False
    return True

def graph_coloring_util(graph, colors, vertex, K):
    """ Utility function to solve graph coloring using backtracking. """
    if vertex == len(graph):  
        return True

    for color in range(1, K+1):
        if is_valid(graph, colors, vertex, color):
            colors[vertex] = color
            if graph_coloring_util(graph, colors, vertex + 1, K):
                return True
            colors[vertex] = 0  
    
    return False  

def graph_coloring(graph, N, M, K):
    """ Function to check if the graph can be colored with K colors. """
 
    colors = [0] * N  
    
    
    if graph_coloring_util(graph, colors, 0, K):
        print(f"Coloring Possible with {K} Colors")
        print(f"Color Assignment: {colors}")
    else:
        print(f"Coloring Not Possible with {K} Colors")

def main():

    input_files = ['input_case1.txt', 'input_case2.txt']
    
    for file_name in input_files:

        print(f"\nProcessing {file_name}...\n")
        
        file_path = os.path.join(os.getcwd(), file_name)  
        
        try:

            with open(file_path, "r") as file:
                N, M, K = map(int, file.readline().split())  
                graph = [[] for _ in range(N)]

                for _ in range(M):
                    u, v = map(int, file.readline().split())
                    graph[u].append(v)
                    graph[v].append(u)

            graph_coloring(graph, N, M, K)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")

if __name__ == "__main__":
    main()
