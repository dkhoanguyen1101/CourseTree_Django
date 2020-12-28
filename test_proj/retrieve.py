#libraries
import pyodbc #sql server
from bs4 import BeautifulSoup #data scraping
import requests #data scraping

#connect to server
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-H322HOI;'
                      'Database=UofC_Tree_Apps;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()



def get_course_info(s):

    little_soup_src = requests.get(s).text
    little_soup = BeautifulSoup(little_soup_src, 'lxml')

    
    code = little_soup.find('span', class_='page-title').contents[0].strip().split(' ')[-1]
    name = little_soup.find('span', class_='page-title').contents[0].strip().replace(code, '').strip()
    #   print(code)
    # print(name)

    courses = []
    getAll = little_soup.findAll('div', class_='item-container')
    for i in getAll:
        if (i.find('td', class_='myCell') != None):
            courses.append(i)
    #print(courses)
    return courses, code, name

def log_course(courses, code, name):
    
    for i in courses:
        j = i.findAll('span', class_='course-code')
        number = j[1].contents[0]
        acode = code
        acode = acode.replace("PPLAN", "PLAN").replace("TTRAN", "TRAN")
        course_code = " ".join([acode, number])
        course_name = j[2].contents[0]
        
        if (len(i.find('span', class_="course-prereq").contents) > 0):
            course_pre = "".join(i.find('span', class_="course-prereq").findAll(text=True))
        else:
            course_pre = 'none'
        
        if (len(i.find('span', class_="course-antireq").contents) > 0):
            course_anti = "".join(i.find('span', class_="course-antireq").findAll(text=True))
        else:
            course_anti = 'none'

        if (len(i.find('span', class_="course-coreq").contents) > 0):
            course_con = "".join(i.find('span', class_="course-coreq").findAll(text=True))
        else:
            course_con = 'none'

        if (len(i.find('span', class_="course-desc").contents) > 0):
            course_desc = "".join(i.find('span', class_="course-desc").findAll(text=True))
        else:
            course_desc = 'none'
        val = [code, number, course_name, course_code, course_pre, course_anti, course_con, course_desc]
        
        course_name = course_name.replace("'", "''")
        course_pre = course_pre.replace("'", "''")
        course_anti = course_anti.replace("'", "''")
        course_con = course_con.replace("'", "''")
        course_desc = course_desc.replace("'", "''")

        # sql = f"INSERT INTO {code} (number, name , code , pre , anti , con , des) VALUES (\'{number}\', \'{course_name}\', \'{course_code}\', \'{course_pre}\', \'{course_anti}\', \'{course_con}\', \'{course_desc}\')"
        sql = f"INSERT INTO {code} (number, name , code , pre , anti , con ) VALUES ({int(number)}, \'{course_name}\', \'{course_code}\', \'{course_pre}\', \'{course_anti}\', \'{course_con}\')"
        # print(sql)
        cursor.execute(sql)

        # print(course_code)
        # print(f"pre: {course_pre}, anti:{course_anti}, co:{course_co}" )
        
        

def get_data(soup):

    cursor.execute("DROP TABLE IF EXISTS dbo.courses")
    cursor.execute("CREATE TABLE courses (code VARCHAR(255), name VARCHAR(255))")
    for i in soup.findAll('span', class_='contents-text' , style='margin-left:15px;' ):
        j = (i.find('a').get('href'))
        courses, code, name = get_course_info('https://www.ucalgary.ca/pubs/calendar/current/'+str(j))

        if (code == "PLAN"):
            code = "PPLAN"
        elif (code == "TRAN"):
            code = "TTRAN"
        sql = "INSERT INTO courses (code, name) VALUES (?, ?)"
        val = (code, name)
        cursor.execute(sql, val)
        
        # sql = f"CREATE TABLE {code} (number VARCHAR(255), name VARCHAR(255), code VARCHAR(255), pre VARCHAR(1023), anti VARCHAR(1023), con VARCHAR(1023), des VARCHAR(1023))"
        sql = f"DROP TABLE IF EXISTS {code}"
        cursor.execute(sql)
        sql = f"CREATE TABLE {code} (number INT, name VARCHAR(255), code VARCHAR(255), pre VARCHAR(1023), anti VARCHAR(1023), con VARCHAR(1023))"

        cursor.execute(sql)
        log_course(courses, code, name)
        
        

        

if __name__=="__main__":
    src = requests.get('https://www.ucalgary.ca/pubs/calendar/current/course-desc-main.html').text
    soup = BeautifulSoup(src, 'lxml')
    get_data(soup)
    conn.commit()
    print('done')
