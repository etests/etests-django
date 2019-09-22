import * as axios from "axios";
import handleResponse from "./handleResponse"

let token = JSON.parse(localStorage.getItem("token"));

export const paymentService = { create };

async function create(data) {
  var headers = {
    Authorization: "Bearer " + token,
    "Content-Type": "multipart/form-data"
  };
  let response = await axios({
    method: "post",
    url: `${process.env.VUE_APP_API_URL}/payment/`,
    data,
    headers
  })
  return response;
  
}
