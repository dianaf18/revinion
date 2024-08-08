const socket = io();
let mediaRecorder;

document.getElementById('startButton').addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener('dataavailable', event => {
                socket.emit('audio_stream', event.data);
            });
        })
        .catch(err => console.error('Error accessing media devices.', err));
});

document.getElementById('stopButton').addEventListener('click', () => {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
});

socket.on('transcription', data => {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML += `<p>${data.data}</p>`;
});
