from flask import Flask, request
import pyodbc
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Database connection setup
server = 'DESKTOP-FFQ7VJV\YASMEEN'
database = 'InteractionsDB'

# Construct the connection string with integrated security
connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Define a function to establish a database connection
def get_database_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        # Handle database connection error
        raise e

# Define a function to execute a database query and return results
def execute_database_query(query, params=None):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

@app.route('/')
def home():
    return "Welcome to the XML Request Form"

@app.route('/process-xml', methods=['POST'])
def process_xml():
    try:
        xml_data = request.data
        
        # Print or log the received XML data (for debugging)
        print("Received XML Data:")
        print(xml_data)
        
        root = ET.fromstring(xml_data)

        # Extract data from the XML request
        drug_code = root.find('drug').text
        disease_code = root.find('disease').text
        type_value = int(root.find('type').text)

        # Query the database
        query = """
            SELECT id, description
            FROM Interactions
            WHERE drugCode = ? AND diseaseCode = ? AND [type] = ?
        """
        params = (drug_code, disease_code, type_value)
        results = execute_database_query(query, params)

        response = ET.Element("responses")
        for result in results:
            interaction = ET.SubElement(response, "response")
            id_element = ET.SubElement(interaction, "id")
            id_element.text = str(result.id)
            description_element = ET.SubElement(interaction, "description")
            description_element.text = result.description

        response_xml = ET.tostring(response, encoding="utf-8").decode()

        return response_xml, 200, {'Content-Type': 'application/xml'}
    except ET.ParseError as e:
        return str(e), 400  # Bad Request for invalid XML
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
