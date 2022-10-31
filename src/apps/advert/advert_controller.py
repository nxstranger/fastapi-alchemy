from bson.objectid import ObjectId
from ...mongoose import adv_collection

# async def show_databases():
#     databases = client.execute('SHOW DATABASES')
#     return databases
#
#
# # async def create_new_table(table_name):
# #     t_name = 'request_stats'
# #     result = client.execute(
# #         'CREATE TABLE IF NOT EXISTS {0} ({1} String, {2} String, {3} String, {4} String, {5} DateTime) ENGINE = Memory'.format(
# #             t_name,
# #             'agent',
# #             'client',
# #             'path',
# #             'method',
# #             'stamp',
# #
# #         )
# #     )
# #     return result
#
#


async def insert_advert(dict_adv):
    result = adv_collection.insert_one(dict_adv).inserted_id
    return result


async def get_adverts(page, limit):
    result = adv_collection.find(
            {},
            {'_id': 1, 'price': 1, 'name': 1, 'created_at': 1}
        )\
        .sort('created_at', -1)\
        .skip(page * limit)\
        .limit(limit)

    return list(result)


async def get_advert_by_id(adv_id):
    result = adv_collection.find_one(
            {'_id': ObjectId(adv_id)},
            {'_id': 1, 'price': 1, 'name': 1, 'created_at': 1}
        )

    return result
