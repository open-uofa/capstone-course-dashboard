<script>
	export let only_logo = false;
</script>

<a href="/dashboard">
	<img
		class:logo={only_logo}
		src="https://www.ualberta.ca/_assets/images/ua-logo-green.svg"
		alt="uAlberta Logo"
	/>
</a>

<style>
	img {
		height: 100%;
		width: 100%;
		text-align: center;
	}

	.logo {
		clip-path: inset(0% 75% 0% 0%);
		transform: translateX(120%) scale(300%);
	}
</style>
