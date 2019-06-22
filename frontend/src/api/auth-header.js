export function authHeader() {
  let auth = JSON.parse(localStorage.getItem("auth"));

  if (auth && auth.token) {
    return {
      Authorization: "Bearer " + auth.token,
      "Content-Type": "application/json"
    };
  } else {
    return {};
  }
}
