document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('xml-form');
    const responseContainer = document.getElementById('response-container');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // Get form data
        const drug = document.getElementById('drug').value;
        const disease = document.getElementById('disease').value;
        const type = document.getElementById('type').value;

        // Create an XML request
        const xmlData = `
            <request>
                <drug>${drug}</drug>
                <disease>${disease}</disease>
                <type>${type}</type>
            </request>
        `;

        // Send AJAX request to Flask API
        fetch('http://127.0.0.1:5000/process-xml', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/xml',
            },
            body: xmlData,
        })
        .then(response => response.text())
        .then(data => {
            // Display the XML response
            responseContainer.innerHTML = data;
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
        });
    });
});
