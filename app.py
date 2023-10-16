from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import mysql.connector


def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS sd")


# Configure MySQL connection
mysql_connection = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='Psatpsat'
)

# Create a cursor
cursor = mysql_connection.cursor()

# Create the database
create_database(cursor)

# Switch to the 'sd' database
cursor.execute("USE sd")

# Create a table (if needed)
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), father_name VARCHAR(255), mother_name VARCHAR(255), dob DATE, email VARCHAR(255), gender VARCHAR(10), mobile VARCHAR(15), address TEXT, hobbies VARCHAR(255), state_district_pincode VARCHAR(255))")



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            print("Recieved POST request")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            # Extract form fields
            first_name = form_data.get('first-name', [''])[0]
            last_name = form_data.get('last-name', [''])[0]
            father_name = form_data.get('father-name', [''])[0]
            mother_name = form_data.get('mother-name', [''])[0]
            dob = form_data.get('dob', [''])[0]
            email = form_data.get('email', [''])[0]
            gender = form_data.get('gender', [''])[0]
            mobile = form_data.get('mobile', [''])[0]
            address = form_data.get('address', [''])[0]
            hobbies = form_data.get('hobbies', [''])[0]
            state_district_pincode = form_data.get('state-district-pincode', [''])[0]

            # Open a cursor and execute the MySQL query
            cursor = mysql_connection.cursor()
            query = "INSERT INTO users (first_name, last_name, father_name, mother_name, dob, email, gender, mobile, address, hobbies, state_district_pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (first_name, last_name, father_name, mother_name, dob,email, gender, mobile, address, hobbies, state_district_pincode)
            cursor.execute(query, values)

            # Commit the transaction and close the cursor
            mysql_connection.commit()
            cursor.close()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Registration successful!")
        except Exception as e:
            print('Error in POST request:', str(e))
            self.send_error(500, 'Internal Server Error')
    def do_GET(self):
        print('Received GET request for:', self.path)
        try:
            if self.path == '/':
                self.path = '/index.html'
            if self.path.endswith('.html'):
                mimetype = 'text/html'
            elif self.path.endswith('.css'):
                mimetype = 'text/css'
            else:
                raise IOError("File type not supported.")
            # Open and serve the requested file
            with open('.' + self.path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(file.read())
        except IOError:
            print('Error: File Not Found')
            self.send_error(404, 'File Not Found: %s' % self.path)


def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()

