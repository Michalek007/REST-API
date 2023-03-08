
function get_note(){
    const input = document.getElementById("search").value;
    const request = fetch("http://127.0.0.1:5000/notes/" + input)
        .then((response) => response.json())
        .then((json) => {
            try {
            console.log(json["note"]["note"]);
            document.getElementById("note").innerText = json["note"]["note"];
            }
            catch (TypeError){
              document.getElementById("note").innerText = json["message"];
            }
        });
    console.log(request);
}

function add_note(){
    const input = document.getElementById("add").value;
    let data = new FormData();
    data.append("note", input);
    const request = fetch("http://127.0.0.1:5000/add_note/?note=" + input, {method: "POST", body: data})
        .then((response) => response.json())
        .then((json) => {
            console.log(json["message"]);
        });
    console.log(request);
}

function delete_note(){
    const input = document.getElementById("delete").value;
    const request = fetch("http://127.0.0.1:5000/delete_note/" + input, {method: "DELETE"})
        .then((response) => response.json())
        .then((json) => {
            console.log(json["message"]);
        });
    console.log(request);
}

function update_note(){
    const id = document.getElementById("update_id").value;
    const note = document.getElementById("update_note").value;
    const request = fetch("http://127.0.0.1:5000/update_note/" + id + "/?note=" + note, {method: "PUT"})
        .then((response) => response.json())
        .then((json) => {
            console.log(json["message"]);
        });
    console.log(request);
}

function save_note(){
    const text_area = document.getElementById("note2");
    const text = text_area.value;
    const rect = text_area.getBoundingClientRect();
    const height = text_area.offsetHeight;
    const width = text_area.offsetWidth;
    console.log(rect.top, rect.right, rect.bottom, rect.left);
    console.log(text);
    console.log(height, width);
    console.log(rect.bottom-rect.top, rect.right-rect.left);
}

function display_note(){
    const text_area = document.getElementById("note2");
    const text = text_area.value;
    const rect = text_area.getBoundingClientRect();
    const height = text_area.offsetHeight;
    const width = text_area.offsetWidth;
    const new_element = document.createElement("textarea");
    new_element.style.width = "400px";
    new_element.style.height = "400px";
    // new_element.style.top = "50%";
    // new_element.style.bottom = "50%";
    document.getElementById("test").appendChild(new_element);
}
