// config axios to send CSRFToken to server in X-CSRFToken header 
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';
let dialog_assign_window = null;

// service1: increment counter user by agen
function incrementCounter(button) {
    const postData = {
        agent_id: button.getAttribute('data-agent-id'),
        number_window: button.getAttribute('data-window-num')
    }
    
    const refOffice = button.getAttribute('data-office-id');
    const url = `/tcn/api/offices/${refOffice}/increment-counter/`;
    axios.post(url , postData)
        .then(function (response) {
            // Handle success, update UI with new counter value
            document.getElementById('counter-display-agent').innerText = response.data.counter;
        })
        .catch(function (error) {
            // Handle error
            console.error('Error incrementing counter:', error);
        });
}
// service2 : assign  agent to window 

function assignAgentToWindow(button) {
    const postData = {
        agent_id: button.getAttribute('data-agent-id'),
        office_id: button.getAttribute('data-office-id'),
    }
    const idSelect = `windowSelect${postData.agent_id}`
    const selectedWindow = document.getElementById(idSelect).value ;
    const idResponseAssignWindow =  `response_assign_window${postData.agent_id}`
    dialog_assign_window =  document.getElementById(idResponseAssignWindow)
    if (selectedWindow === "Select a window") {
        alert("Please select a window");
        return;
    }
    const url = `/tcn/api/windows/${selectedWindow}/assign-agent/`;

    //initit 
    dialog_assign_window.innerText = "";
    axios.post(url , postData)
        .then(function (response) {
            dialog_assign_window.classList.add("text-success");
            dialog_assign_window.innerText = response.data.message
        })
        .catch(function (error) {
            dialog_assign_window.classList.add("text-danger");
            dialog_assign_window.innerText = error.response.data.error
            console.error('Error assignAgentToWindow:', error);
        });
}
//helper function to clear the response server in <p> tag 
function clearOldData(){
    if (dialog_assign_window) {
        dialog_assign_window.innerText = "";
    }
}
