import csv

def convert_to_csv():
    fo = open('data/cpiai.txt')
    lines = fo.read().split('\n')
    lines = lines[18:]
    print lines[0]

    out = []
    for line in lines:
        cells = line.strip().split()
        if not cells:
            continue
        year = cells.pop(0)
        months = cells[:12]
        for idx, month in enumerate(months):
            out.append(['%s-%0d-01' % (year, idx+1), month])

    outfo = 'data/cpiai.csv'
    writer = csv.writer(open(outfo, 'w'))
    writer.writerow(['Date', 'Value'])
    writer.writerows(out)

