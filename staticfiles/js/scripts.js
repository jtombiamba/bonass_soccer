document.addEventListener('DOMContentLoaded', function() {
    // console.log("in script");
    const form = document.getElementById('randomize_players');
    const dynamicContent = document.getElementById('dynamic-content');

    function renderObject(obj, parentKey = '') {
        let html = '';
        for (const [key, value] of Object.entries(obj)) {
            const fullKey = parentKey ? `${parentKey}.${key}` : key;
            if (typeof value === 'object' && value !== null) {
                html += renderObject(value, fullKey); // Recursively handle nested objects
            } else {
                html += `<p><strong>${fullKey}:</strong> ${value}</p>`;
            }
        }
        return html;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting traditionally

        // Get form data
        const formData = new FormData(form);
        const formAction = form.action; // This retrieves the action attribute
        const secret_code = formData.get('secret_code');
        const csrfToken = formData.get('csrfmiddlewaretoken');

        data = {secret_code: secret_code}

        // Send the data using Fetch API
        fetch(formAction, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken, // Include CSRF token in the headers
                'Content-Type': 'application/json',
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: JSON.stringify(data) // Encode form data
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // Parse the response as HTML
            })
            .then(data => {
                let html = '';

                // Loop through the key-value pairs of the JSON object
                html+= `<p><strong>${data.message}</strong></p>`;
                content = Object.entries(data.content)
                for (const [key, value] of content) {
                    html += `<p><strong>${key}</strong></p>`;
                    for (const player of value) {
                        html += `<li>${player}</li>`;
                    }
                }

                // Insert the generated HTML into the dynamic content area
                dynamicContent.innerHTML = html;

//                dynamicContent.innerHTML = `
//                    <p><strong>${data.message}</strong></p>
//                    <p>${data.content}</p>`;
                    form.reset();
            })
//            .then(html => {
//                // Update the dynamic content area with the response
//                dynamicContent.innerHTML = html;
//                form.reset(); // Clear the form
//            })
            .catch(error => {
                console.error('Error:', error);
                dynamicContent.innerHTML = "<p>An error occurred. Please try again.</p>";
            });
    });

//    document.getElementById('randomize_players').addEventListener('click', function() {
//        var url = event.target.getAttribute('data-url');
//        fetch(url, {
//            method: 'POST',
//            headers: {
//                // 'X-CSRFToken': csrfToken,  // Include the CSRF token
//                'Content-Type': 'application/json',
//            },
//        })
//            .then(response => response.json())
//            .then(data => {
//                document.getElementById('dynamic-content').innerHTML = `
//                    <p><strong>${data.message}</strong></p>
//                    <p>${data.content}</p>`;
//            })
//            .catch(error => console.error('Error:', error));
//    });

});
