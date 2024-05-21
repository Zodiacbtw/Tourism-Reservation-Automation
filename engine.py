import pdfplumber
import win32com.client
from mydatabase import *
import re
from datetime import datetime
import json

min_stay = 3


def process():
    imlec.execute("SELECT FilePath FROM RezervasyonTb WHERE IsRead = ?", (False,))
    okunmamis_rez = imlec.fetchall()
    for rez in okunmamis_rez:
        file_path = rez[0]
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                name_pattern = r'(?:Mr|Mrs|Miss|Chd)\s+((?:\b(?:[A-Z]\w*\s*){1,2}))'
                names = re.findall(name_pattern, text)
                names_str = ' '.join(names)
                print(type(names_str))
                print(names_str)

                age_pattern = r'(\d{1,3})\s*(?:MALE|FEMALE)'
                ages = re.findall(age_pattern, text)
                ages_str = ' '.join(ages)

                date_pattern = r'Room .* (\d{2}\.\d{2}\.\d{4}) (\d{2}\.\d{2}\.\d{4})'
                in_out_dates = re.findall(date_pattern, text)
                if in_out_dates:
                    date1 = in_out_dates[0][0]
                    date2 = in_out_dates[0][1]
                else:
                    print("Tarih bilgisi bulunamadı.")
                date_format = "%d.%m.%Y"
                date1_obj = datetime.strptime(date1, date_format)
                date2_obj = datetime.strptime(date2, date_format)
                days = abs((date2_obj - date1_obj).days)

                voucher_pattern = r'Vno (\d+) Booked Date'
                voucher_no = re.findall(voucher_pattern, text)
                voucher_no_str = ' '.join(voucher_no)

                imlec.execute("SELECT SenderMailAddress FROM RezervasyonTb")
                sonuc = imlec.fetchone()
                sender_mail_address = ' '.join(sonuc)

                imlec.execute("INSERT INTO InfoTb (VoucherNo, CheckIn, CheckOut, MailAddress, GuestName, GuestAge)"
                              f" VALUES ('{voucher_no_str}', '{date1}', '{date2}', '{sender_mail_address}',"
                              f"'{names_str}', '{ages_str}')")
                imlec.commit()

                if days >= min_stay:
                    outlook1 = win32com.client.Dispatch('outlook.application')
                    mail = outlook1.CreateItem(0)
                    mail.To = sender_mail_address
                    mail.Subject = 'ZODIAC TEST'
                    mail.Body = (
                        f'{voucher_no_str} voucher numaralı rezervasyonunuzun CONFIRM işlemi gerçekleştirilmiştir. '
                        f'\n KUŞTUR TATİL KÖYÜ')

                    try:
                        mail.Send()
                        print("E-posta başarıyla gönderildi!")
                        imlec.execute("UPDATE RezervasyonTb SET IsRead = ?", (True,))
                        imlec.commit()
                    except Exception as e:
                        print("E-posta gönderilirken bir hata oluştu:", str(e))
                else:
                    outlook1 = win32com.client.Dispatch('outlook.application')
                    mail = outlook1.CreateItem(0)
                    mail.To = sender_mail_address
                    mail.Subject = 'ZODIAC TEST'
                    mail.Body = (f'Üzülerek {voucher_no_str} voucher numaralı rezervasyonunuza minimum '
                                 f'konaklama şartımıza uymadığından dolayı NOT CONFIRM verildiğini '
                                 f'bildiriyoruz. \n KUŞTUR TATİL KÖYÜ')

                    try:
                        mail.Send()
                        print("E-posta başarıyla gönderildi!")
                        imlec.execute("UPDATE RezervasyonTb SET IsRead = ?", (True,))
                        imlec.commit()
                    except Exception as e:
                        print("E-posta gönderilirken bir hata oluştu:", str(e))
    else:
        print("Zaten okundu ve e-posta gönderildi.")
    # return {
    #     "names_str": names_str,
    #     "ages_str": ages_str,
    #     "date1": date1,
    #     "date2": date2,
    #     "days": days,
    #     "voucher_no_str": voucher_no_str,
    #     "sender_mail_address": sender_mail_address
    # }


def job():
    check_new_mails_and_insert_into_db()
    process()
