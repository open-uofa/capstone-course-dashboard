<script>
	let shown = false;
	export function show() {
		shown = true;
	}

	export function hide() {
		shown = false;
	}
</script>

<svelte:window
	on:keydown={(e) => {
		if (e.key == 'Escape') {
			hide();
		}
	}}
/>

{#if shown}
	<div class="modal-wrapper">
		<div class="modal">
			<span class="close" on:click={() => hide()}>&times</span>
			<slot />
		</div>
	</div>
{/if}

<style>
	/* width */
	::-webkit-scrollbar {
		width: 4px;
		height: 4px;
	}

	/* Handle */
	::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, 0.25);
	}
	::-webkit-scrollbar-track {
		margin-top: 10px;
		margin-bottom: 10px;
	}

	/* Handle on hover */
	::-webkit-scrollbar-thumb:hover {
		background: #555;
	}
	.modal-wrapper {
		background-color: rgb(0, 0, 0);
		background-color: rgba(0, 0, 0, 0.7);
		position: fixed;
		width: 100vw;
		height: 100vh;
		top: 0;
		left: 0;
		z-index: 100;
	}

	.modal {
		background-color: white;
		max-width: 50vw;
		height: auto;
		max-height: 60vh;
		padding: 2rem;
		margin: 9.5% auto;
		text-align: center;
		border-radius: 0.5em;
		border: 00.005em solid;
		border-color: rgb(150, 150, 150);
		overflow: auto;
		overflow-x: hidden;
	}

	.close {
		float: right;
		cursor: pointer;
		font-size: 2rem;
	}
	.close:hover {
		font-weight: bold;
	}
</style>
