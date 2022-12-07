const urlVideo = document.querySelector("#music-input")
const searchBtn = document.querySelector("#search")
const title = document.querySelector("#title")
const album = document.querySelector("#album")
const channel = document.querySelector("#channel")
const metadata = document.querySelector("#metadata")
const updateBtn = document.querySelector("#update")
const downloadBtn = document.querySelector("#download")
const clearCacheBtn = document.querySelector("#clear_cache")


// Funções
const getMetadata = async(video_id) => {
    if (video_id.includes("www")) {
        split_url = video_id.split("&")
        video_id = split_url[0].slice(32, 43)
    }
    const youtubeDownloader = `http://127.0.0.1:8000/update/${video_id}`
    const res = await fetch(youtubeDownloader, {method: 'POST'})
    const data = await res.json()
    return data
}

const deleteCache = (url) =>{
    const youtubeDownloader = `http://127.0.0.1:8000/cache`
    fetch(youtubeDownloader, {method: 'DELETE'})
    window.alert("Cache deletado")
}

const updateMetadata = async (video_id) =>{
    if (video_id.includes("www")) {
        split_url = video_id.split("&")
        video_id = split_url[0].slice(32, 43)
    }
    console.log('cheguei')
    var metadata = {
        title: document.getElementById("title").value,
		album: document.getElementById("album").value,
		channel: document.getElementById("channel").value
    }
    console.log({metadata})
    const youtubeDownloader = `http://127.0.0.1:8000/update/${video_id}/metadata`
    const res = await fetch(youtubeDownloader, {method: 'PUT', headers:{'Content-Type': 'application/json'}, body: JSON.stringify(metadata)})
    console.log({res})
    const data = await res.json()
    console.log(data)
    return data
}

const downloadMP3 = async (video_id) =>{
    if (video_id.includes("www")) {
        split_url = video_id.split("&")
        video_id = split_url[0].slice(32, 43)
    }
    console.log('to aqui')
    const youtubeDownloader = `http://127.0.0.1:8000/downloadMP3/${video_id}`
    await fetch(youtubeDownloader, {method: 'POST'})
    
}

const showMusic = async (music) => {
    const data = await getMetadata(music)
    document.getElementById("title").value = data.title  
    document.getElementById("album").value = data.album
    document.getElementById("channel").value = data.channel
    metadata.classList.remove("hide")
}

const showNewMetada = async (video_id) => {
    const data = await updateMetadata(video_id)
    document.getElementById("title").value = data.title  
    document.getElementById("album").value = data.album
    document.getElementById("channel").value = data.channel
}



// Eventos
searchBtn.addEventListener("click", (e) => {
    e.preventDefault()
    const music = urlVideo.value
    showMusic(music)
})

urlVideo.addEventListener("keyup", (e) => {
    if(e.code === "Enter"){
        const music = e.target.value
        showMusic(music)
    }
})

clearCacheBtn.addEventListener("click", (e) => {
    e.preventDefault()
    deleteCache(null)
})

updateBtn.addEventListener("click", (e) => {
    e.preventDefault()
    const music = urlVideo.value
    showNewMetada(music)
})

downloadBtn.addEventListener("click", (e) => {
    e.preventDefault()
    const music = urlVideo.value
    downloadMP3(music)
})

