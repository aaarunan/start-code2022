import axios from 'axios'

export default () => {
  return axios.create({
    baseURL: 'http://localhost:1243/',
    withCredentials: false,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  });
}
