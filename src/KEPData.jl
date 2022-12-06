struct Edge
    node_1::Int
    node_2::Int
    weight::Float64
    edge_id::Int
end

Base.string(edge::Edge) = "($(edge.node_1), $(edge.node_2), $(edge.weight))"

Base.show(io::IO, edge::Edge) = print(io, string(edge))

struct KEPData
    nb_vertices::Int
    nb_edges::Int
    list_of_altruists::Vector{Int}
    adjacency_matrix::Matrix{Int}
    list_of_edges::Vector{Edge}
    K::Int
    L::Int
    name::String
end

function parse_data(file_path::String)
    try
        file = open(file_path, "r")
        data = read(file, String)
        data = split(data, "\n")[10:end]
        nb_vertices = parse(Int, split(data[1], ":")[2])
        nb_edges = parse(Int, split(data[2], ":")[2])
        list_of_altruists = []
        for line in data[3:3 + nb_vertices]
            if occursin("Alturist", line)
                push!(list_of_altruists, parse(Int, split(line, " ")[end]))
            end
        end
        adjacency_matrix = fill(0, nb_vertices + 1, nb_vertices + 1)
        list_of_edges = []
        cpt = 0
        for line in data[3 + nb_vertices:length(data)-1]
            source, destination, weight = split(line, ",")
            adjacency_matrix[parse(Int, source), parse(Int, destination)] = parse(Float64, weight)
            if parse(Float64, weight) > 0
                push!(list_of_edges, Edge(parse(Int, source), parse(Int, destination), parse(Float64, weight), cpt))
                cpt += 1
            end
        end
        close(file)
        return (nb_vertices, nb_edges, list_of_altruists, adjacency_matrix, list_of_edges)
    catch e
        error("Error: $(e).")
        exit(1)
    end
end

Base.string(data::KEPData) = "Instance n°" * data.name * ": graph with " * string(data.nb_vertices) * " vertices and " * string(data.nb_edges) * " edges."

Base.show(io::IO, data::KEPData) = print(io, string(data))
