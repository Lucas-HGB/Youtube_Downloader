import { useState, useEffect } from 'react'
import axios from "axios"
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faYoutube} from '@fortawesome/free-brands-svg-icons'
import Button from 'react-bootstrap/Button';

const NewPost = () => {
  const [post, SetPosts] = useState()

    const getPosts = async(video_id) => {
        try {
            const response = await axios.post(`http://127.0.0.1:8000/update/${video_id}`)
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        getPosts()
    }, [])
  return (
    <div className='form'>
      <h2>Faça o Download de sua Música!</h2>
      <div>
          <label htmlFor="link">Link:</label>
          <input type="text" name='link' id='title' placeholder='Copie o Link do vídeo/música que você quer baixar'></input>
          <Button as="a" variant="danger">
            <FontAwesomeIcon icon={faYoutube}/>
          </Button>
        </div>
    </div>
  )
}

export default NewPost