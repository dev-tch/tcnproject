let wsScheme = window.location.protocol === 'http:' ? 'ws' : 'ws';
let wsPath = `${wsScheme}://${window.location.host}/ws/counter/`;
let websocket = new WebSocket(wsPath);

websocket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    updateCounterUI(data.counter);
};

function updateCounterUI(counter) {
    console.log(counter)
    // Update the UI with the latest counter value
    document.getElementById('counter-display1').innerText = counter;
}

websocket.onopen = function(event) {
    console.log('WebSocket connection established.');
};

websocket.onerror = function(event) {
    console.error('WebSocket error:', event);
};