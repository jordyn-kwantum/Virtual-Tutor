import axios from "axios";



export default axios.create({
    withCredentials:true,
    contentType: "application/json",
    crossDomain: true,
    mode: "cors",
    // baseURL:"http://localhost:5000" //Dev only
})