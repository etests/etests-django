import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const testSeriesService = {
  create,
  remove,
  getMy,
  getAll
};

function create(data) {
  const requestOptions = {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(`${process.env.API_URL}/testseries/`, requestOptions).then(
    handleResponse
  );
}

function remove(id) {
  const requestOptions = {
    method: "DELETE",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/testseries/${id}/`, requestOptions).then(
    handleResponse
  );
}

function getMy() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(`${process.env.API_URL}/testseries/`, requestOptions).then(
    handleResponse
  );
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(`${process.env.API_URL}/testseries/all/`, requestOptions).then(
    handleResponse
  );
}
