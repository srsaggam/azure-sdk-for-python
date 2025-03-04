# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_query_table_async.py

DESCRIPTION:
    These samples demonstrate the following: querying a table for entities.

USAGE:
    python sample_query_table_async.py

    Set the environment variables with your own values before running the sample:
    1) TABLES_STORAGE_ENDPOINT_SUFFIX - the Table service account URL suffix
    2) TABLES_STORAGE_ACCOUNT_NAME - the name of the storage account
    3) TABLES_PRIMARY_STORAGE_ACCOUNT_KEY - the storage account access key
"""

import os
import copy
import random
import asyncio
from dotenv import find_dotenv, load_dotenv


class SampleTablesQuery(object):
    def __init__(self):
        load_dotenv(find_dotenv())
        self.access_key = os.getenv("TABLES_PRIMARY_STORAGE_ACCOUNT_KEY")
        self.endpoint_suffix = os.getenv("TABLES_STORAGE_ENDPOINT_SUFFIX")
        self.account_name = os.getenv("TABLES_STORAGE_ACCOUNT_NAME")
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
            self.account_name, self.access_key, self.endpoint_suffix
        )
        self.table_name = "OfficeSupplies"

    async def insert_random_entities(self):
        from azure.data.tables.aio import TableClient
        from azure.core.exceptions import ResourceExistsError

        brands = ["Crayola", "Sharpie", "Chameleon"]
        colors = ["red", "blue", "orange", "yellow"]
        names = ["marker", "pencil", "pen"]
        entity_template = {
            "PartitionKey": "pk",
            "RowKey": "row",
        }

        table_client = TableClient.from_connection_string(self.connection_string, self.table_name)
        async with table_client:
            try:
                await table_client.create_table()
            except ResourceExistsError:
                print("Table already exists")

            for i in range(25):
                e = copy.deepcopy(entity_template)
                e["RowKey"] += str(i)
                e["Name"] = random.choice(names)
                e["Brand"] = random.choice(brands)
                e["Color"] = random.choice(colors)
                e["Value"] = random.randint(0, 100)
                await table_client.create_entity(entity=e)

    async def sample_query_entities(self):
        from azure.data.tables.aio import TableClient
        from azure.core.exceptions import HttpResponseError

        print("Entities with name: marker")
        table_client = TableClient.from_connection_string(self.connection_string, self.table_name)
        # [START query_entities]
        async with table_client:
            try:
                parameters = {u"name": u"marker"}
                name_filter = u"Name eq @name"
                queried_entities = table_client.query_entities(
                    query_filter=name_filter, select=[u"Brand", u"Color"], parameters=parameters
                )

                async for entity_chosen in queried_entities:
                    print(entity_chosen)

            except HttpResponseError as e:
                pass
            # [END query_entities]

    async def sample_query_entities_without_metadata(self):
        from azure.data.tables.aio import TableClient
        from azure.core.exceptions import HttpResponseError

        print("Entities with name: marker")
        table_client = TableClient.from_connection_string(self.connection_string, self.table_name)
        # [START query_entities]
        async with table_client:
            try:
                parameters = {u"name": u"marker"}
                name_filter = u"Name eq @name"
                headers = {"Accept" : "application/json;odata=nometadata"}
                queried_entities = table_client.query_entities(
                    query_filter=name_filter, select=[u"Brand", u"Color"], parameters=parameters, headers=headers
                )

                async for entity_chosen in queried_entities:
                    print(entity_chosen)

            except HttpResponseError as e:
                pass
            # [END query_entities]

    async def sample_query_entities_multiple_params(self):
        from azure.data.tables.aio import TableClient
        from azure.core.exceptions import HttpResponseError

        print("Entities with name: marker and brand: Crayola")
        # [START query_entities]
        async with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:
            try:
                parameters = {u"name": u"marker", u"brand": u"Crayola"}
                name_filter = u"Name eq @name and Brand eq @brand"
                queried_entities = table_client.query_entities(
                    query_filter=name_filter, select=[u"Brand", u"Color"], parameters=parameters
                )

                async for entity_chosen in queried_entities:
                    print(entity_chosen)

            except HttpResponseError as e:
                print(e.message)
        # [END query_entities]

    async def sample_query_entities_values(self):
        from azure.data.tables.aio import TableClient
        from azure.core.exceptions import HttpResponseError

        print("Entities with 25 < Value < 50")
        # [START query_entities]
        async with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:
            try:
                parameters = {u"lower": 25, u"upper": 50}
                name_filter = u"Value gt @lower and Value lt @upper"
                queried_entities = table_client.query_entities(
                    query_filter=name_filter, select=[u"Value"], parameters=parameters
                )

                async for entity_chosen in queried_entities:
                    print(entity_chosen)

            except HttpResponseError as e:
                print(e.message)
        # [END query_entities]

    async def clean_up(self):
        print("cleaning up")
        from azure.data.tables.aio import TableClient

        async with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:
            await table_client.delete_table()


async def main():
    stq = SampleTablesQuery()
    try:
        await stq.insert_random_entities()
        await stq.sample_query_entities()
        await stq.sample_query_entities_without_metadata()
        await stq.sample_query_entities_multiple_params()
        await stq.sample_query_entities_values()
    except Exception as e:
        print(e)
    finally:
        await stq.clean_up()


if __name__ == "__main__":
    asyncio.run(main())
