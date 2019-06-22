import { authHeader } from "./auth-header";

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
    .then(auth => {
      // login successful if there's a jwt token in the response
      if (auth.token) {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem("auth", JSON.stringify(auth));
      }

      return auth;
    });
}

function register(userData) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData)
  };

  if (userData.user.is_student)
    return fetch(
      `${process.env.API_URL}/register/student/`,
      requestOptions
    ).then(handleResponse);
  else if (userData.user.is_institute)
    return fetch(
      `${process.env.API_URL}/register/institute/`,
      requestOptions
    ).then(handleResponse);
}

function updateProfile(userData) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData)
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
      localStorage.removeItem("auth");
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

function handleResponse(response) {
  return response.text().then(text => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        // logout();
        // location.reload(true);
      }

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
