import requests
import pymysql.cursors
import MySQLdb
import pymysql
import pandas as pd
from datetime import date



host = "202.92.4.71"
user = "qfzovpphosting_thaitn"
password = "Xngancon9x"
db = "qfzovpphosting_MCI_Database"
database = MySQLdb.connect(host=host, user=user, password=password, db=db)
cursor = database.cursor()

#lấy ra thông tin của học viên
def getStudentInfo():
    query = """ 
    WITH tmp_tbl AS (
        SELECT 
            ins.id,
            ins.inforregister_id,
            ins.schedulecourse_id,
            inf.name,
            inf.email,
            scc.class_name,
            scc.class_code,
            scc.start_date,
            scc.end_date,
            datediff(scc.end_date, curdate()) as so_ngay_con_lai
	
    FROM nhanvien_inforregister_schedule ins
    INNER JOIN nhanvien_inforregister inf
        ON ins.inforregister_id = inf.id
    INNER JOIN nhanvien_schedulecourse scc
        ON ins.schedulecourse_id = scc.id
    )

    SELECT *, 
        ROW_NUMBER() OVER(partition by inforregister_id order by start_date ) as dem
    FROM tmp_tbl
    WHERE so_ngay_con_lai >= 3
    """
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(data=result, columns=["id", "inforregister_id", "schedulecourse_id",
                                            "name", "email", "class_name", "class_code", 
                                            "start_date", "end_date", "so_ngay_con_lai", "dem"])
    return df




#hàm gửi email
def createEmail(name, finish_course, end_date, syllabus_link):
    mail_content = f'''
        <h5 style = "color: #4caf50; font-size: 16pt; font-family: 'Times New Roman', serif; background: white;"> Kính gửi anh/chị {name} </h5>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Khóa học {finish_course} sẽ kết thúc vào {end_date}</p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Anh chị có thể theo dõi lộ trình khóa học tiếp theo của mình <a href = {syllabus_link}>tại đây</a></p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;">Cảm ơn anh/chị đã tin tưởng lựa chọn Học viện Đào tạo Lập trình MCI Việt Nam.</p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Học viện Đào tạo Lập trình MCI Việt Nam <br>
        Trân trọng!
        <hr/>
        <p style = "color: #E87500; font-size: 13pt; font-family: 'Times New Roman', serif; background: white;">
            Học viện Đào tạo Lập trình MCI Việt Nam<br>
            Trân trọng cảm ơn, <br>
            CÔNG TY CỔ PHẦN ĐÀO TẠO VÀ TƯ VẤN MCI VIỆT NAM (MCI) <br>
            Trụ sở chính: Số 5/23/165, Thái Hà, Đống Đa, Hà Nội <br>
            Chi nhánh: Số 284A, Nam Kì Khởi Nghĩa, Quận 3, tp HCM <br>
            Hotline: 024 7106 8368 - Bộ phận tư vấn khóa học lập trình và phân tích dữ liệu<br>
        </p>
    '''
    return mail_content


#lấy ra lộ trình khóa học từ website dựa vào class_code
def getSyllabus(course):
    if course[0: 2] == "PY" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-python-for-data-LJNQ0L/"
    if course[0: 2] == "PY" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-python-for-mach-1LOCB2/"
    if course[0: 2] == "PB" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-analyzing-and-v-LEY8HR/"
    if course[0: 2] == "PB" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-applying-power--OVAYKN/"
    if course[0: 2] == "SQ" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-sql-for-newbies-LEY8HR/"
    if course[0: 2] == "SQ" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-database-and-sq-LEY8HR/"
    if course[0: 2] == "EX" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-intermediate-to-SM6W3T/"
    if course[0: 2] == "EX" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-combo-excel-l-WE5BFV/"
    if course[1] == "V" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-vba-tu-co-ban-t-SM6W3T/"
    if course[1] == "V" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-vba-sieu-ung-du-SM6W3T/"
    if course[0: 2] == "BA" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-business-analys-Z1CJGF/"
    if course[0: 2] == "BA" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-applied-busines-PKC1GJ/"
    if course[0: 2] == "RP" and course[-2:] == "L1":
        return "https://mcivietnam.com/course-detail-2/MCI-rpa-uipath-auto-1VONEI/"
    if course[0: 2] == "RP" and course[-2:] == "L2":
        return "https://mcivietnam.com/course-detail-2/MCI-advanced-rpa-ui-1VONEI/"


def sendEmail():
    email_url = "https://appv4.zozo.vn/api/v1/email/send?"
    data = {}
    data['api_token'] = "RAlR9h8EFrSLdEGllv4YUyQwLrQa0e9fj6KwJLp1UQBH9ZqOs0xHjhfa56Nu"
    data['subject'] = "Thông báo lộ trình khóa học tiếp theo"
    data['from_email'] = "cskh@mcivietnam.com"
    data['from_name'] = "MCI_BOT_6"
    data['reply_to'] = "cskh@mcivietnam.com"
    #email test
    data['to'] = "datnx@mcivietnam.com"
    df = getStudentInfo()
    for r in range(df.shape[0] - 1):
        if df.iloc[r]["email"] == df.iloc[r + 1]["email"]:
            if df.iloc[r]["so_ngay_con_lai"] == 3 and df.iloc[r + 1]["start_date"] > date.today():
                # print(df.iloc[r]["email"], df.iloc[r+1]["email"])
                # print(df.iloc[r]["start_date"], df.iloc[r+1]["start_date"])
                # print(df.iloc[r]["end_date"], df.iloc[r+1]["end_date"])
                # print(df.iloc[r]["class_code"], df.iloc[r+1]["class_code"])
                # print(df.iloc[r]["so_ngay_con_lai"], df.iloc[r+1]["so_ngay_con_lai"])
                email = df.iloc[r]["email"]
                name = df.iloc[r]["name"]
                finish_course = df.iloc[r]["class_name"]
                end_date = df.iloc[r]["end_date"]
                #gửi lộ trình khóa học tiếp theo
                syllabus_link = getSyllabus(df.iloc[r+1]["class_code"])
                html = createEmail(name, finish_course, end_date, syllabus_link)
                data['html'] = html
                res = requests.post(email_url, data)
                #email học viên
                # data["to"]    = email

sendEmail()