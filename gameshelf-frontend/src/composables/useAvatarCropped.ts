import { ref } from 'vue'

export function useAvatarCropper() {
  const showCropper = ref(false)
  const rawImage = ref<string | null>(null)
  const avatarFile = ref<File | null>(null)
  const avatarPreview = ref<string | null>(null)

  function openCropper(file: File) {
    if (rawImage.value) URL.revokeObjectURL(rawImage.value)

    rawImage.value = URL.createObjectURL(file)
    showCropper.value = true
  }

  function setCropped(result: { file: File; preview: string }) {
    avatarFile.value = result.file
    avatarPreview.value = result.preview
  }

  return {
    showCropper,
    rawImage,
    avatarFile,
    avatarPreview,
    openCropper,
    setCropped,
  }
}
