from sqlalchemy import text, insert, select, update, func, cast, and_, or_, not_, delete, Integer
from src.database import async_engine, sync_engine, session_factory, async_session_factory
from src.models import metadata_obj, WorkersOrm, Base, ResumesOrm, Workload, VacanciesOrm
from sqlalchemy.orm import aliased, selectinload, joinedload, selectin_polymorphic, contains_eager

class SyncORM:
    @staticmethod
    def create_table():
     sync_engine.echo = False
     Base.metadata.drop_all(sync_engine)  
     Base.metadata.create_all(sync_engine) 
     sync_engine.echo = True

    @staticmethod
    def insert_data():
        with session_factory() as session:
            try:
                # Create the tables first if they don't exist
                # Base.metadata.create_all(sync_engine)
        
                worker_anna = WorkersOrm(username="Anna")
                worker_peter = WorkersOrm(username="Peter")
                
                # Add workers to session and commit
                session.add_all([worker_anna, worker_peter])
                session.commit()
                
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def select_data():
        with session_factory() as session:
            # worker_id = 1
            # worker_john = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.all()
            print(f"{workers=}")

    @staticmethod
    def update_data(worker_id: int = 2, new_username: str = "John"):
       with session_factory() as session:
           worker_peter = session.get(WorkersOrm, worker_id)
           if worker_peter:
            worker_peter.username = new_username
            session.commit()
        #to get new data   
        #    session.refresh(worker_peter)
        
        #to delete changes in data
        #    session.expire_all()
           session.commit()

    @staticmethod
    def insert_resumes():
            with session_factory() as session:
                resume_anna = ResumesOrm(
                    title="Python Junior Developer", compensation=50000, workload=Workload.part_time, worker_id=1)
                resume_peter = ResumesOrm(
                    title="Data Scientist", compensation=300000, workload=Workload.full_time, worker_id=2)
                session.add_all([resume_anna, resume_peter])
                session.flush()
                session.commit()

    @staticmethod
    def select_resumes_avg_compensation():
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    func.avg(cast(ResumesOrm.compensation, Integer)).label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains("Python"),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(func.avg(cast(ResumesOrm.compensation, Integer)) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result= session.execute(query)
            print(result.all()) 

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  
                {"username": "Roman"},  
                {"username": "Petr"},   
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload":Workload.full_time, "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload":Workload.part_time, "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload":Workload.part_time, "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload":Workload.full_time, "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload":Workload.full_time, "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()    
            
    @staticmethod
    def join_cte_subquery_window_func(like_language: str = "Python"):
     with session_factory() as session:
        r = aliased(ResumesOrm)
        w = aliased(WorkersOrm)

        subq = (
            select(
                r,
                w,
                func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"),
            )
            .join(r, r.worker_id == w.id).subquery("helper1")
        )
        cte = (
            select(
                subq.c.id,
                subq.c.title,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
            )
            .cte("helper2")
        )

        query = (
            select(cte)
            .order_by(cte.c.compensation_diff.desc())
        )

        res = session.execute(query)
        result = res.all()
        print(f"{result=}")        

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
            )

            res = session.execute(query)
            result = res.scalars().all() 

            worker_1_resumes = result[0].resumes
            print(f"{worker_1_resumes=}")

            worker_2_resumes = result[1].resumes
            print(f"{worker_2_resumes=}")

    @staticmethod
    def select_workers_with_joined_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                #many to one, one to one
                .options(joinedload(WorkersOrm.resumes))    
            )

            res = session.execute(query)
            result = res.unique().scalars().all() 

            worker_1_resumes = result[0].resumes
            print(f"{worker_1_resumes=}")

            worker_2_resumes = result[1].resumes
            print(f"{worker_2_resumes=}")

    @staticmethod
    def select_workers_with_selectin_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                #many to many, one to many
                .options(selectinload(WorkersOrm.resumes))    
            )

            res = session.execute(query)
            result = res.unique().scalars().all() 

            worker_1_resumes = result[0].resumes
            print(f"{worker_1_resumes=}")

            worker_2_resumes = result[1].resumes
            print(f"{worker_2_resumes=}")    

    @staticmethod
    def select_workers_with_condition_relationship():  
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes_parttime))    
            )

            res = session.execute(query)
            result = res.unique().scalars().all() 
            print(f"{result=}")

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():  
        with session_factory() as session:  
            query = (
                select(WorkersOrm)
                .join(WorkersOrm.resumes)  
                .options(contains_eager(WorkersOrm.resumes))
                .filter(ResumesOrm.workload == 'part_time')
            )

            res = session.execute(query)
            result = res.unique().scalars().all() 
            print(f"{result=}")    

    @staticmethod
    def select_workers_with_relationship_contains_eager_with_limit():
        with session_factory() as session:
            subq = (
                select(ResumesOrm.id.label("parttime_resume_id"))
                .filter(ResumesOrm.worker_id == WorkersOrm.id)
                .order_by(WorkersOrm.id.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(WorkersOrm)
            )

            query = (
                select(WorkersOrm)
                .join(ResumesOrm, ResumesOrm.id.in_(subq))
                .options(contains_eager(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)  

    @staticmethod
    def add_vacancies_and_replies():
        with session_factory() as session:
            new_vacancy = VacanciesOrm(title="Python разработчик", compensation=100000)
            resume_1 = session.get(ResumesOrm, 1)
            resume_2 = session.get(ResumesOrm, 2)
            resume_1.vacancies_replied.append(new_vacancy)
            resume_2.vacancies_replied.append(new_vacancy)
            session.commit() 

    @staticmethod
    def select_resumes_with_all_relationship():
        with session_factory() as session:
            query = (
                select(ResumesOrm)
                .options(joinedload(ResumesOrm.worker))
                .options(selectinload(ResumesOrm.vacancies_replied).load_only(VacanciesOrm.title))
            )         

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)               









class AsyncORM:
    @staticmethod
    async def async_create_table():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def insert_data():
        async with async_session_factory() as session:
            worker_num_one = WorkersOrm(username="Anna")
            worker_num_two = WorkersOrm(username="Peter")
            session.add_all([worker_num_one, worker_num_two])
            await session.commit()

    @staticmethod
    async def select_data():
        async with async_session_factory() as session:
            query = select(WorkersOrm)
            result = await session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    async def update_data(worker_id: int = 2, new_username: str = "Petuh"):
        async with async_session_factory() as session:
            worker_peter = await session.get(WorkersOrm, worker_id)
            worker_peter.username = new_username
            await session.refresh(worker_peter)
            await session.commit()

    @staticmethod
    async def insert_resumes():
        async with async_session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title="Python Junior Developer", compensation=50000, workload=Workload.full_time, worker_id=1)
            resume_jack_2 = ResumesOrm(
                title="Python Разработчик", compensation=150000, workload=Workload.full_time, worker_id=1)
            resume_michael_1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000, workload=Workload.part_time, worker_id=2)
            resume_michael_2 = ResumesOrm(
                title="Data Scientist", compensation=300000, workload=Workload.full_time, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2, 
                             resume_michael_1, resume_michael_2])
            await session.commit()

    @staticmethod
    async def select_resumes_avg_compensation(like_language: str = "Python"):
        async with async_session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    # 1 вариант использования cast
                    # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    # 2 вариант использования cast (предпочтительный способ)
                    func.avg(ResumesOrm.compensation).cast(Integer).label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(func.avg(ResumesOrm.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.all()
            print(result)

    @staticmethod
    async def insert_additional_resumes():
        async with async_session_factory() as session:
            workers = [
                {"username": "Artem"},  
                {"username": "Roman"},  
                {"username": "Petr"},   
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload":Workload.full_time, "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload":Workload.part_time, "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload":Workload.part_time, "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload":Workload.full_time, "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload":Workload.full_time, "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            await session.execute(insert_workers)
            await session.execute(insert_resumes)
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func(like_language: str = "Python"):
     async with async_session_factory() as session:
        r = aliased(ResumesOrm)
        w = aliased(WorkersOrm)

        subq = (
            select(
                r,
                w,
                func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"),
            )
            .join(r, r.worker_id == w.id).subquery("helper1")
        )
        cte = (
            select(
                subq.c.id,
                subq.c.title,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
            )
            .cte("helper2")
        )

        query = (
            select(cte)
            .order_by(cte.c.compensation_diff.desc())
        )

        res = await session.execute(query)
        result = res.all()
        print(f"{result=}")

        # print(query.compile(compile_kwargs={"literal_binds": True}))