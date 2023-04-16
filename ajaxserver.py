from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import unquote
import urllib
import sys     # to get command line argument for port
import MolDisplay  # code to parse for data
import io
import molsql

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = ['./index.html', './upload.html',
                './elements.html', './style.css', './script.js']


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.db = molsql.Database(reset=False)
        self.db.create_tables()
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path is "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            fp = open(public_files[0])
            page = fp.read()
            fp.close()
            self.send_header("Content-length", len(page))
            self.end_headers()
            self.wfile.write(bytes(page, "utf-8"))

        elif self.path == '/molecules':
            molecules = self.db.get_molecules()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(molecules).encode())

        elif self.path == '/upload':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            fp = open(public_files[1])
            page = fp.read()
            fp.close()
            self.send_header("Content-length", len(page))
            self.end_headers()
            self.wfile.write(bytes(page, "utf-8"))

        elif self.path.startswith('/molecule/'):
            name = unquote(self.path.split('/')[2])
            name = name.split('(')[0].strip()
            MolDisplay.radius = self.db.radius()
            MolDisplay.element_name = self.db.element_name()
            MolDisplay.header += self.db.radial_gradients()
            molecule = self.db.load_mol(name)
            molecule.sort()
            svg_contents = molecule.svg()
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()
            self.wfile.write(svg_contents.encode('utf-8'))

        elif self.path == '/elements':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            fp = open(public_files[2])
            page = fp.read()
            fp.close()
            self.send_header("Content-length", len(page))
            self.end_headers()
            self.wfile.write(bytes(page, "utf-8"))

        elif self.path == ('/elementslist'):
            elements = self.db.get_elements()
            self.send_response(200)
            self.send_header('Content-type', "application/json")
            self.wfile.write(json.dumps(elements).encode())

        else:
            # if the requested URL is not one of the public_files
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

    def do_POST(self):
        if self.path == "/molecule":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            # Retrieve the molecule name and file from the form data
            fileobj = io.StringIO(parsed_data[' filename'][0])
            file_data = parsed_data[' filename'][0]
            mol_name = parsed_data[' name'][0]
            mol_name = mol_name.split("\n")[2]
            mol_name = mol_name.replace('\r', '')
            
            for i in range(3):
                fileobj.readline()
            # Create a file object from the post data
            # Call the add_molecule function with the file object and molecule name
            self.db.add_molecule(mol_name, fileobj)
            self.send_response(200)  # OK
            self.end_headers()

        elif self.path == "/form_handler.html":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            print(repr(body.decode('utf-8')))

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))

            print(postvars)

            message = "data received"

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(message))
            self.end_headers()

            self.wfile.write(bytes(message, "utf-8"))

        elif self.path == "/addelement":
            # Add element
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            element_number = parsed_data['element_number'][0]
            element_code = parsed_data['element_code'][0]
            element_name = parsed_data['element_name'][0]
            colour1 = parsed_data['colour1'][0]
            colour2 = parsed_data['colour2'][0]
            colour3 = parsed_data['colour3'][0]
            radius = float(parsed_data['radius'][0])

            self.db['Elements'] = (element_number, element_code, element_name, colour1, colour2,colour3, radius)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

    def do_DELETE(self):
        if self.path.startswith('/deleteelement'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            print(parsed_data)
            self.db.delete_element(parsed_data['element_no'][0])
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
httpd.serve_forever()