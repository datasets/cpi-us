import csv
outfo = 'data/cpiai.csv'

source_url = 'ftp://ftp.bls.gov/pub/special.requests/cpi/cpiai.txt'

def download():
    urllib.urlretrieve(source_url, 'data/cpiai.txt')

def convert_to_csv():
    fo = open('data/cpiai.txt')
    lines = fo.read().split('\n')
    lines = lines[18:]
    out = []
    for line in lines:
        cells = line.strip().split()
        if not cells:
            continue
        year = cells.pop(0)
        months = cells[:12]
        for idx, month in enumerate(months):
            out.append(['%s-%02d-01' % (year, idx+1), float(month)])
    for idx, row in enumerate(out[1:]):
        thismonth = row[1]
        lastmonth = out[idx][1]
        # really this isn't quite right since price index is average of that
        # month and i want
        # inflation this month = price index start of month - index at end of month
        inflation = round(100*(thismonth - lastmonth) / lastmonth, 2)
        row.append(inflation)
    # no value for inflation in first month
    row[0].append('')

    writer = csv.writer(open(outfo, 'w'))
    writer.writerow(['Date', 'Index', 'Inflation'])
    writer.writerows(out)

def upload():
    import datastore.client as c
    client = c.DataStoreClient('http://datahub.io/dataset/us-consumer-price-index/resource/27e14656-ba2a-4b81-855d-0f167809d87d')
    client.delete()
    mapping = {
        'properties': {
            'Value': {
                'type': "double"
            },
            'Date': {
                'type': "date",
                'format': "dateOptionalTime"
            }
        }
    }
    client.mapping_update(mapping)
    client.upload(outfo)

if __name__ == '__main__':
    convert_to_csv()

