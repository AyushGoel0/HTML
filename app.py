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
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), father_name VARCHAR(255), mother_name VARCHAR(255), dob DATE, email VARCHAR(255), gender VARCHAR(10), mobile VARCHAR(15), address TEXT, hobbies VARCHAR(255), state_district_pincode VARCHAR(255), password VARCHAR(20))")


class RequestHandler(BaseHTTPRequestHandler):

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor = mysql_connection.cursor()
    
    cursor = mysql_connection.cursor()

    def do_POST(self):
        try:
            if self.path == '/index':
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
                state_district_pincode = form_data.get(
                'state-district-pincode', [''])[0]
                password = form_data.get('password', [''])[0]  # Extract password field
                # Open a cursor and execute the MySQL query
                self.cursor = mysql_connection.cursor()
                query = "INSERT INTO users (first_name, last_name, father_name, mother_name, dob, email, gender, mobile, address, hobbies, state_district_pincode, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (first_name, last_name, father_name, mother_name, dob, email,gender, mobile, address, hobbies, state_district_pincode, password)
                self.cursor.execute(query, values)
                # Commit the transaction and close the cursor
                mysql_connection.commit()
                self.cursor.close()
                # Registration successful, redirect to home page
                self.send_response(302)
                self.send_header('Location', '/home.html')
                self.end_headers()
                self.wfile.write(b"Registration successful!")
            elif self.path == '/login':
                print("Recieved POST request")
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                form_data = urllib.parse.parse_qs(post_data)
                # Extract form fields
                # Inside do_POST for login
                email = form_data.get('email', [''])[0]
                password = form_data.get('password', [''])[0]
                print("Recieved POST request-2")
                # Query to fetch user data based on username
                self.cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
                result = self.cursor.fetchone()

                if result:
                    stored_password = result[0]
                    if password == stored_password:
                        # Login successful, redirect to home page
                        self.send_response(302)
                        self.send_header('Location', '/home.html')
                        self.end_headers()
                        self.wfile.write(b"Login successful!")
                    else:
                        self.send_response(401)
                        self.end_headers()
                        self.wfile.write(b"User not found. Login failed.")
                else:
                    raise IOError("Invalid request.")
            
        except Exception as e:
            print('Error in POST request:', str(e))
            self.send_error(500, 'Internal Server Error')
        finally:
            # Close the cursor
            self.cursor.close()

    def do_GET(self):
        print('Received GET request for:', self.path)
        try:
            if self.path == '/index.html':
                self.path = '/index.html'
            elif self.path == '/login':
                self.path = '/login.html'  # Serve the login page
            elif self.path == '/home.html':  # Added this block to serve home.html
                self.path = '/home.html'
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


# Inside the run_server function
def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    with server_class(server_address, handler_class) as httpd:
        print(f'Starting server on port {port}')
        httpd.serve_forever()



if __name__ == '__main__':
    run_server()

