import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const instituteService = {
  getAll,
  join
};

function join(id) {
  const requestOptions = {
    method: "POST",
    headers: authHeader()
  };

  return fetch(
    `${process.env.API_URL}/institute/join/${id}/`,
    requestOptions
  ).then(handleResponse);
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/institutes/`, requestOptions).then(
    handleResponse
  );
}
