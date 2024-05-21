from mydatabase import imlec

imlec.execute("UPDATE RezervasyonTb SET IsRead = 0")
imlec.commit()
imlec.close()