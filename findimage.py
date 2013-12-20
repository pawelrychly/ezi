
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

#e = {
#    "lab": {
#        "file1": {
#            "f1": 0.1,
#            "f2": 0.9
#        },
#        "file2": {
#            "f1": 0.1,
#            "f2": 0.2
#        }
#    },
#    "rgb": {
#        "file1": {
#            "f1": 0.1,
#            "f2": 0.4
#        },
#        "file2": {
#            "f1": 0.3,
#            "f2": 0.4
#        }
#    }
#}

#files_func = "max"
#features_func = "max"
#print e

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


#-1
#sys.argv.append("4285.jpeg")
#sys.argv.append("ColorHCLCov")
#-2
#sys.argv.append("min")
#sys.argv.append("2")
#sys.argv.append("4285.jpeg")
#sys.argv.append("404.jpeg")
#sys.argv.append("min")
#sys.argv.append("3")
#sys.argv.append("ColorHCLCov")
#sys.argv.append("ColorRGBCov")
#sys.argv.append("ColorLabCov")



if len(sys.argv) < 3:
    print("Liczba argumentow jest nieprawidlowa. Przykladowe wywolania:")
    print("findimage query_file_name feature")
    print("findimage [min|max|avg] num_of_queryies queries [min|max|avg] num_of_features features")
    print("Possible features: [ ColorRGBCov | ColorHCLCov | ColorLabCov | ColorHist64 | ColorHist256 | TextureLumGabor ]")
    exit()

if len(sys.argv) == 3:
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

if len(sys.argv) > 3:
    #try:
    files_func = sys.argv[1]
    num_of_files = int(sys.argv[2])
    query_file_names = []
    for i in range(num_of_files):
        query_file_names.append(sys.argv[i+3])
    features_func = sys.argv[num_of_files+3]
    num_of_features = int(sys.argv[num_of_files+4])
    features = []
    for i in range(num_of_features):
        features.append(sys.argv[num_of_files+5+i])

    similarities_dict = {}
    for attribute in features:
        similarities_dict[attribute] = {}
        data = [ line.strip().split(" ") for line in open("data-images/features/" + attribute + ".dat", 'r')]
        data_dictionary = dict((line[0], line[1:]) for line in data)

        for key, vec in data_dictionary.items():
            for index, value in enumerate(vec):
                data_dictionary[key][index] = float(value)

        vectors = get_vectors_of_values(data_dictionary)
        std_values = get_std_vectors(vectors)
        avg_values = get_avg_vectors(vectors)

        data_dictionary = normalize_data(data_dictionary, std_values, avg_values)
        for query_file_name in query_file_names:
            query = data_dictionary[query_file_name]
            similarities = similarity_function(query, data_dictionary, std_values, avg_values)
            similarities_dict[attribute][query_file_name] = similarities

    #print similarities_dict
    #agragacja

    aggregated_by_filenames = {}
    for feature, similarities_by_filenames in similarities_dict.items():
        min_by_file_name = {}
        max_by_file_name = {}
        avg_by_file_name = {}
        num = {}
        for file_name, similarities in similarities_by_filenames.items():
            for image_name, value in similarities.items() :
                if not min_by_file_name.has_key(image_name):
                    min_by_file_name[image_name] = 1.0
                if not max_by_file_name.has_key(image_name):
                    max_by_file_name[image_name] = 0.0
                if not avg_by_file_name.has_key(image_name):
                    avg_by_file_name[image_name] = 0.0
                    num[image_name] = 0.0
                num[image_name] += 1.0
                if value < min_by_file_name[image_name]:
                    min_by_file_name[image_name] = value
                if value > max_by_file_name[image_name]:
                    max_by_file_name[image_name] = value
                avg_by_file_name[image_name] += value
        for key, value in avg_by_file_name.items():
            avg_by_file_name[key] = avg_by_file_name[key] / float(num[key])

        if files_func == "max":
            aggregated_by_filenames[feature] = max_by_file_name
        elif files_func == "min":
            aggregated_by_filenames[feature] = min_by_file_name
        else:
            aggregated_by_filenames[feature] = avg_by_file_name

    #print aggregated_by_filenames

    aggregated_feature = {}
    min_feature = {}
    max_feature = {}
    avg_feature = {}
    num_feature = {}

    for feature, similarities_by_feature in aggregated_by_filenames.items():
        for image_name, value in similarities_by_feature.items():
            if not min_feature.has_key(image_name):
                min_feature[image_name] = 1.0
            if not max_feature.has_key(image_name):
                max_feature[image_name] = 0.0
            if not avg_feature.has_key(image_name):
                avg_feature[image_name] = 0.0
                num_feature[image_name] = 0.0
            num_feature[image_name] += 1.0
            if value < min_feature[image_name]:
                min_feature[image_name] = value
            if value > max_feature[image_name]:
                max_feature[image_name] = value
            avg_feature[image_name] += value

    for key, value in avg_feature.items():
        avg_feature[key] = avg_feature[key] / float(num_feature[key])


    if features_func == "max":
        aggregated_feature = max_feature
    elif features_func == "min":
        aggregated_feature = min_feature
    else:
        aggregated_feature = avg_feature

    # aggregated_feature

    sorted_similarities = sorted(aggregated_feature.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(12):
        if i < len(sorted_similarities):
            print "{0} \t {1}".format(sorted_similarities[i][0], sorted_similarities[i][1])
    exit()