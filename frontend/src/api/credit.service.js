import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const creditService = {
  get
};

function get(id) {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/credit-used/`, requestOptions).then(
    handleResponse
  );
}
