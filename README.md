# DiaCraft - AI UML Diagram Generator

DiaCraft is an AI-powered UML Diagram Generator that leverages OpenAI's GPT model and PlantUML to create various types of UML diagrams effortlessly. The application is designed to simplify the diagram creation process for software developers, engineers, and architects by transforming textual requirements into precise UML diagrams.

---

## Features

- **AI-Driven UML Diagrams:** Generate class, sequence, use case, activity, state, component, deployment, object, ER, and system architecture diagrams.
- **PlantUML Integration:** Convert generated UML syntax into interactive and downloadable diagrams using PlantUML.
- **Customizable Input:** Flexible input options for product requirements and non-programming diagram requirements.
- **Responsive Web Interface:** A user-friendly, dark-mode interface built with Flask, HTML, CSS, and JavaScript.
- **Download & Copy Options:** Users can download diagrams or copy the PlantUML syntax for reuse.

---

## Requirements

### Software and Libraries

- **Backend:**
  - Flask (3.0.3)
  - Flask-CORS (4.0.1)
  - OpenAI (1.35.13)
  - PlantUML (0.3.0)
  - Python 3.9+
  
- **Frontend:**
  - HTML
  - CSS (Dark Mode Styling)
  - JavaScript (Dynamic Interactions and Diagram Generation)

- **Dependencies:**
  - Install the required Python libraries using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

Create a `.env` file in the root directory and include the following environment variables:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Installation and Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/bhagirathsinhp/diacraft-AI-diagram-generator.git
    cd diacraft
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables:**

    Create a `.env` file with your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ```

4. **Run the Application:**

    ```bash
    python app.py
    ```

5. **Access the Application:**

    Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Usage

1. **Input Requirements:**
   - Enter your textual requirements in the provided textarea.
   - Select the input type and diagram type.

2. **Generate Diagram:**
   - Click on the **Generate Diagram** button to create a UML diagram.
   - View the generated diagram and PlantUML syntax.

3. **Download or Copy:**
   - Download the generated diagram as an SVG file.
   - Copy the PlantUML syntax for further customization.

---

## Supported Diagram Types

### Product Requirements (UML)
- Class Diagram
- Sequence Diagram
- Use Case Diagram
- Activity Diagram
- State Diagram
- Component Diagram
- Deployment Diagram
- Object Diagram
- Entity-Relationship Diagram
- System Architecture Diagram

---

## Architecture

- **Frontend:**
  - User interface with interactive form inputs and real-time diagram rendering.
- **Backend:**
  - Flask application handles AI-driven diagram generation and integration with PlantUML.
- **Diagram Generation Workflow:**
  1. User input is processed by OpenAI GPT to generate PlantUML syntax.
  2. The PlantUML server converts the syntax into diagrams.
  3. The diagram is displayed in the UI and made available for download.

---

## Screenshot

[Diacraft](https://github.com/user-attachments/assets/c55047a2-5fcc-47fd-a604-15a3b1c67917)

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your branch.
4. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- **OpenAI:** For powering the AI-driven diagram generation.
- **PlantUML:** For rendering the UML diagrams.
- **Flask Framework:** For building the backend API.

---

Happy Diagramming with DiaCraft!

© 2025 Bhagirathsinh D. Parmar. All rights reserved.

