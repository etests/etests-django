import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const instituteService = {
  getFollowing,
  follow,
  getAll
};

function getFollowing() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(
    `${process.env.API_URL}/institutes/following/`,
    requestOptions
  ).then(handleResponse);
}

function follow(id) {
  const requestOptions = {
    method: "POST",
    headers: authHeader()
  };
  return fetch(
    `${process.env.API_URL}/institute/follow/${id}/`,
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
