axios.defaults.baseURL = "http://localhost:3000";
axios.defaults.timeout = 7000;

export function getAllData() {
  return axios({
    url: "/api/winning_data"
  });
}
