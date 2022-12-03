<script>
	import Banner from '$lib/Banner.svelte';
	import Login from '$lib/Login.svelte';
	import Logo from '$lib/UAlbertaLogo.svelte';
	import { onMount } from 'svelte';

	onMount(() => {
		window.localStorage.clear();
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Capstone Course Dashboard" />
</svelte:head>

<main>
	<Banner has_icon={false} header="Capstone Dashboard" username="" />
	<section id="login">
		<Logo />
		<div class="login_btn"><Login text="Sign In" /></div>
	</section>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		width: 100%;
		min-height: 100vh;
		background-color: hsl(0, 0%, 90%);
	}

	#login {
		display: grid;
		align-items: center;
		justify-content: place-around;
		grid-template-rows: 3fr 2fr 0.5fr 1.5fr;

		margin: auto;
		padding: 5vw;
		width: clamp(10rem, 40vw, 20rem);
		aspect-ratio: 4/5;

		font-size: 2em;
		background-color: white;
		box-shadow: 5px 5px 0.5rem hsl(0, 0%, 55%);
	}

	.login_btn {
		grid-row: 3;
	}
</style>
