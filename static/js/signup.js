document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("form").addEventListener("submit", function(event) {
        event.preventDefault();
        let username = document.querySelector("#username").value;
        let password = document.querySelector("#password").value;
        if (username && password) {
            this.submit();
        } else {
            alert("Please fill out all fields");
        }
    });
});
