const audioRecordButton = document.getElementById('audioStart')
audioRecordButton.addEventListener("click", async event => {
    const microphonePermission = await navigator.permissions.query({name: 'microphone'})
    console.log(microphonePermission.state)
    microphonePermission.onchange = results => {
        if(results.target){
            console.log("changed", results.target.state)
        }
    }
})
