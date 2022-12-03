<script>
	import RefreshArrow from '$lib/images/refresh-arrow.svg';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	const handleClick = () => dispatch('click');
</script>

<button on:click={handleClick}>
	<img src={RefreshArrow} alt="Refresh meeting minutes" />
</button>

<style>
	button {
		display: grid;
		place-items: center;
		grid-template-rows: 1fr;
		grid-template-columns: 1fr;

		width: 1.5rem;
		aspect-ratio: 1/1;
		margin: 0;
		padding: 0.2em;
		border: 0;
		border-radius: 0.25rem;

		background-color: hsl(0 0% 85%);
		cursor: pointer;
	}

	button > img {
		width: 90%;
	}
</style>
