import { authHeader } from "./auth-header";
import handleResponse from "./handleResponse";

export const examService = {
  getAll
};

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };

  return fetch(`${process.env.VUE_APP_API_URL}/exams/`, requestOptions).then(
    handleResponse
  );
}
