import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const TransactionsService = {
  get
};

function get() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.VUE_APP_API_URL}/transactions/`, requestOptions).then(
    handleResponse
  );
}
