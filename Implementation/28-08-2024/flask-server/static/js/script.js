document.getElementById('keyExchangeBtn').addEventListener('click', function() {
    fetch('/api/key-exchange', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('keyExchangeResult');
        resultDiv.innerHTML = `
            <strong>Server Public Key:</strong> ${data.client_public_key}<br>
            <strong>Shared Secret (Server):</strong> ${data.shared_secret_server}<br>
            <strong>Shared Secret (Client):</strong> ${data.shared_secret_client}<br>
            <strong>Keys Match:</strong> ${data.keys_match ? 'Yes' : 'No'}
        `;
    });
});

document.getElementById('signMessageBtn').addEventListener('click', function() {
    const message = document.getElementById('messageInput').value;

    fetch('/api/signature', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('signatureResult');
        resultDiv.innerHTML = `
            <strong>Signer Public Key:</strong> ${data.signer_public_key}<br>
            <strong>Signature:</strong> ${data.signature}
        `;
    });
});



// document.getElementById('verifySignatureBtn').addEventListener('click', function() {
//     // Check if the event listener is triggered
//     console.log("Verify button clicked");

//     // Fetch the message from the input field
//     let message = document.getElementById('messageInput').value;

//     // Log the message to see if it's correctly retrieved
//     console.log("Message:", message);

//     // Fetch the signature and public key
//     const signature = document.getElementById('signatureResult').querySelector('strong:nth-child(2)').nextSibling.textContent.trim();
//     const signer_public_key = document.getElementById('signatureResult').querySelector('strong:nth-child(1)').nextSibling.textContent.trim();

//     // Log the signature and public key for debugging
//     console.log("Signature:", signature);
//     console.log("Public Key:", signer_public_key);

//     // Check if the message is being correctly passed
//     if (!message) {
//         console.error("Message is empty!");
//     }

//     // Send the data to the server for verification
//     fetch('/api/verify-signature', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ message, signature, signer_public_key })
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Log the server response for debugging
//         console.log("Server Response:", data);

//         const resultDiv = document.getElementById('verificationResult');
//         resultDiv.innerHTML = `
//             <strong>Valid Signature:</strong> ${data.is_valid ? 'Yes' : 'No'}
//         `;
//     })
//     .catch(error => console.error("Error during fetch:", error));
// });


document.getElementById('verifySignatureBtn').addEventListener('click', function() {
    console.log("Verify button clicked");

    let message = document.getElementById('messageInput').value;
    console.log("Message:", message);

    // Try to find the signatureResult element
    const signatureResultElement = document.getElementById('signatureResult');
    console.log("Signature Result Element:", signatureResultElement);

    if (signatureResultElement) {
        // Check for the strong tags and their content
        const publicKeyElement = signatureResultElement.querySelector('strong:nth-child(1)');
        const signatureElement = signatureResultElement.querySelector('strong:nth-child(1)');

        console.log("Public Key Element:", publicKeyElement);
        console.log("Signature Element:", signatureElement);

        if (publicKeyElement && signatureElement) {
            const signer_public_key = publicKeyElement.nextSibling.textContent.trim();
            const signature = signatureElement.nextSibling.textContent.trim();

            console.log("Signer Public Key:", signer_public_key);
            console.log("Signature:", signature);

            // Proceed with the fetch request
            fetch('/api/verify-signature', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message, signature, signer_public_key })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server Response:", data['is_valid']);

                const resultDiv = document.getElementById('verificationResult');
                resultDiv.innerHTML = `
                    <strong>Valid Signature:</strong> ${data.is_valid ? 'Yes' : 'No'}
                `;
            })
            .catch(error => console.error("Error during fetch:", error));
        } else {
            console.error("Public Key or Signature elements not found or not correctly structured.");
        }
    } else {
        console.error("Signature result element not found.");
    }
});
