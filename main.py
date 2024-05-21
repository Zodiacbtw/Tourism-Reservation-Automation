from engine import job
import schedule
import time

# Mesajı text dosyasına yazdırmak
# Path(target_folder / "EMAIL_BODY.txt").write_text(str(body))


def main():
    # Örneğin, her dakika bir işi zamanlamak için
    schedule.every(5).seconds.do(job)

    """# Her saat başında bir işi zamanlamak için
    schedule.every().hour.do(job)
    
    # Her gün saat 10:30'da bir işi zamanlamak için
    schedule.every().day.at("10:30").do(job)
    
    # Haftanın her Pazartesi günü saat 13:15'te bir işi zamanlamak için
    schedule.every().monday.at("13:15").do(job)"""

    # Zamanlanmış işlerin çalıştırılması
    while True:
        schedule.run_pending()
        time.sleep(1)  # CPU'yu çok yormamak için küçük bir bekleme ekleyebilirsiniz


if __name__ == "__main__":
    main()
