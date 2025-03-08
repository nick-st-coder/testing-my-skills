import os
import sys
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.queries.orm import SyncORM, AsyncORM
from src.queries.core import SyncCore, AsyncCore
from src.database import Base

SyncORM.create_table() 
SyncORM.insert_data()
SyncORM.insert_resumes()
SyncORM.select_resumes_avg_compensation()
SyncORM.insert_additional_resumes()
SyncORM.join_cte_subquery_window_func()
SyncORM.select_workers_with_joined_relationship()
SyncORM.select_workers_with_selectin_relationship()
SyncORM.select_workers_with_condition_relationship()
SyncORM.select_workers_with_condition_relationship_contains_eager()
SyncORM.add_vacancies_and_replies()

# async def main():
#     await AsyncORM.async_create_table()
#     await AsyncORM.insert_data()
#     await AsyncORM.select_data()
#     await AsyncORM.update_data()
#     await AsyncORM.insert_resumes()
#     await AsyncORM.select_resumes_avg_compensation()
#     await AsyncORM.insert_additional_resumes()
#     await AsyncORM.join_cte_subquery_window_func()


# if __name__ == "__main__":
#     if sys.platform.startswith("win"):
#         asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
#     asyncio.run(main())