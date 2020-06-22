let form = document.getElementById("add-inv");
let table = document.getElementById("data_table");
let tableBody = document.getElementById("data-body");
let designer_select = document.getElementById("designer");
let client_select = document.getElementById("client");
let row_id = 1;
let btn_key = 10;

designer_select.onchange = function() {
    designer = designer_select.value;

    fetch("/super_employee/add-inv/" + designer).then(function(response) {
       response.json().then(function(data) {

            let optionHTML = "";

            for(let client of data.clients) {
                optionHTML += "<option value=" + client + ">" + client + "</option>";

            }

            client_select.innerHTML = optionHTML;

           });
    });
}
function add_row(){

    let row = document.createElement("tr");
    row.setAttribute('id', row_id);
    let btn_id = row_id + btn_key;

    var fields = new Array(
        "<td><button id="+btn_id+" onclick=remove_row(this.id)>Remove row</button></td>",
        "<td><input type='Text' name='volume'></td>",
        "<td><input type='Text' name='description'></td>",
        "<td><input type='Text' name='location'></td>",
        "<td><input type='Text' name='image_number'></td>",
        )


    row_id = row_id + 1;
    row.innerHTML = fields.join("");
    tableBody.appendChild(table.appendChild(row));

    document.getElementById(btn_id).addEventListener("click", function(event){
        event.preventDefault();
        remove_row(btn_id);
        });


}

document.getElementById("add-btn").addEventListener("click", function(event){
event.preventDefault();
add_row();

});

function remove_row(b_id){
    let therow_id = b_id - btn_key;
    let delElement = document.getElementById(therow_id);
    delElement.parentNode.removeChild(delElement);
}

form.onsubmit = function submitted() {
    //pulls
    let allData = new Array;
    let rowData = new Array;
    let designer_select = document.getElementById("designer").value;
    let client_select = document.getElementById("client").value;
    let designerArray = [designer_select, client_select];
    allData.push(designerArray);

    let rowCount = tableBody.rows.length;

    for(i=0; i < rowCount; i++) {

        let cellBody = tableBody.rows[i].cells;
        let cellLength = cellBody.length;

        let rowData = new Array;

        for(j=0; j < cellLength; j++ ) {

            let data = cellBody[j].children[0].value;

            rowData.push(data);

            if(j+1 >= cellLength) {                           
                allData.push(rowData);
            }

        }

        if(i+1 >= rowCount) {
            //added return false so browser would redirect.
            let dataJson = JSON.stringify(allData);
            window.location.href = "https://calebthomas.herokuapp.com/super_employee/add-inv/success?data="+dataJson;
            return false;
        }

    }
}