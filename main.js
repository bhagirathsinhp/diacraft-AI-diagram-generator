document.addEventListener("DOMContentLoaded", function () {
  // DOM elements for form interactions and diagram generation
  const inputForm = document.getElementById("diagramForm");
  const diagramTypeSelection = document.getElementById("diagramType");
  const inputTypeRadios = document.querySelectorAll(
    "input[name = 'input-type']"
  );
  const loadingMessage = document.getElementById("loadingMessage");
  const errorMessage = document.getElementById("errorMessage");
  const diagramContainer = document.getElementById("diagramContainer");
  const diagramImage = document.getElementById("diagramImage");
  const plantUMLSyntaxTextarea = document.getElementById("plantUMLSyntax");
  const copySyntaxBtn = document.getElementById("copySyntaxBtn");
  const downloadDiagramBtn = document.getElementById("downloadDiagram");

  // Predefined diagram options for input types
  const similarOptions = [
    { value: "class", label: "Class Diagram" },
    { value: "sequence", label: "Sequence Diagram" },
    { value: "usecase", label: "Use Case Diagram" },
    { value: "activity", label: "Activity Diagram" },
    { value: "state", label: "State Diagram" },
    { value: "component", label: "Component Diagram" },
    { value: "deployment", label: "Deployment Diagram" },
    { value: "object", label: "Object Diagram" },
    { value: "er-diagram", label: "Entity-Relationship Diagram" },
  ];

  // Map input types for selected radios
  const diagramOptions = {
    "product-requirements": similarOptions,
    "non-programming": [
      { value: "flowchart", label: "Flowchart" },
      { value: "business-model", label: "Business Model" },
      { value: "mind-map", label: "Mind Map" },
      { value: "org-chart", label: "Organizational Chart" },
      { value: "er-diagram", label: "Entity-Relationship Diagram" },
      { value: "gantt-chart", label: "Gantt Chart" },
      { value: "pert-chart", label: "PERT Chart" },
    ],
  };

  // Dynamic population of diagram types
  function populateDiagramOptions(inputType) {
    const options = diagramOptions[inputType] || []; // Get options for selected input types
    diagramTypeSelection.innerHTML = "";

    // Add diagram type to the dropdown
    options.forEach((option) => {
      const opt = document.createElement("option");
      opt.value = option.value;
      opt.textContent = option.label;
      diagramTypeSelection.appendChild(opt);
    });
  }

  // Listen for changes in input types and update diagrams
  inputTypeRadios.forEach((radio) => {
    radio.addEventListener("change", function () {
      populateDiagramOptions(this.value); // Populate diagrams acc. to the selected input type
    });
  });

  // Set initial diagram type based on default input type
  populateDiagramOptions(
    document.querySelector('input[name="input-type"]:checked').value
  );

  // Handle form submission to generate diagram
  inputForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    const inputText = document.getElementById("inputText").value.trim(); // Get and trim user input
    const diagramType = diagramTypeSelection.value; // Get selected diagram type

    // Empty input text validation and error handling
    if (!inputText) {
      errorMessage.innerText = "Please fill the Input.";
      errorMessage.style.display = "block";
      return;
    }

    // Hide error messages & show loading message
    errorMessage.style.display = "none";
    loadingMessage.style.display = "block";
    diagramContainer.style.display = "none"; // Hide diagram section until diagram generated

    // Send diagram generation request
    try {
      const response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Send data as JSON
        },
        body: JSON.stringify({
          // Send input and diagram type as payload
          input: inputText,
          diagram_type: diagramType,
        }),
      });

      const data = await response.json(); // Parse JSON response

      // Check for error returned by the back-end server
      if (data.error) {
        errorMessage.innerText = data.error;
        errorMessage.style.display = "block";
        loadingMessage.style.display = "none";
        return;
      }

      // Display generated diagram is successfully received
      diagramImage.src = "data:image/svg+xml;base64," + btoa(data.diagram);

      // Display received Generated PlantUML syntax
      plantUMLSyntaxTextarea.value = data.plantuml_code || "";

      // Hide loading message and show diagram
      loadingMessage.style.display = "none";
      diagramContainer.style.display = "block";

      // Smooth scroll to the diagram
      diagramContainer.scrollIntoView({ behavior: "smooth" });

      // Allow user to copy PlantUML syntax to clipboard
      copySyntaxBtn.addEventListener("click", () => {
        navigator.clipboard
          .writeText(plantUMLSyntaxTextarea.value)
          .then(() => alert("UML Code copied to clipboard!"))
          .catch((err) => alert("Failed to copy code: " + err)); // Handle clipboard error
      });
    } catch (error) {
      // Error message for failure in Diagram generation
      errorMessage.innerText =
        "An Error has occurred while generating the Diagram.";
      errorMessage.style.display = "block";
      loadingMessage.style.display = "none"; // Hide loading message
    }
  });

  // Handle download of generated diagram as SVG file
  downloadDiagramBtn.addEventListener("click", () => {
    const link = document.createElement("a"); // Create temp download link
    link.href = diagramImage.src;
    link.download = "diagram.svg"; // Default filename for downloaded file
    link.click();
  });
});
