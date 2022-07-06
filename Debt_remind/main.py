import requests
import email_template
from fake import fake_data

# Đường dẫn email API - Inet
email_url = "https://appv4.zozo.vn/api/v1/email/send?"
data_url = "https://www.mcivietnam.com/nhanvien/unconfirm-register/"

# hàm gửi email


def send_email():
    data = {}
    count = 0
    data['api_token'] = "RAlR9h8EFrSLdEGllv4YUyQwLrQa0e9fj6KwJLp1UQBH9ZqOs0xHjhfa56Nu"
    data['subject'] = "Email nhắc nợ"
    data['from_email'] = "cskh@mcivietnam.com"
    data['from_name'] = "MCI CSKH"
    data['reply_to'] = 'cskh@mcivietnam.com'
    # list_unpaids = get_data()
    list_unpaids = fake_data
    for item in list_unpaids:
        if item["email"] != "":
            count += 1
            name = item["name"]
            data['to'] = item["email"]
            html = email_template.create_email_debt_remind(name)
            data['html'] = html
            print(data)
            # response = requests.post(email_url, data=data)
    print(f"Gửi thành công {count} email nhắc nợ!!!")

# hàm lấy dữ liệu từ api về


def get_data():
    res = requests.get(data_url)
    data = res.json()
    return data


def main():
    send_email()


if __name__ == "__main__":
    main()
