<template>
  <Transition name="fade">
    <button
      v-show="visible"
      @click="scrollTop"
      class="
        fixed
        z-40

        bottom-20 right-4
        sm:bottom-8 sm:right-8

        w-11 h-11
        sm:w-12 sm:h-12

        rounded-full

        border border-white/10
        bg-white/[0.06]
        backdrop-blur-xl

        text-gsmenta

        shadow-[0_0_30px_rgba(0,0,0,0.35)]

        flex items-center justify-center

        transition-all duration-300

        hover:scale-110
        hover:border-gsmenta
        hover:bg-gsmenta
        hover:text-black

        active:scale-95
      "
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="
          h-5 w-5
          sm:h-6 sm:w-6
          transition-transform duration-300
          group-hover:-translate-y-1
        "
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 15l7-7 7 7"
        />
      </svg>
    </button>
  </Transition>
</template>

<script setup lang="ts">
import {
  onUnmounted,
  ref,
  watch
} from 'vue'

const props = defineProps<{
  target?: HTMLElement | null
  threshold?: number
}>()

const visible = ref(false)

let currentTarget: HTMLElement | null = null

const handleScroll = () => {
  if (!currentTarget) return

  visible.value =
    currentTarget.scrollTop > (props.threshold ?? 300)
}

const scrollTop = () => {
  currentTarget?.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

watch(
  () => props.target,
  (newTarget, oldTarget) => {
    if (oldTarget) {
      oldTarget.removeEventListener(
        'scroll',
        handleScroll
      )
    }

    if (newTarget) {
      currentTarget = newTarget

      newTarget.addEventListener(
        'scroll',
        handleScroll
      )

      handleScroll()
    }
  },
  {
    immediate: true
  }
)

onUnmounted(() => {
  currentTarget?.removeEventListener(
    'scroll',
    handleScroll
  )
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>