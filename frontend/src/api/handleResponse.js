import { userService } from "./user.service";

function isObject(value) {
  return value && typeof value === "object" && value.constructor === Object;
}

function isArray(value) {
  return value && typeof value === "object" && value.constructor === Array;
}

export default function handleResponse(response) {
  return response.text().then(text => {
    const data = text && JSON.parse(text);
    var messages = [];
    if (!response.ok) {
      if (response.status === 401) {
        userService.logout();
        location.reload(true);
      } else if (isObject(data))
        for (var prop in data) {
          if (!data.hasOwnProperty(prop)) continue;
          if (isArray(data[prop]))
            for (var i in data[prop]) messages.push(data[prop][i]);
          else messages.push(data[prop]);
        }
      else messages.push(data);
      const error = messages.join("<br/>");
      return Promise.reject(error);
    }

    return data;
  });
}
