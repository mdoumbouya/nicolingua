let chunks = [];
dialog_state = 0
dialog_language = 'none'
dialog_context = {}
contacts = []


function resetDialog(){
    dialog_state = 0;
    dialog_context = {};
}

function handleUnableToFindContact(){
    // play sound: couldn't find contact
}

function respondToDialog(){

}


function handleFinalDialogState(stateId, dialogCtxData){
    // handle ADD_OR_UPDATE_CONTACT
    if(stateId == 6){
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

        resetDialog();
    }

    // handle SEACH_CONTACT unsuccessful
    else if (stateId == 7){
        var contactIndex = contacts.findIndex(function(c){
            return c.contact_name == dialogCtxData.contact_name;
        });
        if (contactIndex == -1){
            handleUnableToFindContact();
            resetDialog();
        }
    }

    // handle CALL_CONTACT
    else if (stateId == 9){
        var contactIndex = contacts.findIndex(function(c){
            return c.contact_name == dialogCtxData.contact_name;
        });
        
        window.open('tel:' + contacts[contactIndex].phone_number);
        resetDialog();
    }

    // handle DELETE_CONTACT
    else if (stateId == 11){
        var contactIndex = contacts.findIndex(function(c){
            return c.contact_name == dialogCtxData.contact_name;
        });
        delete contacts[contactIndex];

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
            dialog_state = response.new_state;
            dialog_language = response.new_language;
            Object.assign(dialog_context, response.dialog_context)

            $("#textFromSpeech").text(
                response['class']['utt']
            );

            $("#resultLoading").hide();
            $("#resultFailure").hide();
            $("#resultSuccess").show();
            
            handleFinalDialogState(dialog_state, dialog_context);
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


startup();
