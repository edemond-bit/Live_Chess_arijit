const axios = require('axios');

/* Create your personal token on https://lichess.org/account/oauth/token */
const personalToken = 'RboOwEdRt7C5fEhX';

axios.get('/api/account', {
    baseURL: 'https://lichess.org/',
    headers: { 'Authorization': 'Bearer ' + personalToken }
}).then(
    console.log,
    err => console.error(err.message)
);