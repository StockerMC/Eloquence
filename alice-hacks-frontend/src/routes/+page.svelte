<script>
	import { FileDropzone } from "@skeletonlabs/skeleton";
	import "iconify-icon";
</script>

<div class="flex justify-center items-center flex-col p-4">
	<h1 class="text-9xl mt-12 mb-12">Eloquence</h1>
	<div class="w-3/4 mt-12">
		<FileDropzone name="files">
			<svelte:fragment slot="lead">
				<iconify-icon icon="bi:upload" class="icon" />
			</svelte:fragment>
			<svelte:fragment slot="message">
				<span class="font-bold">Upload a file </span>
				<span>or drag and drop</span>
			</svelte:fragment>
			<svelte:fragment slot="meta">(meta)</svelte:fragment>
		</FileDropzone>
	</div>
</div>

<style>
	.icon {
		font-size: 3rem;
	}
</style>