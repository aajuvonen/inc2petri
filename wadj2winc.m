function incidence_matrix = wadj2winc(adjacency_matrix)
    [num_nodes, ~] = size(adjacency_matrix);
    num_edges = nnz(adjacency_matrix);

    incidence_matrix = zeros(num_nodes, num_edges);
    edge_index = 1;

    for i = 1:num_nodes
        for j = i:num_nodes
            if i ~= j && adjacency_matrix(i, j) ~= 0
                incidence_matrix(i, edge_index) = -adjacency_matrix(i, j);
                incidence_matrix(j, edge_index) = adjacency_matrix(i, j);
                edge_index = edge_index + 1;
            end
        end
    end
end