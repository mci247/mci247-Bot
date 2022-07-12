import requests
import pandas as pd
from datetime import date, datetime

email_url = "https://appv4.zozo.vn/api/v1/email/send?"
api_url = "http://127.0.0.1:8000/apis/v1/get-customers/"


def create_email(name, voucher):
    mail_content = f'''
        <h5 style = "color: #4caf50; font-size: 16pt; font-family: 'Times New Roman', serif; background: white;"> Kính gửi anh/chị {name} </h5>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> MCI xin gửi đến anh chị voucher trị giá {voucher} VND áp dụng cho khóa học tiếp theo </p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Voucher có giá trị trong 15 ngày kể từ ngày email này được gửi. Nếu anh chị có nhu cầu vui lòng liên hệ... </p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;">Xin cảm ơn!</p>
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


def get_data():
    res = requests.get(api_url)
    data = res.json()
    df = pd.DataFrame(data)
    df['delta_date'] = df.apply(
        lambda row: change_row(row['payment_date']), axis=1)
    df['voucher'] = df.apply(
        lambda row: get_voucher(row['payment_amount']), axis=1)
    df = df.loc[((df["delta_date"] == 5) | (df["delta_date"] == 10)
                 | (df["delta_date"] == 15)) & (df["voucher"] > 0)]
    return df


def change_row(row):
    cv = datetime.strptime(row, '%Y-%m-%d')
    delta = (date.today() - cv.date()).days
    return delta


def get_voucher(amount):
    voucher = 0
    if amount == 5e6:
        voucher = 500000
    if amount > 5e6 and amount <= 1e7:
        voucher = 1000000
    if amount > 1e7 and amount <= 3e7:
        voucher = 1500000
    if amount > 3e7:
        voucher = 3000000
    return voucher


def send_email():
    df = get_data()
    data = {}
    data['api_token'] = "RAlR9h8EFrSLdEGllv4YUyQwLrQa0e9fj6KwJLp1UQBH9ZqOs0xHjhfa56Nu"
    data['subject'] = "Voucher giảm giá khóa học"
    data['from_email'] = "cskh@mcivietnam.com"
    data['from_name'] = "MCI_BOT_5"
    data['reply_to'] = 'cskh@mcivietnam.com'
    data['to'] = "datnx@mcivietnam.com"

    for r in range(df.shape[0]):
        name = df.iloc[r]["customer_name"]
        email = df.iloc[r]["customer_email"]
        voucher = df.iloc[r]["voucher"]
        voucher_format = "{:,}".format(voucher)
        html = create_email(name, voucher_format)
        data['html'] = html
        # data['to'] = email
        response = requests.post(email_url, data=data)


print(get_data())
# print(df.loc[(df.voucher > 0) & ((df.delta_date == 5) |
#       (df.delta_date == 10) | (df.delta_date == 15))])
