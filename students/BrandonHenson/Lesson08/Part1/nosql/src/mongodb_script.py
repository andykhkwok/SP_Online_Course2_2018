"""
    mongodb example
"""

from pprint import pprint as prpr
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    mongodb
    """

    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called dev')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['dev']

        log.info('And in that database use a collection called furniture')
        log.info('If it doesnt exist mongodb creates it')

        furniture = db['furniture']
        
        log.info('New Item')
        new_item = {
            'product':
                {'type': 'Chair',
                 'color': 'Brown'},
            'description': 'Wood',
            'monthly_rental_cost': 15.34,
            'in_stock_quantity': 2
        }
        new_item_id = furniture.insert_one(new_item).inserted_id
        
        log.info('Step 2: Now we add data from the dictionary above')
        furniture.insert_many(furniture_items)

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find(query)
        
        log.info('Print Red Items')
        query1 = {'product.color': 'Red'}
        results1 = furniture.find(query1)

        log.info('Step 4: Print the plastic products')
        print('Plastic products')
        for item in results:
            prpr(item)
        log.info('Red Products')
        print('Red products')
        for item in results1:
            prpr(item)
        
        log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({'$and': [{'product.type': 'Couch'},
                                  {'product.color': 'Blue'}]})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'$and': [{'product.type': 'Couch'},
                                  {'product.color': 'Blue'}]}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        prpr(results)

        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')
