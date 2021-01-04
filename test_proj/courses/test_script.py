# from models import baseCourseNum, baseCourseCode
# import pyodbc




# conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
#                     'Server=DESKTOP-H322HOI;'
#                     'Database=UofC_Tree_Apps;'
#                     'Trusted_Connection=yes;')

# cursor = conn.cursor()

# for  i in baseCourseCode.objects.all():
#     result = cursor.execute(f"SELECT * FROM {i.code}")
#     for j in result:
#         x = baseCourseNum.objects.create(num = int(j[0]), code=i)
# conn.commit()
