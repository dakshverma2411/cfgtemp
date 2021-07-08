import smtplib, ssl

class Email():

    @classmethod
    def send_email(cls,email, link):
        query_email = "team18cfg@gmail.com"
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "team18cfg@gmail.com"
        receiver_email = email
        password = "codeforgood"
        message = f"""\
        Subject: Email Confirmation.


        {link}
        """

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            try:
                server.sendmail(sender_email, receiver_email, message)
                return True
            except:
                return False

Email.send_email("dakshverma.verma@gmail.com", "https://www.google.co.in")
