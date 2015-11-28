import caffe, lmdb, sys
import caffe.proto.caffe_pb2
from caffe.io import datum_to_array

def main():
    infolder = sys.argv[1]
    outfile = sys.argv[2]

    lmdb_env = lmdb.open(infolder)
    lmdb_txn = lmdb_env.begin()
    lmdb_cursor = lmdb_txn.cursor()
    datum = caffe.proto.caffe_pb2.Datum()

    extract = {}
    for key, value in lmdb_cursor:
        datum.ParseFromString(value)
        label = datum.label
        data = caffe.io.datum_to_array(datum)
        values = []
        for d in data:
            values.append(d[0][0])
        extract[key] = values

    with open(outfile, 'w') as output_file:
        for key, features in extract.iteritems():
            output_file.write("%s %s\n" % (key, str(features)))

if __name__ == "__main__":
    main()