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

  return fetch(`${process.env.API_URL}/exams/`, requestOptions).then(
    handleResponse
  );
}
