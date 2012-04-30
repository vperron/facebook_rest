#fql.query
query=SELECT name FROM user WHERE (uid IN (SELECT uid2 FROM friend WHERE uid1=GIVENUID));
#fql.query
query=SELECT name,cell,contact_email FROM user WHERE (uid IN (SELECT uid2 FROM friend WHERE uid1=GIVENUID));
#fql.query
query=SELECT name,pic_big FROM user WHERE (uid IN (SELECT uid2 FROM friend WHERE uid1=GIVENUID));
#mailbox.send
body=This is a message body. \nAnd now on a newline.
subject=3 times same message for you...
to=GIVENUID,GIVENUID,GIVENUID
