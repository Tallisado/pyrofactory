# send_mail    
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText


msg = MIMEText(u'\u3053\u3093\u306b\u3061\u306f\u3001\u4e16\u754c\uff01\xe9\n',"plain", "utf-8")
#msg = MIMEText('hello',"plain", "utf-8")
msg['Subject'] = "test"
msg['From'] = 'DVT-AUTOMATION@ADTRAN.COM'
msg['To'] = 'tallis.vanek@adtran.com'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail('DVT-AUTOMATION@ADTRAN.COM', ['tallis.vanek@adtran.com'], msg.as_string())
s.quit()