from sqlalchemy import text, insert, select, update
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from src.database import async_engine, sync_engine
import asyncio
from src.models import metadata_obj, WorkersOrm, Base, ResumesOrm, Workload, workers_table, resumes_table  

class SyncCore:
   @staticmethod
   def create_table():
    sync_engine.echo = False
   #  with sync_engine.connect() as conn:
   #          #!!!!!!!!
   #          conn.execute(text("DROP TABLE IF EXISTS resumes CASCADE"))
   #          conn.execute(text("DROP TABLE IF EXISTS workers CASCADE"))
   #          conn.commit()
    Base.metadata.drop_all(sync_engine) 
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True

   @staticmethod
   def insert_data():
    with sync_engine.connect() as connection:
      stmt = insert(WorkersOrm).values(
         [ 
            {"username": "Anna"},
            {"username": "Peter"}
         ]
      )
      connection.execute(stmt)
      connection.commit()      

   @staticmethod
   def select_data():
    with sync_engine.connect() as connection:
      query = select(workers)  
      result = connection.execute(query)
      workers = result.all()
      print(f"{workers=}")

   @staticmethod
   def update_data(worker_id: int = 2, new_username: str = "John"):
    with sync_engine.connect() as connection:
      #  stmt = text("UPDATE workers SET username=:username WHERE id=:id")
      #  stmt = stmt.bindparams(username=new_username, id=worker_id)
      stmt = (
         update(WorkersOrm)
         .values(username=new_username)
         # .where(workers_table.c.id == worker_id)
         .filter_by(id=worker_id)
      )
      connection.execute(stmt)
      connection.commit() 

    @staticmethod
    def insert_additional_resumes():
        with sync_engine.connect() as conn:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(workers_table).values(workers)
            insert_resumes = insert(resumes_table).values(resumes)
            conn.execute(insert_workers)
            conn.execute(insert_resumes)
            conn.commit()              

class AsyncCore:
   @staticmethod
   async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)  
            await conn.run_sync(metadata_obj.create_all)