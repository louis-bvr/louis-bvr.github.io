import csv

l = [[1, 2], [2, 3], [4, 5]]

out = open('out.csv', 'w')
for row in l:
    for column in row:
        out.write('%d;' % column)
    out.write('\n')
out.close()