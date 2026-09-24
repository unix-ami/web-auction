import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    base: '/static/api/spa/',  // ← CHANGE THIS
    build: {
        outDir: "../api/static/api/spa",
    },
    plugins: [vue()],
    resolve: {
        alias: {
            '@': '/src',
        },
    },
})