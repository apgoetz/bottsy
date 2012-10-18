DIR=/u/$(USER)/public_html/
SERVER=web.cecs.pdx.edu
FILES=bottsy.py .htaccess linuxwords
all:
	scp $(FILES) $(SERVER):$(DIR)

