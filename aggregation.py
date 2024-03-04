from json import JSONDecodeError, loads
from datetime import datetime
from pymongo import ASCENDING
from database import collection

exception = """Невалидный запос. Пример запроса:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""


async def aggregate_salary(data: str):
    try:

        data_dict = loads(data)

    except JSONDecodeError:

        return exception
    
    try:
        dt_from = datetime.fromisoformat(data_dict["dt_from"])
        dt_upto = datetime.fromisoformat(data_dict["dt_upto"])
        group_type = data_dict["group_type"]
        
        dict_date_formats = {"month": "%Y-%m-01", "day": "%Y-%m-%d", "hour": "%Y-%m-%dT%H"}
        date_format = dict_date_formats[group_type]
        
        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {"$group": {
                "_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
                "total_payment": {"$sum": "$value"}
            }
            },
            {'$sort': {'_id': ASCENDING}},
            {"$addFields": {"_id": {"$toString": "$_id"}}}
            
        ]

        result = list(collection.aggregate(pipeline))

        response = {
            "dataset": [item["total_payment"] for item in result],
            "labels": [datetime.fromisoformat(item["_id"]).isoformat() for item in result]
        }

        return response
    
    except ValueError:
        return exception
    
    except KeyError:
        return exception
    
    except TypeError:
        return exception



