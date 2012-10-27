DIR=/u/$(USER)/
SERVER=rita.cat.pdx.edu
FILES=bottsy.py .htaccess linuxwords bottsydb dbclient.py render.py 
all:
	scp $(FILES) $(SERVER):$(DIR)

