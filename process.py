import csv
outfo = 'data/cpiai.csv'

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
            out.append(['%s-%0d-01' % (year, idx+1), month])

    writer = csv.writer(open(outfo, 'w'))
    writer.writerow(['Date', 'Value'])
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
    import logging
    logging.basicConfig(level=logging.DEBUG)
    convert_to_csv()
    upload()

