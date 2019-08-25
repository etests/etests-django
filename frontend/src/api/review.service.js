import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const reviewService = {
  get
};

function get(id) {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.API_URL}/review/${id}/`, requestOptions).then(
    handleResponse
  );
}
