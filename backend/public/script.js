
const socket=io('/')
const videoGrid = document.getElementById('video-grid');
const myPeer = new Peer(undefined,{
    host:'/',
    port:'3001'
})
let togglemic = 1,togglevideo=1;
let text = "";
const myVideo = document.createElement('video');
myVideo.muted=true;
const peers={}

navigator.mediaDevices.getUserMedia({
    video:true,
    audio:true
}).then(async (stream) =>{
    addVideoStream(myVideo , stream,"mine")
    //

    myPeer.on('call',(call)=>{
        console.log("IM In");
        call.answer(stream);
        console.log(stream.id);
        const video =document.createElement('video');
        call.on('stream',userVideoStream=>{
            addVideoStream(video,userVideoStream,"in");
        })
        document.getElementById("mictoggle").onclick = ()=>{
            let recognition;
            let output= "";
            if(togglemic){
                stream.getAudioTracks()[0].enabled = false;
                togglemic =0;
                document.getElementById("mictoggle").innerText="MIC(🔇)";
                console.log("mic off");
                if (recognition) {
                    recognition?.stop();
                    console.log('Recording stopped...');
                }
            }
            else {
                stream.getAudioTracks()[0].enabled = true;
                document.getElementById("mictoggle").innerText="MIC(🎙️)";
                console.log("mic on");
                recognition = new webkitSpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = false;
                recognition.onstart = () => {
                    console.log('Recording started...');
                };

                recognition.onresult = (event) => {
                    let interimTranscript = '';
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            // outputDiv.innerHTML += `<p>${transcript}</p>`;
                            console.log("transcript->",transcript);
                            //speech from other user
                            text+= "\n"+transcript;
                        } else {
                            interimTranscript += transcript;
                        }
                    }
                    if(interimTranscript!="") output= interimTranscript;
                    // console.log('Interim transcript:', interimTranscript);
                };

                recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error);
                };

                recognition.onend = () => {
                    console.log('Recording ended...');
                };

                recognition.start();
                togglemic =1;
        
            }
        }
        document.getElementById("videotoggle").onclick = ()=>{
            if(togglevideo){
                stream.getVideoTracks()[0].enabled = false;
                togglevideo =0;
                document.getElementById("videotoggle").innerText="VIDEO👇🏻(on)";
                console.log("video off");
            }
            else {
                stream.getVideoTracks()[0].enabled = true;
                togglevideo =1;
                document.getElementById("videotoggle").innerText="VIDEO👇🏻(off)";
                console.log("video on");
        
            }
        }
    })
    
    socket.on('user-connected',(userId)=>{
        console.log("USER CONNECTED "+userId);
        // connectToNewUser(userId,stream);
        setTimeout(connectToNewUser,1000,userId,stream)
    })
    socket.on('user-disconnected',(userId)=>{
        console.log("USER DISCONNECTED "+userId);
        document.getElementById(userId).remove();
        if (peers[userId]){
            console.log("CLOSED");
            peers[userId].close()
        }
        
    })

}).catch((error)=>{
    console.log(error);
})

myPeer.on('open',id=>{
    console.log("OPEN");
    socket.emit('join-room',ROOM_ID,id);
    myVideo.setAttribute('id',id);
})

function connectToNewUser(userId,stream)
{
    console.log("NEW USER");
    const call =myPeer.call(userId,stream);
    const video=document.createElement('video');
    video.setAttribute('id',userId);
    call.on('stream',(userVideoStream)=>{
        console.log("ADD NEW VIDEO");
        addVideoStream(video, userVideoStream ,"new");
    })
    console.log("MIC ",stream.getAudioTracks()[0]);
    document.getElementById("mictoggle").onclick = ()=>{
        let recognition;
        let output= "";
        if(togglemic){
            stream.getAudioTracks()[0].enabled = false;
            togglemic =0;
            document.getElementById("mictoggle").innerText="MIC(🔇)";
            console.log("mic off");
           // if (recognition) {
                recognition?.stop();
                console.log('Recording stopped...');
            //}
           // else  console.log('Recording not stopped...',recognition); 
        }
        else {
            stream.getAudioTracks()[0].enabled = true;
            document.getElementById("mictoggle").innerText="MIC(🎙️)";
            console.log("mic on");
            recognition = new webkitSpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = false;
                recognition.onstart = () => {
                    console.log('Recording started...');
                };

                recognition.onresult = (event) => {
                    let interimTranscript = '';
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            // outputDiv.innerHTML += `<p>${transcript}</p>`;
                            console.log("transcript ",transcript);
                            //speech from current user
                            text+= "\n"+transcript;
                        } else {
                            interimTranscript += transcript;
                        }
                    }
                    if(interimTranscript!="") output= interimTranscript;
                    // console.log('Interim transcript:', interimTranscript);
                };

                recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error);
                };

                recognition.onend = () => {
                    console.log('Recording ended...');
                };

                recognition.start();
                togglemic =1;
        }
    }
    document.getElementById("videotoggle").onclick = ()=>{
        if(togglevideo){
            stream.getVideoTracks()[0].enabled = false;
            togglevideo =0;
            document.getElementById("videotoggle").innerText="VIDEO👇🏻(on)";
            console.log("video off");
        }
        else {
            stream.getVideoTracks()[0].enabled = true;
            togglevideo =1;
            document.getElementById("videotoggle").innerText="VIDEO👇🏻(off)";
            console.log("video on");
    
        }
    }
    call.on('close',()=>{
        // videoGrid.remove(video);
        video.remove();
    })

    peers[userId] = call;
}

function addVideoStream(video,stream,stat){
    console.log("VIDEO "+stat);
    video.srcObject=stream
    video.addEventListener('loadedmetadata',()=>{
        video.play();
    })
    videoGrid.append(video);
}

document.getElementById("recording").onclick = ()=>{
    console.log("the transcript for this user is\n",text);

    //send this text to summary api

}