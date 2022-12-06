include("KEPData.jl")

function print_usage()
    println("Usage: julia main.jl <instance_file> (<time_limit>)")
    println("<time_limit> is optional, its default value is set to 600 seconds")
    exit(1)
end

function main()
    if length(ARGS) < 1 || length(ARGS) > 2
        print_usage()
    end

    file_path = ARGS[1]
    if length(ARGS) == 2
        time_limit = parse(Int64, ARGS[2])
    else
        time_limit = 600
    end

    nb_vertices, nb_edges, list_of_altruists, adjacency_matrix, list_of_edges = parse_data(file_path)
    name = split(file_path, "/")[end]
    K = 3
    L = 3

    instance = KEPData(nb_vertices, nb_edges, list_of_altruists, adjacency_matrix, list_of_edges, K, L, name)

    println(instance)

    return 0
end

main()
