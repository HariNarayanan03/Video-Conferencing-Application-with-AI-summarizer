const socket=io('/')
const videoGrid = document.getElementById('video-grid');
const myPeer = new Peer(undefined,{
    host:'/',
    port:'3001'
})
const myVideo = document.createElement('video');
myVideo.muted=true;
const peers={}
navigator.mediaDevices.getUserMedia({
    video:true,
    audio:true
}).then((stream) =>{
    addVideoStream(myVideo , stream,"mine")
    //
    myPeer.on('call',(call)=>{
        console.log("IM In");
        call.answer(stream);
        const video =document.getElementById('video')
        call.on('stream',userVideoStream=>{
            addVideoStream(video,userVideoStream,"in");
        })
    })
    
    socket.on('user-connected',(userId)=>{
        console.log("USER CONNECTED "+userId);
        connectToNewUser(userId,stream);
    })
    socket.on('user-disconnected',(userId)=>{
        console.log("USER DISCONNECTED "+userId);
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
})

function connectToNewUser(userId,stream)
{
    console.log("NEW USER");
    const call =myPeer.call(userId,stream);
    const video=document.createElement('video');
    call.on('stream',(userVideoStream)=>{
        console.log("ADD NEW VIDEO");
        addVideoStream(video, userVideoStream ,"new");
    })
    call.on('close',()=>{
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