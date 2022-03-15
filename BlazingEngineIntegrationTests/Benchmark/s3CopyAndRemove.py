from boto.s3.connection import S3Connection

conn = S3Connection('AKIAIPG7TI6LRZY7P3CA', 'iIgBUHt5tSQ7UC6wo+qUIzkFCNEC/SMFQlPQy0d7')

tpchBucket = conn.get_bucket('blazing-test')

key = tpchBucket.get_key('entity.csv')
key.get_contents_to_filename('/home/ubuntu/entity.csv')

#
# rs = conn.get_all_buckets()
#
# print len(rs)
#
# for b in rs:
#     print b.name
