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
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  };

  return fetch(`${process.env.API_URL}/login/`, requestOptions)
    .then(handleResponse)
    .then(data => {
      if (data.token) {
        localStorage.setItem("token", JSON.stringify(data.token));
        localStorage.setItem("user", JSON.stringify(data.user));
      }

      return data;
    });
}

function refresh() {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: {
      token: JSON.parse(localStorage.getItem("token"))
    }
  };
  return fetch(`${process.env.API_URL}/refresh/`, requestOptions).then(
    response => {
      return response;
    }
  );
}

function register(data) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.API_URL}/register/`, requestOptions).then(
    handleResponse
  );
}

function updateProfile(data) {
  const requestOptions = {
    method: "PATCH",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.API_URL}/profile/update/`, requestOptions).then(
    handleResponse
  );
}

function logout() {
  const requestOptions = {
    method: "POST"
  };

  return fetch(`${process.env.API_URL}/logout/`, requestOptions)
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

  return fetch(`${process.env.API_URL}/users/`, requestOptions).then(
    handleResponse
  );
}
