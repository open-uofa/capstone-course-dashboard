<script>
	import Logo from '$lib/UAlbertaLogo.svelte';
	import DropdownArrow from '$lib/images/down-arrow.svg';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { variables } from '$lib/variables';

	export let has_icon = false;
	export let header;
	export let username;

	let usernameDisplay;
	let usernameDialog;

	onMount(() => {
		setInterval(refresh, 840000);
	});

	async function refresh() {
		if (window.location.pathname != '/') {
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
					if (data['result'] === true) {
						window.localStorage.setItem('jwt', data['access_token']);
					}
				})
				.catch((error) => {
					console.log('Error fetching data', error.message);
				});
		}
	}

	async function logout() {
		await fetch(variables.basePath + '/logout', {
			headers: {
				Authorization: `Bearer ${window.localStorage.getItem('jwt')}`
			}
		})
			.then((response) => {
				if (response.status === 200) {
					window.localStorage.clear();
					goto('/');
				} else {
					console.log('Error: ' + response.statusText);
				}
			})
			.catch((error) => {
				console.log(error);
			});
	}

	async function showLogout() {
		if (!('open' in usernameDialog.attributes)) {
			usernameDisplay.style.backgroundColor = 'hsl(139, 41%, 30%)';
			return usernameDialog.show();
		}

		usernameDisplay.style.backgroundColor = 'hsl(139, 41%, 40%)';
		usernameDialog.close();
	}
</script>

<nav class="banner">
	{#if has_icon}
		<div class="logo">
			<Logo />
		</div>
	{/if}

	{#if header}
		<h1>{header}</h1>
	{/if}

	{#if username}
		<div
			class="username"
			bind:this={usernameDisplay}
			on:click={showLogout}
			on:keypress={showLogout}
		>
			<p>{username}</p>
			<img src={DropdownArrow} alt="Dropdown arrow" role="img" />
			<dialog class="username-dropdown" bind:this={usernameDialog}>
				<button on:click={logout}>Logout</button>
			</dialog>
		</div>
	{/if}
</nav>

<style>
	nav {
		position: relative;
		display: grid;
		grid-template-columns: 1fr 3fr 1fr;
		align-items: center;
		min-height: 4rem;
		max-width: 100%;
		z-index: 2;

		background-color: hsl(139, 41%, 40%);
	}

	nav,
	nav * {
		margin: 0;
		padding-block: auto;
		border: 0;
	}

	.logo {
		padding-inline: 1.5rem;
		margin-right: auto;
		height: 60%;
		min-width: 9rem;
	}

	h1 {
		grid-column: 2;
		margin-inline: auto;
		font-size: clamp(100%, 4ch, 5vw);
		font-weight: 400;
		color: white;
	}

	.username {
		grid-column: 3;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;

		position: relative;
		padding-inline: 1.5rem;
		margin-left: auto;
		height: 100%;

		color: white;
		font-size: 2.5ch;
		background-color: hsl(139, 41%, 40%);
		user-select: none;
	}

	.username:hover {
		cursor: pointer;
	}

	.username > img {
		height: 15%;
		padding-top: 0.1rem;
		max-width: 1rem;
	}

	.username-dropdown[open] {
		position: absolute;
		top: 100%;
		left: 0%;
		width: 100%;
		padding: 0;
		z-index: -1;

		animation: slideDown 75ms forwards;
		background-color: hsl(139 41% 40%);
	}

	.username-dropdown[open] > button {
		min-height: 3rem;
		width: 100%;

		background: transparent;
		color: white;
		text-align: center;
		user-select: none;
	}

	.username-dropdown[open] > button:hover {
		cursor: pointer;
		background-color: hsl(139, 41%, 30%);
	}

	@keyframes slideDown {
		from {
			transform: translateY(-100%);
		}

		to {
			transform: translateY(0%);
		}
	}
</style>
