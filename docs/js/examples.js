// js/examples.js
// Handles loading YAML demos from GitHub and populating the example selector

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/zokrezyl/imery/main/';

// Load initial example
async function loadInitialExample() {
    // Load the first example by default
    const examples = await fetchExampleMetadata();
    if (examples.length > 0) {
        await loadExample(examples[0]);
    } else {
        // Fallback YAML
        editor.setValue(`# No examples available
# Add demos to examples.json
app:
  widget: builtin.text
  data: demo-data

data:
  demo-data:
    metadata:
      label: "Hello from Imery!"
`);
    }
}

// Fetch example metadata from JSON
async function fetchExampleMetadata() {
    try {
        const response = await fetch('examples/examples.json');
        const data = await response.json();
        return data.examples;
    } catch (error) {
        console.error('Error fetching example metadata:', error);
        displayError('Failed to fetch example metadata. See console for details.');
        return [];
    }
}

// Load example YAML from GitHub
async function loadExample(example) {
    try {
        // Fetch app.yaml from GitHub
        const url = `${GITHUB_RAW_BASE}${example.github_path}/${example.entry}`;
        console.log(`Loading example from: ${url}`);

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const yamlContent = await response.text();

        // Set editor content
        editor.setValue(yamlContent);

        // Store the example metadata for running
        window.currentExample = example;

        clearError();
    } catch (error) {
        console.error('Error loading example:', error);
        displayError(`Failed to load example from GitHub: ${error.message}`);
    }
}

// Populate example selector dropdown
async function populateExampleSelector() {
    const examplesList = await fetchExampleMetadata();

    const exampleSelector = document.getElementById('example-selector');
    exampleSelector.innerHTML = '<option value="">-- Select an Example --</option>';

    examplesList.forEach((example, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = example.label;
        if (example.description) {
            option.title = example.description;
        }
        exampleSelector.appendChild(option);
    });

    // Set first example as selected
    if (examplesList.length > 0) {
        exampleSelector.selectedIndex = 1; // Index 0 is "-- Select --"
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Populate selector
    await populateExampleSelector();

    // Load initial example
    await loadInitialExample();

    // Add event listener for example selector changes
    const exampleSelector = document.getElementById('example-selector');
    const examplesList = await fetchExampleMetadata();

    exampleSelector.addEventListener('change', async (event) => {
        const selectedIndex = event.target.value;
        if (selectedIndex !== '') {
            const example = examplesList[parseInt(selectedIndex)];
            await loadExample(example);
        }
    });
});
