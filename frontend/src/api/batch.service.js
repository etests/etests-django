import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const batchService = {
  get,
  list,
  detailedList,
  create,
  update,
  join,
  remove
};

function get(id) {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(
    `${process.env.VUE_APP_API_URL}/batches/${id}/`,
    requestOptions
  ).then(handleResponse);
}

function create(data) {
  const requestOptions = {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.VUE_APP_API_URL}/batches/`, requestOptions).then(
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
    `${process.env.VUE_APP_API_URL}/batches/${data.id}/`,
    requestOptions
  ).then(handleResponse);
}

function join(data) {
  const requestOptions = {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data)
  };
  return fetch(
    `${process.env.VUE_APP_API_URL}/batch/join/`,
    requestOptions
  ).then(handleResponse);
}

function remove(id) {
  const requestOptions = {
    method: "DELETE",
    headers: authHeader()
  };

  return fetch(
    `${process.env.VUE_APP_API_URL}/batches/${id}/`,
    requestOptions
  ).then(handleResponse);
}

function list() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(
    `${process.env.VUE_APP_API_URL}/batches/simple/`,
    requestOptions
  ).then(handleResponse);
}

function detailedList() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(`${process.env.VUE_APP_API_URL}/batches/`, requestOptions).then(
    handleResponse
  );
}
