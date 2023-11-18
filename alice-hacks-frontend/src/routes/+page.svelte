<script lang="ts">
	import { FileDropzone, ProgressBar } from "@skeletonlabs/skeleton";
	import "iconify-icon";
	import { enhance } from "$app/forms";
	import type { PageServerData } from "../../.svelte-kit/types/src/routes/$types";

	export let form: PageServerData;
	$: if (form) {
		playLoadingAnimation = false;
	}

	let playLoadingAnimation = false;
	let file: FileList;
</script>

<div class="flex justify-center items-center flex-col p-4">
	<h1 class="mt-24 mb-12 title p-12">Eloquence</h1>
	<form
		class="w-3/4 mt-12 mb-8 flex justify-center items-center flex-col"
		method="POST"
		use:enhance
	>
		<div class="w-3/4">
			<!--TODO: Make it darker on hover instead of lighter-->
			<FileDropzone
				name="file"
				bind:files={file}
				required
				accept="audio/*"
				enctype="multipart/form-data"
			>
				<svelte:fragment slot="lead">
					<iconify-icon icon="bi:upload" class="icon" />
				</svelte:fragment>
				<svelte:fragment slot="message">
					<span class="font-bold">Upload a file </span>
					<span>or drag and drop</span>
				</svelte:fragment>
				<svelte:fragment slot="meta">
					MP3, and WAV are allowed.
					{#if file && file?.length > 0}
						<br />
						<br />
						<span class="font-semibold">{file?.[0].name}</span>
					{/if}
				</svelte:fragment>
			</FileDropzone>
		</div>
		{#if playLoadingAnimation}
			<div class="w-3/4 mt-4">
				<ProgressBar value={undefined} meter="bg-primary-800" />
			</div>
		{/if}
		<button
			on:click={() => (playLoadingAnimation = true)}
			type="submit"
			class="btn variant-filled-primary text-2xl w-3/4 mt-4"
		>
			<span class="pt-1 pb-1"> Analyse </span>
		</button>
	</form>
</div>

<style>
	.title {
		font-size: 12em;
		font-family: "MrsSaintDelafield", cursive;
	}

	.icon {
		font-size: 3rem;
	}
</style>
