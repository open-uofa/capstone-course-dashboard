import { variables } from '$lib/variables';
import { goto } from '$app/navigation';

export async function refresh() {
	if (window.localStorage.getItem('refresh') == null) {
		goto('/');
	}

	if (window.location.pathname != '/' && window.localStorage.getItem('refresh') != null) {
		await fetch(variables.basePath + '/refresh', {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt'),
				'Content-Type': 'application/json;'
			},
			method: 'POST',
			body: JSON.stringify({
				grant_type: 'refresh_token',
				refresh_token: window.localStorage.getItem('refresh')
			})
		})
			.then((response) => {
				if (response.status === 401) {
					window.localStorage.clear();
					goto('/');
				}
				return response.json();
			})
			.then((data) => {
				console.log(data);
				if (data['result'] === true) {
					window.localStorage.setItem('jwt', data['access_token']);
					window.location.reload();
				}
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}
}
