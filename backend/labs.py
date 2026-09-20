import os
from decimal import Decimal

import boto3

_table = None


def _labs_table():
    global _table
    if _table is None:
        _table = boto3.resource("dynamodb").Table(os.environ["LABS_TABLE_NAME"])
    return _table


def _from_ddb(item):
    if item is None:
        return None
    out = {}
    for key, value in item.items():
        if isinstance(value, Decimal):
            out[key] = int(value) if value % 1 == 0 else float(value)
        else:
            out[key] = value
    return out


def put_lab(item):
    _labs_table().put_item(Item=item)


def get_lab(username):
    resp = _labs_table().get_item(Key={"username": username})
    return _from_ddb(resp.get("Item"))


def delete_lab(username):
    resp = _labs_table().delete_item(
        Key={"username": username},
        ReturnValues="ALL_OLD",
    )
    return "Attributes" in resp


def scan_labs():
    table = _labs_table()
    items = []
    resp = table.scan()
    items.extend(resp.get("Items", []))
    while "LastEvaluatedKey" in resp:
        resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
        items.extend(resp.get("Items", []))
    return [_from_ddb(item) for item in items]
