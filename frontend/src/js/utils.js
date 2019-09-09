const utils = {
  formatDate
};

function formatDate(dateString) {
  var date = new Date(Date.parse(dateString));
  return (
    date.getDate() +
    "/" +
    (date.getMonth() + 1) +
    "/" +
    date.getFullYear() +
    " " +
    date.getHours() +
    ":" +
    date.getMinutes() +
    ":" +
    date.getSeconds()
  );
}

export default utils;
