<script lang="ts">
	import { FileDropzone } from "@skeletonlabs/skeleton";
	import "iconify-icon";

	let files: FileList;
</script>

<div class="flex justify-center items-center flex-col p-4">
	<h1 class="mt-24 mb-12 title p-12">Eloquence</h1>
	<div class="w-3/4 mt-12">
		<!--TODO: Make it darker on hover instead of lighter-->
		<FileDropzone name="files" bind:files required accept="audio/*">
			<svelte:fragment slot="lead">
				<iconify-icon icon="bi:upload" class="icon" />
			</svelte:fragment>
			<svelte:fragment slot="message">
				<span class="font-bold">Upload a file </span>
				<span>or drag and drop</span>
			</svelte:fragment>
			<svelte:fragment slot="meta">MP3, and WAV are allowed.</svelte:fragment>
		</FileDropzone>
	</div>
	<h1>{files?.length}</h1>
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
