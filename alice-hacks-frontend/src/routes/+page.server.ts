import type { Actions } from "./$types";

interface Response {
    transcript: string,
    filler_indices: [number, number][],
    filler_count: number,
    wpm: number,
    words: string[],
};

export const actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const file = formData.get("file") as File;

		const postFormData = new FormData();
		postFormData.append('input', file);

		const response = await fetch("http://127.0.0.1:3100/api", {
			method: 'post',
			body: postFormData
		});

		const json: Response = (await response.json());
		console.log(json);

		return {
			success: true,
			result: (json)
		};
	}
} satisfies Actions;
