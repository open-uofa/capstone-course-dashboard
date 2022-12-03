<script>
	export let closeOnClickOutside = true;
	let dialog;

	function handleModalClick(event) {
		let client = {
			width: dialog.clientWidth,
			height: dialog.clientHeight
		};

		let offset = {
			x: dialog.offsetLeft,
			y: dialog.offsetTop
		};

		if (
			event.x < offset.x ||
			event.x > client.width + offset.x ||
			event.y < offset.y ||
			event.y > client.height + offset.y
		) {
			event.stopPropagation();
			dialog.removeEventListener('click', handleModalClick);
			dialog.close();
		}
	}

	function showModal() {
		if (!('open' in dialog.attributes)) dialog.showModal();

		if (closeOnClickOutside) dialog.addEventListener('click', handleModalClick);
	}
</script>

<item on:click={showModal} on:keypress={showModal}>
	<article>
		<slot />
	</article>
	<dialog bind:this={dialog}>
		<article>
			<slot />
		</article>
		<!--Event does not bubble to prevent triggering above click event which
        will reopen the dialog-->
		<button
			on:click|stopPropagation={() => {
				dialog.close();
			}}>Close</button
		>
	</dialog>
</item>

<style>
	dialog[open] {
		display: flex;
		flex-direction: column;

		height: clamp(10vh, 45rem, 75vh);
		aspect-ratio: 9/7;
		padding: 0;
		border: 0;
		box-shadow: 1px 1px 5px hsl(0 0% 0% / 0.3);

		overflow-y: scroll;
		cursor: auto;
	}

	dialog::backdrop {
		background-color: hsl(0 0% 0% / 0.3);
	}

	item:hover {
		cursor: pointer;
	}

	dialog > :last-child {
		position: sticky;
		bottom: 0;
		left: 0;

		width: 100%;
		margin-top: 1rem;
		padding-block: 1rem;
		border: 0;
		border-top: 1px solid hsl(0 0% 85%);

		background: white;
		cursor: pointer;
		transition: background 250ms ease;
	}

	dialog > :last-child:hover {
		background-color: hsl(0 0% 95%);
	}

	dialog > article {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 3rem;
	}

	/* Styling for the entire item */
	item > article {
		max-height: 5rem;
		padding: 1rem;
		border: 1px solid gray;
		border-radius: 0.25rem;
		overflow: hidden;
	}
</style>
