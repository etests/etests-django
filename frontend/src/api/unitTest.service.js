import { authHeader } from "./auth-header";

export const unitTestService = {
  create,
  remove,
  getAll
};

function create(data) {
  const requestOptions = {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.API_URL}/unittests/`, requestOptions).then(
    handleResponse
  );
}

function remove(id) {
  const requestOptions = {
    method: "DELETE",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/unittests/${id}`, requestOptions).then(
    handleResponse
  );
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(`${process.env.API_URL}/unittests/`, requestOptions).then(
    handleResponse
  );
}
function handleResponse(response) {
  return response.text().then(text => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
