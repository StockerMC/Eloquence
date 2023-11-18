import type { Actions } from "./$types";

export const actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const file = formData.get("file") as File;

		return {
			success: true
		};
	}
} satisfies Actions;
