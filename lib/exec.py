import jsonpickle as j
import init       as i
import argparse
import ast

parser = argparse.ArgumentParser()
parser.add_argument('names')
parser.add_argument('products')
parser.add_argument('matrix')
parser.add_argument('path')
args     = parser.parse_args()
names    = ast.literal_eval(args.names)
products = ast.literal_eval(args.products)
path     = args.path

if path:
    matrixPath = args.matrix
    with open(matrixPath) as f:
        matrix = f.read().splitlines()
    for index in range(0, len(matrix)):
        matrix[index] = matrix[index].split(',')
        matrix[index] = map(int,matrix[index])
    f.close()
else:
    matrix = ast.literal_eval(args.matrix)

if type(names) != list:
    names = len(matrix)
if type(products) != list:
    products = len(matrix[0])

results = i.init(names, products, matrix)

def sanitizeResults(res):
    if not isinstance(results[2], list):
        results[2] = results[2].tolist()
    for l in range(6,9):
        if len(results[l]) > 0:
            for m in range(0,len(results[l])):
                for n in range(0,len(results[l][m][0])):
                    for o in range(0,len(results[l][m][0][n])):
                        results[l][m][0][n][o] = results[l][m][0][n][o].name
                
                for n in range(0,len(results[l][m][1])):
                    results[l][m][1][n] = results[l][m][1][n].tolist()
                
                for n in range(0,len(results[l][m][4])):
                    results[l][m][4][n] = float(results[l][m][4][n])

                results[l][m][5] = float(results[l][m][5])

    results[9] = results[9].tolist()
    results[6] = results[6][0]

sanitizeResults(results)

print j.encode(results)
