import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const userService = {
  login,
  register,
  update,
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
        if (data.user) {
          if (data.user["is_student"]) data.user.type = "student";
          else if (data.user["is_institute"]) data.user.type = "institute";
          else if (data.user["is_staff"]) data.user.type = "staff";
        }
        if (data.profile) data.user.profile = data.profile;
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

function update(data) {
  const requestOptions = {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.API_URL}/user/`, requestOptions).then(
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
