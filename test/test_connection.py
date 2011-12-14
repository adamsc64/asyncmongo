import tornado.ioloop
import logging
import time

import test_shunt
import asyncmongo

TEST_TIMESTAMP = int(time.time())

class ConnectionTest(test_shunt.MongoTest):
    def test_query(self):
        logging.info('in test_query')
        test_shunt.setup()
        db = asyncmongo.Client(pool_id='test_query', host='127.0.0.1', port=27017, dbname='test', mincached=3)
        
        def insert_callback(response, error):
            tornado.ioloop.IOLoop.instance().stop()
            logging.info(response)
            assert len(response) == 1
            test_shunt.register_called('inserted')

        db.test_users.insert({"_id" : "test_connection.%d" % TEST_TIMESTAMP}, safe=True, callback=insert_callback)
        
        tornado.ioloop.IOLoop.instance().start()
        test_shunt.assert_called('inserted')
        
        def callback(response, error):
            tornado.ioloop.IOLoop.instance().stop()
            assert len(response) == 1
            test_shunt.register_called('got_record')

        db.test_users.find({}, limit=1, callback=callback)
        
        tornado.ioloop.IOLoop.instance().start()
        test_shunt.assert_called("got_record")
