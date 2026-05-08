<template>
  <div v-show="modelValue" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4">

    <div
      class="relative w-full max-w-xl bg-gsoscuro text-gsblanco rounded-2xl shadow-2xl border border-white/8 overflow-hidden">

      <!-- TOP BORDER -->
      <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>

      <div class="p-6">

        <h2 class="text-center text-lg font-semibold mb-6">
          Adjust your profile picture
        </h2>

        <div class="w-full h-80 relative bg-[#11151c] rounded-xl overflow-hidden">

          <Cropper ref="cropperRef" :src="image" class="w-full h-full" :stencil-component="CircleStencil" />

        </div>

        <div class="flex justify-between mt-6">

          <button class="text-gsgris hover:text-gsblanco" @click="close">
            Cancel
          </button>
          <button class="bg-gsmenta text-gsoscuro px-5 py-2 rounded-full font-bold" @click="emitCrop">
            Apply
          </button>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'

const props = defineProps<{
  modelValue: boolean
  image: string | null
}>()

const emit = defineEmits(['update:modelValue', 'cropped'])

const cropperRef = ref()
function close() {
  emit('update:modelValue', false)
}
function emitCrop() {
  const canvas = cropperRef.value.getResult().canvas

  canvas.toBlob((blob: Blob | null) => {
    if (!blob) return

    const file = new File([blob], 'avatar.jpg', { type: 'image/jpeg' })

    emit('cropped', {
      file,
      preview: URL.createObjectURL(file)
    })

    close()
  }, 'image/jpeg')
}
</script>