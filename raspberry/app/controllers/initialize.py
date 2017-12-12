from ConnectionWithDataBase import ConnectionWithDataBase

def InitializeConnection(securityKey):
	dataBaseDirectory = 'mysql+pymysql://root:utfpr8@localhost/picadel'
	raspberryName = "E003"

	connectionBD = ConnectionWithDataBase(raspberryName, dataBaseDirectory)
	
	conectionBD.AllowEntry(securityKey)
