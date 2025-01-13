var sku_copy_open = false;
var edit_menu_open = false;
var dialogs_open = {};
var mouse_x = 0;
var mouse_y = 0;
var rclick_section = -1;
var rclick_entry = -1;
var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

if (windowHeight > windowWidth) {
    var elem = document.createElement("link");
    elem.setAttribute("rel", "stylesheet");
    elem.setAttribute("href", "mobile.css");
    document.head.appendChild(elem);
}


document.addEventListener('keydown', (e) => {
    var key = e.which;
    
    if (key == 27) {                // ESCAPE

        for (d in dialogs_open) {
            if (dialogs_open[d] == true) {
                close_dialog(null, d)
            }
        }
    } else if (key == 13) {         // ENTER

    }
})

function on_enter(key, function_do) {
    if (key == 13) {
        function_do();
    }
}

function next_textbox(next_el) {
    document.querySelector(`${next_el}`).focus();
}

document.onmousemove = (event) => {
    var eventDoc, doc, body;
    event = event || window.event; // IE-ism
    // If pageX/Y aren't available and clientX/Y are,
    // calculate pageX/Y - logic taken from jQuery.
    // (This is to support old IE)
    if (event.pageX == null && event.clientX != null) {
        eventDoc = (event.target && event.target.ownerDocument) || document;
        doc = eventDoc.documentElement;
        body = eventDoc.body;
        event.pageX = event.clientX +
            (doc && doc.scrollLeft || body && body.scrollLeft || 0) -
            (doc && doc.clientLeft || body && body.clientLeft || 0);
        event.pageY = event.clientY +
            (doc && doc.scrollTop  || body && body.scrollTop  || 0) -
            (doc && doc.clientTop  || body && body.clientTop  || 0 );
    }
    mouse_x = event.pageX;
    mouse_y = event.pageY;
}

function open_dialog(targ_class) {
    var inputs = document.querySelectorAll(`.${targ_class} input`);
    for (i in inputs) {
        inputs[i].value = "";
    }

    if (targ_class == "remove-dialog-wrapper") {
        if (rclick_entry == -1) {   // IT IS A SECTION
            document.querySelector(`.remove-dialog-wrapper span.type`).innerHTML = "section";
            document.querySelector(`.remove-dialog-wrapper span.name`).innerHTML = lumber_db[rclick_section]["name"];
        } else {    // IT IS AN ENTRY
            document.querySelector(`.remove-dialog-wrapper .type`).innerHTML = "entry";
            document.querySelector(`.remove-dialog-wrapper span.name`).innerHTML = `${lumber_db[rclick_section]["contents"][rclick_entry]["SKU"]} - ${lumber_db[rclick_section]["contents"][rclick_entry]["DESC"]}`;
        }
        
    } else if (targ_class == "edit-section-dialog-wrapper") {
        document.querySelector(".edit-section-dialog .index-input").value = parseInt(rclick_section);
        document.querySelector(".edit-section-dialog .name-input").value = lumber_db[rclick_section]["name"];
    } else if (targ_class == "edit-entry-dialog-wrapper") {
        document.querySelector(".edit-entry-dialog .index-input").value = parseInt(rclick_entry) ;
        document.querySelector(".edit-entry-dialog .sku-input").value = lumber_db[rclick_section]["contents"][rclick_entry]["SKU"];
        document.querySelector(".edit-entry-dialog .desc-input").value = lumber_db[rclick_section]["contents"][rclick_entry]["DESC"];
        document.querySelector(".edit-entry-dialog .loc-input").value = lumber_db[rclick_section]["contents"][rclick_entry]["LOC"];
    }

    document.querySelector(`.${targ_class}`).style.display = "";
    var autofocus = document.querySelector(`.${targ_class} input[autofocus]`);
    if (autofocus != null) {
        autofocus.focus();
    }
    dialogs_open[`${targ_class}`] = true;
}

function close_dialog(target=null, targ_class) {
    function the_do() {
        document.querySelector(`.${targ_class}`).style.display = "none";
        dialogs_open[`${targ_class}`] = false;
    }
    if (target != null) {
        if (target.classList.contains(`${targ_class}`)) {
            the_do();
        }
    } else {
        the_do();
    }
}

document.querySelector("#imagefile").addEventListener('change', () => {
    document.querySelector("#photoform").submit();
});


// imagebox = $('#imagebox')
//     input = $('#imageinput')[0]
//     if(input.files && input.files[0])
//     {
//         let formData = new FormData();
//         formData.append('image' , input.files[0]);
//         $.ajax({
//             url: "http://localhost:5000/test", // fix this to your liking
//             type:"POST",
//             data: formData,
//             cache: false,
//             processData:false,
//             contentType:false,
//             error: function(data){
//                 console.log("upload error" , data);
//                 console.log(data.getAllResponseHeaders());
//             },
//             success: function(data){
//                 // alert("hello"); // if it's failing on actual server check your server FIREWALL + SET UP CORS
//                 bytestring = data['status']
//                 image = bytestring.split('\'')[1]
//                 imagebox.attr('src' , 'data:image/jpeg;base64,'+image)
//             }
//         });
//     }



// fetch(`/logout?auth_username=${auth_username}&auth_password=${auth_password}&auth_key=${auth_auth_key}&page=${this_page}`)
//   .then(function (response) {
//     return response.json();
//   }).then(function (text) {
    
//     console.log(text)
//     //put stoof here

//     if (text["status"]) {
//       window.location.replace("login")
//       localStorage.removeItem("groceries-auth key")
//     } else {

//     }

//   }).catch((error) => {
//     //console.error("[GET] API down!");
//     console.error(error)
//     notif("[POST] API down!", error);
//   });