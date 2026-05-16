<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>

        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-6 sm:p-12 text-white relative">
            <div v-if="game" class="max-w-[1200px] mx-auto">

                <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-4 relative">
                    <div>
                        <h1 class="text-3xl font-bold block mb-1">{{ game.title }}</h1>

                        <div class="flex flex-wrap items-center gap-2 mt-1">
                            <p class="text-gray-400 text-sm">{{ game.released_at }}</p>

                            <i class="pi pi-circle-fill text-gray-600" style="font-size: 3px;"></i>

                            <div class="flex items-center justify-center px-1.5 py-0.5 text-xs text-gray-400 select-none"
                                :title="`Region: ${game.region?.name || 'Unknown'}`">

                                <span v-if="['eu', 'us', 'nz', 'jp', 'cn', 'kr', 'br'].includes(region)"
                                    :class="`fi fi-${region}`" class="text-xs rounded-sm" />

                                <i v-else-if="region === 'world'" class="pi pi-globe text-[11px]" />

                                <i v-else-if="region === 'asia'" class="pi pi-compass text-[11px]" />

                                <i v-else class="pi pi-exclamation-triangle text-[11px] text-yellow-400" />

                                <span class="text-[9px] font-bold uppercase ml-1 tracking-wider text-gray-400">
                                    {{ region === 'warning' ? 'TBA' : region }}
                                </span>
                            </div>

                            <template v-if="game.platforms && game.platforms.length">
                                <i class="pi pi-circle-fill text-gray-600" style="font-size: 3px;"></i>

                                <div class="flex items-center gap-3 ml-1">
                                    <div v-for="p in game.platforms" :key="p.id"
                                        class="relative group flex items-center justify-center text-gray-400 hover:text-gsmenta transition-colors duration-200 cursor-pointer">

                                        <Icon
                                            :icon="PLATFORM_MAP[p.slug || ''] || PLATFORM_MAP[p.name?.toLowerCase().trim().replace(/ /g, '-') || ''] || 'mdi:gamepad-variant'"
                                            class="text-xl" />

                                        <div
                                            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-[#151921] border border-white/10 text-[10px] font-bold text-gray-200 uppercase tracking-wider rounded shadow-2xl opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-150 pointer-events-none whitespace-nowrap z-50">
                                            {{ p.name }}
                                            <div
                                                class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-[#151921]">
                                            </div>
                                        </div>

                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>

                    <div class="flex gap-2 sm:ml-auto z-40">
                        <button @click="openDropdown = openDropdown === 'favorites' ? null : 'favorites'"
                            :disabled="!isAuthenticated" class="p-2 rounded-full transition-all duration-300" :class="isAuthenticated
                                ? 'hover:bg-white/10 active:scale-125 cursor-pointer'
                                : 'opacity-40 cursor-not-allowed select-none'"
                            :title="isAuthenticated ? 'Manage favorites' : 'Log in to add to favorites'">
                            <Icon :icon="isGameFavorite && isAuthenticated ? 'mdi:heart' : 'mdi:heart-outline'"
                                class="text-4xl"
                                :class="isGameFavorite && isAuthenticated ? 'text-red-500' : 'text-gray-400' + (isAuthenticated ? ' hover:text-red-400' : '')" />
                        </button>

                        <button @click="openDropdown = openDropdown === 'wishlist' ? null : 'wishlist'"
                            :disabled="!isAuthenticated" class="p-2 rounded-full transition-all" :class="isAuthenticated
                                ? 'hover:bg-white/10 cursor-pointer'
                                : 'opacity-40 cursor-not-allowed select-none'"
                            :title="isAuthenticated ? 'Wishlist' : 'Log in to use wishlist'">
                            <Icon :icon="isAnyWishlist && isAuthenticated ? 'mdi:bookmark' : 'mdi:bookmark-outline'"
                                class="text-4xl"
                                :class="isAnyWishlist && isAuthenticated ? 'text-gsmenta' : 'text-gray-400' + (isAuthenticated ? ' hover:text-gsmenta' : '')" />
                        </button>

                        <button @click="openDropdown = openDropdown === 'library' ? null : 'library'"
                            :disabled="!isAuthenticated" class="p-2 rounded-full transition-all" :class="isAuthenticated
                                ? 'hover:bg-white/10 cursor-pointer'
                                : 'opacity-40 cursor-not-allowed select-none'"
                            :title="isAuthenticated ? 'Add into my collection' : 'Log in to add to your library'">
                            <Icon :icon="isInLibrary && isAuthenticated ? 'mdi:library-shelves' : 'mdi:library-outline'"
                                class="text-4xl"
                                :class="isInLibrary && isAuthenticated ? 'text-gsmenta' : 'text-gray-400' + (isAuthenticated ? ' hover:text-gsmenta' : '')" />
                        </button>

                        <button @click="openDropdown = openDropdown === 'collections' ? null : 'collections'"
                            :disabled="!isAuthenticated" class="p-2 rounded-full transition-all" :class="isAuthenticated
                                ? 'hover:bg-white/10 cursor-pointer'
                                : 'opacity-40 cursor-not-allowed select-none'"
                            title="isAuthenticated ? 'My Collections' : 'Log in to manage collections'">
                            <Icon
                                :icon="userCollections.some(c => c.items.some(i => i.game.id === game?.id)) && isAuthenticated ? 'mdi:folder-star' : 'mdi:folder-plus-outline'"
                                class="text-4xl"
                                :class="userCollections.some(c => c.items.some(i => i.game.id === game?.id)) && isAuthenticated ? 'text-gsmenta' : 'text-gray-400' + (isAuthenticated ? ' hover:text-gsmenta' : '')" />
                        </button>
                    </div>

                    <div v-if="openDropdown"
                        class="absolute top-full left-0 right-0 sm:left-auto sm:right-0 mt-3 bg-[#151921] border border-white/10 rounded-xl shadow-2xl z-50 w-full sm:w-85 max-h-[60vh] sm:max-h-[480px] flex flex-col overflow-hidden backdrop-blur-md">

                        <div v-if="openDropdown === 'favorites'"
                            class="p-4 flex flex-col gap-1 overflow-y-auto custom-scrollbar">
                            <div class="flex justify-between items-center mb-3 px-1">
                                <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">
                                    Add as favorite for:
                                </span>
                            </div>
                            <div class="flex flex-col gap-1">
                                <button v-for="p in game.platforms" :key="p.id" @click="toggleFavorite(p.id)"
                                    class="flex justify-between items-center px-3 py-2 rounded-md hover:bg-white/5 transition-colors group">
                                    <span
                                        :class="favoritePlatforms.includes(p.id) ? 'text-gsmenta font-bold' : 'text-gray-300 group-hover:text-white'">
                                        {{ p.name }}
                                    </span>
                                    <Icon
                                        :icon="favoritePlatforms.includes(p.id) ? 'mdi:check-circle' : 'mdi:plus-circle-outline'"
                                        class="text-xl"
                                        :class="favoritePlatforms.includes(p.id) ? 'text-gsmenta' : 'text-gray-600 group-hover:text-gray-400'" />
                                </button>
                            </div>
                        </div>

                        <div v-if="openDropdown === 'wishlist'" class="p-4 overflow-y-auto custom-scrollbar flex-1">
                            <p class="text-xs font-bold text-gray-500 uppercase mb-3">Add into Wishlist</p>
                            <div v-for="p in game.platforms" :key="p.id"
                                class="mb-4 last:mb-0 border-b border-white/5 pb-3 last:border-0">
                                <span class="text-xs text-gray-500 block mb-2">{{ p.name }}</span>
                                <div class="flex gap-2">
                                    <button @click="toggleWishlist(p.id, 'D')"
                                        :class="wishlistItems.find(i => i.platform.id === p.id && i.type === 'D') ? 'bg-gsmenta text-black' : 'bg-white/5 text-white'"
                                        class="flex-1 text-[10px] py-1.5 rounded uppercase font-bold transition-all">Digital</button>
                                    <button @click="toggleWishlist(p.id, 'P')"
                                        :class="wishlistItems.find(i => i.platform.id === p.id && i.type === 'P') ? 'bg-gsmenta text-black' : 'bg-white/5 text-white'"
                                        class="flex-1 text-[10px] py-1.5 rounded uppercase font-bold transition-all">Physical</button>
                                </div>
                            </div>
                        </div>

                        <div v-if="openDropdown === 'library'" class="p-4 overflow-y-auto custom-scrollbar flex-1">
                            <p class="text-xs font-bold text-gray-500 uppercase mb-4">My library</p>
                            <div v-for="p in game.platforms" :key="p.id"
                                class="mb-6 last:mb-0 border-b border-white/5 pb-4 last:border-0">
                                <div class="flex justify-between items-center mb-2">
                                    <span class="text-sm font-bold text-white">{{ p.name }}</span>
                                    <span v-if="libraryItems.find(i => i.platform.id === p.id)"
                                        class="text-[10px] text-gsmenta uppercase font-bold">In library</span>
                                </div>
                                <div class="grid grid-cols-2 gap-2">
                                    <button v-for="status in LIBRARY_STATUS" :key="status.id"
                                        @click="toggleLibrary(p.id, status.id)"
                                        :class="libraryItems.some(i => Number(i.platform.id) === Number(p.id) && i.status === status.name) ? 'bg-gsmenta text-black shadow-[0_0_10px_#00ff99]' : 'bg-white/5 text-gray-400 hover:bg-white/10'"
                                        class="text-[10px] py-1.5 rounded uppercase font-bold transition-all">{{
                                            status.name }}</button>
                                </div>
                            </div>
                        </div>

                        <div v-if="openDropdown === 'collections'" class="flex flex-col h-full overflow-hidden flex-1">
                            <div class="p-4 border-b border-white/5 bg-[#1a1f29] flex-shrink-0">
                                <p class="text-xs font-bold text-gray-500 uppercase mb-3">Add into collection</p>
                                <div class="flex gap-2">
                                    <input v-model="newCollectionName" type="text" placeholder="New collection..."
                                        class="flex-1 bg-white/5 border border-white/10 rounded px-2 py-1.5 text-xs focus:outline-none focus:border-gsmenta text-white"
                                        @keyup.enter="createNewCollection" />
                                    <button @click="createNewCollection"
                                        class="bg-gsmenta text-black px-3 py-1 rounded font-bold hover:brightness-110">
                                        <Icon icon="mdi:plus" class="text-xl" />
                                    </button>
                                </div>
                            </div>
                            <div class="overflow-y-auto p-4 space-y-4 custom-scrollbar flex-1">
                                <div v-for="col in collectionItemsForGame" :key="col.id"
                                    class="border-b border-white/5 pb-4 last:border-0 last:pb-0">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="text-sm font-bold text-gray-200 truncate">{{ col.name }}</span>
                                        <span v-if="col.is_private"
                                            class="text-[10px] text-gray-600 uppercase">Private</span>
                                    </div>
                                    <div v-for="p in game.platforms" :key="p.id" class="mt-2 space-y-1">
                                        <p class="text-[9px] text-gray-500 font-bold ml-1 uppercase">{{ p.name }}</p>
                                        <div class="flex gap-2">
                                            <button @click="toggleCollectionItem(col.id, p.id, 'D')"
                                                :class="isInCollection(col, p.id, 'D') ? 'bg-gsmenta text-black' : 'bg-white/5 text-gray-400'"
                                                class="flex-1 text-[9px] py-1.5 rounded font-bold transition-all uppercase">Digital</button>
                                            <button @click="toggleCollectionItem(col.id, p.id, 'P')"
                                                :class="isInCollection(col, p.id, 'P') ? 'bg-gsmenta text-black' : 'bg-white/5 text-gray-400'"
                                                class="flex-1 text-[9px] py-1.5 rounded font-bold transition-all uppercase">Physical</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <div class="h-[2px] w-full bg-gradient-to-r from-gsmenta/50 via-white/10 to-transparent mb-8"></div>

                <div class="flex flex-col md:flex-row gap-12 mb-12">

                    <div class="w-full md:w-[350px] flex-shrink-0">
                        <img :src="game.cover_detail" :alt="game.title"
                            class="w-full rounded shadow-2xl border-3 border-gsmenta" />

                        <div v-if="game.genres && game.genres.length"
                            class="flex flex-wrap gap-2 mt-4 justify-center md:justify-start">
                            <span v-for="genre in game.genres" :key="genre.id"
                                class="text-[11px] font-bold uppercase tracking-wider bg-white/5 border border-gsmenta/40 px-3 py-1.5 rounded-md text-gray-300 hover:text-white transition-colors select-none">
                                {{ genre.name }}
                            </span>
                        </div>
                    </div>

                    <div class="flex-1">

                        <div class="flex flex-col gap-3 text-md mb-8 text-left">
                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Developer:</span>
                                <span v-if="formatText(game?.developers, 'developer')" class="text-gsmenta">
                                    {{ formatText(game?.developers, 'developer') }}
                                </span>
                                <span v-else class="text-gray-500 italic font-semibold">TBA</span>
                            </div>

                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Publisher:</span>
                                <span v-if="formatText(game?.publishers, 'publisher')" class="text-gsmenta">
                                    {{ formatText(game?.publishers, 'publisher') }}
                                </span>
                                <span v-else class="text-gray-500 italic font-semibold">TBA</span>
                            </div>

                            <div class="flex flex-wrap items-center gap-3 mt-1">
                                <div
                                    class="flex items-center bg-white/5 border border-white/10 rounded-md px-2.5 py-1 text-xs select-none">
                                    <span class="text-gray-400 font-medium uppercase mr-1">
                                        {{ game.region?.rating_organization || 'Rating' }}:
                                    </span>
                                    <span :class="game.age_rating ? 'text-gsmenta font-bold' : 'text-gray-500 italic'">
                                        {{ game.age_rating || 'TBA' }}
                                    </span>
                                </div>

                                <div v-if="game.mature_content !== undefined && game.mature_content !== null"
                                    class="flex items-center border rounded-md px-2.5 py-1 text-xs select-none transition-colors"
                                    :class="game.mature_content
                                        ? 'bg-red-500/10 border-red-500/30 text-red-400'
                                        : 'bg-white/5 border-white/10 text-gray-400'">
                                    <Icon :icon="game.mature_content ? 'mdi:alert-decagram' : 'mdi:shield-check'"
                                        class="text-sm mr-1.5" />
                                    <span class="font-medium mr-1">Mature Content:</span>
                                    <span class="font-bold uppercase text-[10px]">
                                        {{ game.mature_content ? 'Yes' : 'No' }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <p class="text-gray-300 leading-relaxed text-lg text-justify max-w-3xl mb-12">
                            {{ game.description }}
                        </p>

                        <div class="mt-12 border-t border-white/5 pt-10">
                            <div class="flex items-center justify-between mb-8">
                                <h2 ref="reviewsTitle" class="text-2xl font-bold tracking-wide uppercase text-gray-100">
                                    Reviews
                                </h2>
                                <span
                                    class="text-xs bg-white/5 px-3 py-1 rounded-full border border-white/10 text-gray-400 font-medium">
                                    {{ reviews.length }} total
                                </span>
                            </div>

                            <div v-if="reviewsLoading" class="text-gray-500 text-center py-10">
                                Loading reviews...
                            </div>

                            <div v-else-if="isAuthenticated">
                                <div v-if="!userHasReviewed || isEditingReview"
                                    class="bg-[#121620] p-5 sm:p-6 rounded-xl mb-10 border border-white/10 shadow-xl relative overflow-hidden backdrop-blur-sm">
                                    <div class="absolute top-0 left-0 w-1 h-full"
                                        :class="isEditingReview ? 'bg-amber-500' : 'bg-gsmenta'"></div>

                                    <h3 class="text-lg font-bold mb-4 flex items-center gap-2"
                                        :class="isEditingReview ? 'text-amber-400' : 'text-gsmenta'">
                                        <Icon :icon="isEditingReview ? 'mdi:pencil' : 'mdi:comment-plus-outline'" />
                                        {{ isEditingReview ? 'Edit your review' : 'Write a review' }}
                                    </h3>

                                    <textarea v-model="reviewForm.content"
                                        class="w-full bg-black/20 border border-white/10 rounded-lg p-4 text-white text-sm mb-4 min-h-[120px] focus:outline-none focus:border-gsmenta/60 focus:shadow-[0_0_15px_rgba(0,255,153,0.15)] transition-all resize-y"
                                        placeholder="What did you think about this game? Share your thoughts with the community..."></textarea>

                                    <div
                                        class="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-4">
                                        <div class="flex flex-col sm:flex-row gap-2 sm:items-center">
                                            <span
                                                class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1 sm:mb-0 sm:mr-2">
                                                Do you recommend it?
                                            </span>
                                            <div class="grid grid-cols-2 sm:flex gap-2">
                                                <label class="cursor-pointer group">
                                                    <input type="radio" v-model="reviewForm.recommend" :value="true"
                                                        class="hidden peer" />
                                                    <div
                                                        class="p-2 px-4 rounded-full border border-white/10 text-xs text-center peer-checked:bg-gsmenta peer-checked:text-white group-hover:bg-white/5 transition-all font-bold flex items-center justify-center gap-2">
                                                        <Icon icon="mdi:thumb-up" class="text-sm" /> Yes
                                                    </div>
                                                </label>
                                                <label class="cursor-pointer group">
                                                    <input type="radio" v-model="reviewForm.recommend" :value="false"
                                                        class="hidden peer" />
                                                    <div
                                                        class="p-2 px-4 rounded-full border border-white/10 text-xs text-center peer-checked:bg-red-500 peer-checked:text-white group-hover:bg-white/5 transition-all font-bold flex items-center justify-center gap-2">
                                                        <Icon icon="mdi:thumb-down" class="text-sm" /> No
                                                    </div>
                                                </label>
                                            </div>
                                        </div>

                                        <div class="flex gap-2 justify-end">
                                            <button v-if="isEditingReview" @click="cancelEdit"
                                                class="bg-white/5 text-gray-300 font-bold text-xs py-2.5 px-4 rounded-full hover:bg-white/10 transition-colors border border-white/5">
                                                Cancel
                                            </button>
                                            <button @click="saveReview"
                                                class="bg-gsmenta text-black font-bold text-xs py-2.5 px-5 rounded-full hover:brightness-110 transition-all shadow-[0_0_15px_rgba(0,255,153,0.2)]">
                                                {{ isEditingReview ? 'Update Review' : 'Post Review' }}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-else
                                class="bg-[#121620]/60 p-6 rounded-xl mb-10 border border-dashed border-white/10 shadow-lg text-center backdrop-blur-sm relative overflow-hidden flex flex-col items-center justify-center min-h-[140px]">
                                <div class="bg-white/5 p-3 rounded-full mb-3 border border-white/5 text-gray-400">
                                    <Icon icon="mdi:lock-outline" class="text-2xl text-gsmenta/80" />
                                </div>
                                <p class="text-sm text-gray-300 mb-4 max-w-sm">
                                    Want to share your thoughts with the community? Join us to leave your review!
                                </p>
                                <div class="flex items-center gap-3">
                                    <router-link to="/login"
                                        class="bg-gsmenta text-black font-bold text-xs py-2 px-5 rounded-full hover:brightness-110 transition-all shadow-[0_0_15px_rgba(0,255,153,0.15)]">
                                        Log In
                                    </router-link>
                                    <span class="text-xs text-gray-600 font-semibold uppercase tracking-wider">or</span>
                                    <router-link to="/register"
                                        class="bg-white/5 text-white font-bold text-xs py-2 px-5 rounded-full hover:bg-white/10 border border-white/10 transition-colors">
                                        Register
                                    </router-link>
                                </div>
                            </div>

                            <div class="space-y-4">
                                <div v-if="reviews.length === 0"
                                    class="text-gray-500 italic text-center py-12 border border-dashed border-white/5 rounded-xl bg-white/[0.01]">
                                    No reviews yet. Be the first to share your thoughts!
                                </div>

                                <div v-for="review in reviews" :key="review.id"
                                    class="bg-gradient-to-b from-[#161a24] to-[#12151d] p-5 rounded-xl border border-white/10 transition-all hover:border-white/20 shadow-md">

                                    <div
                                        class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/5 mb-4">

                                        <div class="flex items-center gap-3">
                                            <div
                                                class="w-10 h-10 rounded-full overflow-hidden flex items-center justify-center border border-white/10 flex-shrink-0">
                                                <img v-if="review.author?.avatar" :src="review.author?.avatar"
                                                    :alt="review.author?.username || 'User avatar'"
                                                    class="w-full h-full object-cover" />

                                                <div v-else
                                                    class="bg-gradient-to-br from-white/10 to-white/[0.02] w-full h-full flex items-center justify-center font-bold text-md text-gsmenta shadow-inner">
                                                    {{ review.author?.username?.charAt(0).toUpperCase() || 'U' }}
                                                </div>
                                            </div>

                                            <div>
                                                <div class="flex items-center gap-2 flex-wrap">
                                                    <p class="font-bold text-sm text-gray-200">
                                                        {{ review.author?.username || 'Unknown User' }}
                                                    </p>

                                                    <i class="pi pi-circle-fill text-gray-600 self-center"
                                                        style="font-size: 3px;"></i>

                                                    <span class="text-[11px] text-gray-500">
                                                        {{ formatDate(review.created_at) }}
                                                    </span>

                                                    <span v-if="review.created_at !== review.updated_at"
                                                        class="text-[10px] text-gray-500 italic select-none">
                                                        (edited)
                                                    </span>
                                                </div>

                                                <div class="inline-flex items-center gap-1.5 text-[11px] font-bold mt-1 px-2 py-0.5 rounded-full border"
                                                    :class="review.recommend
                                                        ? 'text-gsmenta bg-gsmenta/5 border-gsmenta/20'
                                                        : 'text-red-400 bg-red-500/5 border-red-500/20'">
                                                    <Icon :icon="review.recommend ? 'mdi:thumb-up' : 'mdi:thumb-down'"
                                                        class="text-xs" />
                                                    <span>{{ review.recommend ? 'Recommended' : 'Not Recommended'
                                                        }}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div v-if="review.author?.id === currentUserId"
                                            class="flex gap-1 self-end sm:self-center">
                                            <button @click="startEdit(review)"
                                                class="p-2 bg-white/5 rounded-md text-gray-400 hover:text-gsmenta hover:bg-white/10 transition-all"
                                                title="Edit">
                                                <Icon icon="mdi:pencil" class="text-lg" />
                                            </button>
                                            <button @click="deleteReview(review.id)"
                                                class="p-2 bg-white/5 rounded-md text-gray-400 hover:text-red-400 hover:bg-white/10 transition-all"
                                                title="Delete">
                                                <Icon icon="mdi:trash-can" class="text-lg" />
                                            </button>
                                        </div>

                                    </div>

                                    <p
                                        class="text-gray-300 text-sm leading-relaxed text-justify whitespace-pre-wrap px-1">
                                        {{ review.content }}
                                    </p>
                                </div>

                                <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-8 pt-4">
                                    <button @click="changePage(currentPage - 1)" :disabled="!hasPreviousPage"
                                        class="p-2 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-20 disabled:hover:bg-white/5 disabled:cursor-not-allowed transition-all border border-white/5">
                                        <Icon icon="mdi:chevron-left" class="text-2xl text-white" />
                                    </button>

                                    <div
                                        class="flex items-center gap-1.5 bg-white/5 px-4 py-2 rounded-lg border border-white/5 text-xs font-semibold uppercase tracking-wider">
                                        <span class="text-gray-400">Page</span>
                                        <span class="text-gsmenta font-bold text-sm">{{ currentPage }}</span>
                                        <span class="text-gray-600">/</span>
                                        <span class="text-gray-400">{{ totalPages }}</span>
                                    </div>

                                    <button @click="changePage(currentPage + 1)" :disabled="!hasNextPage"
                                        class="p-2 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-20 disabled:hover:bg-white/5 disabled:cursor-not-allowed transition-all border border-white/5">
                                        <Icon icon="mdi:chevron-right" class="text-2xl text-white" />
                                    </button>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

            </div>

            <div v-else-if="loading" class="flex justify-center items-center h-64 text-gsmenta">
                Loading...
            </div>
        </section>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import axios from 'axios';
import { Icon } from '@iconify/vue'
import api from "@/api/client";
import Navbar from '@/components/Navbar.vue';
import type { Developer, Game, Platform, Publisher, Review } from '@/types/gameDetailsType';
import { useAuthStore } from '@/stores/authStore';
import type { Collection, CollectionItem, Library, LibraryItem, Wishlist, WishlistItem } from '@/types/profileTypes';
import { PLATFORM_MAP } from '@/constants/app';

const route = useRoute()
const authStore = useAuthStore()


const gameId = route.params.id
const game = ref<Game | null>(null);

const loading = ref(true)
const openDropdown = ref<null | 'favorites' | 'wishlist' | 'library' | 'collections'>(null)
const reviewsLoading = ref(true);
const isAuthenticated = computed(() => authStore.isLogged);
const region = computed(() => {
    const regionMaps: Record<string, string> = {
        europe: 'eu',
        north_america: 'us',
        new_zeland: 'nz',
        japan: 'jp',
        china: 'cn',
        korea: 'kr',
        brazil: 'br',

        asia: 'asia',
        worldwide: 'world',

        to_be_add: 'warning',
    }

    const regionName = game.value?.region?.name ?? 'to_be_add'

    return regionMaps[regionName] || 'warning'
})
onMounted(async () => {
    try {
        const data = await getGame();
        game.value = data;

        await loadReviews();

        if (isAuthenticated.value) {
            await loadCollections();
            await loadFavoriteStatus();
            await loadWishlistStatus();
            await loadLibraryStatus();
        }

    } catch (error: any) {
        console.error('Error:', error);
    } finally {
        loading.value = false;
    }
});

async function getGame() {
    const response = await api.get(`/api/games/${gameId}/`)
    return response.data
}

// --- Lógica de Add into Favoritos ---
const showPlatformSelector = ref(false);
const favoritePlatforms = ref<number[]>([]);

const loadFavoriteStatus = async () => {
    const userId = authStore.getSelfId();

    const response = await api.get(
        `/api/favorites/user/${userId}/`
    );
    // Filtramos los favoritos que pertenecen a este juego y guardamos sus IDs de plataforma
    favoritePlatforms.value = response.data
        .filter((fav: any) => fav.game.id === game.value?.id)
        .map((fav: any) => fav.platform.id);
};

const toggleFavorite = async (platformId: number) => {
    try {

        const response = await api.post(
            `/api/favorites/toggle/`,
            {
                pk_game: gameId,
                pk_platform: platformId
            }
        );

        // Actualizamos la lista local
        if (response.data.is_favorite) {
            favoritePlatforms.value.push(platformId);
        } else {
            favoritePlatforms.value = favoritePlatforms.value.filter(id => id !== platformId);
        }
    } catch (error: any) {
        alert(error.response?.data?.error || "Error al marcar favorito");
    }
};

const isGameFavorite = computed(() => favoritePlatforms.value.length > 0);

// --- LÓGICA DE WISHLIST ---
const isInWishlist = ref(false);
const wishlistData = ref<Wishlist | null>(null);
const wishlistItems = ref<WishlistItem[]>([]);
const wishlistId = computed(() => wishlistData.value?.id);

const showWishlistSelector = ref(false);

const loadWishlistStatus = async () => {
    try {
        // Obtenemos la wishlist del propio usuario autenticado
        const response = await api.get(`/api/wishlist/`);

        wishlistData.value = response.data;

        // Filtramos los items del game actual
        wishlistItems.value = response.data.items.filter(
            (item: WishlistItem) => item.game.id === game.value?.id
        );
    } catch (error: any) {
        console.error('Error cargando wishlist:', error);
    }
};

const toggleWishlist = async (platformId: number, type: 'P' | 'D') => {
    // TS sabe que existingItem será un WishlistItem o undefined
    const existingItem = wishlistItems.value.find(
        (item: WishlistItem) => item.platform.id === platformId && item.type === (type as any)
        // Nota: Si 'type' en tu interfaz es string, quizás necesites un cast pequeño o actualizar la interfaz
    );

    try {
        if (existingItem) {
            await api.delete(
                `/api/wishlist/items/${existingItem.id}/`
            );
            wishlistItems.value = wishlistItems.value.filter(item => item.id !== existingItem.id);
        } else {
            if (!wishlistId.value) return;

            const payload = {
                game_id: game.value?.id,
                platform_id: platformId,
                priority: 5,
                annotation: "",
                is_private: false,
                type: type
            };

            const response = await api.post(
                `/api/wishlist/${wishlistId.value}/`,
                payload
            );

            // console.log({
            //     game_id: game.value?.id,
            //     platform_id: platformId,
            //     type
            // });

            // Añadimos el nuevo item (que viene con el formato WishlistItem)
            wishlistItems.value.push(response.data);
        }
    } catch (error: any) {
        console.error(error);
    }
};

// Computed para saber si el icono de wishlist debe resaltar
const isAnyWishlist = computed(() => wishlistItems.value.length > 0);

// --- LÓGICA DE LIBRERÍA ---
const libraryData = ref<Library | null>(null);
const libraryItems = ref<LibraryItem[]>([]);
const showLibrarySelector = ref(false);

// Mapeo de estados para el select/botones
const LIBRARY_STATUS = [
    { id: 'PLN', name: 'Planning' },
    { id: 'PLY', name: 'Playing' },
    { id: 'CMP', name: 'Completed' },
    { id: 'PSD', name: 'Paused' },
    { id: 'DRP', name: 'Dropped' },
];

const loadLibraryStatus = async () => {
    try {
        const response = await api.get(`/api/library/`);
        libraryData.value = response.data;
        // Filtramos items para este juego
        libraryItems.value = response.data.items.filter(
            (item: LibraryItem) => item.game.id === game.value?.id
        );
    } catch (error: any) {
        console.error('Error cargando librería:', error);
    }
};

const toggleLibrary = async (platformId: number, status?: string) => {
    // 1. Buscamos si el juego ya existe en esta plataforma dentro de la librería
    const existingItem = libraryItems.value.find(
        (item: LibraryItem) => item.platform.id === platformId
    );

    try {
        if (existingItem) {
            // Si el usuario pulsa el MISMO estado que ya tiene, lo borramos (Toggle)
            // Si pulsa un estado diferente, lo actualizamos (PATCH)
            if (!status || existingItem.status === status) {
                await api.delete(
                    `/api/library/${existingItem.id}/`
                );
                libraryItems.value = libraryItems.value.filter(item => item.id !== existingItem.id);
            } else {
                // ACTUALIZAR ESTADO (PATCH)
                const response = await api.patch(
                    `/api/library/${existingItem.id}/`,
                    {
                        status,
                        platform_id: platformId
                    }
                );
                // Actualizamos el item en nuestro array local
                const index = libraryItems.value.findIndex(item => item.id === existingItem.id);
                if (index !== -1) libraryItems.value[index] = response.data;
            }
        } else if (status) {
            // CREAR NUEVO (POST)
            const payload = {
                game_id: game.value?.id,
                platform_id: platformId,
                status: status,
                is_private: false,
                hours_played: 0
            };

            await api.post(
                `/api/library/`,
                payload
            );

            // Recargamos para traer el objeto con el formato correcto del serializador
            await loadLibraryStatus();
        }
    } catch (error: any) {
        console.error("Error en Library:", error.response?.data);
    }
};

const isInLibrary = computed(() => libraryItems.value.length > 0);

// --- LÓGICA DE COLECCIONES ---
const userCollections = ref<Collection[]>([]);
const showCollectionSelector = ref(false);
const newCollectionName = ref("");
const isNewCollectionPrivate = ref(false);

const loadCollections = async () => {
    try {
        const response = await api.get('/api/collections/')
        // console.log("STATUS:", response.status)
        // console.log("DATA:", response.data)

        userCollections.value = response.data.map((col: any) => ({
            ...col,
            items: col.items ?? []
        }));

        // userCollections.value = response.data;
        newCollectionName.value = "";
    } catch (err: any) {
        console.error("ERROR:", err.response?.status)
        console.error("DETAIL:", err.response?.data)
    }
}

const collectionItemsForGame = computed(() => {
    if (!game.value) return [];

    return userCollections.value.map(col => ({
        ...col,
        items: col.items.filter(
            (i: any) => i.game?.id === game.value?.id
        )
    }));
});

const createNewCollection = async () => {

    if (!newCollectionName.value.trim()) return;

    try {

        const response = await api.post(
            `/api/collections/`,
            {
                name: newCollectionName.value,
                is_private: isNewCollectionPrivate.value
            }
        );

        userCollections.value.push({
            ...response.data,
            items: []
        });

        newCollectionName.value = "";

    } catch (error: any) {

        alert("Error al crear la colección");

    }
};

const toggleCollectionItem = async (
    collectionId: number,
    platformId: number,
    type: 'P' | 'D'
) => {

    const collection = userCollections.value.find(
        c => c.id === collectionId
    );

    if (!collection) return;

    const existingItem: CollectionItem | undefined =
        collection.items.find(
            item =>
                item.game.id === game.value?.id &&
                item.type === type &&
                item.platform.id === platformId
        );

    try {

        if (existingItem) {

            await api.delete(
                `/api/collections/${collectionId}/items/${existingItem.id}/`
            );

        } else {

            await api.post(
                `/api/collections/${collectionId}/`,
                {
                    game_id: game.value?.id,
                    platform_id: platformId,
                    is_private: false,
                    type: type
                }
            );
        }

        await loadCollections();

    } catch (error: any) {

        console.error(error.response?.data);

        alert(
            error.response?.data?.error ||
            "Error al gestionar colección"
        );
    }
};

// Helper para saber si un juego está en una colección específica
const isInCollection = (
    collection: Collection,
    platformId: number,
    type: 'P' | 'D'
) => {

    return collection.items.some(
        item =>
            item.game.id === game.value?.id &&
            item.type === type &&
            item.platform.id === platformId
    );
};

// --- Details del Game

// --- LÓGICA DE PLATAFORMAS ---
const LIMIT_ICONS = 3; // Número de iconos antes de mostrar los puntos
const showAllPlatforms = ref(false);

// 2. Procesar el string de plataformas a un array de iconos
const processedIcons = computed(() => {
    if (!game.value?.platforms) return [];

    const slugs = game.value.platforms.map(p => p.slug.trim()) // Extraemos solo el nombre de cada plataforma

    return slugs.map(slug => ({
        slug: slug,
        icon: PLATFORM_MAP[slug] || 'mdi:controller-classic' // Icono por defecto si no existe en el mapa
    }));
});

// 3. Lista visible basada en el límite y el estado de expansión
const visibleIcons = computed(() => {
    if (showAllPlatforms.value) return processedIcons.value;
    return processedIcons.value.slice(0, LIMIT_ICONS);
});


// --- LÓGICA DE INFORMACIÓN AMPLIADA ---
const LIMIT = 20;
const expanded = ref({
    developer: false,
    publisher: false,
    platform: false
});

// Comprobar la longitud del texto para decidir si mostrar el botón de expansión
// const isLong = (list: Array<any> | undefined) => {
//     if (!list || list.length === 0) return false;
//     return list.map(item => item.name).join(', ').length > LIMIT;
// };

// Función para alternar el estado
// const toggleField = (field: 'developer' | 'publisher' | 'platform') => {
//     expanded.value[field] = !expanded.value[field];
// };

// Función para mostrar el texto procesado
const formatText = (list: Array<Developer> | Array<Publisher> | Array<Platform> | undefined, field: 'developer' | 'publisher' | 'platform') => {
    if (!list || list.length === 0) return '';

    const text = list.map(item => item.name).join(', ');

    if (text.length <= LIMIT || expanded.value[field]) return text;

    return text.substring(0, LIMIT);
};


// --- LÓGICA DE REVIEWS ---

const reviews = ref<Review[]>([]);
const currentUserId = computed(() => authStore.getSelfId());

// Formulario
const reviewForm = ref({
    content: '',
    recommend: true as boolean | null
});
const isEditingReview = ref<number | null>(null);

// Comprobamos si el usuario actual ya ha escrito una review
const userHasReviewed = computed(() => {
    return reviews.value.some(r => r.author?.id === currentUserId.value);
});

const loadReviews = async (page = 1) => {
    try {
        reviewsLoading.value = true;

        const response = await api.get(`/api/reviews/?game_id=${gameId}&page=${page}`);

        reviews.value = response.data.results;

        currentPage.value = response.data.current_page;
        totalPages.value = response.data.total_pages;
        hasNextPage.value = response.data.has_next;
        hasPreviousPage.value = response.data.has_previous;

    } catch (error) {
        console.error('Error cargando reviews:', error);
    } finally {
        reviewsLoading.value = false;
    }
};

const saveReview = async () => {
    if (!reviewForm.value.content.trim() || reviewForm.value.recommend === null) {
        alert("Please write a review and select a recommendation.");
        return;
    }

    try {
        if (isEditingReview.value) {
            // EDITAR (PATCH) - Tu backend espera pk_game según el views.py
            await api.patch(`/api/reviews/${isEditingReview.value}/`, {
                content: reviewForm.value.content,
                recommend: reviewForm.value.recommend,
                pk_game: Number(gameId),
                // pk_author: authStore.getSelfId()
            });
        } else {
            // CREAR NUEVA (POST) - Tu backend espera game_id según el views.py
            await api.post(`/api/reviews/`, {
                content: reviewForm.value.content,
                recommend: reviewForm.value.recommend,
                game_id: Number(gameId)
            });
        }

        // Limpiar estado y recargar
        cancelEdit();
        await loadReviews();

    } catch (error: any) {
        console.error('Error guardando review:', error.response?.data);
        alert(error.response?.data?.error || "Error saving the review.");
    }
};

const startEdit = (review: Review) => {
    isEditingReview.value = review.id;
    reviewForm.value = {
        content: review.content,
        recommend: review.recommend
    };
};

const cancelEdit = () => {
    isEditingReview.value = null;
    reviewForm.value = { content: '', recommend: true };
};

const deleteReview = async (reviewId: number) => {
    if (!confirm('Are you sure you want to delete this review?')) return;

    try {
        await api.delete(`/api/reviews/${reviewId}/`);

        // Si estaba editando la review que acaba de borrar, reseteamos el formulario
        if (isEditingReview.value === reviewId) {
            cancelEdit();
        }

        await loadReviews();
    } catch (error: any) {
        console.error('Error borrando review:', error.response?.data);
    }
};

const formatDate = (dateString: string | undefined) => {
    if (!dateString) return '';
    const date = new Date(dateString);

    // Esto lo formateará automáticamente según el idioma del navegador (ej: "16 may 2026")
    return date.toLocaleDateString(undefined, {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    });
};

// Nuevos estados para la paginación
const currentPage = ref(1);
const totalPages = ref(1);
const hasNextPage = ref(false);
const hasPreviousPage = ref(false);
const reviewsTitle = ref<HTMLElement | null>(null);

const changePage = async (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages.value) {
        await loadReviews(newPage);

        reviewsTitle.value?.scrollIntoView({
            behavior: 'smooth'
        });
    }
};

</script>

<style scoped></style>