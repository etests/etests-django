import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const userService = {
  login,
  register,
  updateProfile,
  logout,
  getAll,
  refresh
};

function login(username, password) {
  var x = process.env.VUE_APP_API_URL;
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  };

  return fetch(`${process.env.VUE_APP_API_URL}/login/`, requestOptions)
    .then(handleResponse)
    .then(data => {
      if (data.refresh) {
        var token = {
          access: data.access,
          refresh: data.refresh,
        }
        localStorage.setItem("token", JSON.stringify(token));
        localStorage.setItem("user", JSON.stringify(data.user));
      }
      return data;
    });
}

function refresh() {
  const token = JSON.parse(localStorage.getItem("token"));
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({refresh: token.refresh})
  };
  return fetch(`${process.env.VUE_APP_API_URL}/refresh/`, requestOptions)
  .then(handleResponse)
  .then(
    data => {
      if(data.access){
        token.access = data.access;
        localStorage.setItem("token", JSON.stringify(token));
      }
    }
  );
}

function register(data) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.VUE_APP_API_URL}/register/`, requestOptions).then(
    handleResponse
  );
}

function updateProfile(data) {
  const requestOptions = {
    method: "PATCH",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(
    `${process.env.VUE_APP_API_URL}/profile/update/`,
    requestOptions
  ).then(handleResponse);
}

function logout() {
  const requestOptions = {
    method: "POST"
  };

  return fetch(`${process.env.VUE_APP_API_URL}/logout/`, requestOptions)
    .then(handleResponse)
    .then(function() {
      localStorage.removeItem("user");
      localStorage.removeItem("token");
    });
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.VUE_APP_API_URL}/users/`, requestOptions).then(
    handleResponse
  );
}
