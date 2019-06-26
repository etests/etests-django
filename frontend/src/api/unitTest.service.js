import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const unitTestService = {
  get,
  create,
  update,
  remove,
  getAll
};

function get(id) {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/unittests/${id}/`, requestOptions).then(
    handleResponse
  );
}

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

function update(data) {
  const requestOptions = {
    method: "PATCH",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(
    `${process.env.API_URL}/unittests/${data.id}/`,
    requestOptions
  ).then(handleResponse);
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
