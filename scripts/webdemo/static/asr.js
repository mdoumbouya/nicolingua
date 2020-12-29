let chunks = [];


function stoppedRecording(e){
    console.log("stopped recording");
    
    // const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
    const blob = new Blob(chunks, { 'type' : chunks[0].type });
    chunks = [];

    // const audioURL = window.URL.createObjectURL(blob);
    var formdata = new FormData();
    formdata.append('audiodata', blob);

    $.ajax({
        url : "/asr",
        type: "POST",
        data: formdata,
        contentType: false,
        processData: false,

        success: function(response) {
            response = JSON.parse(response);
            console.log(response);
            console.log($("#textFromSpeech"));
            console.log(response[0]);
            console.log(response[0]['c']);

            $("#textFromSpeech").text(
                response[0]['c']
            );

            console.log("Done displaying result");
        },

        error: function() {
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
        evt.preventDefault();
        console.log("handleStartTalking.");
        var el = document.getElementById("btnParler");
        el.classList.remove("btn-success");
        el.classList.add("btn-danger");
    
        mediaRecorder.start();
        console.log(mediaRecorder.state);
        console.log("recorder started");
        
    }
    
    
    function handleEndTalking(evt){
        evt.preventDefault();
        console.log("handleEndTalking.");
        var el = document.getElementById("btnParler");
        el.classList.remove("btn-danger");
        el.classList.add("btn-success");

        mediaRecorder.stop();
        console.log(mediaRecorder.state);
        console.log("recorder stopped");
    }


    var el = document.getElementById("btnParler");
    el.addEventListener("touchstart", handleStartTalking, false);
    // el.addEventListener("mousedown", handleStartTalking, false);

    el.addEventListener("touchend", handleEndTalking, false);
    el.addEventListener("touchcancel", handleEndTalking, false);
    el.addEventListener("touchmove", handleEndTalking, false);
    // el.addEventListener("mouseup", handleEndTalking, false);

    mediaRecorder.onstop = stoppedRecording;
    mediaRecorder.ondataavailable = recordingDataAvailable;
}


function startup() {
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