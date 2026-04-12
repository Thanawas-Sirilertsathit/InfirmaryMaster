<template>
	<div v-if="isOpen" class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg">Edit Medicine</h3>
			<form @submit.prevent="submitForm">
				<div class="form-control">
					<label class="label">
						<span class="label-text">Medicine Name</span>
					</label>
					<input
						v-model="form.name"
						type="text"
						placeholder="Enter medicine name"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Description</span>
					</label>
					<textarea
						v-model="form.description"
						placeholder="Enter description"
						class="textarea textarea-bordered"
						required
					></textarea>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Category</span>
					</label>
					<select
						v-model="form.category"
						class="select select-bordered"
						required
					>
						<option value="">Select category</option>
						<option value="powder">Powder</option>
						<option value="liquid">Liquid</option>
						<option value="pill">Pill</option>
						<option value="capsule">Capsule</option>
					</select>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Dosage</span>
					</label>
					<input
						v-model="form.dosage"
						type="text"
						placeholder="Enter dosage"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Minimum Stock</span>
					</label>
					<input
						v-model.number="form.minimum_stock"
						type="number"
						min="0"
						placeholder="Enter minimum stock"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Image URL</span>
					</label>
					<input
						v-model="form.image"
						type="url"
						placeholder="Enter image URL"
						class="input input-bordered"
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Side Effects</span>
					</label>
					<textarea
						v-model="form.side_effects"
						placeholder="Enter side effects"
						class="textarea textarea-bordered"
					></textarea>
				</div>
				<div class="modal-action">
					<button type="submit" class="btn btn-primary">Save</button>
					<button type="button" class="btn" @click="closeModal">
						Cancel
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
const createEmptyForm = () => ({
	name: '',
	description: '',
	category: '',
	dosage: '',
	minimum_stock: 0,
	image: '',
	side_effects: '',
});

export default {
	name: 'EditMedicineModal',
	props: {
		isOpen: {
			type: Boolean,
			required: true,
		},
		medicine: {
			type: Object,
			default: null,
		},
	},
	data() {
		return {
			form: createEmptyForm(),
		};
	},
	watch: {
		medicine: {
			immediate: true,
			handler(value) {
				if (!value) {
					this.form = createEmptyForm();
					return;
				}

				this.form = {
					name: value.name || '',
					description: value.description || '',
					category: value.category || '',
					dosage: value.dosage || '',
					minimum_stock: Number(value.minimum_stock || 0),
					image: value.image || '',
					side_effects: value.side_effects || '',
				};
			},
		},
	},
	methods: {
		submitForm() {
			this.$emit('save', {
				...this.form,
				minimum_stock: Number(this.form.minimum_stock),
				image: this.form.image || null,
				side_effects: this.form.side_effects || null,
			});
		},
		closeModal() {
			this.$emit('close');
		},
	},
};
</script>

<style scoped>
.modal {
	display: flex;
	align-items: center;
	justify-content: center;
}
</style>
