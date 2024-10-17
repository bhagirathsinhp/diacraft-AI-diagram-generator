import os
import logging
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import OpenAI, ChatOpenAI
from plantuml import PlantUML
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing (CORS)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the LLM
clients = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt templates for UML diagrams with the types
prompts = {
    # Class diagram template
    "class": """ 
    Extract detailed UML class diagrams from the following user requirement document. Include classes, attributes, methods, and relationships between classes. Ensure each class has at least one attribute and one method if applicable. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    skinparam class {{
    direction vertical
    }}
    class User {{
        +name: String
        +email: String
        +login(): void
        +logout(): void
    }}

    class Product {{
        +productName: String
        +price: Float
        +addToCart(): void
    }}

    User --> Product: buys
    @enduml
    """,
    # Sequence diagram template 
    "sequence": """
    Generate a UML sequence diagram from the following user requirement document. Include actors, objects, messages, and interactions. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    actor User
    participant "Login Page" as LP
    participant "Home Page" as HP

    User -> LP: Enters login details
    LP -> User: Validates login details
    LP -> HP: Redirect to Home Page
    HP -> User: Display homepage
    @enduml
    """,
    # Usecase diagram template
    "usecase": """
    Generate a UML use case diagram from the following user requirement document. Include actors and use cases. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    left to right direction
    skinparam packageStyle rectangle
    
    actor User
    actor Admin

    usecase "Login" as UC1
    usecase "Manage Products" as UC2
    usecase "Checkout" as UC3
    
    User --> UC1
    User --> UC3
    Admin --> UC2
    @enduml
    """,
    # Activity diagram template
    "activity": """
    Generate a UML activity diagram from the following user requirement document. Include actions, decisions, and transitions. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    :Start;
    :Login;
    ->yes;
    :Display Home;
    if (Is Admin?) then (yes)
      :Display Admin Panel;
    else (no)
      :Display User Dashboard;
    endif
    @enduml
    """,
    # State diagram template
    "state": """
    Generate a UML state diagram from the following user requirement document. Include states and transitions. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    
    
    [*] --> State1
    State1 --> State2 : Event1
    State2 --> [*]
    @enduml
    """,
    # Component diagram template
    "component": """
    Generate a UML component diagram from the following user requirement document. Include components and interfaces. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    component UserService
    component OrderService
    UserService --> OrderService : "uses"
    @enduml
    """,
    # Deployment diagram template
    "deployment": """
    Generate a UML deployment diagram from the following user requirement document. Include nodes, components, and relationships. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    node "Web Server" {{
      [Application]
    }}
    node "Database Server" {{
      [Database]
    }}
    [Application] --> [Database] : "connects to"
    @enduml
    """,
    # Object diagram template
    "object": """
    Generate a UML object diagram from the following user requirement document. Include objects and relationships. Use PlantUML syntax.

    Document:
    {document}

    Example of the expected output:
    @startuml
    object user1 {{
      name = "John Doe"
      email = "john@example.com"
    }}
    object product1 {{
      productName = "Laptop"
      price = 1000
    }}
    user1 --> product1 : "owns"
    @enduml
    """,
    #E-R diagram template
    "er-diagram": """
    Generate a complex Entity-Relationship (E-R) diagram from the following user requirement document. The E-R diagram should include:

    1. **Entities**: List the entities and their attributes, clearly indicating primary keys (PK), foreign keys (FK), composite attributes, and multivalued attributes.
    2. **Weak Entities**: Include weak entities that rely on other entities for their existence.
    3. **Relationships**: Include one-to-one, one-to-many, many-to-many, ternary, and recursive relationships, indicating the cardinality between entities.
    4. **Cardinality Constraints**: Clearly state the cardinality of each relationship (e.g., one-to-many, zero-to-many, one-to-one).
    5. **Special Constraints**: Include specific constraints like uniqueness, total participation, and partial participation.
    6. **Advanced Attributes**: Include derived attributes, multivalued attributes, and composite attributes.
    7. **Ternary Relationships**: If applicable, include relationships that involve more than two entities.

    Use PlantUML syntax to create the diagram.

    Document:
    {document}

    Example of the expected output:
    @startuml
    ' Entities and attributes
    entity "Student" {{
      +StudentID : int
      Name : string
      DateOfBirth : date
    }}

    entity "PhoneNumber" {{
      +PhoneNumberID : int
      Number : string
    }}

    entity "Dependent" {{
      +DependentID : int
      Name : string
    }}

    entity "Enrollment" {{
      +EnrollmentID : int
      Semester : string
      Year : int
      Grade : string
      *StudentID : int
      *CourseID : int
    }}

    entity "Course" {{
      +CourseID : int
      CourseName : string
    }}

    entity "Department" {{
      +DepartmentID : int
      DepartmentName : string
    }}

    entity "Prerequisite" {{
      +PrerequisiteID : int
      *CourseID : int
      *PrerequisiteCourseID : int
    }}

    entity "Supervision" {{
      +SupervisionID : int
      *SupervisorID : int
      *SuperviseeID : int
    }}

    ' Relationships with Multiplicity
    Student "1" ||--o{{ "0..*" PhoneNumber : "has"
    Student "1" ||--o{{ "0..*" Dependent : "has"
    Student "1" ||--o{{ "0..*" Enrollment : "enrolls in"
    Course "1" ||--o{{ "0..*" Enrollment : "includes"
    Course "1" }}o--|| "1" Department : "belongs to"
    @enduml
    """,
}


# Initialize the chat model with parameters
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0)

@app.route('/generate', methods=['POST'])
def generate_diagram():
  try: 
    # Start time measurement
    start_time = time.time()
    
    # Parse incoming JSON request data
    data = request.json
    input_text = data.get('input')
    diagram_type = data.get('diagram_type')
    
    # Validate that data is provided
    if not input_text or not diagram_type:
      logger.error("Missing required parameters")
      return jsonify({"error": "Missing required parameters"}), 400
      
    # Retrieve corresponding prompt template for the diagram type
    prompt = prompts.get(diagram_type)
    if not prompt:
      logger.error("Unsupported Diagram Type. Please Try Again.")
      return jsonify({"error": "Unsupported Diagram Type. Please Try Again."}), 400
     
    # Run the prompt and user input through the model 
    response = chat_model(
      messages= [
        {"role": "system", "content":"You are a helpful assistant. You are a veteran software engineer."},
        {"role": "user", "content": prompt.format(document=input_text)}
      ]
    )
    
    # Get the response content from the model
    response_text = response.content
    logger.info("Received response from chat model.")
      
    # Extract the PlantUML syntax from the response using markers (@startuml and @enduml)
    start_index = response_text.find("@startuml")
    end_index = response_text.find("@enduml") + len("@enduml")
    if start_index != -1 and end_index != -1:
        plantuml_code = response_text[start_index:end_index]
        logger.info(f"Extracted PlantUML code: {plantuml_code}")

    else:
        logger.error("Failed to generate valid diagram syntax")
        return jsonify({"error": "Failed to generate valid diagram syntax"}), 500
    
    # PlantUML Server Connection
    plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/svg/")

    # Send the PlantUML syntax to the PlantUML server using POST
    plantuml_url = plantuml_server.get_url(plantuml_code)
    logger.info(f"PlantUML URL: {plantuml_url}")
    
    # GET the response from PlantUML
    response = requests.get(plantuml_url)
    
    # Extract Image data and Syntax 
    if response.status_code == 200:
        image_data = response.content.decode('utf-8')
        logger.info(f"Generated image data: {image_data[:20]}...")
        # Log the time taken to generate the diagram
        end_time = time.time()
        time_taken = end_time - start_time
        logger.info(f"Diagram generated in {time_taken:.2f} seconds")
        return jsonify({"diagram": image_data, "plantuml_code": plantuml_code}), 200
    else:
        logger.error("Failed to generate the diagram from PlantUML server")
        return jsonify({"error": "Failed to generate the diagram from PlantUML server"}), 500

  except Exception as e:
    # Log and return any unexpected errors that occur during the process
    logging.error(f"Error occurred: {e}")
    return jsonify({"error": str(e)}), 500
  
# Run Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)