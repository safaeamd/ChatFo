document.addEventListener('DOMContentLoaded', function() {
    var chatLog = document.getElementById('chat-log');
    var userInput = document.getElementById('user-input');
    var sendButton = document.getElementById('send-button');

    // Ajoutez un événement de clic au bouton d'envoi
    sendButton.addEventListener('click', function() {
        var userQuestion = userInput.value;
        if (userQuestion.trim() !== '') {
            addMessage('Vous', userQuestion);
            getResponse(userQuestion);
            userInput.value = '';
        }
    });

    // Fonction pour ajouter un message au journal de chat
    function addMessage(sender, message) {
        var messageElement = document.createElement('div');
        messageElement.innerHTML = '<strong>' + sender + ':</strong> ' + message;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Fonction pour obtenir une réponse du chatbot
    function getResponse(question) {
        // Envoyer la question au backend (par exemple, via une requête AJAX)
        // Récupérer la réponse du backend et l'ajouter au journal de chat
        // Utiliser l'API OpenAI pour générer la réponse (voir l'exemple précédent)

        // Exemple de requête AJAX pour le backend avec Flask
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/get_response', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                addMessage('Chatbot', response);
            }
        };
        xhr.send(JSON.stringify({ 'question': question }));
    }
});
