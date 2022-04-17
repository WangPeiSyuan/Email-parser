# Email-parser
Email parser for forwarding email in tyrc.<br>
Working log https://hackmd.io/2zRjsuVFTbeV4VuPvnbZYw#1223

### mbox_parser.py
Main program of process 'soc' mailbox.

### utlis.py
Function of parsing email context.

### sender.py
Function of send mail and line.

### connectDB.py
Connect to DB.

### preprocess.py
Preprocess raw data of school net, and insert to DB.

### checkDB.py
List new data in ewa/soc tables within 2 weeks. 

### checkMbox.py
List ewa/soc mail in current mailbox.

### checkCompare.py
Compare if mailbox's mails are in DB.

### resend.py
Resend mail by soc_id/ewa_id.

### verify.py
Check if email was send and forwarding to 'verify'.
 
### test/ 
Test for if mail/line function work.
