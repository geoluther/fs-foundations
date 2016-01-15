
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_restaurants():
    try:
        restaurants = session.query(Restaurant).all()
        names = [r.name for r in restaurants]
        return names
    except:
        print "error, could not connect to database"


def addRestaurant(rname):
    try:
        restaurant1 = Restaurant(name=rname)
        session.add(restaurant1)
        session.commit()
    except:
        print "error, could not add restaurant"


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # get names for db query function
                names = get_restaurants()
                output = ""
                output += "<html><body>"
                output += "<a href='./new'>Add A Restaurant</a><br>"
                output += "<h2>Where do you want to Eat?</h2>"

                for restaurant in names:
                    output += restaurant + "<br>"
                    output += "<a href='#'>Edit</a><br>"
                    output += "<a href='#'>Delete</a><br>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new'>
                           <h2>Enter A New Restaurant</h2>
                           <input name="newRestaurantName" type="text">
                           <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                teststring = "woo dat?"
                self.wfile.write(teststring)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hola'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):

        try:
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':

                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    addRestaurant(messagecontent[0])

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

        # try:
        #     self.send_response(301)
        #     self.send_header('Content-type', 'text/html')
        #     self.end_headers()
        #     ctype, pdict = cgi.parse_header(
        #         self.headers.getheader('content-type'))
        #     if ctype == 'multipart/form-data':
        #         fields = cgi.parse_multipart(self.rfile, pdict)
        #         messagecontent = fields.get('message')
        #         addRestaurant(messagecontent[0])
        #     output = ""
        #     output += "<html><body>"
        #     output += " <h2>You Added: </h2>"
        #     output += "<h1> %s </h1>" % messagecontent[0]
        #     output += '''<form method='POST' enctype='multipart/form-data' action='/new'>
        #     <h2>Would you like to add another restaurant?</h2><input name="message" type="text" >
        #     <input type="submit" value="Submit"></form>'''
        #     output += "<a href='/restaurants'>Return to Restaurants</a><br>"
        #     output += "</body></html>"
        #     self.wfile.write(output)
        #     print output
        # except:
        #     pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()


