<script>
	import { T, useFrame } from "@threlte/core";
	import { interactivity } from "@threlte/extras";
	import { spring } from "svelte/motion";

	interactivity();
	const scale = spring(2);

	let rotation = 0;
	useFrame((state, delta) => {
		rotation += delta;
	});
</script>

<T.PerspectiveCamera
	makeDefault
	position={[3, 3, 4]}
	on:create={({ ref }) => {
		ref.lookAt(0, 1, 0);
	}}
/>
<T.DirectionalLight position={[0, 5, 5]} castShadow intensity={4} />

<T.Mesh
	rotation.y={rotation}
	position.y={1}
	scale={$scale}
	on:pointerenter={() => scale.set(2.5)}
	on:pointerleave={() => scale.set(2)}
	castShadow
>
	<T.IcosahedronGeometry />
	<T.MeshStandardMaterial color="hotpink" />
</T.Mesh>
