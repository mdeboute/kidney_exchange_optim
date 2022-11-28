import localsolver
import sys
import math
#import KEPData
import random

def kep_LS(data, timeLimit, solFile):
    nb_vertices_first = 10
    nb_vertices = int(nb_vertices_first*1.5)
    L = 3
    K = 2
    edges = [(0,2), (0,5), (1,3), (1,4), (3,2), (3,5), (4,7), (5,2), (6,3), (6,7), (7,9), (8,6), (8,9), (9,7)]
    adjacencyMatrix = [[0 for i in range(nb_vertices)] for j in range(nb_vertices)]
    for e in edges:
        adjacencyMatrix[e[0]][e[1]] = 1
    for i in range(nb_vertices_first, nb_vertices):
        adjacencyMatrix[i][i] = 1

    donnors = range(nb_vertices)
    donnors_altruist = [0, 1]
    altruist = [0 for i in range(nb_vertices)]
    for a in donnors_altruist:
        altruist[a] = 1
    weight = [[0 for j in range(nb_vertices)] for i in range(nb_vertices)]
    for e in edges:
        weight[e[0]][e[1]] = 1

    # set list size to upper bound + 1 that is unsatisfied couples
    nbLists = int((nb_vertices/2)+1)

    with localsolver.LocalSolver() as ls:
        #
        # Declares the optimization model
        #
        model = ls.model

        # Sequence of customers visited by each truck.
        couplesSequences = [model.list(nb_vertices) for k in range(nbLists)]

        # All sequences needs to be disjoints, including unsatisfied couples
        model.constraint(model.partition(couplesSequences))

        # Create distance as an array to be able to access it with an "at" operator
        weightsArray = model.array()
        for n in range(nb_vertices):
            weightsArray.add_operand(model.array(weight[n]))

        altruistArray = model.array(altruist)
        donnorArray = model.array(donnors)
        adjacencyMatrixArray = model.array()
        for n in range(nb_vertices):
            adjacencyMatrixArray.add_operand(model.array(adjacencyMatrix[n]))
        edgesArray = model.array(edges)

        sequencesWeights = [None] * nbLists
        sequencesWeights[nbLists-1] = 0

        for k in range(nbLists-1):
            sequence = couplesSequences[k]
            c = model.count(sequence)

            isAltruistSequence = model.at(altruistArray,sequence[0])

            #size limit
            limit = K + (L-K)*isAltruistSequence
            model.constraint(c <= limit)

            #edges existance
            couplesSelector = model.lambda_function(lambda i: model.at(adjacencyMatrixArray,sequence[i],sequence[i+1]))
            model.constraint(model.sum(model.range(0, c-1), couplesSelector) >= c-1)

            #return edge existance
            finalIsExisting = model.at(adjacencyMatrixArray,sequence[c-1],sequence[0])
            model.constraint((finalIsExisting + isAltruistSequence) >= 1)

            #objective calculations
            weightSelector = model.lambda_function(lambda i: model.at(weightsArray, sequence[i], sequence[i + 1]))
            sequencesWeights[k] = model.sum(model.range(0, c-1), weightSelector) + (1-isAltruistSequence)*model.at(weightsArray, sequence[c-1], sequence[0])

        # Total distance traveled
        totalWeight = model.sum(sequencesWeights)

        model.maximize(totalWeight)

        model.close()

        #
        # Parameterizes the solver
        #
        ls.param.time_limit = timeLimit

        ls.solve()

        for k in range(nbLists) :
            sequenceToText = ""
            if len(couplesSequences[k].value) == 1:
                continue
            for cloheleator in couplesSequences[k].value:
                if cloheleator >= nb_vertices_first:
                    cloheleator = "*"
                sequenceToText += str(cloheleator) + " "
            print(sequenceToText)

kep_LS(0,5,0)
