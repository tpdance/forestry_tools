__author__ = 'Nick Erlacker'
# date created: 7/27/17
# last modified: 7/27/17
# abstract: this script checks an SDE feature class for edits and notifies the data owner for approval

# Import arcpy module
import arcpy
import smtplib
import arcinfo
# Local variables:
# example SDE connection: "Database Connections\\SOMEDB.sde\\DB.DBO.Layer"
LAYER = "SOME DB CONNECTION"

# Process: Get Count
result = arcpy.GetCount_management(LAYER)

count = int(result.getOutput(0))

if count > 0:
    sender = 'sender@email.com'
    receivers = ['person1@email.com', 'person2@email.com']
    message = """ From: SENDER@email.com
To: RECEIVER1@email.com, RECEIVER2@email.com
Subject: Features in Redline Stands Layer

There are currently """ +str(count)  + """ features in the Layer that need to be
reviewed. Please do not reply. """

    try:
       smtpObj = smtplib.SMTP('SMTP DOMAIN')
       smtpObj.sendmail(sender, receivers, message)
       print "Successfully sent email"
    except SMTPException:
       print "Error: unable to send email"
    smtpObj.quit()
else:
    print('No Features Present.')
