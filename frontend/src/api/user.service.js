import { authHeader } from "./auth-header";

export const userService = {
  login,
  logout,
  getAll
};

function login(username, password) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  };

  return fetch(`${process.env.API_URL}/auth/obtain_token/`, requestOptions)
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

function logout() {
  // remove user from local storage to log user out
  localStorage.removeItem("auth");
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  console.log(requestOptions);

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
        logout();
        location.reload(true);
      }

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
