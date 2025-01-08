let audioRecorderButton = document.getElementById("audioStart")
audioRecorderButton.addEventListener("click", event => {
    console.log("clicked")
})
let audioRecorder = {
    audioBlobs: [],
    streamBeingRecorded: null, 
    mediaRecorder: null,  /*of type MediaRecorder*/
    //constructor(){
    //}
/** Start recording the audio
* @returns {Promise} - returns a promise that resolves if audio recording successfully started
*/
    start: async function(){
        if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
            return Promise.reject(new Error('mediaDevices API or getUserMedia method is not supported in this browser.'));
        }else{
            const audioRecording = await navigator.mediaDevices.getUserMedia({audio: true})
            this.streamBeingRecorded = audioRecording
            this.mediaRecorder = new MediaRecorder(audioRecording)
            this.audioBlobs = []
            this.mediaRecorder.addEventListener("dataavailable", event => {
                this.audioBlobs.push(event.data)
            })
            this.mediaRecorder.start()

        }

    }
}
audioRecorder.start()
