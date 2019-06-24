import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const instituteService = {
  getAll
};

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/institutes/`, requestOptions).then(
    handleResponse
  );
}
