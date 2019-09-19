import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const sessionService = {
  get,
  update,
  remove,
  getAll
};

function get(id) {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.VUE_APP_API_URL}/get-session/${id}/`, requestOptions)
    .then(handleResponse)
    .then(data => {
      if (data) {
        localStorage.setItem("session", JSON.stringify(data));
      }
      return data;
    });
}

function update(data) {
  const requestOptions = {
    method: "PATCH",
    headers: authHeader(),
    body: JSON.stringify(data)
  };
  return fetch(
    `${process.env.VUE_APP_API_URL}/update-session/${data.id}/`,
    requestOptions
  ).then(handleResponse);
}

function remove(id) {
  const requestOptions = {
    method: "DELETE",
    headers: authHeader()
  };

  return fetch(`${process.env.VUE_APP_API_URL}/update-session/${id}/`, requestOptions)
    .then(handleResponse)
    .then(_ => {
      localStorage.removeItem("session");
    });
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(`${process.env.VUE_APP_API_URL}/get-sessions/`, requestOptions).then(
    handleResponse
  );
}
