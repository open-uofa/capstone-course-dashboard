<script>
	import axios from 'axios';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { variables } from '$lib/variables';

	export let text;
	let result = null;

	let access_token;
	let client;
	let gAuthScopes = 'https://www.googleapis.com/auth/userinfo.email';

	function initClient() {
		client = google.accounts.oauth2.initTokenClient({
			client_id: variables.googleClientId,
            scope: gAuthScopes,
			callback: (tokenResponse) => {
				// Callback runs after token is fetched
				access_token = tokenResponse.access_token;
				doPost()
					.then((response) => {
						if (response.status === 200) {
							window.localStorage.clear();
							window.localStorage.setItem('jwt', response.data['access_token']);
							window.localStorage.setItem('username', response.data['email']);
							window.localStorage.setItem('refresh', response.data['refresh_token']);

							goto('/dashboard');
						} else {
							if (response.status === 401) {
								alert('Error: Invalid email address. Please try again.');
							} else {
								alert('Error: ' + response.statusText);
								console.log('Error: ' + response.statusText);
							}
						}
					})
					.catch((error) => {
						console.log(error);
						alert('Error: Invalid email address. Please try again.');
					});
			}
		});
	}

	async function doPost() {
		const res = await axios.post(variables.basePath + '/auth', {
			token: access_token
		});

		const data = await res;
		return data;
	}

	function getToken() {
		try {
			client.requestAccessToken();
		} catch {
			console.log('[Login] Clicked before Google Sign-In could load');
		}
	}

	onMount(async () => {
		// Block until Google Sign-in libraries load
		let google_undefined = true;
		while (google_undefined) {
			await new Promise((resolve) => setTimeout(resolve, 1000));
			google_undefined = typeof google === 'undefined';
		}

		await initClient();
	});
</script>

<svelte:head>
	<script src="https://accounts.google.com/gsi/client" async></script>
</svelte:head>

<div class="login_btn">
	<div id="googleSignIn" />
	<button on:click={getToken}>{text}</button>
</div>

<style>
	.login_btn {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.login_btn > button {
		padding: 0 0.5rem;
		font-size: 10pt;
		font-weight: bold;
		color: white;
		background-color: hsl(139, 41%, 35%);

		min-height: 2.5rem;
		width: 100%;
		border: solid;
		border-radius: 0.25rem;
		border-width: 0px;
		box-shadow: 2px 2px 0.25rem hsl(0, 0%, 55%);
	}

	.login_btn > button:hover {
		cursor: pointer;
	}

	div#googleSignIn {
		display: none;
	}
</style>
