<script>
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import { variables } from '$lib/variables';

	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import csv from '$lib/csv-file-icon.svg';
	import { refresh } from '$lib/refresh.js';
	let course_to_add = '';
	let use_github = false;
	let use_team_structure = false;
	let use_student_form = false;
	let course_csv;

	// once the user clicks on cancel button, this function is called to redirect to the dashboard page
	function redirect_to_dashboard() {
		window.location.href = '../';
	}

	async function create_course() {
		if (course_to_add == '' || course_csv == undefined) {
			alert('Please enter all required fields');
		} else {
			// create the course
			await fetch(variables.basePath + '/courses/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: 'Bearer ' + localStorage.getItem('jwt')
				},
				body: JSON.stringify({
					name: course_to_add,
					roster_file_name: course_csv[0].name,
					use_github: use_github,
					use_team_structure: use_team_structure,
					use_student_experience_form: use_student_form
				})
			}).then((response) => {
				if (response.status === 401) {
					refresh();
				}
				if (response.ok) {
					submit_course_csv();
				} else {
					console.log('error creating course');
					alert('Error creating course. Error' + response.status);
					return null;
				}
			});
		}
	}

	// use this function to submit the course csv to backend
	async function submit_course_csv() {
		const dataArray = new FormData();
		dataArray.append('file', course_csv[0]);

		fetch(variables.basePath + '/students/' + course_to_add + '/' + 0, {
			method: 'POST',
			headers: {
				Authorization: 'Bearer ' + localStorage.getItem('jwt')
			},
			body: dataArray
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				if (response.ok) {
					alert('Course created successfully');
					redirect_to_dashboard();
				} else {
					alert(
						'Course created but the file contains error. Please go to edit page and upload the file again'
					);
					throw new Error('Something went wrong');
				}
			})
			.then((data) => {
				console.log(data);
			})
			.catch((error) => {
				console.error('Error uploading course data:', error);
			});
	}

	async function checkAuth() {
		fetch(`${variables.basePath}/auth/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}
</script>

{#await checkAuth() then}
	<DefaultLayout banner_username="Username" show_navbar={false}>
		<section>
			<Breadcrumbs>
				<a href="/dashboard">Dashboard</a>
				<p>Add Course</p>
			</Breadcrumbs>

			<section class="add-grid">
				<h2>Add Course</h2>
				<!-- https://freefrontend.com/css-tabs/ -->
				<div class="warpper">
					<input class="radio" id="one" name="group" type="radio" checked />
					<input class="radio" id="two" name="group" type="radio" />
					<div class="tabs">
						<label class="tab" id="one-tab" for="one">Add Manually </label>
						<label class="tab" id="two-tab" for="two">Fetch from link</label>
					</div>
					<div class="panels">
						<div class="panel" id="one-panel">
							<div>
								<input
									class="course-name"
									type="text"
									placeholder="*Enter Course Name"
									bind:value={course_to_add}
								/>
							</div>
							<div>
								<!-- https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_custom_checkbox -->
								<label class="check-container github"
									>Use Github
									<input type="checkbox" bind:checked={use_github} />
									<span class="checkmark git-check" />
								</label>
								<label class="check-container team"
									>Team Structure
									<input type="checkbox" bind:checked={use_team_structure} />
									<span class="checkmark team-check" />
								</label>
								<label class="check-container student"
									>Student Experience Form
									<input type="checkbox" bind:checked={use_student_form} />
									<span class="checkmark student-check" />
								</label>
								<section class="file-input">
									*
									<img class="img" src={csv} alt="csv file" />Course File
									<input bind:files={course_csv} type="file" accept=".csv" />
								</section>
								<section>
									<button on:click={create_course} class="confirm-btn manual-confirm">
										Confirm
									</button>

									<button on:click={redirect_to_dashboard} class="cancel-btn manual-cancel">
										Cancel
									</button>
								</section>
							</div>
						</div>
						<div class="panel" id="two-panel">
							<h1>Coming Soon.....</h1>

							<del>
								<p>Link <input class="fetch-link" type="text" /></p>
							</del>

							<section class="not-implemented">
								<button disabled class="confirm-btn"> Confirm </button>

								<button disabled class="cancel-btn"> Cancel </button>
							</section>
						</div>
					</div>
				</div>
			</section>
		</section>
	</DefaultLayout>
{/await}

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

	:global(body) {
		background-color: hsl(0, 0%, 90%);
	}

	.add-grid {
		margin-left: auto;
		margin-right: auto;
		margin-top: 4rem;
		background-color: white;
		position: relative;
		border-radius: 0.5em;
		border: 00.005em solid;
		border-color: silver;
		height: 100%;
		padding: 2em;
		min-width: 450px;
		width: 30vw;
		text-align: center;
		padding-left: 5vw;
		padding-right: 5vw;
		overflow: auto;
	}

	@import url('https://fonts.googleapis.com/css?family=Arimo:400,700&display=swap');

	h2 {
		color: #000;
		text-align: center;
		font-size: 1.5em;
	}
	.warpper {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.tab {
		cursor: pointer;
		padding: 10px 20px;
		margin: 0px 2px;
		background: #000;
		display: inline-block;
		color: #fff;
		border-radius: 3px 3px 0px 0px;
		box-shadow: 0 0.5rem 0.8rem #00000080;
	}
	.panels {
		background: #fffffff6;
		min-height: 300px;
		width: 100%;
		border-radius: 3px;
		overflow: hidden;
		padding: 20px;
	}
	.panel {
		display: none;
		animation: fadein 0.5s;
	}
	@keyframes fadein {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	.radio {
		display: none;
	}
	#one:checked ~ .panels #one-panel,
	#two:checked ~ .panels #two-panel {
		display: block;
	}
	#one:checked ~ .tabs #one-tab,
	#two:checked ~ .tabs #two-tab {
		background: #fffffff6;
		color: #000;
		border-top: 3px solid #000;
	}

	.fetch-link {
		margin-left: 1rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1.5px solid #3b3b3b;
		width: 20em;
	}
	.course-name {
		margin-top: 2rem;
		margin-left: -3rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		font-size: 22px;
		border-bottom: 1.5px solid #3b3b3b;
		width: 15rem;
	}

	.confirm-btn {
		margin-top: 2.5em;
		margin-left: auto;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 8em;
	}
	.cancel-btn {
		margin-top: 2.5em;
		margin-left: 2vw;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 8em;
	}

	/* The container */
	.check-container {
		display: block;
		position: relative;
		margin-top: 2rem;
		margin-bottom: 12px;
		margin-left: -11rem;
		cursor: pointer;
		font-size: 22px;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}
	/* The container */
	.team {
		display: block;
		position: relative;
		margin-top: 1.5rem;
		margin-bottom: 12px;
		margin-left: -8.6rem;
		cursor: pointer;
		font-size: 22px;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}

	.student {
		display: block;
		position: relative;
		margin-top: 1.5rem;
		margin-bottom: 12px;
		margin-left: -2.3rem;
		cursor: pointer;
		font-size: 22px;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}

	.file-input {
		margin-top: 1.5rem;
		font-size: 18px;
		margin-left: 6.5rem;
		margin-left: auto;
		margin-right: auto;

		border: 00.05em solid;
		border-color: hsl(54, 78%, 60%);
		background-color: #fffbfb;
		border-radius: 0.5em;
		padding: 0.5em;
	}
	.file-input > img {
		height: 1.5rem;
		width: 1.5rem;
		margin-left: 5rem;
	}

	/* Hide the browser's default checkbox */
	.check-container input {
		position: absolute;
		opacity: 0;
		cursor: pointer;
		height: 0;
		width: 0;
	}

	/* Create a custom checkbox */
	.checkmark {
		position: absolute;
		top: 0;
		margin-left: 11rem;
		height: 25px;
		width: 25px;
		border: 2px solid #000;
		background-color: rgb(255, 255, 255);
	}

	.team-check {
		position: absolute;
		top: 0;
		margin-left: 8.6rem;
		height: 25px;
		width: 25px;
		border: 2px solid #000;
		background-color: rgb(255, 255, 255);
	}
	.student-check {
		position: absolute;
		top: 0;
		margin-left: 2.35rem;
		height: 25px;
		width: 25px;
		border: 2px solid #000;
		background-color: rgb(255, 255, 255);
	}

	/* On mouse-over, add a grey background color */
	.check-container:hover input ~ .checkmark {
		background-color: #ccc;
	}

	/* When the checkbox is checked, add a blue background */
	.check-container input:checked ~ .checkmark {
		background-color: hsl(139, 41%, 40%);
	}

	/* Create the checkmark/indicator (hidden when not checked) */
	.checkmark:after {
		content: '';
		position: absolute;
		display: none;
	}

	/* Show the checkmark when checked */
	.check-container input:checked ~ .checkmark:after {
		display: block;
	}

	/* Style the checkmark/indicator */
	.check-container .checkmark:after {
		left: 9px;
		top: 5px;
		width: 5px;
		height: 10px;
		border: solid white;
		border-width: 0 3px 3px 0;
		-webkit-transform: rotate(45deg);
		-ms-transform: rotate(45deg);
		transform: rotate(45deg);
	}

	.not-implemented > button:hover {
		cursor: default;
	}
</style>
