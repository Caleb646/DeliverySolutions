let designer_select = document.getElementById("designer");
let client_select = document.getElementById("client");
            
            designer_select.onchange = function() {
                let designer = designer_select.value;
                fetch("/super_employee/add-inv/" + designer).then(function(response) {
                   response.json().then(function(data) {

                        let optionHTML = "";

                        for(let client of data.clients) {
                            console.log(typeof(client));
                            optionHTML += "<option value="+client+">"+client+"</option>";

                        }

                        client_select.innerHTML = optionHTML;

                       });
                });
            }