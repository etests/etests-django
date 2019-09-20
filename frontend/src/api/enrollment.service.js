import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const enrollmentService = {
  batchEnroll,
  remove,
  getAll
};

function batchEnroll(data) {
  const requestOptions = {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data)
  };

  return fetch(
    `${process.env.VUE_APP_API_URL}/batch/enroll/`,
    requestOptions
  ).then(handleResponse);
}

function remove(id) {
  const requestOptions = {
    method: "DELETE",
    headers: authHeader()
  };

  return fetch(
    `${process.env.VUE_APP_API_URL}/enrollments/${id}/`,
    requestOptions
  ).then(handleResponse);
}

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(
    `${process.env.VUE_APP_API_URL}/enrollments/`,
    requestOptions
  ).then(handleResponse);
}
