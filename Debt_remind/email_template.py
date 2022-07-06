def create_email_debt_remind(name):
    mail_content = f'''
        <h5 style = "color: #4caf50; font-size: 16pt; font-family: 'Times New Roman', serif; background: white;"> Thân gửi anh/chị {name}, </h5>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Anh chị đang còn nợ xxx.xxx.xxx </p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Đề nghị anh chị sớm hoàn thiện nốt học phí. Nếu không MCI rất tiếc sẽ không cấp chứng chỉ cho anh/chị </p>
        <p style="font-size: 13pt; font-family: 'Times New Roman', serif; background: white;"> Cảm ơn anh/chị. Chúc anh/chị có một ngày hạnh phúc và tốt lành! </p>
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
