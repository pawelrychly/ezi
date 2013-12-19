
import sys
import math
import numpy
import operator

def get_vectors_of_values(data_dictionary):
    vectors = []
    for key, line in data_dictionary.items():
        if len(vectors) <= 0:
            vectors = [[] for column in line]
        for index, value in enumerate(line):
            vectors[index].append(value)

    return vectors

def get_std_vectors(vectors_of_values):
    return [numpy.std(a = values, ddof = 1) for values in vectors_of_values]

def get_avg_vectors(vectors_of_values):
    return [numpy.average(a = values) for values in vectors_of_values]


#d = {
#    "a": ['2', '2', '5'],
#    "b": ['2', '2', '2'],
#    "c": ['5', '5', '2'],
#    "d": ['7', '7', '7']
#}

def normL1(query, vector_of_values, std_vector, avg_vector):
    sum = 0.0
    for index, value in enumerate(vector_of_values):
        sum += float(1/float(std_vector[index])) * math.fabs(query[index] - value)
    return sum

def similarity_function(query, data_dictionary, std_values, avg_values):
    distances = dict((key, normL1(query, vector, std_values, avg_values)) for (key, vector) in data_dictionary.items())
    max_distance = distances[max(distances.items(), key=operator.itemgetter(1))[0]]
    min_distance = distances[min(distances.items(), key=operator.itemgetter(1))[0]]

    similarities = dict((key, (float(max_distance - value) / float(max_distance - min_distance))) for (key, value) in distances.items())
    #similarities = [(float(max_distance - value) / float(max_distance - min_distance)) for value in distances]
    return similarities



def normalize_data(data_dictionary, std_values, avg_values):
    for key, vector in data_dictionary.items():
        for index, value in enumerate(vector):
            data_dictionary[key][index] = ( float(value) - float(avg_values[index]) ) / float(std_values[index])
    return data_dictionary



sys.argv.append("4029.jpeg")
sys.argv.append("ColorRGBCov")

if len(sys.argv) < 3:
    print("Wymagane sa dwa argumenty. Przykladowe uruchomienie:")
    print("findimage query_file_name [ ColorRGBCov | ColorHCLCov | ColorLabCov | ColorHist64 | ColorHist256 | TextureLumGabor ]")
    exit()

query_file_name = sys.argv[1]
attribute = sys.argv[2]

data = [ line.strip().split(" ") for line in open("data-images/features/" + attribute + ".dat", 'r')]
data_dictionary = dict((line[0], line[1:]) for line in data)

for key, vec in data_dictionary.items():
    for index, value in enumerate(vec):
        data_dictionary[key][index] = float(value)

vectors = get_vectors_of_values(data_dictionary)
std_values = get_std_vectors(vectors)
avg_values = get_avg_vectors(vectors)


data_dictionary = normalize_data(data_dictionary, std_values, avg_values)
query = data_dictionary[query_file_name]

similarities = similarity_function(query, data_dictionary, std_values, avg_values)
sorted_similarities = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
for i in range(12):
    if i < len(sorted_similarities):
        print "{0} \t {1}".format(sorted_similarities[i][0], sorted_similarities[i][1])
