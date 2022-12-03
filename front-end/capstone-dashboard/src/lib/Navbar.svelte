<script>
	import Logo from '$lib/UAlbertaLogo.svelte';
</script>

<div class="navbar" id="background">
	<nav>
		<Logo only_logo="true" />
		<slot />
	</nav>
</div>

<!--TODO: Make nav mobile responsive by placing it on the bottom-->
<style>
	#background {
		position: relative;
		min-height: 100%;
		width: 7rem;
		z-index: 1;

		background-color: hsl(0, 0%, 15%);
		transition-property: background-color, font-size, width;
		transition-duration: 200ms;
		transition-timing-function: ease-in-out;
		overflow: clip;
	}

	#background:hover {
		width: 15rem;
		font-size: 1.5em;
		background-color: hsl(139, 41%, 40%);
	}

	nav {
		position: sticky;
		top: 0;
		display: flex;
		flex-direction: column;
	}

	nav > :global(:first-child) {
		margin: 3rem auto;
		width: 5rem;
		filter: brightness(1.6);
		transition: filter 200ms ease-in-out;
	}

	div:hover > nav > :global(:first-child) {
		filter: brightness(1);
	}

	nav > :global(:not(:first-child)) {
		/* Use flex to keep items centered in their boxes */
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		min-height: 7rem;
		border: 0;
		color: white;
		text-align: center;
		text-decoration: none;
		background-color: transparent;
	}

	nav > :global(:not(:first-child)):hover {
		cursor: pointer;
		background-color: hsl(139, 41%, 30%);
	}
</style>
