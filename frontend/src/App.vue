<template>
    <main class="container pt-4">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <ul class="navbar-nav mx-auto mt-2 mt-lg-0">
                <li class="nav-item active">
                    <router-link
                    class=""
                    :to="{name: 'Main Page'}"
                    >
                        <button class="btn text-light">
                            Home
                        </button>
                
                    </router-link>
                </li>
            
                <li>
                    <router-link
                    class=""
                    :to="{name: 'Sell Page'}"
                    >
                        <button class="btn text-light">
                            Sell
                        </button>
                    </router-link>
                </li>
            
            
                <li>
                    <router-link
                    class=""
                    :to="{name: 'Bids Page'}"
                    >
                        <button class="btn text-light">
                            My Bids
                        </button>
                    </router-link>
                </li>

                <li>
                    <router-link
                    class=""
                    :to="{name: 'Profile Page'}"
                    >
                        <button class="btn text-light">
                            Profile
                        </button>
                    </router-link>
                </li>

                <li>
                    <a href="/logout/" class="btn text-light"> 
                        Logout
                    </a>
                </li>

            </ul>
        </nav>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>

<style scoped>
</style>
