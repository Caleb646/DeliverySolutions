let sort_field = document.getElementById("sort_methods");
let client_field = document.getElementById("clients");
let clients = document.getElementById("client-list").innerText.match(/\b[A-Za-z]+\b/g);
let description_field = document.getElementById("description");

let specific_client_description = "This method will sum all the storage fees for this client sorted by due date."
let all_client_description = "This method will sum all the storage fees for all your clients and will be sorted by client/due date."
let all_individual_description = "This method will sum the storage fees for each item."

window.onload = function () {

    let sort_val = sort_field.value;

    switch(sort_val) {

        case "specific_client_sum": { 
            let optionHTML = "";

            for(let client of clients) {

                optionHTML += "<option value=" + client + ">" + client + "</option>";
            }
            client_field.innerHTML = optionHTML;
            description_field.innerText = specific_client_description;
            break;
        }

        case "all_clients_sum": { 
            let optionHTML = "<option value='EMPTY'>EMPTY</option>";
            client_field.innerHTML = optionHTML;
            description_field.innerText = all_client_description;
            break;
        }

        case "individual_items": { 
            let optionHTML = "<option value='EMPTY'>EMPTY</option>";
            client_field.innerHTML = optionHTML;
            description_field.innerText = all_individual_description;
            break;
        }
    }
}


sort_field.onchange = function () {

    let sort_val = sort_field.value;

    switch(sort_val) {

        case "specific_client_sum": { 
            let optionHTML = "";
            client_field.style.display = "initial";
            for(let client of clients) {

                optionHTML += "<option value=" + client + ">" + client + "</option>";
            }
            client_field.innerHTML = optionHTML;
            description_field.innerText = specific_client_description;
            break;
        }

        case "all_clients_sum": { 
            client_field.style.display = "none";
            description_field.innerText = all_client_description;
            break;
        }

        case "individual_items": { 
            client_field.style.display = "none";
            description_field.innerText = all_individual_description;
            break;
        }
    }
}