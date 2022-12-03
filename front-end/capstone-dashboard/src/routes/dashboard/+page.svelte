<script>
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import { variables } from '$lib/variables';
	import add from '$lib/add.svg';
	import { refresh } from '$lib/refresh.js';
	let course_data = {};
	//Fetch all courses from datatbase
	async function getCourses() {
		const res = await fetch(
			variables.basePath + '/courses' + '/' + window.localStorage.getItem('username'),
			{
				headers: {
					Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
				}
			}
		)
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				if (response.ok) {
					return response.json();
				}
			})
			.then((data) => {
				course_data = data;
			});
	}
</script>

<DefaultLayout show_navbar={false} banner_has_icon="true" banner_title="Dashboard">
	<section>
		{#await getCourses()}
			<h2>Loading...</h2>
		{:then data}
			{#each course_data as course}
				<button
					class="course"
					onclick="window.location.href='dashboard/course?course={course.name}'"
					>{course.name}</button
				>
			{/each}
			<section class="add-course" onclick="window.location.href='dashboard/course/add-course'">
				<img class="add-button" src={add} alt="Add course" />
				<h3>Add Course</h3>
			</section>
		{/await}
	</section>
</DefaultLayout>

<style>
	section {
		display: flex;
		flex-wrap: wrap;
		max-width: 100%;
		padding: min(3rem, 3vw);
		gap: 3rem;
	}

	.course {
		display: inline-block;
		align-items: center;
		justify-content: center;
		height: 10rem;
		aspect-ratio: 9/5;

		background-color: rgb(239, 239, 239);
		font-size: 4ch;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 0.5rem;
		word-wrap: break-word;
		overflow: hidden;
	}

	.course:hover {
		cursor: pointer;
		background-color: rgba(10, 138, 29, 0.1);
	}

	.add-button {
		height: 4rem;
		width: 4rem;
	}

	.add-course {
		display: inline;
		text-align: center;
	}
	.add-course:hover {
		cursor: pointer;
	}
</style>
