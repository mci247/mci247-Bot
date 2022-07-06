import requests
import pandas as pd
from pretty_html_table import build_table

# Đường dẫn email API - Inet
email_url = "https://appv4.zozo.vn/api/v1/email/send?"
data_url = "https://www.mcivietnam.com/apis/v1/unconfirm-register/"

# template email


def create_email(table):
    mail_content = f'''
        <h5 style = "color: #4caf50; font-size: 16pt; font-family: 'Times New Roman', serif; background: white;"> Kính gửi bộ phận kế toán FSAP, </h5>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Đây là email test tự động, vui lòng không reply!</p>
        {table}
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Đây là danh sách những người chưa được Phòng FSAP xác nhận. Kính đề nghị Phòng xác nhận để Phòng OCS thực hiện việc sắp xếp lớp. </p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Công việc này sẽ được thực hiện vào 9h sáng hàng ngày. </p>
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

# hàm gửi email


def send_email():
    data = {}
    receive_address = ["accounting@mcivietnam.com", "tieplv@mcivietnam.com"]
    data['api_token'] = "RAlR9h8EFrSLdEGllv4YUyQwLrQa0e9fj6KwJLp1UQBH9ZqOs0xHjhfa56Nu"
    data['subject'] = "Tổng hợp đơn đăng ký học chưa được FSAP xác nhận"
    data['from_email'] = "info@mcivietnam.com"
    data['from_name'] = "MCI_BOT_4"
    data['reply_to'] = 'info@mcivietnam.com'
    table = get_data()
    html = create_email(table)
    data['html'] = html

    for item in receive_address:
        data['to'] = item
        response = requests.post(email_url, data=data)


def get_data():
    res = requests.get(data_url)
    data = res.json()
    df = pd.DataFrame(data)
    df['STT'] = range(1, len(df) + 1)
    table = df[['STT', 'created', 'name', 'mobile', 'email']]
    output = build_table(table, "green_light", font_size='small',
                         width='auto', font_family='Open Sans, sans-serif')
    return output


def main():
    send_email()


if __name__ == "__main__":
    main()
