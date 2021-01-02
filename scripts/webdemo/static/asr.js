let chunks = [];
previous_dialog_state = 0
dialog_state = 0
dialog_language = 'none'

class DialogContext {
    get phone_number(){
        return `${this.phone_number_digit_1}${this.phone_number_digit_2}${this.phone_number_digit_3}${this.phone_number_digit_4}${this.phone_number_digit_5}${this.phone_number_digit_6}${this.phone_number_digit_7}${this.phone_number_digit_8}${this.phone_number_digit_9}`;
    }
}

dialog_context = new DialogContext()

function load_contacts(){
    var c_str = localStorage.getItem("contacts");
    if (c_str == null) {
        return [];
    }
    else{
        return JSON.parse(c_str);
    }
}

function save_contacts(contacts){
    var c_str = JSON.stringify(contacts)
    localStorage.setItem("contacts", c_str);
}


var contact_template = `{{#contacts}}
    <div class='col-12'>
        <div class='row d-flex align-items-center justify-content-center contact'>
            <div class='col-3'>
            <img src='/static/bootstrap-icons-1.2.2/person-square.svg' class='align-middle'>
            </div>
            <div class='col-9'>
            <div style='height:8vh' class='align-middle'>
                <h5>{{contact_name}}</h5>
                <h5>{{phone_number}}</h5>
            </div>
            </div>
        </div>
    </div>
{{/contacts}}`

function render_contacts() {
    var rendered = Mustache.render(contact_template, {contacts: load_contacts()});
    document.getElementById('contactList').innerHTML = rendered;
}


response_speech_keys = {
    "0__1":"wake_yes",

    "1__2":"request_contact_name",
    "1__3":"request_contact_name",

    "2__4":"request_contact_phone",

    "3__7":"request_found_contact_action",
    
    "4__0":"contact_already_exists",

    "4__51":"request_another_digit",
    "51__52":"request_another_digit",
    "52__53":"request_another_digit",
    "53__54":"request_another_digit",
    "54__55":"request_another_digit",
    "55__56":"request_another_digit",
    "56__57":"request_another_digit",
    "57__58":"request_another_digit",
    "58__59":"confirm_add_update",

    "59__0":"canceled_adding_contact",
    "6__0":"added_contact",

    "7__0":"contact_not_found",
    "7__2":"request_contact_new_name",
    "7__8":"confirm_call_contact",
    "7__10":"confirm_delete_contact",
    
    "8__0":"canceled_calling_contact",
    "9__0":"calling_contact",

    "10__0":"canceled_deleting_contact",
    "11__0":"deleted_contact",
}

function resetDialog(){
    previous_dialog_state = dialog_state;
    dialog_state = 0;
    dialog_context = new DialogContext();
    render_contacts();
}


function speakBack(previous_dialog_state, dialog_state) {
    var transition_key = previous_dialog_state + "__" + dialog_state;
    if (transition_key in response_speech_keys){
        var speech_key = response_speech_keys[transition_key];
        var a = new Audio("/static/agent_speech/" + dialog_language + "/" + speech_key + ".mp3");
        a.play();
    }
}

function handleFinalDialogState(stateId, dialogCtxData){
    // handle ADD_OR_UPDATE_CONTACT
    if(stateId == 6){
        var contacts = load_contacts();

        if(dialogCtxData.updating_contact){    
            var contactIndex = contacts.findIndex(function(c){
                return c.contact_name == dialogCtxData.contact_name;
            });
            
            contacts[contactIndex].contact_name = dialogCtxData.contact_new_name;
            contacts[contactIndex].phone_number = dialogCtxData.phone_number;
        }else{
            contacts.push(
                {
                    contact_name: dialogCtxData.contact_new_name, 
                    phone_number: dialogCtxData.phone_number
                }
            );
        }

        save_contacts(contacts);
        resetDialog();
    }

    // handle existing contact name
    else if(stateId == 4){
        if(dialogCtxData.updating_contact === undefined){
            var contacts = load_contacts();
            var contactIndex = contacts.findIndex(function(c){
                return c.contact_name == dialogCtxData.contact_new_name;
            });
            
            if (contactIndex != -1){
                // contact name already exist
                resetDialog();
            }
        }

    }

    // handle SEACH_CONTACT unsuccessful
    else if (stateId == 7){
        var contacts = load_contacts();
        var contactIndex = contacts.findIndex(function(c){
            return c.contact_name == dialogCtxData.contact_name;
        });
        if (contactIndex == -1){
            resetDialog();
        }
    }

    // handle CALL_CONTACT
    else if (stateId == 9){
        var contacts = load_contacts();
        var contactIndex = contacts.findIndex(function(c){
            return c.contact_name == dialogCtxData.contact_name;
        });
        
        window.open('tel:' + contacts[contactIndex].phone_number);
        resetDialog();
    }

    // handle DELETE_CONTACT
    else if (stateId == 11){
        var contacts = load_contacts();
        var contactIndex = contacts.findIndex(function(c){
            return c.contact_name == dialogCtxData.contact_name;
        });
        // delete contacts[contactIndex];
        contacts.splice(contactIndex, 1)

        save_contacts(contacts);
        resetDialog();
    }
}


function stoppedRecording(e){
    console.log("stopped recording");
    
    // const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
    const blob = new Blob(chunks, { 'type' : chunks[0].type });
    chunks = [];

    // const audioURL = window.URL.createObjectURL(blob);
    var formdata = new FormData();
    formdata.append('audiodata', blob);
    formdata.append('current_state', dialog_state)
    formdata.append('current_language', dialog_language)

    $("#resultLoading").show();
    $("#resultFailure").hide();
    $("#resultSuccess").hide();

    $.ajax({
        url : "/asr",
        type: "POST",
        data: formdata,
        contentType: false,
        processData: false,

        success: function(response) {
            response = JSON.parse(response);
            console.log(response);

            // dialog state transition, as computed by dialog manager
            previous_dialog_state = dialog_state
            dialog_state = response.new_state;
            dialog_language = response.new_language;
            Object.assign(dialog_context, response.dialog_context)

            $("#textFromSpeech").text(
                response['class']['utt']
            );

            $("#resultLoading").hide();
            $("#resultFailure").hide();
            $("#resultSuccess").show();
            setTimeout(() => {
                $("#resultSuccess").hide();
            }, 1500);
            
            
            handleFinalDialogState(dialog_state, dialog_context);
            speakBack(previous_dialog_state, dialog_state);
        },

        error: function() {
            $("#resultLoading").hide();
            $("#resultFailure").show();
            $("#resultSuccess").hide();
            console.log("Ajax error");
        }
    });
}

function recordingDataAvailable(e) {
    chunks.push(e.data);
}


function onMediaeviceSuccess(stream){
    const mediaRecorder = new MediaRecorder(stream);

    function handleStartTalking(evt){
        console.log("handleStartTalking.");
        var el = document.getElementById("btnParler");
        el.classList.remove("btn-success");
        el.classList.add("btn-danger");
    
        mediaRecorder.start();
        console.log(mediaRecorder.state);
        console.log("recorder started");

        // evt.preventDefault();
        
    }
    
    function handleEndTalking(evt){
        console.log("handleEndTalking.");
        var el = document.getElementById("btnParler");
        el.classList.remove("btn-danger");
        el.classList.add("btn-success");

        mediaRecorder.stop();
        console.log(mediaRecorder.state);
        console.log("recorder stopped");

        // evt.preventDefault();
    }


    var el = document.getElementById("btnParler");

    if('ontouchstart' in window){
        el.addEventListener("touchstart", handleStartTalking, false);
        
    
        el.addEventListener("touchend", handleEndTalking, false);
        el.addEventListener("touchcancel", handleEndTalking, false);
        el.addEventListener("touchmove", handleEndTalking, false);
        
    }
    else
    {
        el.addEventListener("mousedown", handleStartTalking, false);
        el.addEventListener("mouseup", handleEndTalking, false);
    }
    

    mediaRecorder.onstop = stoppedRecording;
    mediaRecorder.ondataavailable = recordingDataAvailable;
}


function startup() {
    $("#resultLoading").hide();
    $("#resultFailure").hide();
    $("#resultSuccess").show();
    render_contacts();

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        console.log('getUserMedia supported.');
        navigator.mediaDevices.getUserMedia (
           // constraints - only audio needed for this app
           {
              audio: true
           })
     
           // Success callback
           .then(function(stream) {
                onMediaeviceSuccess(stream);
           })
     
           // Error callback
           .catch(function(err) {
              console.log('The following getUserMedia error occurred: ' + err);
           }
        );
     } else {
        console.log('getUserMedia not supported on your browser!');
     }

}

/*
$("body").on("contextmenu",function(e){
    return false;
});*/
startup();
