import { authHeader } from "./auth-header";

export const testSeriesService = {
  getAll
};

function getAll() {
  const requestOptions = {
    method: "GET",
    headers: authHeader()
  };
  return fetch(`${process.env.API_URL}/api/testseries/`, requestOptions).then(
    handleResponse
  );
}
function handleResponse(response) {
  return response.text().then(text => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
