import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const resultService = {
  get
};

function get(id) {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/get-result/${id}/`, requestOptions).then(
    handleResponse
  );
}
