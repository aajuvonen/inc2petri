function mat2py(matrix)
    [rows, cols] = size(matrix);

    fprintf('[');
    for i = 1:rows
        fprintf('[');
        for j = 1:cols
            fprintf('%d', matrix(i, j));
            if j < cols
                fprintf(', ');
            end
        end
        fprintf(']');
        if i < rows
            fprintf(', ');
        end
    end
    fprintf(']\n');
end