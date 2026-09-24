<template>
  <div class="mt-4">
    <div class="search-bar d-flex justify-content-center"> 
      <input type="text" placeholder="Search..." id="search-input" :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)">
      <img src="../assets/search.png" alt="search icon" id="search-icon" @click="$emit('search', modelValue)">
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
  search: [query: string]
}>()
</script>

<style scoped>
.search-bar {
    border: 1px solid #dee2e6;
    border-radius: 20px;
    background-color: #f8f9fa;
    width: 400px;
    justify-content: center;
    align-items: center;
}
#search-input {
    border: none;
    border-radius: 20px;
    background-color: #f8f9fa;
    padding: 9.5px 15px;
    outline: none;
    width: 100%;
    font-size: 16px;
}
#search-icon {
    height: 24px;
    width: 24px;
    margin-right: 10px;
    cursor: pointer;
}
</style>
