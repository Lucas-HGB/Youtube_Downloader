// const API_URL = process.env.API_URL;
import axios from "axios";
const API_URL = "http://127.0.0.1:8000";

export function update_video(searchUrl) {
    var request = new XMLHttpRequest();
    request.open("POST", `${API_URL}/update/${searchUrl}`)
    request.send(null);
}

export const get_metadata = async () => {
    const response = await axios.get(`${API_URL}/visualize/metadata`);
    console.log(response);  
    return JSON.parse(response.responseText);
}






