import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const userService = {
  login,
  register,
  updateProfile,
  logout,
  getAll
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
      // login successful if there's a jwt token in the response
      if (data.token) {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        if (data.user) {
          if (data.user["is_student"]) data.user.type = "student";
          else if (data.user["is_institute"]) data.user.type = "institute";
          else if (data.user["is_staff"]) data.user.type = "staff";
        }
        localStorage.setItem("token", JSON.stringify(data.token));
        localStorage.setItem("user", JSON.stringify(data.user));
      }

      return data;
    });
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
    method: "POST",
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
