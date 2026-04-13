import axios from 'axios';

const DEFAULT_API_ROOT = 'http://localhost:8000';

const configuredApiRoot =
	import.meta.env.VITE_BACKEND_URL ?? import.meta.env.BACKEND_URL;

const apiRoot = (configuredApiRoot ?? DEFAULT_API_ROOT).replace(/\/+$/, '');

const client = axios.create({
	baseURL: apiRoot,
});

const getAuthHeaders = (headers = {}) => {
	const authToken = localStorage.getItem('authToken');

	if (!authToken) {
		throw new Error('Authentication token is missing. Please log in.');
	}

	return {
		Accept: 'application/json',
		...headers,
		Authorization: `Bearer ${authToken}`,
	};
};

const request = (config) => client.request(config);
const get = (url, config = {}) => client.get(url, config);
const post = (url, data, config = {}) => client.post(url, data, config);
const put = (url, data, config = {}) => client.put(url, data, config);
const patch = (url, data, config = {}) => client.patch(url, data, config);
const remove = (url, config = {}) => client.delete(url, config);

export default {
	apiRoot,
	client,
	request,
	get,
	post,
	put,
	patch,
	delete: remove,
	getAuthHeaders,
};
