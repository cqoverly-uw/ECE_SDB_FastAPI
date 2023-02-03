from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, and_
from sqlalchemy.sql.expression import or_, or_


engine = create_engine("mssql+pyodbc://cqoverly:12rover12@EDW")
meta = MetaData(bind=engine)
student_1 = Table("student_1", meta, schema='sec', autoload=True, autoload_with=engine)
time_schedule = Table("time_schedule", meta, schema='sec', autoload=True, autoload_with=engine)


def get_ts(year, quarter, dept):
    s = select(
        time_schedule.c.ts_year,
        time_schedule.c.ts_quarter,
        time_schedule.c.dept_abbrev,
        time_schedule.c.course_no,
        time_schedule.c.section_id).where(
            and_(
                time_schedule.c.ts_year == year,
                time_schedule.c.ts_quarter == quarter,
                time_schedule.c.dept_abbrev == dept
            )
        ).order_by(time_schedule.c.course_no, time_schedule.c.section_id)
    
    conn = engine.connect()
    result = conn.execute(s)
    print(result)
    return result


def get_student(sid):
    s = select(student_1.c.system_key, student_1.c.student_no, student_1.c.student_name_lowc).where(
        student_1.c.student_no == sid
    )
    con = engine.connect()
    result = con.execute(s)
    return result


if __name__ == '__main__':
    r = get_ts(2021, 1, 'E E')
    # r = get_student(1834009)

    for row in r:
        print(row)

    # for c in time_schedule.columns:
    #     print(c)