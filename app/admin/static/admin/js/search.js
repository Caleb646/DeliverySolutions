

let designer_select = document.getElementById("designer");
            let client_select = document.getElementById("client");
            designer_select.onchange = function() {
                designer = designer_select.value;

                fetch("/admin/search/" + designer).then(function(response) {
                   response.json().then(function(data) {

                        let optionHTML = "";

                        for(let client of data.clients) {
                            optionHTML += "<option value=" + client + ">" + client + "</option>";

                        }

                        client_select.innerHTML = optionHTML;

                       });
                });
            }