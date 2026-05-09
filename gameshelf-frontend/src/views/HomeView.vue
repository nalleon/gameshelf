<template>
  <div class="min-h-dvh flex flex-col bg-gsoscuro/55 overflow-hidden">
    <Navbar />

    <main class="flex-1 flex justify-center items-center px-4 py-8 lg:py-10">

      <!-- Card Principal -->
      <section
        class="relative overflow-hidden max-w-5xl w-full rounded-3xl border border-white/8 bg-gsoscuro shadow-2xl">

        <!-- Glow decorativo -->
        <div class="absolute inset-0 bg-linear-to-br from-gsmenta/5 via-transparent to-gsbosque/5 pointer-events-none">
        </div>

        <!-- Línea superior -->
        <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>

        <!-- Content -->
        <div class="relative grid lg:grid-cols-2 gap-8 items-center p-6 sm:p-8 lg:p-10">

          <!-- Logo -->
          <div class="flex justify-center">
            <div class="flex flex-col items-center gap-4">

              <div
                class="w-44 h-44 sm:w-52 sm:h-52 lg:w-64 lg:h-64 rounded-full overflow-hidden border border-white/10 shadow-2xl">
                <img class="w-full h-full object-cover" src="../assets/cover-logo.png" alt="Logo">
              </div>

              <!-- Subtítulo -->
              <p class="text-gsgris uppercase tracking-[0.35em] text-xs sm:text-sm font-semibold text-center">
                Organize. Show. Find
              </p>

            </div>
          </div>

          <!-- Texto -->
          <div class="text-gsblanco">

            <p class="text-gsmenta uppercase tracking-[0.25em] text-xs font-bold mb-3">
              Video Game Collection Platform
            </p>

            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-black leading-tight mb-4">
              Track your collection.
              <span class="text-gsmenta">Organize your backlog.</span>
            </h1>

            <p class="text-sm sm:text-base text-gsgris leading-relaxed mb-6">
              A platform built for video game collectors to organize physical and digital collections &
              track gaming progress across regions and platforms.
            </p>

            <!-- Features -->
            <div class="space-y-3">

              <div class="flex items-start gap-3 p-3 rounded-xl bg-white/3 border border-white/5">
                <div class="w-2 h-2 rounded-full bg-gsmenta mt-2 shrink-0"></div>
                <div>
                  <h3 class="font-bold text-gsblanco text-sm mb-1">
                    Regional & format tracking
                  </h3>
                  <p class="text-xs sm:text-sm text-gsgris">
                    Organize games by region, platform and physical formats.
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-3 p-3 rounded-xl bg-white/3 border border-white/5">
                <div class="w-2 h-2 rounded-full bg-gsbosque mt-2 shrink-0"></div>
                <div>
                  <h3 class="font-bold text-gsblanco text-sm mb-1">
                    Wishlist system
                  </h3>
                  <p class="text-xs sm:text-sm text-gsgris">
                    Keep track of desired games and future acquisitions.
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-3 p-3 rounded-xl bg-white/3 border border-white/5">
                <div class="w-2 h-2 rounded-full bg-gsmenta mt-2 shrink-0"></div>
                <div>
                  <h3 class="font-bold text-gsblanco text-sm mb-1">
                    Progress tracking
                  </h3>
                  <p class="text-xs sm:text-sm text-gsgris">
                    Manage statuses like playing, completed, dropped or planned.
                  </p>
                </div>
              </div>

            </div>

            <!-- CTA -->
            <div class="mt-6 flex flex-col sm:flex-row gap-3">

              <router-link to="/register"
                class="bg-gsmenta hover:bg-gsbosque text-gsoscuro font-bold px-5 py-3 rounded-full transition-all uppercase tracking-wider text-xs text-center">
                Get Started
              </router-link>

              <router-link to="/login"
                class="border border-white/10 hover:border-gsmenta/40 text-gsblanco px-5 py-3 rounded-full transition-all bg-white/[0.03] hover:bg-white/[0.05] uppercase tracking-wider text-xs text-center">
                Login
              </router-link>

            </div>

          </div>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
</script>