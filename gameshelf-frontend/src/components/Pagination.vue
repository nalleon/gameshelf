<template>
  <nav
    v-if="totalPages > 1"
    class="
      mt-12
      flex items-center justify-center
      gap-2 sm:gap-3
      px-2
      w-full
    "
  >
    <!-- Prev -->
    <button
      @click="$emit('change', currentPage - 1)"
      :disabled="currentPage === 1"
      class="
        w-9 h-9
        sm:w-11 sm:h-11
        rounded-full
        border border-white/10
        bg-white/[0.03]
        backdrop-blur-md
        flex items-center justify-center
        text-sm sm:text-base
        text-gsblanco
        transition-all duration-300
        hover:border-gsmenta
        hover:text-gsmenta
        hover:scale-105
        disabled:opacity-30
        disabled:cursor-not-allowed
        shrink-0
      "
    >
      <i class="pi pi-chevron-left"></i>
    </button>

    <!-- Pages -->
    <div
      class="
        flex items-center
        gap-1 sm:gap-2
        px-2 sm:px-3
        py-2
        rounded-full
        border border-white/10
        bg-white/[0.03]
        backdrop-blur-md
        shadow-[0_0_30px_rgba(0,0,0,0.25)]

        max-w-full
        overflow-x-auto
        scrollbar-none
      "
    >
      <template
        v-for="page in visiblePages"
        :key="page"
      >
        <button
          v-if="typeof page === 'number'"
          @click="$emit('change', page)"
          class="
            min-w-[34px]
            h-[34px]

            sm:min-w-[42px]
            sm:h-[42px]

            px-2 sm:px-3
            rounded-full
            text-xs sm:text-sm
            font-medium
            transition-all duration-300
            flex-shrink-0
          "
          :class="
            currentPage === page
              ? 'bg-gsmenta text-black shadow-lg shadow-gsmenta/30 scale-105'
              : 'text-gsblanco/70 hover:bg-white/10 hover:text-white'
          "
        >
          {{ page }}
        </button>

        <span
          v-else
          class="
            text-gsgris/50
            px-1
            text-xs sm:text-sm
            flex-shrink-0
          "
        >
          ...
        </span>
      </template>
    </div>

    <!-- Next -->
    <button
      @click="$emit('change', currentPage + 1)"
      :disabled="currentPage === totalPages"
      class="
        w-9 h-9
        sm:w-11 sm:h-11
        rounded-full
        border border-white/10
        bg-white/[0.03]
        backdrop-blur-md
        flex items-center justify-center
        text-sm sm:text-base
        text-gsblanco
        transition-all duration-300
        hover:border-gsmenta
        hover:text-gsmenta
        hover:scale-105
        disabled:opacity-30
        disabled:cursor-not-allowed
        flex-shrink-0
      "
    >
      <i class="pi pi-chevron-right"></i>
    </button>
  </nav>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

defineEmits<{
  (e: 'change', page: number): void
}>()

const isMobile = ref(false)

const updateMedia = () => {
  isMobile.value = window.innerWidth < 640
}

onMounted(() => {
  updateMedia()
  window.addEventListener('resize', updateMedia)

  setTimeout(updateMedia, 0)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateMedia)
})

const visiblePages = computed(() => {
  const total = props.totalPages
  const current = props.currentPage

  const pages: (number | string)[] = []

  const add = (val: number | string) => {
    if (pages[pages.length - 1] !== val) {
      pages.push(val)
    }
  }

  if (isMobile.value) {
    add(1)

    if (current > 3) {
      add('...')
    }

    if (current !== 1 && current !== total) {
      add(current)
    }

    if (current < total - 2) {
      add('...')
    }

    if (total > 1) {
      add(total)
    }

    return pages
  }

  const delta = 2
  const range: number[] = []
  const result: (number | string)[] = []

  let last: number | undefined

  for (let i = 1; i <= total; i++) {
    if (
      i === 1 ||
      i === total ||
      (i >= current - delta && i <= current + delta)
    ) {
      range.push(i)
    }
  }

  for (const i of range) {
    if (last !== undefined) {
      if (i - last === 2) {
        result.push(last + 1)
      } else if (i - last !== 1) {
        result.push('...')
      }
    }

    result.push(i)
    last = i
  }

  return result
})
</script>